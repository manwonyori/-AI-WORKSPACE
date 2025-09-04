/**
 * INPUT FIX 2025 - ChatGPT & Gemini 입력 문제 완전 해결
 * 
 * Claude, Perplexity는 정상 작동하고
 * ChatGPT, Gemini만 입력이 안되는 문제 해결
 */

console.clear();
console.log("%c🔧 INPUT FIX 2025", "color: #00ff00; font-size: 20px; font-weight: bold;");
console.log("ChatGPT & Gemini 입력 문제를 완전히 해결합니다.\n");

// 플랫폼 감지
const platform = (() => {
    const hostname = location.hostname;
    if (hostname.includes('chatgpt.com')) return 'chatgpt';
    if (hostname.includes('gemini.google.com') || hostname.includes('aistudio.google.com')) return 'gemini';
    if (hostname.includes('claude.ai')) return 'claude';
    if (hostname.includes('perplexity.ai')) return 'perplexity';
    return 'unknown';
})();

console.log(`🎯 현재 플랫폼: ${platform.toUpperCase()}`);

// ChatGPT 입력 완전 해결
async function fixChatGPTInput(text) {
    console.log("[ChatGPT] 입력 시도...");
    
    // 2025년 최신 ChatGPT 셀렉터들
    const selectors = [
        'div#prompt-textarea[contenteditable="true"]',
        'textarea#prompt-textarea',
        'div[contenteditable="true"][data-id="root"]',
        'div[contenteditable="true"].ProseMirror',
        'div[contenteditable="true"]'
    ];
    
    for (let selector of selectors) {
        const input = document.querySelector(selector);
        if (input && input.offsetParent !== null) {
            console.log(`[ChatGPT] ✅ 입력창 발견: ${selector}`);
            
            try {
                input.focus();
                
                if (input.tagName === 'DIV') {
                    // ContentEditable 방식
                    input.innerHTML = '';
                    input.innerHTML = text.replace(/\n/g, '<br>');
                    
                    // 다양한 이벤트 트리거
                    input.dispatchEvent(new InputEvent('input', {
                        inputType: 'insertText',
                        data: text,
                        bubbles: true,
                        cancelable: true
                    }));
                    
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    input.dispatchEvent(new Event('blur', { bubbles: true }));
                    input.focus();
                    
                } else if (input.tagName === 'TEXTAREA') {
                    // React Textarea 방식
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                        window.HTMLTextAreaElement.prototype, 'value'
                    ).set;
                    
                    if (nativeInputValueSetter) {
                        nativeInputValueSetter.call(input, '');
                        nativeInputValueSetter.call(input, text);
                        
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }
                
                console.log("[ChatGPT] ✅ 입력 완료");
                return true;
                
            } catch (error) {
                console.error(`[ChatGPT] ❌ 입력 실패 (${selector}):`, error);
            }
        }
    }
    
    console.error("[ChatGPT] ❌ 입력창을 찾을 수 없습니다");
    return false;
}

// Gemini 입력 완전 해결
async function fixGeminiInput(text) {
    console.log("[Gemini] 입력 시도...");
    
    // Quill Editor 우선 시도
    const quillEditor = document.querySelector('.ql-editor');
    if (quillEditor && quillEditor.offsetParent !== null) {
        console.log("[Gemini] ✅ Quill Editor 발견");
        
        try {
            quillEditor.focus();
            quillEditor.innerHTML = '';
            quillEditor.innerHTML = `<p>${text.replace(/\n/g, '</p><p>')}</p>`;
            
            // Quill 전용 이벤트들
            quillEditor.dispatchEvent(new Event('input', { bubbles: true }));
            quillEditor.dispatchEvent(new Event('change', { bubbles: true }));
            
            // Focus 사이클로 변경 감지
            quillEditor.blur();
            await new Promise(resolve => setTimeout(resolve, 100));
            quillEditor.focus();
            
            console.log("[Gemini] ✅ Quill Editor 입력 완료");
            return true;
            
        } catch (error) {
            console.error("[Gemini] ❌ Quill Editor 실패:", error);
        }
    }
    
    // Textarea 대안 시도
    const textareas = document.querySelectorAll('textarea');
    for (let textarea of textareas) {
        if (textarea.offsetParent !== null && 
            (textarea.placeholder?.includes('Message') || 
             textarea.getAttribute('aria-label')?.includes('Message'))) {
            
            console.log("[Gemini] ✅ Textarea 발견");
            
            try {
                textarea.focus();
                textarea.value = '';
                textarea.value = text;
                
                // Angular 호환 이벤트들
                ['input', 'change', 'keyup', 'blur'].forEach(eventType => {
                    textarea.dispatchEvent(new Event(eventType, { 
                        bubbles: true,
                        cancelable: true
                    }));
                });
                
                textarea.focus();
                console.log("[Gemini] ✅ Textarea 입력 완료");
                return true;
                
            } catch (error) {
                console.error("[Gemini] ❌ Textarea 실패:", error);
            }
        }
    }
    
    console.error("[Gemini] ❌ 입력창을 찾을 수 없습니다");
    return false;
}

