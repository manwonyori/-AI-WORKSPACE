/**
 * Gemini/AI Studio Ctrl+Enter 테스트
 * https://aistudio.google.com/prompts/new_chat 에서 실행
 */

console.clear();
console.log('=== GEMINI CTRL+ENTER TEST ===');

// 1. 입력창 찾기
function findInput() {
    const selectors = [
        '.ql-editor',
        'div.ql-editor',
        'div[contenteditable="true"].ql-editor',
        'textarea[aria-label*="Enter a prompt"]',
        'textarea[placeholder*="Enter a prompt"]',
        'textarea.prompt-textarea',
        'textarea',
        'div[contenteditable="true"]'
    ];
    
    for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el) {
            console.log(`✅ Found input with: ${sel}`);
            console.log('  Element:', el);
            console.log('  Tag:', el.tagName);
            console.log('  Class:', el.className);
            return el;
        }
    }
    
    console.log('❌ No input element found');
    return null;
}

// 2. 텍스트 입력 테스트
function setInputText(input, text) {
    console.log('\n📝 Setting text...');
    
    if (!input) {
        console.log('❌ No input element');
        return false;
    }
    
    try {
        input.focus();
        
        if (input.classList && input.classList.contains('ql-editor')) {
            // Quill Editor
            console.log('Using Quill editor method');
            input.innerHTML = `<p>${text}</p>`;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            
            // Quill specific events
            input.dispatchEvent(new Event('blur', { bubbles: true }));
            setTimeout(() => {
                input.dispatchEvent(new Event('focus', { bubbles: true }));
            }, 100);
            
        } else if (input.tagName === 'TEXTAREA') {
            // Regular textarea
            console.log('Using textarea method');
            input.value = text;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            
        } else if (input.contentEditable === 'true') {
            // ContentEditable div
            console.log('Using contenteditable method');
            input.textContent = text;
            input.dispatchEvent(new InputEvent('input', {
                data: text,
                inputType: 'insertText',
                bubbles: true
            }));
        }
        
        console.log('✅ Text set successfully');
        return true;
    } catch (e) {
        console.error('❌ Error setting text:', e);
        return false;
    }
}

// 3. Ctrl+Enter 전송 테스트
function sendWithCtrlEnter(input) {
    console.log('\n⌨️ Sending with Ctrl+Enter...');
    
    if (!input) {
        console.log('❌ No input element');
        return false;
    }
    
    try {
        input.focus();
        
        // Method 1: KeyboardEvent with ctrlKey
        console.log('Method 1: KeyboardEvent with ctrlKey');
        const ctrlEnterEvent = new KeyboardEvent('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13,
            ctrlKey: true,
            bubbles: true,
            cancelable: true,
            composed: true
        });
        
        const result = input.dispatchEvent(ctrlEnterEvent);
        console.log('  Event dispatched:', result);
        
        // Method 2: Also try keyup
        setTimeout(() => {
            console.log('Method 2: KeyboardEvent keyup');
            const keyupEvent = new KeyboardEvent('keyup', {
                key: 'Enter',
                code: 'Enter',
                keyCode: 13,
                which: 13,
                ctrlKey: true,
                bubbles: true,
                cancelable: true
            });
            input.dispatchEvent(keyupEvent);
        }, 100);
        
        // Method 3: Try keypress (deprecated but sometimes works)
        setTimeout(() => {
            console.log('Method 3: KeyboardEvent keypress');
            const keypressEvent = new KeyboardEvent('keypress', {
                key: 'Enter',
                code: 'Enter',
                keyCode: 13,
                which: 13,
                ctrlKey: true,
                bubbles: true,
                cancelable: true
            });
            input.dispatchEvent(keypressEvent);
        }, 200);
        
        console.log('✅ Ctrl+Enter events sent');
        return true;
    } catch (e) {
        console.error('❌ Error sending Ctrl+Enter:', e);
        return false;
    }
}

// 4. 버튼 찾기 (폴백)
function findSendButton() {
    console.log('\n🔘 Looking for send button as fallback...');
    
    const selectors = [
        'button[aria-label*="Send"]',
        'button[aria-label*="Run"]',
        'button[title*="Send"]',
        'button[title*="Run"]',
        'button[mattooltip*="Send"]',
        'button[mattooltip*="Run"]',
        'mat-icon-button[aria-label*="Send"]',
        'button.send-button',
        'button[type="submit"]'
    ];
    
    for (const sel of selectors) {
        const btn = document.querySelector(sel);
        if (btn && !btn.disabled) {
            console.log(`✅ Found button with: ${sel}`);
            console.log('  Button:', btn);
            console.log('  AriaLabel:', btn.getAttribute('aria-label'));
            console.log('  Title:', btn.getAttribute('title'));
            return btn;
        }
    }
    
    console.log('❌ No send button found');
    return null;
}

// 5. 실행
console.log('\n🚀 Running test...\n');

const input = findInput();
if (input) {
    // 하이라이트
    input.style.border = '3px solid lime';
    
    // 텍스트 설정
    const testText = 'Test message from Chrome Extension v1.3.2';
    const textSet = setInputText(input, testText);
    
    if (textSet) {
        // Ctrl+Enter 시도
        setTimeout(() => {
            const sent = sendWithCtrlEnter(input);
            
            if (!sent) {
                // 버튼 폴백
                console.log('\n⚠️ Ctrl+Enter might not have worked, trying button fallback...');
                const button = findSendButton();
                if (button) {
                    button.style.border = '3px solid blue';
                    console.log('💡 Click the highlighted button to send');
                    // button.click(); // 실제로 클릭하려면 주석 해제
                }
            }
        }, 1000);
    }
} else {
    console.log('\n❌ Cannot proceed without input element');
    console.log('Make sure you are on: https://aistudio.google.com/prompts/new_chat');
}

console.log('\n=== END TEST ===');
console.log('💡 If message didn\'t send, Ctrl+Enter may need different approach');