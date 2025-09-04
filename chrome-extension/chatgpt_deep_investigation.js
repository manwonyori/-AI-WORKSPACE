/**
 * ChatGPT 심층 조사 스크립트
 * chatgpt.com에서 F12 콘솔에 실행
 */

console.clear();
console.log('=== CHATGPT DEEP INVESTIGATION ===');
console.log('URL:', location.href);
console.log('Time:', new Date().toLocaleTimeString());

// 1. 입력창 정확히 찾기
console.log('\n📝 INPUT ELEMENT SEARCH:');

// 모든 가능한 입력 요소 찾기
const inputCandidates = [
    'textarea#prompt-textarea',
    'div#prompt-textarea', 
    'textarea[data-id]',
    'textarea[placeholder]',
    'textarea',
    'div[contenteditable="true"]',
    '[role="textbox"]'
];

let mainInput = null;
for (const selector of inputCandidates) {
    try {
        const el = document.querySelector(selector);
        if (el) {
            console.log(`✅ Found with selector: ${selector}`);
            console.log('  Element:', el);
            console.log('  Tag:', el.tagName);
            console.log('  ID:', el.id);
            console.log('  Class:', el.className);
            
            if (el.tagName === 'TEXTAREA') {
                console.log('  Value:', el.value);
                console.log('  Placeholder:', el.placeholder);
                console.log('  ReadOnly:', el.readOnly);
                console.log('  Disabled:', el.disabled);
            } else if (el.contentEditable) {
                console.log('  ContentEditable:', el.contentEditable);
                console.log('  InnerText:', el.innerText?.substring(0, 50));
            }
            
            // 하이라이트
            el.style.outline = '3px solid lime';
            el.style.outlineOffset = '2px';
            
            if (!mainInput) {
                mainInput = el;
            }
            break;
        }
    } catch(e) {
        // Skip invalid selectors
    }
}

if (!mainInput) {
    console.log('❌ No input element found!');
}

// 2. Send 버튼 찾기 (메시지 입력 후)
console.log('\n🔘 SEND BUTTON SEARCH:');

// aria-label로 버튼 찾기
const buttonsByAria = [
    '[aria-label*="Send"]',
    '[aria-label*="send"]',
    '[aria-label*="메시지"]',
    '[aria-label*="보내기"]',
    'button[data-testid*="send"]'
];

let sendButton = null;
for (const selector of buttonsByAria) {
    try {
        const btn = document.querySelector(selector);
        if (btn && !btn.disabled) {
            console.log(`✅ Found send button: ${selector}`);
            console.log('  Button:', btn);
            console.log('  Text:', btn.textContent);
            console.log('  AriaLabel:', btn.getAttribute('aria-label'));
            console.log('  Disabled:', btn.disabled);
            
            btn.style.outline = '3px solid blue';
            btn.style.outlineOffset = '2px';
            sendButton = btn;
            break;
        }
    } catch(e) {
        // Skip
    }
}

// SVG 아이콘이 있는 버튼 찾기
if (!sendButton) {
    console.log('\n🔍 Searching for buttons with SVG icons...');
    const allButtons = document.querySelectorAll('button');
    
    for (const btn of allButtons) {
        const svg = btn.querySelector('svg');
        if (svg) {
            const path = svg.querySelector('path');
            if (path && path.getAttribute('d') && path.getAttribute('d').includes('M')) {
                // Send 아이콘 패턴 체크
                const rect = btn.getBoundingClientRect();
                if (rect.width < 60 && rect.height < 60) { // 작은 아이콘 버튼
                    console.log('Found icon button:', {
                        width: rect.width,
                        height: rect.height,
                        ariaLabel: btn.getAttribute('aria-label'),
                        className: btn.className,
                        visible: btn.offsetParent !== null
                    });
                }
            }
        }
    }
}

// 3. 입력 테스트
console.log('\n🧪 INPUT MECHANISM TEST:');