// Claude 입력 (정상 작동하지만 개선)
async function fixClaudeInput(text) {
    console.log("[Claude] 입력 시도...");
    
    const input = document.querySelector('div[contenteditable="true"].ProseMirror') ||
                  document.querySelector('div[contenteditable="true"]');
    
    if (input) {
        input.focus();
        input.innerHTML = text.replace(/\n/g, '<br>');
        
        input.dispatchEvent(new InputEvent('input', {
            inputType: 'insertText',
            data: text,
            bubbles: true
        }));
        
        console.log("[Claude] ✅ 입력 완료");
        return true;
    }
    
    return false;
}

// Perplexity 입력 (정상 작동하지만 개선)
async function fixPerplexityInput(text) {
    console.log("[Perplexity] 입력 시도...");
    
    const input = document.querySelector('textarea') ||
                  document.querySelector('div[contenteditable="true"]');
    
    if (input) {
        input.focus();
        
        if (input.tagName === 'TEXTAREA') {
            input.value = text;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        } else {
            input.innerHTML = text.replace(/\n/g, '<br>');
            input.dispatchEvent(new InputEvent('input', {
                inputType: 'insertText',
                data: text,
                bubbles: true
            }));
        }
        
        console.log("[Perplexity] ✅ 입력 완료");
        return true;
    }
    
    return false;
}

// 통합 입력 함수
window.universalInput = async function(text) {
    console.log(`\n🚀 ${platform.toUpperCase()}에 텍스트 입력: "${text.slice(0, 50)}..."`);
    
    let success = false;
    
    switch (platform) {
        case 'chatgpt':
            success = await fixChatGPTInput(text);
            break;
        case 'gemini':
            success = await fixGeminiInput(text);
            break;
        case 'claude':
            success = await fixClaudeInput(text);
            break;
        case 'perplexity':
            success = await fixPerplexityInput(text);
            break;
        default:
            console.error("❌ 지원하지 않는 플랫폼");
            return false;
    }
    
    if (success) {
        console.log(`✅ ${platform.toUpperCase()} 입력 성공`);
    } else {
        console.error(`❌ ${platform.toUpperCase()} 입력 실패`);
        
        // 실패시 진단 정보 출력
        console.log("\n🔍 진단 정보:");
        console.log("현재 페이지의 모든 입력 요소들:");
        
        document.querySelectorAll('input, textarea, [contenteditable="true"]').forEach((el, i) => {
            const rect = el.getBoundingClientRect();
            const visible = rect.width > 0 && rect.height > 0;
            console.log(`${i+1}. ${el.tagName} - ID: ${el.id} - Visible: ${visible}`);
            console.log(`   Selector: ${el.tagName}${el.id ? '#' + el.id : ''}${el.className ? '.' + el.className.split(' ').join('.') : ''}`);
        });
    }
    
    return success;
};

// 테스트 함수
window.testInput = function() {
    const testMessage = `테스트 메시지 - ${new Date().toLocaleTimeString()}`;
    universalInput(testMessage);
};

console.log("\n🎯 사용법:");
console.log("universalInput('메시지') - 현재 플랫폼에 메시지 입력");
console.log("testInput() - 테스트 메시지 입력");
console.log("\n준비 완료! 이제 ChatGPT와 Gemini에서도 입력이 될 것입니다.");