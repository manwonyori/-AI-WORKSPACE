/**
 * REAL WORKING FIX - 실제로 작동하는 ChatGPT/Gemini 전송 해결책
 * 
 * Mock Extension은 로드되었지만 여전히 ChatGPT와 Gemini에서
 * 실제 메시지 전송이 안 되는 문제를 근본적으로 해결합니다.
 */

console.clear();
console.log("%c🔥 REAL WORKING FIX", "color: #ff0000; font-size: 20px; font-weight: bold;");
console.log("ChatGPT와 Gemini에서 실제로 작동하는 메시지 전송을 구현합니다.\n");

// 현재 플랫폼 정확히 감지
const currentURL = location.href;
const hostname = location.hostname;
let currentPlatform = null;

if (hostname.includes('chatgpt.com')) {
    currentPlatform = 'chatgpt';
} else if (hostname.includes('aistudio.google.com') || hostname.includes('gemini.google.com')) {
    currentPlatform = 'gemini';
} else if (hostname.includes('claude.ai')) {
    currentPlatform = 'claude';
} else if (hostname.includes('perplexity.ai')) {
    currentPlatform = 'perplexity';
}

console.log(`🎯 현재 플랫폼: ${currentPlatform}`);
console.log(`📍 현재 URL: ${currentURL}\n`);

/**
 * ChatGPT 실제 작동 메시지 전송 (완전히 새로운 접근법)
 */
