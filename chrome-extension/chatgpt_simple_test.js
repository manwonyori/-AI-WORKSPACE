/**
 * ChatGPT 간단 입력 테스트
 * chatgpt.com에서 F12 콘솔에 실행
 */

// 1. 입력창 찾기
const textarea = document.querySelector('textarea#prompt-textarea');
if (!textarea) {
    console.error('❌ Textarea not found! Looking for any textarea...');
    const anyTextarea = document.querySelector('textarea');
    if (anyTextarea) {
        console.log('Found textarea:', anyTextarea);
    }
} else {
    console.log('✅ Textarea found:', textarea);
    textarea.style.border = '3px solid lime';
}

// 2. 텍스트 입력 시도 (여러 방법)
console.log('\n🔬 Testing input methods...\n');

// Method A: Simple value set
function methodA() {
    console.log('Method A: Simple value set');
    const ta = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
    if (ta) {
        ta.focus();
        ta.value = 'Hello from Method A';
        console.log('  ✓ Value set to:', ta.value);
        
        // Check for send button
        setTimeout(() => {
            const sendBtn = document.querySelector('button[data-testid="send-button"]') || 
                           document.querySelector('button[aria-label*="Send"]') ||
                           document.querySelector('button[aria-label*="send"]');
            if (sendBtn) {
                console.log('  ✓ Send button appeared:', sendBtn);
                sendBtn.style.border = '3px solid blue';
            } else {
                console.log('  ✗ Send button not found');
            }
        }, 500);
    }
}

// Method B: With input event
function methodB() {
    console.log('Method B: Value + Input event');
    const ta = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
    if (ta) {
        ta.focus();
        ta.value = 'Hello from Method B';
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        console.log('  ✓ Value set and event dispatched');
        
        // Check for send button
        setTimeout(() => {
            const sendBtn = document.querySelector('button[data-testid="send-button"]') || 
                           document.querySelector('button[aria-label*="Send"]') ||
                           document.querySelector('button[disabled="false"]');
            if (sendBtn) {
                console.log('  ✓ Send button appeared:', sendBtn);
                sendBtn.style.border = '3px solid blue';
            }
        }, 500);
    }
}

// Method C: React-style
function methodC() {
    console.log('Method C: React-style setter');
    const ta = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
    if (ta) {
        ta.focus();
        
        // Use native setter
        const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLTextAreaElement.prototype, 
            'value'
        ).set;
        
        nativeTextAreaValueSetter.call(ta, 'Hello from Method C');
        
        // Dispatch events
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        
        console.log('  ✓ React-style value set');
        
        // Check for send button
        setTimeout(() => {
            checkSendButton();
        }, 500);
    }
}

// Method D: Simulate real typing
function methodD() {
    console.log('Method D: Simulate real typing');
    const ta = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
    if (ta) {
        ta.focus();
        ta.value = '';
        
        const text = 'Hello from Method D';
        let index = 0;
        
        const typeChar = () => {
            if (index < text.length) {
                ta.value += text[index];
                ta.dispatchEvent(new InputEvent('input', {
                    data: text[index],
                    inputType: 'insertText',
                    bubbles: true
                }));
                index++;
                setTimeout(typeChar, 50);
            } else {
                console.log('  ✓ Typing complete');
                setTimeout(checkSendButton, 500);
            }
        };
        
        typeChar();
    }
}

// Helper function to check for send button
function checkSendButton() {
    // Look for any button that might be send
    const possibleSelectors = [
        'button[data-testid="send-button"]',
        'button[aria-label*="Send"]',
        'button[aria-label*="send"]',
        'button:not([disabled])[aria-label*="메시지"]',
        'button.btn-primary',
        'button[type="submit"]:not([disabled])'
    ];
    
    let foundButton = false;
    for (const selector of possibleSelectors) {
        try {
            const btn = document.querySelector(selector);
            if (btn && !btn.disabled && btn.offsetParent !== null) {
                console.log(`  ✓ Send button found with selector: ${selector}`);
                console.log('    Button:', btn);
                console.log('    AriaLabel:', btn.getAttribute('aria-label'));
                btn.style.border = '3px solid blue';
                btn.style.backgroundColor = 'rgba(0, 123, 255, 0.1)';
                foundButton = true;
                break;
            }
        } catch(e) {
            // Skip invalid selector
        }
    }
    
    if (!foundButton) {
        console.log('  ✗ No send button found');
        
        // List all visible buttons
        console.log('\n  Available buttons:');
        const allButtons = document.querySelectorAll('button:not([disabled])');
        allButtons.forEach((btn, i) => {
            if (btn.offsetParent !== null && i < 10) {
                console.log(`    Button[${i}]:`, {
                    text: btn.textContent.trim().substring(0, 20),
                    ariaLabel: btn.getAttribute('aria-label'),
                    className: btn.className.substring(0, 50)
                });
            }
        });
    }
}

// Execute tests
console.log('Starting tests in 1 second intervals...\n');
setTimeout(methodA, 1000);
setTimeout(methodB, 3000);
setTimeout(methodC, 5000);
setTimeout(methodD, 7000);

console.log('\n💡 Watch which method successfully:');
console.log('  1. Inputs text into the textarea');
console.log('  2. Makes the send button appear');
console.log('\n⏳ Tests will run for the next 10 seconds...');