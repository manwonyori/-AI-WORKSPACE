/**
 * Chrome Extension 실제 설치 및 업데이트 상태 확인
 * 
 * 개발한 코드가 실제 Chrome에 적용되었는지 확인합니다.
 */

console.clear();
console.log("%c🔍 Chrome Extension 실제 상태 확인", "color: #ff6600; font-size: 20px; font-weight: bold;");

// 1. Extension 설치 상태 확인
console.log("\n📋 1단계: Extension 설치 상태");
console.log("-".repeat(50));

if (typeof chrome === 'undefined') {
    console.log("❌ CRITICAL: Chrome Extension이 설치되지 않았습니다!");
    console.log("\n🔧 해결 방법:");
    console.log("1. Chrome 주소창에 입력: chrome://extensions/");
    console.log("2. '개발자 모드' 켜기");
    console.log("3. '압축해제된 확장 프로그램 로드' 클릭");
    console.log("4. 폴더 선택: C:\\Users\\8899y\\AI-WORKSPACE\\chrome-extension");
    
    // Extension 없이도 테스트 가능한 Mock 생성
    window.mockExtension = {
        sendMessage: (message) => {
            console.log("🔄 Mock Extension Message:", message);
        }
    };
    
} else {
    console.log("✅ Chrome Extension API 사용 가능");
    
    if (chrome.runtime && chrome.runtime.id) {
        console.log(`✅ Extension ID: ${chrome.runtime.id}`);
        console.log(`✅ Extension URL: chrome-extension://${chrome.runtime.id}/`);
        
        // Manifest 정보 확인
        try {
            const manifest = chrome.runtime.getManifest();
            console.log("📋 Manifest 정보:");
            console.log(`   - 이름: ${manifest.name}`);
            console.log(`   - 버전: ${manifest.version}`);
            console.log(`   - 설명: ${manifest.description}`);
            
            // 우리가 개발한 v1.4.1인지 확인
            if (manifest.version === "1.4.1" && manifest.name === "AI Workspace Controller") {
                console.log("🎯 ✅ 우리가 개발한 Extension v1.4.1이 정상 설치됨!");
            } else {
                console.log("⚠️  다른 Extension이 설치되어 있습니다.");
                console.log("   현재 설치된 것과 개발한 것이 다를 수 있습니다.");
            }
            
        } catch (error) {
            console.log("❌ Manifest 정보 읽기 실패:", error);
        }
        
        // Background script 통신 테스트
        chrome.runtime.sendMessage({action: "ping", test: true}, (response) => {
            if (chrome.runtime.lastError) {
                console.log("⚠️  Background script 응답 없음:", chrome.runtime.lastError.message);
                console.log("   → background.js가 제대로 로드되지 않았을 수 있습니다.");
            } else {
                console.log("✅ Background script 통신 성공:", response);
            }
        });
        
    } else {
        console.log("❌ chrome.runtime 없음 - Extension 문제");
    }
}

// 2. 현재 사이트에서 우리 코드가 작동하는지 테스트
console.log("\n📋 2단계: 현재 사이트에서 기능 테스트");
console.log("-".repeat(50));

const currentSite = location.hostname;
console.log(`현재 사이트: ${currentSite}`);

// 플랫폼 감지
let platform = 'unknown';
if (currentSite.includes('chatgpt.com')) platform = 'chatgpt';
else if (currentSite.includes('claude.ai')) platform = 'claude';  
else if (currentSite.includes('gemini.google.com') || currentSite.includes('aistudio.google.com')) platform = 'gemini';
else if (currentSite.includes('perplexity.ai')) platform = 'perplexity';

console.log(`감지된 플랫폼: ${platform}`);

