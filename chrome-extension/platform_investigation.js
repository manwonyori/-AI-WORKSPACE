/**
 * 각 AI 플랫폼의 입력 메커니즘을 조사하는 스크립트
 * 각 플랫폼에서 F12 콘솔에 실행하여 정확한 입력 방법을 파악
 */

// ========== CHATGPT 조사 스크립트 ==========
// chatgpt.com에서 실행
function investigateChatGPT() {
    console.clear();
    console.log('=== CHATGPT INPUT INVESTIGATION ===');
    
    // 1. 모든 textarea 찾기
    const textareas = document.querySelectorAll('textarea');
    console.log(`Found ${textareas.length} textareas:`);
    textareas.forEach((ta, i) => {
        console.log(`Textarea[${i}]:`, {
            id: ta.id,
            className: ta.className,
            placeholder: ta.placeholder,
            value: ta.value,
            readOnly: ta.readOnly,
            disabled: ta.disabled,
            parent: ta.parentElement?.className
        });
    });
    
    // 2. contenteditable 찾기
    const editables = document.querySelectorAll('[contenteditable="true"]');
    console.log(`\nFound ${editables.length} contenteditable elements:`);
    editables.forEach((el, i) => {
        if (i < 3) {
            console.log(`ContentEditable[${i}]:`, {
                tagName: el.tagName,
                id: el.id,
                className: el.className,
                innerText: el.innerText?.substring(0, 50)
            });
        }
    });
    
    // 3. 입력 테스트 함수들
    console.log('\n=== INPUT TEST METHODS ===');
    
    // Method 1: Direct value
    function method1() {
        const ta = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
        if (ta) {
            ta.value = 'Test Method 1: Direct value';
            console.log('Method 1 executed');
            return ta;
        }
        return null;
    }
    
    // Method 2: React-style
    function method2() {
        const ta = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
        if (ta) {
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeInputValueSetter.call(ta, 'Test Method 2: React setter');
            
            const event = new Event('input', { bubbles: true });
            ta.dispatchEvent(event);
            console.log('Method 2 executed');
            return ta;
        }
        return null;
    }
    
    // Method 3: Simulate typing
    function method3() {
        const ta = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
        if (ta) {
            ta.focus();
            ta.value = '';
            const text = 'Test Method 3: Simulated typing';
            
            for (let char of text) {
                ta.value += char;
                ta.dispatchEvent(new InputEvent('input', {
                    data: char,
                    inputType: 'insertText',
                    bubbles: true
                }));
            }
            console.log('Method 3 executed');
            return ta;
        }
        return null;
    }
    
    // Method 4: execCommand
    function method4() {
        const ta = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
        if (ta) {
            ta.focus();
            ta.select();
            document.execCommand('insertText', false, 'Test Method 4: execCommand');
            console.log('Method 4 executed');
            return ta;
        }
        return null;
    }
    
    console.log('\n🧪 Testing each method in 1 second intervals...');
    setTimeout(() => { method1(); }, 1000);
    setTimeout(() => { method2(); }, 3000);
    setTimeout(() => { method3(); }, 5000);
    setTimeout(() => { method4(); }, 7000);
    
    console.log('\n✅ Watch which method successfully inputs text!');
    
    // 4. 버튼 찾기
    setTimeout(() => {
        console.log('\n=== SEND BUTTON INVESTIGATION ===');
        const buttons = document.querySelectorAll('button');
        const sendButtons = Array.from(buttons).filter(btn => {
            const text = btn.textContent.toLowerCase();
            const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
            return text.includes('send') || ariaLabel.includes('send') || btn.type === 'submit';
        });
        
        console.log(`Found ${sendButtons.length} potential send buttons:`);
        sendButtons.forEach((btn, i) => {
            console.log(`Button[${i}]:`, {
                text: btn.textContent.trim(),
                ariaLabel: btn.getAttribute('aria-label'),
                type: btn.type,
                disabled: btn.disabled,
                className: btn.className
            });
            btn.style.border = '3px solid blue';
        });
    }, 9000);
}