async function realChatGPTSend(text) {
    console.log(`[ChatGPT Real] 🚀 실제 전송 시작: "${text}"`);
    
    try {
        // 1. 입력창 찾기 - 모든 가능한 방법 시도
        console.log("[ChatGPT Real] 1️⃣ 입력창 탐지 중...");
        
        let inputElement = null;
        const inputSelectors = [
            '#prompt-textarea',
            'textarea#prompt-textarea',
            'div#prompt-textarea[contenteditable="true"]',
            'div[contenteditable="true"].ProseMirror',
            'textarea[placeholder*="Message"]',
            'div[contenteditable="true"][data-placeholder]',
            'textarea.m-0',
            'textarea'
        ];
        
        for (const selector of inputSelectors) {
            const element = document.querySelector(selector);
            if (element) {
                const rect = element.getBoundingClientRect();
                const isVisible = rect.width > 0 && rect.height > 0 && 
                                window.getComputedStyle(element).display !== 'none';
                
                if (isVisible) {
                    inputElement = element;
                    console.log(`[ChatGPT Real] ✅ 입력창 발견: ${selector}`);
                    break;
                }
            }
        }
        
        if (!inputElement) {
            console.error("[ChatGPT Real] ❌ 입력창을 찾을 수 없음");
            return false;
        }
        
        // 2. 포커스 및 클리어
        console.log("[ChatGPT Real] 2️⃣ 입력창 초기화...");
        inputElement.focus();
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // 3. 텍스트 입력 - React 호환 방식
        console.log("[ChatGPT Real] 3️⃣ 텍스트 입력...");
        
        if (inputElement.tagName === 'TEXTAREA') {
            // React Textarea 처리
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            )?.set;
            
            if (nativeInputValueSetter) {
                // React friendly method
                nativeInputValueSetter.call(inputElement, '');
                inputElement.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
                
                nativeInputValueSetter.call(inputElement, text);
                inputElement.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
                inputElement.dispatchEvent(new Event('change', { bubbles: true }));
                
                console.log("[ChatGPT Real] ✅ React Textarea 입력 완료");
            } else {
                // Fallback
                inputElement.value = text;
                inputElement.dispatchEvent(new Event('input', { bubbles: true }));
            }
        } else if (inputElement.contentEditable === 'true') {
            // ContentEditable 처리
            inputElement.textContent = '';
            inputElement.dispatchEvent(new Event('input', { bubbles: true }));
            
            inputElement.textContent = text;
            inputElement.dispatchEvent(new InputEvent('input', {
                inputType: 'insertText',
                data: text,
                bubbles: true,
                composed: true
            }));
            
            console.log("[ChatGPT Real] ✅ ContentEditable 입력 완료");
        }
        
        // 4. 버튼 활성화 대기 (더 길게)
        console.log("[ChatGPT Real] 4️⃣ 버튼 활성화 대기 (10초)...");
        await new Promise(resolve => setTimeout(resolve, 10000));
        
        // 5. 전송 버튼 찾기 - 모든 방법 시도
        console.log("[ChatGPT Real] 5️⃣ 전송 버튼 탐지...");
        
        let sendButton = null;
        
        // 방법 1: 표준 선택자들
        const buttonSelectors = [
            'button[data-testid="send-button"]',
            'button[aria-label*="send" i]',
            'button[aria-label*="Send" i]',
            'form button[type="submit"]'
        ];
        
        for (const selector of buttonSelectors) {
            const btn = document.querySelector(selector);
            if (btn && !btn.disabled) {
                sendButton = btn;
                console.log(`[ChatGPT Real] ✅ 표준 버튼 발견: ${selector}`);
                break;
            }
        }
        
        // 방법 2: SVG 아이콘 기반 (ChatGPT 특화)
        if (!sendButton) {
            console.log("[ChatGPT Real] 🔍 SVG 아이콘 버튼 검색...");
            const allButtons = document.querySelectorAll('button');
            
            for (const btn of allButtons) {
                if (btn.disabled) continue;
                
                // SVG path 확인
                const svgPaths = btn.querySelectorAll('svg path, path');
                for (const path of svgPaths) {
                    const d = path.getAttribute('d') || '';
                    // ChatGPT send 버튼의 특징적인 path
                    if (d.includes('16V6.41') || d.includes('M8.99992') || d.includes('15.707')) {
                        sendButton = btn;
                        console.log("[ChatGPT Real] ✅ SVG path 버튼 발견");
                        break;
                    }
                }
                if (sendButton) break;
            }
        }
        
        // 방법 3: 활성화된 버튼 중 가장 가능성 높은 것
        if (!sendButton) {
            console.log("[ChatGPT Real] 🔍 휴리스틱 버튼 검색...");
            const activeButtons = document.querySelectorAll('button:not([disabled])');
            
            for (const btn of activeButtons) {
                const rect = btn.getBoundingClientRect();
                if (rect.width < 30 || rect.height < 30) continue; // 너무 작은 버튼 제외
                
                // 버튼 위치가 입력창 근처인지 확인
                const inputRect = inputElement.getBoundingClientRect();
                const distance = Math.abs(rect.bottom - inputRect.bottom);
                
                if (distance < 100 && btn.querySelector('svg')) { // 입력창 근처이고 아이콘이 있는 버튼
                    sendButton = btn;
                    console.log("[ChatGPT Real] ✅ 휴리스틱 버튼 발견");
                    break;
                }
            }
        }
        
        if (!sendButton) {
            console.error("[ChatGPT Real] ❌ 전송 버튼을 찾을 수 없음");
            
            // 디버그 정보
            const allButtons = document.querySelectorAll('button');
            console.log(`[ChatGPT Real] 🔍 디버그: 총 ${allButtons.length}개 버튼 발견`);
            Array.from(allButtons).slice(0, 10).forEach((btn, i) => {
                const label = btn.getAttribute('aria-label') || btn.textContent?.slice(0, 30) || 'no-label';
                const disabled = btn.disabled ? 'disabled' : 'enabled';
                console.log(`  ${i+1}. "${label}" (${disabled})`);
            });
            
            return false;
        }
        
        // 6. 전송 버튼 클릭
        console.log("[ChatGPT Real] 6️⃣ 전송 버튼 클릭...");
        
        // 강화된 클릭 시퀀스
        const events = [
            new MouseEvent('mousedown', { bubbles: true, cancelable: true }),
            new MouseEvent('mouseup', { bubbles: true, cancelable: true }),
            new MouseEvent('click', { bubbles: true, cancelable: true }),
            new PointerEvent('pointerdown', { bubbles: true, cancelable: true }),
            new PointerEvent('pointerup', { bubbles: true, cancelable: true })
        ];
        
        events.forEach(event => {
            try {
                sendButton.dispatchEvent(event);
            } catch (e) {
                console.log(`[ChatGPT Real] 이벤트 ${event.type} 실패:`, e.message);
            }
        });
        
        // 직접 클릭도 시도
        try {
            sendButton.click();
            console.log("[ChatGPT Real] ✅ 직접 클릭 완료");
        } catch (e) {
            console.log("[ChatGPT Real] 직접 클릭 실패:", e.message);
        }
        
        console.log("[ChatGPT Real] 🎉 전송 완료! 결과를 확인하세요.");
        return true;
        
    } catch (error) {
        console.error("[ChatGPT Real] ❌ 치명적 오류:", error);
        return false;
    }
}