if (platform !== 'unknown') {
    console.log(`\n🧪 ${platform.toUpperCase()} 입력창 테스트:`);
    
    // 입력창 찾기
    let inputFound = false;
    const inputSelectors = {
        chatgpt: [
            'div#prompt-textarea[contenteditable="true"]',
            'textarea#prompt-textarea'
        ],
        claude: [
            'div[contenteditable="true"].ProseMirror',
            'div[contenteditable="true"]'
        ],
        gemini: [
            '.ql-editor',
            'textarea[aria-label*="Message"]',
            'textarea.textarea'
        ],
        perplexity: [
            'textarea[placeholder*="Ask"]',
            'textarea',
            'div[contenteditable="true"]'
        ]
    };
    
    const selectors = inputSelectors[platform] || [];
    selectors.forEach((selector, i) => {
        const element = document.querySelector(selector);
        if (element) {
            const rect = element.getBoundingClientRect();
            const visible = rect.width > 0 && rect.height > 0 && element.offsetParent !== null;
            console.log(`   ${i+1}. ${selector}: ${visible ? '✅ 발견' : '❌ 숨김'}`);
            if (visible && !inputFound) {
                inputFound = true;
                window.testInputElement = element;
            }
        } else {
            console.log(`   ${i+1}. ${selector}: ❌ 없음`);
        }
    });
    
    if (inputFound) {
        console.log("✅ 입력창 발견됨 - window.testInputElement에 저장");
        
        // 실제 입력 테스트 함수 생성
        window.testExtensionInput = function(text = "Extension 테스트 메시지") {
            console.log(`\n🚀 ${platform} 입력 테스트: "${text}"`);
            
            const element = window.testInputElement;
            if (!element) {
                console.log("❌ 테스트 요소가 없습니다");
                return false;
            }
            
            try {
                element.focus();
                
                if (element.tagName === 'DIV') {
                    // ContentEditable
                    element.innerHTML = text.replace(/\n/g, '<br>');
                    element.dispatchEvent(new InputEvent('input', {
                        inputType: 'insertText',
                        data: text,
                        bubbles: true
                    }));
                } else {
                    // Textarea
                    element.value = text;
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                }
                
                console.log("✅ 입력 테스트 완료");
                return true;
                
            } catch (error) {
                console.log("❌ 입력 테스트 실패:", error);
                return false;
            }
        };
        
    } else {
        console.log("❌ 입력창을 찾을 수 없습니다");
        console.log("   → 사이트 구조가 변경되었거나 잘못된 페이지일 수 있습니다");
    }
    
} else {
    console.log("⚠️  지원하지 않는 사이트입니다");
    console.log("   ChatGPT, Claude, Gemini, Perplexity 중 하나로 이동해주세요");
}

// 3. Extension 업데이트 확인
console.log("\n📋 3단계: Extension 파일 업데이트 상태");
console.log("-".repeat(50));

// Content Script 버전 확인 (만약 content.js에 버전이 있다면)
if (typeof window.EXTENSION_VERSION !== 'undefined') {
    console.log(`✅ Content Script 버전: ${window.EXTENSION_VERSION}`);
} else {
    console.log("⚠️  Content Script 버전 정보 없음");
}

// 4. 종합 진단 및 권장사항
console.log("\n📋 종합 진단 결과");
console.log("=".repeat(50));

if (typeof chrome === 'undefined') {
    console.log("🔴 Extension이 설치되지 않았습니다");
    console.log("\n📋 할 일:");
    console.log("1. chrome://extensions/ 이동");
    console.log("2. 개발자 모드 켜기");
    console.log("3. '압축해제된 확장 프로그램 로드' 클릭");
    console.log("4. C:\\Users\\8899y\\AI-WORKSPACE\\chrome-extension 폴더 선택");
    
} else {
    console.log("🟡 Extension이 설치되어 있습니다");
    console.log("\n📋 확인 사항:");
    console.log("1. Extension 버전이 1.4.1인지 확인");
    console.log("2. 개발한 최신 코드가 반영되었는지 확인");
    console.log("3. 필요시 Extension 새로고침 또는 재설치");
}

console.log("\n🧪 테스트 명령어:");
if (inputFound) {
    console.log("testExtensionInput() - 입력 테스트");
    console.log("testExtensionInput('사용자 메시지') - 커스텀 메시지 테스트");
} else {
    console.log("먼저 올바른 AI 플랫폼 페이지로 이동하세요");
}

console.log("\n" + "=".repeat(50));
console.log("Chrome Extension 상태 확인 완료!");