// ========== GEMINI/AI STUDIO 조사 스크립트 ==========
// aistudio.google.com 또는 gemini.google.com에서 실행
function investigateGemini() {
    console.clear();
    console.log('=== GEMINI/AI STUDIO INPUT INVESTIGATION ===');
    
    // 1. Quill Editor 찾기
    const quillEditors = document.querySelectorAll('.ql-editor');
    console.log(`Found ${quillEditors.length} Quill editors:`);
    quillEditors.forEach((el, i) => {
        console.log(`QuillEditor[${i}]:`, {
            className: el.className,
            contentEditable: el.contentEditable,
            innerHTML: el.innerHTML?.substring(0, 100),
            parent: el.parentElement?.className
        });
    });
    
    // 2. 모든 textarea 찾기
    const textareas = document.querySelectorAll('textarea');
    console.log(`\nFound ${textareas.length} textareas:`);
    textareas.forEach((ta, i) => {
        console.log(`Textarea[${i}]:`, {
            className: ta.className,
            placeholder: ta.placeholder,
            ariaLabel: ta.getAttribute('aria-label')
        });
    });
    
    // 3. 입력 테스트
    console.log('\n=== GEMINI INPUT TEST METHODS ===');
    
    // Method 1: Quill innerHTML
    function method1() {
        const editor = document.querySelector('.ql-editor');
        if (editor) {
            editor.innerHTML = '<p>Test Method 1: Quill innerHTML</p>';
            editor.dispatchEvent(new Event('input', { bubbles: true }));
            console.log('Method 1 executed');
            return editor;
        }
        return null;
    }
    
    // Method 2: Quill with focus events
    function method2() {
        const editor = document.querySelector('.ql-editor');
        if (editor) {
            editor.focus();
            editor.innerHTML = '<p>Test Method 2: With focus events</p>';
            editor.dispatchEvent(new Event('input', { bubbles: true }));
            editor.dispatchEvent(new Event('blur', { bubbles: true }));
            editor.dispatchEvent(new Event('focus', { bubbles: true }));
            console.log('Method 2 executed');
            return editor;
        }
        return null;
    }
    
    // Method 3: Direct text content
    function method3() {
        const editor = document.querySelector('.ql-editor');
        if (editor) {
            editor.focus();
            editor.textContent = 'Test Method 3: Direct textContent';
            editor.dispatchEvent(new InputEvent('input', {
                data: 'Test Method 3',
                inputType: 'insertText',
                bubbles: true
            }));
            console.log('Method 3 executed');
            return editor;
        }
        return null;
    }
    
    // Method 4: Simulate paste
    function method4() {
        const editor = document.querySelector('.ql-editor');
        if (editor) {
            editor.focus();
            const pasteEvent = new ClipboardEvent('paste', {
                clipboardData: new DataTransfer(),
                bubbles: true
            });
            // Note: Real paste event needs browser permissions
            editor.innerHTML = '<p>Test Method 4: Simulated paste</p>';
            editor.dispatchEvent(pasteEvent);
            console.log('Method 4 executed');
            return editor;
        }
        return null;
    }
    
    console.log('\n🧪 Testing each method in 1 second intervals...');
    setTimeout(() => { method1(); }, 1000);
    setTimeout(() => { method2(); }, 3000);
    setTimeout(() => { method3(); }, 5000);
    setTimeout(() => { method4(); }, 7000);
    
    console.log('\n✅ Watch which method successfully inputs text!');
    
    // 4. Send button 찾기
    setTimeout(() => {
        console.log('\n=== SEND BUTTON INVESTIGATION ===');
        const buttons = document.querySelectorAll('button');
        const sendButtons = Array.from(buttons).filter(btn => {
            const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
            const title = (btn.getAttribute('title') || '').toLowerCase();
            return ariaLabel.includes('send') || 
                   ariaLabel.includes('run') || 
                   title.includes('send') ||
                   btn.innerHTML.includes('send');
        });
        
        console.log(`Found ${sendButtons.length} potential send buttons:`);
        sendButtons.forEach((btn, i) => {
            console.log(`Button[${i}]:`, {
                ariaLabel: btn.getAttribute('aria-label'),
                title: btn.getAttribute('title'),
                className: btn.className
            });
            btn.style.border = '3px solid blue';
        });
    }, 9000);
}

// ========== 자동 실행 ==========
if (location.hostname.includes('chatgpt')) {
    investigateChatGPT();
} else if (location.hostname.includes('gemini') || location.hostname.includes('google')) {
    investigateGemini();
} else {
    console.log('⚠️ Please run this script on ChatGPT or Gemini/AI Studio');
    console.log('For ChatGPT: investigateChatGPT()');
    console.log('For Gemini: investigateGemini()');
}