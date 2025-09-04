/**
 * ChatGPT 직접 테스트 - Extension 없이 작동하는 버전
 * 
 * 진단 결과:
 * - 입력창 발견: ✅ DIV (contenteditable) #prompt-textarea
 * - 기본 조건 충족: ✅
 * - chrome.runtime 없음: ❌ (Extension 문제)
 * 
 * Extension 문제를 우회하여 직접 작동시켜보겠습니다.
 */

console.clear();
console.log("%c🎯 ChatGPT 직접 테스트", "color: #00cc00; font-size: 18px; font-weight: bold;");
console.log("Extension 문제를 우회하여 ChatGPT에서 직접 메시지를 전송해보겠습니다.\n");

/**
 * ChatGPT 전용 메시지 전송 함수 (Extension 독립)
 */
async function sendChatGPTDirectly(text = `직접 테스트 메시지 ${Date.now()}`) {
    console.log(`📤 전송할 메시지: "${text}"`);
    
    try {
        // 1단계: 입력창 찾기 (진단에서 확인된 selector 사용)
        console.log("1️⃣ 입력창 찾기...");
        const input = document.querySelector('#prompt-textarea.ProseMirror[contenteditable="true"]') ||
                     document.querySelector('div[contenteditable="true"]#prompt-textarea') ||
                     document.querySelector('#prompt-textarea') ||
                     document.querySelector('div[contenteditable="true"]');
        
        if (!input) {
            console.log("❌ 입력창을 찾을 수 없습니다");
            return false;
        }
        
        console.log("✅ 입력창 발견:", input.tagName, input.id, input.className);
        
        // 2단계: 입력창에 텍스트 입력
        console.log("2️⃣ 텍스트 입력...");
        input.focus();
        
        // Clear first
        input.textContent = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        
        // Insert text
        input.textContent = text;
        
        // 다양한 이벤트 발생 (React 감지용)
        const events = [
            new Event('beforeinput', { bubbles: true }),
            new InputEvent('input', { 
                bubbles: true, 
                inputType: 'insertText', 
                data: text 
            }),
            new Event('change', { bubbles: true }),
            new KeyboardEvent('keydown', { 
                key: 'Unidentified', 
                bubbles: true 
            }),
            new KeyboardEvent('keyup', { 
                key: 'Unidentified', 
                bubbles: true 
            })
        ];
        
        events.forEach(event => input.dispatchEvent(event));
        console.log("✅ 텍스트 입력 완료");
        
        // 3단계: 버튼 활성화 대기
        console.log("3️⃣ 전송 버튼 활성화 대기 (5초)...");
        await new Promise(resolve => setTimeout(resolve, 5000));
        
        // 4단계: 전송 버튼 찾기 (ChatGPT 특화 방법)
        console.log("4️⃣ ChatGPT 전송 버튼 찾기...");
        let sendButton = null;
        
        // 방법 1: data-testid
        sendButton = document.querySelector('button[data-testid="send-button"]');
        if (sendButton && !sendButton.disabled) {
            console.log("✅ 방법 1: data-testid로 전송 버튼 발견");
        } else {
            // 방법 2: aria-label
            sendButton = document.querySelector('button[aria-label*="send" i]') ||
                        document.querySelector('button[aria-label*="Send" i]');
            if (sendButton && !sendButton.disabled) {
                console.log("✅ 방법 2: aria-label로 전송 버튼 발견");
            } else {
                // 방법 3: SVG path (화살표 아이콘)
                const allButtons = document.querySelectorAll('button');
                for (const btn of allButtons) {
                    const paths = btn.querySelectorAll('path');
                    for (const path of paths) {
                        const d = path.getAttribute('d');
                        if (d && (d.includes('M8.99992 16V6.41407') || 
                                 d.includes('16V6.414') || 
                                 d.includes('M8.99992'))) {
                            if (!btn.disabled) {
                                sendButton = btn;
                                console.log("✅ 방법 3: SVG 화살표 path로 전송 버튼 발견");
                                break;
                            }
                        }
                    }
                    if (sendButton) break;
                }
            }
        }
        
        if (!sendButton) {
            console.log("❌ 전송 버튼을 찾을 수 없습니다");
            console.log("💡 활성화된 버튼 목록:");
            
            const activeButtons = document.querySelectorAll('button:not([disabled])');
            Array.from(activeButtons).slice(0, 10).forEach((btn, i) => {
                const label = btn.getAttribute('aria-label') || 
                            btn.textContent?.trim().slice(0, 30) || 
                            'no-label';
                console.log(`   ${i+1}. "${label}"`);
                
                // SVG 확인
                const svg = btn.querySelector('svg');
                if (svg) {
                    console.log(`      → SVG 있음`);
                }
                
                // Path 확인
                const paths = btn.querySelectorAll('path');
                if (paths.length > 0) {
                    console.log(`      → Path ${paths.length}개`);
                    Array.from(paths).slice(0, 2).forEach((path, pi) => {
                        const d = path.getAttribute('d');
                        if (d) {
                            console.log(`        Path ${pi+1}: ${d.slice(0, 50)}...`);
                        }
                    });
                }
            });
            return false;
        }
        
        // 5단계: 전송 버튼 클릭
        console.log("5️⃣ 전송 버튼 클릭...");
        console.log("버튼 정보:", {
            tagName: sendButton.tagName,
            className: sendButton.className,
            ariaLabel: sendButton.getAttribute('aria-label'),
            disabled: sendButton.disabled
        });
        
        // 강화된 클릭 이벤트 시퀀스
        const clickEvents = [
            new PointerEvent('pointerdown', { bubbles: true, cancelable: true }),
            new MouseEvent('mousedown', { bubbles: true, cancelable: true }),
            new FocusEvent('focus', { bubbles: true }),
            new PointerEvent('pointerup', { bubbles: true, cancelable: true }),
            new MouseEvent('mouseup', { bubbles: true, cancelable: true }),
            new MouseEvent('click', { bubbles: true, cancelable: true })
        ];
        
        clickEvents.forEach(event => {
            try {
                sendButton.dispatchEvent(event);
            } catch (e) {
                console.log(`이벤트 발생 실패: ${event.type}`);
            }
        });
        
        // 추가 보장: 직접 click() 호출
        try {
            sendButton.click();
        } catch (e) {
            console.log("직접 click() 실패:", e);
        }
        
        console.log("✅ 전송 버튼 클릭 완료!");
        console.log("🎉 메시지 전송이 성공했는지 ChatGPT 화면을 확인하세요!");
        
        return true;
        
    } catch (error) {
        console.error("❌ 오류 발생:", error);
        return false;
    }
}

