# 🔗 AI 플랫폼 정확한 URL 가이드

## 각 플랫폼 접속 URL

### 1. ChatGPT
- **메인**: https://chatgpt.com
- **새 채팅**: https://chatgpt.com/g/g-2fkFE8rbu-dall-e (DALL-E 포함)
- **로그인**: 8899you@gmail.com

### 2. Claude
- **메인**: https://claude.ai
- **새 채팅**: https://claude.ai/new
- **로그인**: 8899you@gmail.com

### 3. Perplexity
- **메인**: https://www.perplexity.ai
- **검색**: https://www.perplexity.ai/search/new
- **로그인**: 8899you@gmail.com

### 4. Google AI Studio (Gemini)
- **메인**: https://aistudio.google.com
- **새 채팅**: https://aistudio.google.com/prompts/new_chat ⭐
- **Gemini**: https://gemini.google.com
- **로그인**: 8899you@gmail.com

## 셀렉터 확인 스크립트

### 각 플랫폼에서 F12 콘솔 실행:

```javascript
// 현재 플랫폼 자동 감지 및 테스트
const platform = location.hostname.includes('chatgpt') ? 'chatgpt' :
                location.hostname.includes('claude') ? 'claude' :
                location.hostname.includes('perplexity') ? 'perplexity' :
                location.hostname.includes('google') || location.hostname.includes('gemini') ? 'gemini' :
                'unknown';

console.log('Platform:', platform);
console.log('URL:', location.href);

// 입력창 찾기
let input = null;
if (platform === 'chatgpt') {
    input = document.querySelector('textarea#prompt-textarea') || 
            document.querySelector('div#prompt-textarea') ||
            document.querySelector('textarea');
} else if (platform === 'claude') {
    input = document.querySelector('div[contenteditable="true"].ProseMirror') ||
            document.querySelector('div[contenteditable="true"]');
} else if (platform === 'perplexity') {
    input = document.querySelector('textarea[placeholder*="Ask"]') ||
            document.querySelector('textarea');
} else if (platform === 'gemini') {
    input = document.querySelector('div.ql-editor') ||
            document.querySelector('div[contenteditable="true"]') ||
            document.querySelector('textarea');
}

if (input) {
    console.log('✅ Input found:', input);
    input.style.border = '5px solid lime';
} else {
    console.log('❌ Input not found');
}
```

## Extension 테스트 순서

1. **모든 플랫폼 로그인**
   - 8899you@gmail.com 계정 사용

2. **올바른 URL로 접속**
   - Google AI Studio: https://aistudio.google.com/prompts/new_chat
   - 각 플랫폼의 채팅 화면으로 이동

3. **Extension 새로고침**
   - chrome://extensions/
   - AI Workspace Controller → 🔄

4. **상태 확인**
   - Extension 팝업 열기
   - 모든 플랫폼 🟢 확인

## 문제 해결

### Google AI Studio가 인식 안 될 때:
1. URL이 `https://aistudio.google.com/prompts/new_chat` 인지 확인
2. 페이지 완전히 로드 후 테스트
3. F5 새로고침 후 재시도

### 입력이 안 될 때:
1. 로그인 상태 확인
2. 채팅 화면인지 확인
3. F12 콘솔에서 위 스크립트 실행하여 셀렉터 확인