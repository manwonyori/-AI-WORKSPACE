// 각 플랫폼에서 F12 콘솔에 실행하여 입력 테스트

// ChatGPT 테스트
if (location.hostname.includes('chatgpt')) {
    const textarea = document.querySelector('textarea#prompt-textarea');
    if (textarea) {
        console.log('ChatGPT textarea found:', textarea);
        textarea.focus();
        textarea.value = 'Test message from ChatGPT';
        textarea.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
        console.log('✅ ChatGPT test complete');
    } else {
        console.log('❌ ChatGPT textarea not found');
    }
}

// Gemini 테스트  
if (location.hostname.includes('gemini') || location.hostname.includes('google')) {
    const editor = document.querySelector('div.ql-editor');
    if (editor) {
        console.log('Gemini editor found:', editor);
        editor.focus();
        editor.innerHTML = 'Test message from Gemini';
        editor.dispatchEvent(new Event('input', { bubbles: true }));
        editor.dispatchEvent(new Event('blur', { bubbles: true }));
        editor.dispatchEvent(new Event('focus', { bubbles: true }));
        console.log('✅ Gemini test complete');
    } else {
        console.log('❌ Gemini editor not found');
    }
}

// Claude 테스트
if (location.hostname.includes('claude')) {
    const editor = document.querySelector('div[contenteditable="true"].ProseMirror');
    if (editor) {
        console.log('Claude editor found:', editor);
        editor.focus();
        editor.innerText = 'Test message from Claude';
        editor.dispatchEvent(new InputEvent('input', { bubbles: true }));
        console.log('✅ Claude test complete');
    } else {
        console.log('❌ Claude editor not found');
    }
}

// Perplexity 테스트
if (location.hostname.includes('perplexity')) {
    const textarea = document.querySelector('textarea');
    if (textarea) {
        console.log('Perplexity textarea found:', textarea);
        textarea.focus();
        textarea.value = 'Test message from Perplexity';
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        console.log('✅ Perplexity test complete');
    } else {
        console.log('❌ Perplexity textarea not found');
    }
}