/**
 * 버튼 상태 실시간 모니터링
 */
function monitorButtonState() {
    console.log("\n👁️ 실시간 버튼 상태 모니터링 시작...");
    
    let lastButtonCount = 0;
    const checkInterval = setInterval(() => {
        // 현재 활성 버튼 수
        const activeButtons = document.querySelectorAll('button:not([disabled])');
        
        // Send 관련 버튼 찾기
        const sendButtons = Array.from(activeButtons).filter(btn => {
            const label = btn.getAttribute('aria-label')?.toLowerCase() || '';
            const text = btn.textContent?.toLowerCase() || '';
            const hasArrow = btn.querySelector('path[d*="M8.99992"]');
            
            return label.includes('send') || 
                   text.includes('send') || 
                   btn.getAttribute('data-testid') === 'send-button' ||
                   hasArrow;
        });
        
        if (sendButtons.length !== lastButtonCount) {
            lastButtonCount = sendButtons.length;
            console.log(`📊 전송 버튼 상태 변화: ${sendButtons.length}개 활성`);
            
            if (sendButtons.length > 0) {
                console.log("✅ 전송 버튼이 활성화되었습니다!");
                sendButtons.forEach((btn, i) => {
                    const label = btn.getAttribute('aria-label') || 
                                btn.textContent?.trim() || 
                                'icon-button';
                    console.log(`   ${i+1}. "${label}"`);
                });
                
                console.log("💡 이제 sendChatGPTDirectly() 실행해보세요!");
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
window.sendChatGPTDirectly = sendChatGPTDirectly;
window.monitorButtonState = monitorButtonState;

// 사용 안내
console.log("💡 사용법:");
console.log("1. sendChatGPTDirectly()                    - 기본 테스트 메시지 전송");
console.log("2. sendChatGPTDirectly('내가 보낼 메시지')    - 커스텀 메시지 전송");
console.log("3. monitorButtonState()                     - 버튼 상태 실시간 모니터링");

console.log("\n⚠️ Extension 문제:");
console.log("chrome.runtime이 없어서 Extension 기능이 작동하지 않지만,");
console.log("이 직접 방법으로 ChatGPT 메시지 전송이 가능합니다.");

console.log("\n🎯 지금 바로 테스트해보세요:");
console.log("sendChatGPTDirectly('안녕하세요! Extension 없이 직접 전송 테스트입니다.')");

// 자동으로 버튼 모니터링 시작
setTimeout(() => {
    monitorButtonState();
}, 2000);