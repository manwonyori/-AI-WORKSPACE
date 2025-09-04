/**
 * BASIC REALITY CHECK - 가장 기본적인 문제부터 확인
 * 
 * 지금까지 복잡한 코드를 만들었지만 아직 작동하지 않는다면
 * 가장 기본적인 문제가 있을 수 있습니다.
 * 
 * 이 스크립트로 현실을 직시해봅시다.
 */

console.clear();
console.log("%c🔍 BASIC REALITY CHECK", "color: #ff0000; font-size: 20px; font-weight: bold;");
console.log("지금까지 많은 코드를 작성했지만 아직 작동하지 않습니다.");
console.log("가장 기본적인 것부터 다시 확인해봅시다.\n");

// 1. Extension이 실제로 설치되어 있는가?
console.log("📋 1단계: Extension 설치 상태 확인");
console.log("-".repeat(50));

if (typeof chrome === 'undefined') {
    console.log("❌ CRITICAL: chrome API가 없습니다!");
    console.log("   → Chrome 확장 프로그램이 설치되지 않았거나");
    console.log("   → manifest.json이 올바르지 않거나");
    console.log("   → content script가 주입되지 않았습니다.");
    console.log("\n🔧 해결책:");
    console.log("   1. chrome://extensions 로 가서 확장 프로그램이 설치되어 있는지 확인");
    console.log("   2. 개발자 모드가 켜져 있는지 확인");
    console.log("   3. manifest.json의 content_scripts matches가 현재 사이트를 포함하는지 확인");
} else {
    console.log("✅ chrome API 사용 가능");
    
    if (chrome.runtime) {
        console.log(`✅ Extension ID: ${chrome.runtime.id}`);
        
        // Extension과 통신 테스트
        chrome.runtime.sendMessage({action: "ping"}, (response) => {
            if (chrome.runtime.lastError) {
                console.log("❌ Background script 통신 실패:", chrome.runtime.lastError.message);
                console.log("   → background.js가 없거나 오류가 있습니다.");
            } else {
                console.log("✅ Background script 통신 성공:", response);
            }
        });
    } else {
        console.log("❌ chrome.runtime이 없습니다!");
    }
}

// 2. 현재 어떤 사이트에 있는가?
console.log("\n📋 2단계: 현재 위치 확인");
console.log("-".repeat(50));
console.log(`현재 사이트: ${location.href}`);

const site = location.hostname;
let expectedSite = "";
let correctURL = "";

if (site.includes("chatgpt.com")) {
    expectedSite = "ChatGPT";
    correctURL = "https://chatgpt.com/ (메인 채팅 페이지)";
} else if (site.includes("claude.ai")) {
    expectedSite = "Claude";
    correctURL = "https://claude.ai/ (대화 페이지)";
} else if (site.includes("perplexity.ai")) {
    expectedSite = "Perplexity";
    correctURL = "https://www.perplexity.ai/ (메인 페이지)";
} else if (site.includes("aistudio.google.com")) {
    expectedSite = "Google AI Studio";
    correctURL = "https://aistudio.google.com/prompts/new_chat";
    
    if (!location.pathname.includes("/prompts/")) {
        console.log("⚠️ 잘못된 Google AI Studio URL!");
        console.log(`   현재: ${location.href}`);
        console.log(`   올바른 URL로 이동하세요: ${correctURL}`);
    }
} else {
    console.log("❌ 지원하지 않는 사이트입니다!");
    console.log("다음 사이트 중 하나로 이동하세요:");
    console.log("- https://chatgpt.com");
    console.log("- https://claude.ai");
    console.log("- https://www.perplexity.ai");
    console.log("- https://aistudio.google.com/prompts/new_chat");
}

if (expectedSite) {
    console.log(`✅ ${expectedSite} 사이트에 있습니다`);
    if (correctURL && !location.href.includes("prompts")) {
        console.log(`💡 올바른 URL: ${correctURL}`);
    }
}

// 3. 가장 간단한 입력창 찾기
console.log("\n📋 3단계: 입력창 찾기 (간단한 방법)");
console.log("-".repeat(50));

const simpleInputSelectors = [
    "textarea",
    "input[type='text']",
    "[contenteditable='true']",
    ".ql-editor"
];

let foundInput = null;
for (const selector of simpleInputSelectors) {
    const elements = document.querySelectorAll(selector);
    console.log(`"${selector}" → ${elements.length}개 발견`);
    
    for (let i = 0; i < elements.length; i++) {
        const el = elements[i];
        const rect = el.getBoundingClientRect();
        const visible = rect.width > 0 && rect.height > 0;
        
        console.log(`  ${i+1}. ${el.tagName} (${visible ? '보임' : '숨김'}) ${el.id ? '#'+el.id : ''} ${el.className ? '.'+el.className.split(' ')[0] : ''}`);
        
        if (visible && !foundInput) {
            foundInput = el;
        }
    }
}

// 4. 가장 간단한 버튼 찾기
console.log("\n📋 4단계: 전송 버튼 찾기 (간단한 방법)");
console.log("-".repeat(50));

