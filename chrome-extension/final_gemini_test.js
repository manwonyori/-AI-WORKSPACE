/**
 * Gemini Final Integration Test v1.3.8
 * 
 * 이 스크립트를 Gemini/AI Studio 콘솔에서 실행하여
 * v1.3.8 extension과 동일한 방식으로 작동하는지 테스트
 */

console.clear();
console.log("%c🚀 Gemini Final Integration Test v1.3.8", "color: #4CAF50; font-size: 16px; font-weight: bold");
console.log("=" + "=".repeat(60));

// Utility
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

/**
 * sendGeminiMessageReliably - 최종 안정화 버전
 * @param {string} message - 전송할 메시지
 * @returns {Promise<boolean>} 성공 여부
 */
async function sendGeminiMessageReliably(message) {
    console.log("\n📋 Starting Gemini message send process...");
    console.log("Message:", message);
    console.log("-".repeat(60));
    
    const editorSelector = 'div.ql-editor';
    // 전송 버튼 셀렉터: aria-label이 "Send message"인 버튼을 최우선으로 찾고,
    // 그 다음 mat-icon[fonticon="send"]를 포함하는 mat-icon-button 클래스의 버튼을 찾습니다.
    const sendButtonSelector = 'button[aria-label="Send message"], button.mat-icon-button:has(mat-icon[fonticon="send"])'; 

    const editor = document.querySelector(editorSelector);
    if (!editor) {
        console.error('❌ Gemini Quill editor를 찾을 수 없습니다.');
        return false;
    }
    console.log('✅ Found Quill editor');

    // 1. 텍스트 입력: Quill 에디터의 innerHTML을 직접 조작합니다.
    console.log('\n📝 Step 1: Text Input');
    
    // Check for Quill instance first
    const quillInstance = editor.__quill;
    if (quillInstance && typeof quillInstance.setText === 'function') {
        console.log('  Using Quill API (most stable)');
        quillInstance.setText(message);
    } else {
        console.log('  Using innerHTML (primary fallback)');
        editor.innerHTML = `<p>${message}</p>`;
    }
    console.log('✅ 텍스트 입력 완료');

    // 2. 적절한 이벤트 디스패치: Angular의 변경 감지를 트리거
    console.log('\n🔄 Step 2: Event Dispatch for Angular');
    editor.dispatchEvent(new Event('input', { bubbles: true }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
    editor.dispatchEvent(new Event('blur', { bubbles: true }));
    console.log('✅ 이벤트 디스패치 완료 (input, change, blur)');

    // 3. 동적으로 나타나는 전송 버튼을 기다리고 클릭
    console.log('\n⏳ Step 3: Waiting for Button Activation');
    let sendButton = document.querySelector(sendButtonSelector);

    // 버튼이 없거나 비활성화되어 있다면, MutationObserver를 사용하여 기다립니다.
    if (!sendButton || sendButton.hasAttribute('disabled')) {
        console.log('  버튼이 없거나 비활성화 상태, MutationObserver 시작...');
        
        try {
            await new Promise((resolve, reject) => {
                let checkCount = 0;
                const observer = new MutationObserver((mutationsList, observer) => {
                    checkCount++;
                    
                    // Log significant mutations
                    mutationsList.forEach(mutation => {
                        if (mutation.type === 'attributes' && 
                            mutation.attributeName === 'disabled' && 
                            mutation.target.tagName === 'BUTTON') {
                            console.log(`  🔄 Button disabled state changed: ${mutation.target.hasAttribute('disabled') ? 'disabled' : 'enabled'}`);
                        }
                    });
                    
                    sendButton = document.querySelector(sendButtonSelector);
                    // 버튼이 존재하고 'disabled' 속성이 없으면 (활성화되면) 관찰을 중단하고 resolve
                    if (sendButton && !sendButton.hasAttribute('disabled')) {
                        console.log(`  ✅ 버튼 활성화 감지! (after ${checkCount} checks)`);
                        observer.disconnect();
                        resolve();
                    }
                });

                // body 전체를 관찰
                observer.observe(document.body, { 
                    childList: true, 
                    subtree: true, 
                    attributes: true, 
                    attributeFilter: ['disabled'] 
                });

                // 무한 대기를 방지하기 위한 타임아웃 설정
                setTimeout(() => {
                    observer.disconnect();
                    const finalButton = document.querySelector(sendButtonSelector);
                    if (finalButton && !finalButton.hasAttribute('disabled')) {
                        console.log('  ✅ 버튼 활성화 (timeout check)');
                        resolve();
                    } else {
                        console.error("  ❌ 타임아웃: 10초 내에 버튼이 활성화되지 않음");
                        reject(new Error("Timeout waiting for button"));
                    }
                }, 10000); // 10초 타임아웃
            });
        } catch (error) {
            console.error('❌ 버튼 대기 중 오류:', error.message);
            return false;
        }
    }

    // 대기 후 버튼을 다시 쿼리하여 최신 상태를 확보
    console.log('\n🖱️ Step 4: Clicking Send Button');
    sendButton = document.querySelector(sendButtonSelector);
    
    if (sendButton && !sendButton.hasAttribute('disabled')) {
        console.log('  버튼 상태: 활성화됨');
        
        // Enhanced click with pointer events
        try {
            const opts = { bubbles: true, cancelable: true, composed: true };
            sendButton.dispatchEvent(new PointerEvent('pointerdown', opts));
            sendButton.dispatchEvent(new MouseEvent('mousedown', opts));
            sendButton.dispatchEvent(new PointerEvent('pointerup', opts));
            sendButton.dispatchEvent(new MouseEvent('mouseup', opts));
            sendButton.dispatchEvent(new MouseEvent('click', opts));
            console.log('  ✅ Pointer events로 버튼 클릭 완료');
        } catch (e) {
            sendButton.click();
            console.log('  ✅ 기본 click()으로 버튼 클릭 완료');
        }
        
        console.log('\n✅ Gemini 메시지가 성공적으로 전송되었습니다!');
        return true;
    } else {
        console.error('\n❌ 전송 버튼을 찾을 수 없거나 여전히 비활성화 상태입니다.');
        return false;
    }
}

// 테스트 실행 함수
async function runTest() {
    console.log("\n" + "=".repeat(60));
    console.log("🧪 테스트 시작...\n");
    
    const testMessage = `테스트 메시지 - ${new Date().toLocaleTimeString('ko-KR')}`;
    
    try {
        const success = await sendGeminiMessageReliably(testMessage);
        
        console.log("\n" + "=".repeat(60));
        console.log("📊 테스트 결과:");
        console.log(`  결과: ${success ? '✅ 성공' : '❌ 실패'}`);
        console.log(`  메시지: "${testMessage}"`);
        console.log(`  시각: ${new Date().toLocaleString('ko-KR')}`);
        
    } catch (error) {
        console.error("\n❌ 테스트 실패:", error);
    }
    
    console.log("\n" + "=".repeat(60));
}

// 사용법 안내
console.log("\n💡 사용 방법:");
console.log("1. sendGeminiMessageReliably('메시지')  - 메시지 전송");
console.log("2. runTest()                             - 자동 테스트 실행");
console.log("\n예시:");
console.log("  await sendGeminiMessageReliably('안녕하세요, 오늘 날씨 어때요?')");
console.log("\n⏰ 3초 후 자동 테스트가 시작됩니다...");

// 자동 테스트 실행
setTimeout(() => {
    console.clear();
    runTest();
}, 3000);