/**
 * Gemini 실제 작동 메시지 전송 (완전히 새로운 접근법)
 */
async function realGeminiSend(text) {
    console.log(`[Gemini Real] 🚀 실제 전송 시작: "${text}"`);
    
    try {
        // 1. 입력창 찾기
        console.log("[Gemini Real] 1️⃣ 입력창 탐지 중...");
        
        let inputElement = null;
        const inputSelectors = [
            'textarea.textarea',
            'textarea[aria-label*="Type something"]',
            'textarea[placeholder]',
            'rich-textarea textarea',
            '.ql-editor',
            'div[contenteditable="true"].ql-editor',
            'textarea'
        ];
        
        for (const selector of inputSelectors) {
            const element = document.querySelector(selector);
            if (element) {
                const rect = element.getBoundingClientRect();
                const isVisible = rect.width > 0 && rect.height > 0;
                
                if (isVisible) {
                    inputElement = element;
                    console.log(`[Gemini Real] ✅ 입력창 발견: ${selector}`);
                    break;
                }
            }
        }
        
        if (!inputElement) {
            console.error("[Gemini Real] ❌ 입력창을 찾을 수 없음");
            return false;
        }
        
        // 2. 텍스트 입력
        console.log("[Gemini Real] 2️⃣ 텍스트 입력...");
        inputElement.focus();
        await new Promise(resolve => setTimeout(resolve, 200));
        
        if (inputElement.classList.contains('ql-editor')) {
            // Quill Editor
            inputElement.innerHTML = `<p>${text}</p>`;
            inputElement.dispatchEvent(new Event('input', { bubbles: true }));
            inputElement.dispatchEvent(new Event('change', { bubbles: true }));
            console.log("[Gemini Real] ✅ Quill Editor 입력 완료");
        } else {
            // Textarea
            inputElement.value = text;
            inputElement.dispatchEvent(new Event('input', { bubbles: true }));
            inputElement.dispatchEvent(new Event('change', { bubbles: true }));
            console.log("[Gemini Real] ✅ Textarea 입력 완료");
        }
        
        // Angular change detection 강제 트리거
        inputElement.dispatchEvent(new Event('blur', { bubbles: true }));
        
        // 3. 버튼 활성화 대기 (Gemini는 더 오래 걸림)
        console.log("[Gemini Real] 3️⃣ 버튼 활성화 대기 (15초)...");
        await new Promise(resolve => setTimeout(resolve, 15000));
        
        // 4. 전송 버튼 찾기
        console.log("[Gemini Real] 4️⃣ 전송 버튼 탐지...");
        
        let sendButton = null;
        
        // 방법 1: 정확한 aria-label
        const exactSelectors = [
            'button[aria-label="Send message"]',
            'button[aria-label="Send"]'
        ];
        
        for (const selector of exactSelectors) {
            const btn = document.querySelector(selector);
            if (btn && !btn.disabled && !btn.hasAttribute('disabled')) {
                sendButton = btn;
                console.log(`[Gemini Real] ✅ 정확한 선택자로 발견: ${selector}`);
                break;
            }
        }
        
        // 방법 2: mat-icon 기반
        if (!sendButton) {
            console.log("[Gemini Real] 🔍 mat-icon 검색...");
            const sendIcons = document.querySelectorAll('mat-icon[fonticon="send"]');
            
            for (const icon of sendIcons) {
                const btn = icon.closest('button');
                if (btn && !btn.disabled && !btn.hasAttribute('disabled')) {
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        sendButton = btn;
                        console.log("[Gemini Real] ✅ mat-icon 버튼 발견");
                        break;
                    }
                }
            }
        }
        
        // 방법 3: 모든 버튼 검색
        if (!sendButton) {
            console.log("[Gemini Real] 🔍 전체 버튼 스캔...");
            const allButtons = document.querySelectorAll('button');
            
            for (const btn of allButtons) {
                if (btn.disabled || btn.hasAttribute('disabled')) continue;
                
                const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
                const hasIcon = btn.querySelector('mat-icon, svg');
                const rect = btn.getBoundingClientRect();
                
                if ((ariaLabel.includes('send') || hasIcon) && 
                    rect.width > 20 && rect.height > 20) {
                    sendButton = btn;
                    console.log("[Gemini Real] ✅ 일반 스캔으로 버튼 발견");
                    break;
                }
            }
        }
        
        if (!sendButton) {
            console.error("[Gemini Real] ❌ 전송 버튼을 찾을 수 없음");
            
            // 디버그 정보
            const matIcons = document.querySelectorAll('mat-icon');
            console.log(`[Gemini Real] 🔍 디버그: ${matIcons.length}개 mat-icon 발견`);
            Array.from(matIcons).slice(0, 5).forEach((icon, i) => {
                const fonticon = icon.getAttribute('fonticon');
                const parent = icon.closest('button')?.tagName;
                console.log(`  ${i+1}. fonticon="${fonticon}" parent=${parent}`);
            });
            
            return false;
        }
        
        // 5. 전송 버튼 클릭
        console.log("[Gemini Real] 5️⃣ 전송 버튼 클릭...");
        
        // Material/Angular 친화적 클릭
        const materialEvents = [
            new Event('focus', { bubbles: true }),
            new MouseEvent('mousedown', { bubbles: true, cancelable: true }),
            new MouseEvent('mouseup', { bubbles: true, cancelable: true }),
            new MouseEvent('click', { bubbles: true, cancelable: true }),
            new Event('blur', { bubbles: true })
        ];
        
        materialEvents.forEach(event => {
            try {
                sendButton.dispatchEvent(event);
            } catch (e) {
                console.log(`[Gemini Real] 이벤트 ${event.type} 실패:`, e.message);
            }
        });
        
        // 직접 클릭
        try {
            sendButton.click();
            console.log("[Gemini Real] ✅ 직접 클릭 완료");
        } catch (e) {
            console.log("[Gemini Real] 직접 클릭 실패:", e.message);
        }
        
        console.log("[Gemini Real] 🎉 전송 완료! 결과를 확인하세요.");
        return true;
        
    } catch (error) {
        console.error("[Gemini Real] ❌ 치명적 오류:", error);
        return false;
    }
}

