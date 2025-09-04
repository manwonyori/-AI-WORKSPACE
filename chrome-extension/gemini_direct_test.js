/**
 * Google AI Studio/Gemini 직접 테스트 - Extension 없이 작동하는 버전
 * 
 * 진단 결과:
 * - 입력창 발견: ✅ TEXTAREA .textarea (보임)
 * - 기본 조건 충족: ✅
 * - chrome.runtime 없음: ❌ (Extension 문제)
 * 
 * Extension 문제를 우회하여 직접 작동시켜보겠습니다.
 */

console.clear();
console.log("%c🎯 Google AI Studio 직접 테스트", "color: #4285f4; font-size: 18px; font-weight: bold;");
console.log("Extension 문제를 우회하여 Google AI Studio에서 직접 메시지를 전송해보겠습니다.\n");

/**
 * Google AI Studio/Gemini 전용 메시지 전송 함수 (Extension 독립)
 */
async function sendGeminiDirectly(text = `Gemini 직접 테스트 메시지 ${Date.now()}`) {
    console.log(`📤 전송할 메시지: "${text}"`);
    
    try {
        // 1단계: 입력창 찾기 (진단에서 확인된 textarea 사용)
        console.log("1️⃣ 입력창 찾기...");
        const input = document.querySelector('textarea.textarea') ||
                     document.querySelector('textarea[aria-label*="Type something"]') ||
                     document.querySelector('textarea[placeholder]') ||
                     document.querySelector('textarea');
        
        if (!input) {
            console.log("❌ 입력창을 찾을 수 없습니다");
            return false;
        }
        
        console.log("✅ 입력창 발견:", {
            tagName: input.tagName,
            className: input.className,
            ariaLabel: input.getAttribute('aria-label'),
            placeholder: input.getAttribute('placeholder')
        });
        
        // 2단계: 입력창에 텍스트 입력
        console.log("2️⃣ 텍스트 입력...");
        input.focus();
        
        // Clear first
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        
        // Insert text
        input.value = text;
        
        // Angular용 이벤트 시퀀스
        const events = [
            new Event('input', { bubbles: true }),
            new Event('change', { bubbles: true }),
            new Event('blur', { bubbles: true }),  // Angular change detection 트리거
            new KeyboardEvent('keydown', { 
                key: 'Enter', 
                code: 'Enter',
                bubbles: true 
            }),
            new KeyboardEvent('keyup', { 
                key: 'Enter', 
                code: 'Enter',
                bubbles: true 
            })
        ];
        
        events.forEach(event => input.dispatchEvent(event));
        console.log("✅ 텍스트 입력 완료");
        
        // 3단계: 버튼 활성화 대기 (Gemini는 좀 더 오래 걸림)
        console.log("3️⃣ 전송 버튼 활성화 대기 (7초)...");
        await new Promise(resolve => setTimeout(resolve, 7000));
        
        // 4단계: 전송 버튼 찾기 (Gemini/AI Studio 특화 방법)
        console.log("4️⃣ Gemini 전송 버튼 찾기...");
        let sendButton = null;
        
        // 방법 1: Send message aria-label (가장 정확)
        sendButton = document.querySelector('button[aria-label="Send message"]');
        if (sendButton && !sendButton.disabled && !sendButton.hasAttribute('disabled')) {
            console.log("✅ 방법 1: aria-label='Send message'로 전송 버튼 발견");
        } else {
            // 방법 2: mat-icon-button with send icon
            sendButton = document.querySelector('button.mat-icon-button:has(mat-icon[fonticon="send"])');
            if (sendButton && !sendButton.disabled) {
                console.log("✅ 방법 2: mat-icon-button with send로 전송 버튼 발견");
            } else {
                // 방법 3: mat-icon send 아이콘 찾기
                const sendIcons = document.querySelectorAll('mat-icon[fonticon="send"]');
                for (const icon of sendIcons) {
                    const btn = icon.closest('button') || icon.closest('[role="button"]');
                    if (btn && !btn.disabled && !btn.hasAttribute('disabled')) {
                        // 버튼이 보이는지 확인
                        const rect = btn.getBoundingClientRect();
                        const isVisible = rect.width > 0 && rect.height > 0;
                        
                        if (isVisible) {
                            sendButton = btn;
                            console.log("✅ 방법 3: mat-icon send로 전송 버튼 발견");
                            break;
                        }
                    }
                }
            }
        }
        
        // 방법 4: Send 관련 텍스트가 있는 버튼
        if (!sendButton) {
            const allButtons = document.querySelectorAll('button');
            for (const btn of allButtons) {
                const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
                const text = btn.textContent?.toLowerCase() || '';
                const title = btn.getAttribute('title')?.toLowerCase() || '';
                
                if ((ariaLabel.includes('send') || 
                     text.includes('send') || 
                     title.includes('send')) &&
                    !btn.disabled && 
                    !btn.hasAttribute('disabled')) {
                    
                    const rect = btn.getBoundingClientRect();
                    const isVisible = rect.width > 0 && rect.height > 0;
                    
                    if (isVisible) {
                        sendButton = btn;
                        console.log("✅ 방법 4: Send 텍스트로 전송 버튼 발견");
                        break;
                    }
                }
            }
        }
        
        if (!sendButton) {
            console.log("❌ 전송 버튼을 찾을 수 없습니다");
            console.log("💡 활성화된 버튼 목록 (mat-icon 포함):");
            
            const activeButtons = document.querySelectorAll('button:not([disabled])');
            Array.from(activeButtons).slice(0, 15).forEach((btn, i) => {
                const label = btn.getAttribute('aria-label') || 
                            btn.textContent?.trim().slice(0, 30) || 
                            'no-label';
                
                // mat-icon 확인
                const matIcon = btn.querySelector('mat-icon');
                const matIconInfo = matIcon ? 
                    `[mat-icon: ${matIcon.getAttribute('fonticon') || matIcon.textContent || 'unknown'}]` : '';
                
                console.log(`   ${i+1}. "${label}" ${matIconInfo}`);
            });
            
            // 특별히 mat-icon send 찾기
            const sendIcons = document.querySelectorAll('mat-icon[fonticon="send"]');
            console.log(`\n🔍 mat-icon send 아이콘 ${sendIcons.length}개 발견:`);
            sendIcons.forEach((icon, i) => {
                const parent = icon.closest('button') || icon.closest('[role="button"]');
                console.log(`   ${i+1}. Parent: ${parent?.tagName} ${parent?.className}`);
                console.log(`      Disabled: ${parent?.disabled || parent?.hasAttribute('disabled')}`);
            });
            
            return false;
        }
        
        // 5단계: 전송 버튼 클릭
        console.log("5️⃣ 전송 버튼 클릭...");
        console.log("버튼 정보:", {
            tagName: sendButton.tagName,
            className: sendButton.className,
            ariaLabel: sendButton.getAttribute('aria-label'),
            disabled: sendButton.disabled,
            hasDisabledAttr: sendButton.hasAttribute('disabled')
        });
        
        // Angular/Material 호환 클릭 이벤트 시퀀스
        const clickEvents = [
            new PointerEvent('pointerdown', { bubbles: true, cancelable: true }),
            new MouseEvent('mousedown', { bubbles: true, cancelable: true }),
            new FocusEvent('focus', { bubbles: true }),
            new PointerEvent('pointerup', { bubbles: true, cancelable: true }),
            new MouseEvent('mouseup', { bubbles: true, cancelable: true }),
            new MouseEvent('click', { bubbles: true, cancelable: true })
        ];
        
        // 클릭 이벤트 발생
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
        
        // Angular 변경 감지 강제 트리거 (가능한 경우)
        try {
            // ng-zone을 통한 변경 감지 (실험적)
            if (window.ng && window.ng.getComponent) {
                const component = window.ng.getComponent(sendButton);
                if (component && component.changeDetectorRef) {
                    component.changeDetectorRef.detectChanges();
                }
            }
        } catch (e) {
            // 무시 (선택적 기능)
        }
        
        console.log("✅ 전송 버튼 클릭 완료!");
        console.log("🎉 메시지 전송이 성공했는지 Gemini 화면을 확인하세요!");
        
        return true;
        
    } catch (error) {
        console.error("❌ 오류 발생:", error);
        return false;
    }
}