if (mainInput) {
    console.log('Testing input methods on:', mainInput.tagName);
    
    // Test function
    function testInput(method, code) {
        console.log(`\nTesting ${method}...`);
        try {
            code();
            console.log(`✅ ${method} executed`);
            
            // Check if value changed
            setTimeout(() => {
                if (mainInput.tagName === 'TEXTAREA') {
                    console.log(`  Result: "${mainInput.value}"`);
                } else {
                    console.log(`  Result: "${mainInput.innerText}"`);
                }
            }, 100);
        } catch(e) {
            console.log(`❌ ${method} failed:`, e.message);
        }
    }
    
    // Clear first
    if (mainInput.tagName === 'TEXTAREA') {
        mainInput.value = '';
    } else {
        mainInput.innerText = '';
    }
    
    // Test 1: Direct value (for textarea)
    if (mainInput.tagName === 'TEXTAREA') {
        setTimeout(() => {
            testInput('Direct Value', () => {
                mainInput.value = 'Test 1: Direct';
            });
        }, 1000);
        
        // Test 2: React-style setter
        setTimeout(() => {
            testInput('React Setter', () => {
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLTextAreaElement.prototype, 'value'
                ).set;
                nativeInputValueSetter.call(mainInput, 'Test 2: React');
                const event = new Event('input', { bubbles: true });
                mainInput.dispatchEvent(event);
            });
        }, 3000);
        
        // Test 3: Input event with data
        setTimeout(() => {
            testInput('Input Event', () => {
                mainInput.focus();
                mainInput.value = 'Test 3: Event';
                const event = new InputEvent('input', {
                    bubbles: true,
                    cancelable: true,
                    data: 'Test 3: Event'
                });
                mainInput.dispatchEvent(event);
            });
        }, 5000);
        
        // Test 4: Simulate typing
        setTimeout(() => {
            testInput('Simulate Typing', () => {
                mainInput.focus();
                mainInput.value = '';
                const text = 'Test 4: Typing';
                
                // Type each character
                for (let i = 0; i < text.length; i++) {
                    mainInput.value += text[i];
                    mainInput.dispatchEvent(new InputEvent('input', {
                        data: text[i],
                        inputType: 'insertText',
                        bubbles: true
                    }));
                }
            });
        }, 7000);
    }
}

// 4. Event Listeners 확인
console.log('\n👂 EVENT LISTENERS:');
if (mainInput) {
    // Get event listeners (Chrome DevTools API)
    if (typeof getEventListeners !== 'undefined') {
        const listeners = getEventListeners(mainInput);
        console.log('Event listeners on input:', Object.keys(listeners));
    } else {
        console.log('(Run in Chrome DevTools to see event listeners)');
    }
}

// 5. React Props 확인
console.log('\n⚛️ REACT INVESTIGATION:');
function findReactProps(element) {
    const keys = Object.keys(element);
    const reactKeys = keys.filter(key => 
        key.startsWith('__react') || 
        key.startsWith('_react')
    );
    
    if (reactKeys.length > 0) {
        console.log('Found React keys:', reactKeys);
        reactKeys.forEach(key => {
            console.log(`  ${key}:`, element[key]);
        });
    } else {
        console.log('No React keys found on element');
    }
}

if (mainInput) {
    findReactProps(mainInput);
}

// 6. 입력창 주변 구조 분석
console.log('\n🏗️ DOM STRUCTURE:');
if (mainInput) {
    console.log('Input element parents:');
    let parent = mainInput.parentElement;
    let level = 1;
    while (parent && level <= 5) {
        console.log(`  Level ${level}: ${parent.tagName}.${parent.className.split(' ')[0]}`);
        parent = parent.parentElement;
        level++;
    }
}

console.log('\n=== END OF INVESTIGATION ===');
console.log('💡 TIP: 메시지를 입력하면 Send 버튼이 나타날 수 있습니다.');
console.log('💡 TIP: 어떤 Test 방법이 작동했는지 확인하세요.');