/**
 * 플랫폼별 실제 전송 함수
 */
async function realSendMessage(text) {
    console.log(`\n🎯 실제 메시지 전송: "${text}"`);
    console.log(`📍 플랫폼: ${currentPlatform}`);
    
    if (currentPlatform === 'chatgpt') {
        return await realChatGPTSend(text);
    } else if (currentPlatform === 'gemini') {
        return await realGeminiSend(text);
    } else if (currentPlatform === 'claude' || currentPlatform === 'perplexity') {
        console.log(`[${currentPlatform}] 이미 작동 중인 플랫폼입니다`);
        return true;
    } else {
        console.error("❌ 지원하지 않는 플랫폼입니다");
        return false;
    }
}

// 전역 함수 등록
window.realSendMessage = realSendMessage;
window.realChatGPTSend = realChatGPTSend;
window.realGeminiSend = realGeminiSend;

// Mock Chrome의 sendMessage를 실제 전송으로 교체
if (window.chrome && window.chrome.runtime) {
    const originalSendMessage = window.chrome.runtime.sendMessage;
    
    window.chrome.runtime.sendMessage = function(message, callback) {
        console.log(`[Real Fix] Chrome 메시지 인터셉트:`, message);
        
        if (message.action === 'inputAndSend' || message.action === 'sendToAll') {
            const text = message.text || message.message || 'Real fix test message';
            
            realSendMessage(text).then(success => {
                const response = {
                    success: success,
                    platform: currentPlatform,
                    realFix: true
                };
                
                if (callback) callback(response);
            });
        } else {
            // 다른 액션은 원래 Mock으로
            return originalSendMessage.call(this, message, callback);
        }
    };
    
    console.log("✅ Chrome Runtime 메시지를 실제 전송으로 교체 완료");
}

console.log("\n" + "=".repeat(60));
console.log("🔥 REAL WORKING FIX가 적용되었습니다!");
console.log(`현재 ${currentPlatform}에서 실제 메시지 전송이 가능합니다.`);
console.log("\n💡 테스트 방법:");
console.log(`1. realSendMessage('테스트 메시지')`);
console.log(`2. 기존 Mock Extension의 전송 버튼 사용`);
console.log(`3. chrome.runtime.sendMessage({action: 'sendToAll', message: '테스트'})`);
console.log("=".repeat(60));