/**
 * Ctrl+Enter 방식으로 전송 시도
 */
async function sendGeminiWithCtrlEnter(text = `Ctrl+Enter 테스트 ${Date.now()}`) {
    console.log(`📤 Ctrl+Enter 방식으로 전송: "${text}"`);
    
    try {
        const input = document.querySelector('textarea.textarea') ||
                     document.querySelector('textarea');
        
        if (!input) {
            console.log("❌ 입력창을 찾을 수 없습니다");
            return false;
        }
        
        input.focus();
        input.value = text;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        
        // Ctrl+Enter 이벤트
        const ctrlEnterEvent = new KeyboardEvent('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13,
            ctrlKey: true,
            bubbles: true,
            cancelable: true
        });
        
        input.dispatchEvent(ctrlEnterEvent);
        console.log("✅ Ctrl+Enter 전송 완료!");
        
        return true;
    } catch (error) {
        console.error("❌ Ctrl+Enter 오류:", error);
        return false;
    }
}

/**
 * 버튼 상태 모니터링 (Gemini용)
 */
function monitorGeminiButtons() {
    console.log("\n👁️ Gemini 버튼 상태 실시간 모니터링...");
    
    let lastSendButtonCount = 0;
    const checkInterval = setInterval(() => {
        // Send 관련 버튼 찾기
        const sendButtons = [];
        
        // mat-icon send 찾기
        const sendIcons = document.querySelectorAll('mat-icon[fonticon="send"]');
        sendIcons.forEach(icon => {
            const btn = icon.closest('button');
            if (btn && !btn.disabled && !btn.hasAttribute('disabled')) {
                sendButtons.push(btn);
            }
        });
        
        // aria-label Send 찾기
        const labelButtons = document.querySelectorAll('button[aria-label*="send" i]');
        labelButtons.forEach(btn => {
            if (!btn.disabled && !btn.hasAttribute('disabled') && !sendButtons.includes(btn)) {
                sendButtons.push(btn);
            }
        });
        
        if (sendButtons.length !== lastSendButtonCount) {
            lastSendButtonCount = sendButtons.length;
            console.log(`📊 Gemini 전송 버튼 상태: ${sendButtons.length}개 활성`);
            
            if (sendButtons.length > 0) {
                console.log("✅ Gemini 전송 버튼이 활성화되었습니다!");
                sendButtons.forEach((btn, i) => {
                    const label = btn.getAttribute('aria-label') || 
                                btn.textContent?.trim() || 
                                'mat-icon-button';
                    console.log(`   ${i+1}. "${label}"`);
                });
                
                console.log("💡 이제 sendGeminiDirectly() 실행해보세요!");
            }
        }
    }, 1000);
    
    // 30초 후 모니터링 중지
    setTimeout(() => {
        clearInterval(checkInterval);
        console.log("👁️ Gemini 버튼 모니터링 종료");
    }, 30000);
    
    return checkInterval;
}

