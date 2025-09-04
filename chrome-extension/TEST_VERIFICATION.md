# 🧪 Extension Input Test Verification Guide

## Quick Test Commands

각 플랫폼에서 F12 콘솔에 실행하여 Extension이 제대로 작동하는지 확인:

### 1. ChatGPT (chatgpt.com)
```javascript
// Test if React setter works
(function testChatGPT() {
    const textarea = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');
    if (!textarea) {
        console.error('❌ No textarea found');
        return;
    }
    
    // Test React setter
    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
    if (setter) {
        textarea.focus();
        setter.call(textarea, 'Testing ChatGPT input from extension');
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        textarea.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Check if send button appears
        setTimeout(() => {
            const sendBtn = document.querySelector('button[data-testid="send-button"]') || 
                           document.querySelector('button[aria-label*="Send"]');
            if (sendBtn && !sendBtn.disabled) {
                console.log('✅ ChatGPT input successful! Send button is active');
                sendBtn.style.border = '3px solid lime';
            } else {
                console.log('⚠️ Input set but send button not active');
            }
        }, 500);
    } else {
        console.error('❌ React setter not available');
    }
})();
```

### 2. Gemini/AI Studio (aistudio.google.com/prompts/new_chat)
```javascript
// Test Quill editor method
(function testGemini() {
    // Try Quill editor first
    let editor = document.querySelector('.ql-editor');
    
    if (editor) {
        console.log('Found Quill editor');
        editor.focus();
        editor.innerHTML = '<p>Testing Gemini Quill editor input</p>';
        editor.dispatchEvent(new Event('input', { bubbles: true }));
        editor.dispatchEvent(new Event('blur', { bubbles: true }));
        setTimeout(() => {
            editor.dispatchEvent(new Event('focus', { bubbles: true }));
            console.log('✅ Quill editor input set');
        }, 100);
        return;
    }
    
    // Try textarea fallback
    const textarea = document.querySelector('textarea');
    if (textarea) {
        console.log('Found textarea');
        textarea.focus();
        textarea.value = 'Testing Gemini textarea input';
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        console.log('✅ Textarea input set');
        return;
    }
    
    console.error('❌ No input element found');
})();
```

### 3. Claude (claude.ai)
```javascript
// Test contenteditable
(function testClaude() {
    const editor = document.querySelector('div[contenteditable="true"].ProseMirror') || 
                   document.querySelector('div[contenteditable="true"]');
    
    if (editor) {
        editor.focus();
        editor.textContent = 'Testing Claude input';
        editor.dispatchEvent(new InputEvent('input', { 
            bubbles: true, 
            inputType: 'insertText', 
            data: 'Testing Claude input' 
        }));
        console.log('✅ Claude input set successfully');
    } else {
        console.error('❌ No contenteditable found');
    }
})();
```

### 4. Perplexity (perplexity.ai)
```javascript
// Test textarea
(function testPerplexity() {
    const textarea = document.querySelector('textarea[placeholder*="Ask"]') || 
                    document.querySelector('textarea');
    
    if (textarea) {
        textarea.focus();
        textarea.value = 'Testing Perplexity input';
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        console.log('✅ Perplexity input set successfully');
    } else {
        console.error('❌ No textarea found');
    }
})();
```

## Extension 통합 테스트

Extension이 설치된 상태에서 각 플랫폼 테스트:

```javascript
// Extension이 메시지를 받는지 테스트
chrome.runtime.sendMessage(
    {action: 'inputAndSend', text: 'Hello from extension test'},
    response => {
        console.log('Extension response:', response);
        if (response.success) {
            console.log('✅ Extension input successful on', response.platform);
        } else {
            console.log('❌ Extension input failed');
        }
    }
);
```

## 체크리스트

각 플랫폼에서 확인:

### ChatGPT
- [ ] 초록색 "CHATGPT LOADED" 배지 표시
- [ ] 팝업에서 초록색 점 표시
- [ ] 입력 명령 작동
- [ ] Send 버튼 활성화

### Gemini/AI Studio  
- [ ] 초록색 "GEMINI LOADED" 배지 표시
- [ ] 팝업에서 초록색 점 표시
- [ ] 입력 명령 작동
- [ ] Send/Run 버튼 클릭 가능

### Claude
- [ ] 초록색 "CLAUDE LOADED" 배지 표시
- [ ] 팝업에서 초록색 점 표시
- [ ] 입력 명령 작동
- [ ] Send 버튼 클릭 가능

### Perplexity
- [ ] 초록색 "PERPLEXITY LOADED" 배지 표시
- [ ] 팝업에서 초록색 점 표시
- [ ] 입력 명령 작동
- [ ] Submit 버튼 클릭 가능

## 문제 해결

### "빨간색 점이 표시됨"
1. 해당 사이트 새로고침
2. Extension 재로드 (chrome://extensions/)
3. 로그인 확인 (8899you@gmail.com)

### "입력이 안됨"
1. F12 콘솔에서 위 테스트 코드 실행
2. 어떤 방법이 작동하는지 확인
3. content_enhanced.js 적용

### "LOADED 배지가 안보임"
1. 페이지 완전 로드 대기
2. F12 콘솔 확인
3. Extension 권한 확인

## 성공 기준

모든 플랫폼에서:
1. 초록색 LOADED 배지 표시 ✅
2. 팝업에서 초록색 점 ✅
3. 텍스트 입력 성공 ✅
4. Send 버튼 클릭 가능 ✅