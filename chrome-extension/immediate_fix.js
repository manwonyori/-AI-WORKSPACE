/**
 * IMMEDIATE FIX - Extension 없이 직접 작동시키기
 * 
 * Extension이 로드되지 않는 문제를 우회하여
 * 직접 ChatGPT에서 메시지를 전송해보겠습니다.
 */

console.clear();
console.log("%c🚀 IMMEDIATE FIX - Extension 우회 직접 테스트", "color: #00cc00; font-size: 18px; font-weight: bold;");

// ChatGPT 직접 메시지 전송 함수
async function sendChatGPTMessage(text = `직접 테스트 ${Date.now()}`) {
    console.log(`\n📤 ChatGPT 직접 전송: "${text}"`);
    
    try {
        // 1. 입력창 찾기
        console.log("1️⃣ 입력창 찾기...");
        const input = document.querySelector("#prompt-textarea") || 
                     document.querySelector("div[contenteditable='true']");
        
        if (!input) {
            console.log("❌ 입력창을 찾을 수 없습니다");
            return false;
        }
        
        console.log(`✅ 입력창 발견: ${input.tagName}#${input.id}`);
        
        // 2. 포커스 및 텍스트 입력
        console.log("2️⃣ 텍스트 입력...");
        input.focus();
        
        if (input.tagName === 'TEXTAREA') {
            // TextArea의 경우 React setter 사용
            const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            )?.set;
            
            if (nativeTextAreaValueSetter) {
                nativeTextAreaValueSetter.call(input, text);
            } else {
                input.value = text;
            }
        } else {
            // ContentEditable div의 경우
            input.textContent = text;
        }
        
        // 3. 이벤트 발생 (ChatGPT 버튼 활성화를 위해)
        console.log("3️⃣ 이벤트 발생...");
        input.dispatchEvent(new Event('beforeinput', { bubbles: true }));
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('compositionend', { bubbles: true }));
        input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Unidentified', bubbles: true }));
        input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Unidentified', bubbles: true }));
        
        console.log("✅ 텍스트 입력 및 이벤트 완료");
        
        // 4. 잠시 대기 (버튼 활성화)
        console.log("4️⃣ 버튼 활성화 대기 (3초)...");
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // 5. 전송 버튼 찾기
        console.log("5️⃣ 전송 버튼 찾기...");
        let sendButton = null;
        
        // 방법 1: data-testid로 찾기
        sendButton = document.querySelector('button[data-testid="send-button"]');
        if (sendButton && !sendButton.disabled) {
            console.log("✅ send-button 발견 (data-testid)");
        } else {
            // 방법 2: aria-label로 찾기
            sendButton = document.querySelector('button[aria-label*="Send" i]');
            if (sendButton && !sendButton.disabled) {
                console.log("✅ Send button 발견 (aria-label)");
            } else {
                // 방법 3: SVG path로 찾기
                const buttons = document.querySelectorAll('button');
                for (const btn of buttons) {
                    const path = btn.querySelector('path[d*="M8.99992"]') || 
                                btn.querySelector('path[d*="16V6.414"]');
                    if (path && !btn.disabled) {
                        sendButton = btn;
                        console.log("✅ SVG path button 발견");
                        break;
                    }
                }
            }
        }
        
        if (!sendButton) {
            console.log("❌ 전송 버튼을 찾을 수 없습니다");
            console.log("💡 활성 버튼 목록:");
            const activeButtons = document.querySelectorAll('button:not([disabled])');
            Array.from(activeButtons).slice(0, 10).forEach((btn, i) => {
                const label = btn.getAttribute('aria-label') || btn.textContent?.trim().slice(0, 20) || 'no-label';
                console.log(`   ${i+1}. "${label}"`);
            });
            return false;
        }
        
        // 6. 버튼 클릭
        console.log("6️⃣ 전송 버튼 클릭...");
        
        // 향상된 클릭 이벤트 시퀀스
        const clickEvents = [
            new PointerEvent('pointerdown', { bubbles: true, cancelable: true }),
            new MouseEvent('mousedown', { bubbles: true, cancelable: true }),
            new PointerEvent('pointerup', { bubbles: true, cancelable: true }),
            new MouseEvent('mouseup', { bubbles: true, cancelable: true }),
            new MouseEvent('click', { bubbles: true, cancelable: true })
        ];
        
        clickEvents.forEach(event => sendButton.dispatchEvent(event));
        
        console.log("✅ 전송 버튼 클릭 완료!");
        console.log("🎉 메시지 전송 성공!");
        
        return true;
        
    } catch (error) {
        console.log(`❌ 오류 발생: ${error.message}`);
        console.error(error);
        return false;
    }
}

// 실시간 버튼 모니터링
function monitorButtons() {
    console.log("\n👁️ 실시간 버튼 상태 모니터링 시작...");
    
    let buttonCount = 0;
    const checkInterval = setInterval(() => {
        const activeButtons = document.querySelectorAll('button:not([disabled])');
        const sendButtons = Array.from(activeButtons).filter(btn => {
            const label = btn.getAttribute('aria-label')?.toLowerCase() || '';
            const text = btn.textContent?.toLowerCase() || '';
            const hasPath = btn.querySelector('path[d*="M8.99992"]');
            
            return label.includes('send') || 
                   text.includes('send') || 
                   btn.getAttribute('data-testid') === 'send-button' ||
                   hasPath;
        });
        
        if (sendButtons.length !== buttonCount) {
            buttonCount = sendButtons.length;
            console.log(`📊 전송 버튼 상태 변화: ${buttonCount}개 활성`);
            
            if (buttonCount > 0) {
                console.log("✅ 전송 버튼이 활성화되었습니다!");
                sendButtons.forEach((btn, i) => {
                    const label = btn.getAttribute('aria-label') || btn.textContent?.trim() || 'no-label';
                    console.log(`   ${i+1}. "${label}"`);
                });
            }
        }
    }, 1000);
    
    // 30초 후 모니터링 중지
    setTimeout(() => {
        clearInterval(checkInterval);
        console.log("👁️ 버튼 모니터링 종료");
    }, 30000);
    
    return checkInterval;
}

// 전역 함수로 등록
window.__directSend = sendChatGPTMessage;
window.__monitor = monitorButtons;

// 사용 안내
console.log("\n💡 사용법:");
console.log("1. __directSend()              - 직접 메시지 전송");
console.log("2. __directSend('내 메시지')    - 커스텀 메시지 전송");
console.log("3. __monitor()                 - 버튼 상태 실시간 모니터링");

console.log("\n⚠️ Extension 문제 해결:");
console.log("1. chrome://extensions 에서 'AI Workspace Controller' 확인");
console.log("2. 개발자 모드 켜기");
console.log("3. '새로고침' 버튼 클릭");
console.log("4. 오류가 있다면 수정 후 다시 새로고침");

console.log("\n🎯 지금 당장 테스트해보세요: __directSend()");

// 자동으로 버튼 모니터링 시작
setTimeout(() => {
    monitorButtons();
}, 2000);