// 전역 함수로 등록
window.sendGeminiDirectly = sendGeminiDirectly;
window.sendGeminiWithCtrlEnter = sendGeminiWithCtrlEnter;
window.monitorGeminiButtons = monitorGeminiButtons;

// 사용 안내
console.log("💡 사용법:");
console.log("1. sendGeminiDirectly()                     - 기본 테스트 메시지 전송");
console.log("2. sendGeminiDirectly('내가 보낼 메시지')     - 커스텀 메시지 전송");
console.log("3. sendGeminiWithCtrlEnter()               - Ctrl+Enter 방식 전송");
console.log("4. monitorGeminiButtons()                  - 버튼 상태 실시간 모니터링");

console.log("\n⚠️ Extension 문제:");
console.log("chrome.runtime이 없어서 Extension 기능이 작동하지 않지만,");
console.log("이 직접 방법으로 Google AI Studio 메시지 전송이 가능합니다.");

console.log("\n🎯 지금 바로 테스트해보세요:");
console.log("sendGeminiDirectly('안녕하세요! Extension 없이 Gemini 직접 전송 테스트입니다.')");

console.log("\n📍 현재 사이트 정보:");
console.log(`URL: ${location.href}`);
console.log(`Gemini UI 로드 상태: ${document.querySelector('textarea.textarea') ? '✅' : '❌'}`);

// 자동으로 버튼 모니터링 시작
setTimeout(() => {
    monitorGeminiButtons();
}, 2000);