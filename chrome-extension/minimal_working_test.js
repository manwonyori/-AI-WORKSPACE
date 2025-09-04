/**
 * MINIMAL WORKING TEST - 가장 간단하게 작동하는 버전
 * 
 * 복잡한 코드는 제외하고 오직 작동만 하는 최소 버전
 * 각 플랫폼에서 이것부터 테스트해보세요.
 */

console.clear();
console.log("%c🎯 MINIMAL WORKING TEST", "color: #00cc00; font-size: 18px; font-weight: bold;");
console.log("가장 간단한 방법으로 메시지 전송을 시도합니다.\n");

// 현재 플랫폼 확인
const hostname = location.hostname;
let platform = "unknown";

if (hostname.includes("chatgpt.com")) {
    platform = "chatgpt";
} else if (hostname.includes("claude.ai")) {
    platform = "claude";
} else if (hostname.includes("perplexity.ai")) {
    platform = "perplexity";
} else if (hostname.includes("aistudio.google.com")) {
    platform = "gemini";
} else if (hostname.includes("gemini.google.com")) {
    platform = "gemini";
}

console.log(`🌐 Platform: ${platform}`);

/**
 * 가장 간단한 메시지 전송 함수
 */
async function sendMinimalMessage(text = `테스트 메시지 ${Date.now()}`) {
    console.log(`\n🚀 Sending to ${platform}: "${text}"`);
    
    let inputFound = false;
    let buttonFound = false;
    
    try {
        // 1단계: 입력창 찾기
        console.log("1️⃣ 입력창 찾기...");
        let input = null;
        
        if (platform === "chatgpt") {
            input = document.querySelector("textarea") || 
                   document.querySelector("[contenteditable='true']");
        } else if (platform === "claude") {
            input = document.querySelector("[contenteditable='true']") ||
                   document.querySelector("textarea");
        } else if (platform === "perplexity") {
            input = document.querySelector("textarea") ||
                   document.querySelector("[contenteditable='true']");
        } else if (platform === "gemini") {
            input = document.querySelector(".ql-editor") ||
                   document.querySelector("textarea") ||
                   document.querySelector("[contenteditable='true']");
        } else {
            // 범용
            input = document.querySelector("textarea") ||
                   document.querySelector("[contenteditable='true']") ||
                   document.querySelector(".ql-editor");
        }
        
        if (!input) {
            console.log("❌ 입력창을 찾을 수 없습니다");
            return false;
        }
        
        inputFound = true;
        console.log(`✅ 입력창 발견: ${input.tagName}`);
        
        // 2단계: 텍스트 입력
        console.log("2️⃣ 텍스트 입력...");
        input.focus();
        
        if (input.tagName === "TEXTAREA") {
            input.value = text;
        } else if (platform === "gemini" && input.classList.contains("ql-editor")) {
            input.innerHTML = `<p>${text}</p>`;
        } else {
            input.textContent = text;
        }
        
        // 이벤트 발생
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        
        console.log("✅ 텍스트 입력 완료");
        
        // 3단계: 잠시 대기 (버튼 활성화를 위해)
        console.log("3️⃣ 버튼 활성화 대기 (2초)...");
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 4단계: 전송 버튼 찾기 및 클릭
        console.log("4️⃣ 전송 버튼 찾기...");
        let button = null;
        
        // 모든 버튼을 찾아서 가장 적합한 것 선택
        const allButtons = document.querySelectorAll("button");
        console.log(`   총 ${allButtons.length}개 버튼 검사 중...`);
        
        for (const btn of allButtons) {
            // 버튼이 보이고 활성화되어 있는지 확인
            const rect = btn.getBoundingClientRect();
            const visible = rect.width > 0 && rect.height > 0;
            const enabled = !btn.disabled && !btn.hasAttribute('disabled');
            
            if (!visible || !enabled) continue;
            
            // 텍스트나 아이콘으로 전송 버튼인지 판단
            const text = btn.textContent?.toLowerCase() || '';
            const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
            const hasIcon = btn.querySelector('svg, mat-icon, path');
            
            const isSendButton = text.includes('send') || 
                               text.includes('전송') || 
                               ariaLabel.includes('send') ||
                               ariaLabel.includes('전송') ||
                               btn.getAttribute('data-testid') === 'send-button' ||
                               (hasIcon && (text === '' || text.length < 5)); // 아이콘만 있는 버튼
            
            if (isSendButton) {
                button = btn;
                console.log(`   ✅ 전송 버튼 발견: "${ariaLabel || text || 'icon-button'}"`);
                break;
            }
        }
        
        if (!button) {
            console.log("❌ 전송 버튼을 찾을 수 없습니다");
            console.log("💡 수동으로 버튼을 클릭해보세요");
            return false;
        }
        
        buttonFound = true;
        
        // 5단계: 버튼 클릭
        console.log("5️⃣ 전송 버튼 클릭...");
        button.click();
        
        console.log("✅ 메시지 전송 완료!");
        return true;
        
    } catch (error) {
        console.log(`❌ 오류 발생: ${error.message}`);
        return false;
    } finally {
        // 결과 요약
        console.log("\n📊 결과 요약:");
        console.log(`   입력창: ${inputFound ? '✅' : '❌'}`);
        console.log(`   전송버튼: ${buttonFound ? '✅' : '❌'}`);
    }
}

/**
 * 단계별 디버그 함수
 */
function debugStepByStep() {
    console.log("\n🔍 단계별 디버그 시작...");
    
    // 단계 1: 입력창 디버그
    console.log("\n1️⃣ 입력창 디버그:");
    const textareas = document.querySelectorAll("textarea");
    const contentEditables = document.querySelectorAll("[contenteditable='true']");
    const qlEditors = document.querySelectorAll(".ql-editor");
    
    console.log(`   Textareas: ${textareas.length}개`);
    console.log(`   ContentEditables: ${contentEditables.length}개`);
    console.log(`   Quill Editors: ${qlEditors.length}개`);
    
    // 단계 2: 버튼 디버그
    console.log("\n2️⃣ 버튼 디버그:");
    const allButtons = document.querySelectorAll("button");
    const enabledButtons = document.querySelectorAll("button:not([disabled])");
    const sendButtons = Array.from(allButtons).filter(btn => {
        const text = btn.textContent?.toLowerCase() || '';
        const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
        return text.includes('send') || text.includes('전송') || ariaLabel.includes('send');
    });
    
    console.log(`   전체 버튼: ${allButtons.length}개`);
    console.log(`   활성 버튼: ${enabledButtons.length}개`);
    console.log(`   전송 버튼: ${sendButtons.length}개`);
    
    // 단계 3: DOM 상태 체크
    console.log("\n3️⃣ DOM 상태:");
    console.log(`   Document ready: ${document.readyState}`);
    console.log(`   Body children: ${document.body?.children.length || 0}개`);
}

// 전역 함수로 등록
window.__sendTest = sendMinimalMessage;
window.__debug = debugStepByStep;

// 사용 안내
console.log("\n💡 사용법:");
console.log("1. __sendTest()           - 메시지 전송 테스트");
console.log("2. __sendTest('내 메시지') - 커스텀 메시지 전송");
console.log("3. __debug()              - 상세 디버그 정보");

console.log("\n⏰ 5초 후 자동으로 디버그를 실행합니다...");
setTimeout(() => {
    debugStepByStep();
    console.log("\n🎯 이제 __sendTest()를 실행해보세요!");
}, 5000);