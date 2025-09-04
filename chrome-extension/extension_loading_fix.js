/**
 * EXTENSION LOADING FIX - 확장 프로그램 로딩 문제 해결
 * 
 * 진단 결과: chrome API는 있지만 chrome.runtime이 없음
 * 이는 content script가 제대로 주입되지 않았음을 의미합니다.
 */

console.clear();
console.log("%c🔧 EXTENSION LOADING FIX", "color: #ff6600; font-size: 20px; font-weight: bold;");
console.log("Chrome Extension 로딩 문제를 진단하고 해결합니다.\n");

// 1. 현재 상태 확인
console.log("📋 1단계: 현재 Chrome Extension 상태");
console.log("-".repeat(50));

const hasChrome = typeof chrome !== 'undefined';
const hasRuntime = hasChrome && typeof chrome.runtime !== 'undefined';
const hasRuntimeId = hasRuntime && chrome.runtime.id;

console.log(`Chrome API: ${hasChrome ? '✅' : '❌'}`);
console.log(`Chrome Runtime: ${hasRuntime ? '✅' : '❌'}`);
console.log(`Extension ID: ${hasRuntimeId ? '✅ ' + chrome.runtime.id : '❌ 없음'}`);

if (!hasRuntime) {
    console.log("\n🚨 문제 발견: chrome.runtime이 없습니다!");
    console.log("이는 Chrome Extension의 content script가 제대로 주입되지 않았음을 의미합니다.\n");
    
    // 2. 가능한 원인들
    console.log("📋 2단계: 가능한 원인들");
    console.log("-".repeat(50));
    console.log("1. Extension이 비활성화되어 있음");
    console.log("2. manifest.json의 content_scripts 설정 문제");
    console.log("3. 현재 사이트가 허용 목록에 없음");
    console.log("4. Extension에 오류가 있어서 로드되지 않음");
    console.log("5. Chrome 개발자 모드가 꺼져 있음");
    
    // 3. 해결 단계
    console.log("\n📋 3단계: 단계별 해결 방법");
    console.log("-".repeat(50));
    console.log("아래 단계를 순서대로 따라하세요:\n");
    
    console.log("🔧 Step 1: chrome://extensions 페이지로 이동");
    console.log("   → 새 탭에서 chrome://extensions 입력");
    console.log("   → 'AI Workspace Controller' 확장 프로그램 찾기");
    
    console.log("\n🔧 Step 2: 개발자 모드 확인");
    console.log("   → 우측 상단의 '개발자 모드' 토글이 켜져 있는지 확인");
    console.log("   → 꺼져 있다면 켜기");
    
    console.log("\n🔧 Step 3: Extension 상태 확인");
    console.log("   → 'AI Workspace Controller'가 활성화되어 있는지 확인");
    console.log("   → 비활성화되어 있다면 토글로 활성화");
    
    console.log("\n🔧 Step 4: Extension 새로고침");
    console.log("   → 'AI Workspace Controller' 옆의 '새로고침' 버튼 클릭");
    console.log("   → 오류가 표시된다면 해당 오류 해결 필요");
    
    console.log("\n🔧 Step 5: 현재 페이지 새로고침");
    console.log("   → 이 페이지를 새로고침 (F5 또는 Ctrl+R)");
    console.log("   → 확장 프로그램이 다시 로드됨");
    
    // 4. 자동 확인 함수 제공
    window.__checkExtensionStatus = function() {
        console.log("\n🔍 Extension 상태 재확인...");
        
        const nowHasChrome = typeof chrome !== 'undefined';
        const nowHasRuntime = nowHasChrome && typeof chrome.runtime !== 'undefined';
        const nowHasRuntimeId = nowHasRuntime && chrome.runtime.id;
        
        console.log(`Chrome API: ${nowHasChrome ? '✅' : '❌'}`);
        console.log(`Chrome Runtime: ${nowHasRuntime ? '✅' : '❌'}`);
        console.log(`Extension ID: ${nowHasRuntimeId ? '✅ ' + chrome.runtime.id : '❌ 없음'}`);
        
        if (nowHasRuntime) {
            console.log("\n🎉 성공! Extension이 올바르게 로드되었습니다!");
            console.log("이제 ChatGPT와 Gemini에서 메시지 전송이 작동해야 합니다.");
            
            // Background script와 통신 테스트
            chrome.runtime.sendMessage({action: "statusAll"}, (response) => {
                if (chrome.runtime.lastError) {
                    console.log("⚠️ Background script 통신 오류:", chrome.runtime.lastError.message);
                } else {
                    console.log("✅ Background script 통신 성공:", response);
                }
            });
        } else {
            console.log("\n❌ 아직 해결되지 않음. 위의 단계를 다시 확인하세요.");
        }
    };
    
    console.log("\n💡 사용법:");
    console.log("1. 위의 단계들을 완료한 후");
    console.log("2. __checkExtensionStatus() 실행하여 상태 재확인");
    
} else {
    console.log("\n✅ Chrome Extension이 올바르게 로드되어 있습니다!");
    
    // Background script 통신 테스트
    console.log("\n📋 Background Script 통신 테스트");
    console.log("-".repeat(50));
    
    chrome.runtime.sendMessage({action: "statusAll"}, (response) => {
        if (chrome.runtime.lastError) {
            console.log("❌ Background script 통신 실패:", chrome.runtime.lastError.message);
            console.log("→ background.js에 문제가 있을 수 있습니다.");
        } else {
            console.log("✅ Background script 통신 성공");
            console.log("📊 플랫폼 상태:", response);
            
            // 현재 사이트의 상태 확인
            const currentSite = location.hostname;
            let platformStatus = null;
            
            if (currentSite.includes('chatgpt.com')) {
                platformStatus = response.chatgpt;
            } else if (currentSite.includes('claude.ai')) {
                platformStatus = response.claude;
            } else if (currentSite.includes('aistudio.google.com') || currentSite.includes('gemini.google.com')) {
                platformStatus = response.gemini;
            } else if (currentSite.includes('perplexity.ai')) {
                platformStatus = response.perplexity;
            }
            
            if (platformStatus) {
                console.log(`\n🎯 현재 사이트 (${currentSite}) 상태:`);
                console.log(`  준비 상태: ${platformStatus.ready ? '✅' : '❌'}`);
                if (!platformStatus.ready) {
                    console.log(`  문제: ${platformStatus.reason || '알 수 없음'}`);
                }
            }
        }
    });
    
    // Content script 상태 확인
    setTimeout(() => {
        console.log("\n📋 Content Script 기능 테스트");
        console.log("-".repeat(50));
        
        // 입력창 찾기 테스트
        const inputSelectors = [
            'textarea',
            'div[contenteditable="true"]',
            '.ql-editor',
            '#prompt-textarea'
        ];
        
        let foundInput = false;
        for (const selector of inputSelectors) {
            const elements = document.querySelectorAll(selector);
            if (elements.length > 0) {
                console.log(`✅ 입력창 발견: ${selector} (${elements.length}개)`);
                foundInput = true;
                break;
            }
        }
        
        if (!foundInput) {
            console.log("❌ 입력창을 찾을 수 없습니다.");
            console.log("→ 페이지가 완전히 로드되지 않았거나 새로운 UI 구조일 수 있습니다.");
        }
        
        // 전송 버튼 찾기 테스트
        const buttonSelectors = [
            'button[data-testid="send-button"]',
            'button[aria-label*="send" i]',
            'button:has(mat-icon[fonticon="send"])',
            'button:has(svg)'
        ];
        
        let foundButton = false;
        for (const selector of buttonSelectors) {
            try {
                const elements = document.querySelectorAll(selector);
                if (elements.length > 0) {
                    console.log(`✅ 전송 버튼 발견: ${selector} (${elements.length}개)`);
                    foundButton = true;
                    break;
                }
            } catch (e) {
                // 일부 선택자는 구형 브라우저에서 작동하지 않을 수 있음
                continue;
            }
        }
        
        if (!foundButton) {
            console.log("⚠️ 전송 버튼을 찾을 수 없습니다.");
            console.log("→ 텍스트를 입력한 후 버튼이 나타나는지 확인하세요.");
        }
        
        const canWork = foundInput;
        console.log(`\n🎯 기본 작동 가능성: ${canWork ? '✅ 가능' : '❌ 불가능'}`);
        
        if (canWork) {
            console.log("\n💡 테스트 방법:");
            console.log("1. ChatGPT에서: __directSend('테스트') 실행");
            console.log("2. 또는 Extension Popup을 통해 메시지 전송 테스트");
        }
        
    }, 1000);
}

// 5. 실시간 모니터링
console.log("\n📋 실시간 Extension 상태 모니터링");
console.log("-".repeat(50));

let monitorCount = 0;
const monitorInterval = setInterval(() => {
    monitorCount++;
    
    const nowHasRuntime = typeof chrome !== 'undefined' && typeof chrome.runtime !== 'undefined';
    
    if (nowHasRuntime && !hasRuntime) {
        console.log(`\n🎉 Extension이 로드되었습니다! (${monitorCount}초 후)`);
        clearInterval(monitorInterval);
        
        // 자동으로 상태 확인
        setTimeout(() => {
            if (window.__checkExtensionStatus) {
                window.__checkExtensionStatus();
            }
        }, 1000);
    }
    
    // 30초 후 모니터링 중단
    if (monitorCount >= 30) {
        clearInterval(monitorInterval);
        console.log("\n⏰ 모니터링 종료 (30초)");
    }
}, 1000);

console.log("\n" + "=".repeat(60));
console.log("💡 이 스크립트는 Extension 로딩 문제를 해결하는 데 도움을 줍니다.");
console.log("문제가 지속되면 Chrome을 재시작하거나 Extension을 재설치하세요.");
console.log("=".repeat(60));