const simpleButtonSelectors = [
    "button",
    "[role='button']",
    "input[type='submit']"
];

let foundButton = null;
let totalButtons = 0;

for (const selector of simpleButtonSelectors) {
    const elements = document.querySelectorAll(selector);
    totalButtons += elements.length;
    
    for (let i = 0; i < Math.min(elements.length, 5); i++) {  // 처음 5개만 보여주기
        const el = elements[i];
        const rect = el.getBoundingClientRect();
        const visible = rect.width > 0 && rect.height > 0;
        const disabled = el.disabled || el.hasAttribute('disabled');
        const text = el.textContent?.trim().slice(0, 20) || el.getAttribute('aria-label')?.slice(0, 20) || 'no-text';
        
        console.log(`  ${selector}[${i+1}]: "${text}" (${visible ? '보임' : '숨김'}, ${disabled ? '비활성' : '활성'})`);
        
        if (visible && !disabled && !foundButton && 
            (text.toLowerCase().includes('send') || 
             text.toLowerCase().includes('전송') ||
             el.querySelector('svg') || 
             el.querySelector('mat-icon'))) {
            foundButton = el;
        }
    }
    
    if (elements.length > 5) {
        console.log(`  ... 및 ${elements.length - 5}개 더`);
    }
}

console.log(`총 ${totalButtons}개의 버튼이 있습니다.`);

// 5. 초간단 테스트
console.log("\n📋 5단계: 초간단 기능 테스트");
console.log("-".repeat(50));

if (!foundInput) {
    console.log("❌ 입력창을 찾을 수 없습니다!");
    console.log("🔧 해결책: 페이지가 완전히 로드된 후 다시 시도하세요.");
} else {
    console.log("✅ 입력창 발견:", foundInput);
    
    // 입력 테스트
    window.__simpleInputTest = () => {
        const testText = `초간단 테스트 ${Date.now()}`;
        console.log(`🧪 입력 테스트: "${testText}"`);
        
        try {
            foundInput.focus();
            
            if (foundInput.tagName === 'TEXTAREA' || foundInput.tagName === 'INPUT') {
                foundInput.value = testText;
            } else {
                foundInput.textContent = testText;
            }
            
            foundInput.dispatchEvent(new Event('input', { bubbles: true }));
            console.log("✅ 입력 성공!");
            
            // 3초 후 버튼 상태 다시 체크
            setTimeout(() => {
                const buttons = document.querySelectorAll('button:not([disabled])');
                console.log(`📊 활성 버튼: ${buttons.length}개`);
            }, 3000);
            
        } catch (e) {
            console.log("❌ 입력 실패:", e);
        }
    };
    
    console.log("💡 테스트 실행: __simpleInputTest()");
}

if (!foundButton) {
    console.log("⚠️ 활성 전송 버튼을 찾을 수 없습니다.");
    console.log("💡 텍스트를 입력한 후 버튼이 나타나는지 확인하세요.");
} else {
    console.log("✅ 전송 버튼 발견:", foundButton);
    
    window.__simpleButtonTest = () => {
        console.log("🧪 버튼 클릭 테스트");
        try {
            foundButton.click();
            console.log("✅ 버튼 클릭 성공!");
        } catch (e) {
            console.log("❌ 버튼 클릭 실패:", e);
        }
    };
    
    console.log("💡 테스트 실행: __simpleButtonTest()");
}

// 6. 최종 진단
console.log("\n📋 최종 진단");
console.log("=".repeat(50));

const hasChrome = typeof chrome !== 'undefined';
const hasInput = foundInput !== null;
const hasButton = foundButton !== null;
const isCorrectSite = expectedSite !== "";

console.log(`Chrome Extension: ${hasChrome ? '✅' : '❌'}`);
console.log(`올바른 사이트: ${isCorrectSite ? '✅' : '❌'}`);
console.log(`입력창 발견: ${hasInput ? '✅' : '❌'}`);
console.log(`전송 버튼 발견: ${hasButton ? '✅' : '❌'}`);

const canWork = hasChrome && isCorrectSite && hasInput;
console.log(`\n🎯 기본 작동 가능성: ${canWork ? '✅ 가능' : '❌ 불가능'}`);

if (!canWork) {
    console.log("\n🚨 가장 큰 문제들:");
    if (!hasChrome) console.log("1. Chrome Extension이 제대로 설치/로드되지 않음");
    if (!isCorrectSite) console.log("2. 지원하지 않는 사이트이거나 잘못된 페이지");
    if (!hasInput) console.log("3. 입력창을 찾을 수 없음 (페이지 로드 문제?)");
} else {
    console.log("\n✅ 기본 조건은 충족됨");
    console.log("💡 __simpleInputTest() 실행 후 버튼 상태를 확인하세요");
}

console.log("\n" + "=".repeat(50));
console.log("💡 이 진단 결과를 개발자에게 제공하면 정확한 해결책을 받을 수 있습니다.");