# 🐛 ChatGPT & Perplexity 빨간 점 문제 해결 가이드

## 1️⃣ Extension 새로고침
1. Chrome에서 `chrome://extensions/` 열기
2. "AI Workspace Controller" 찾기
3. 🔄 새로고침 버튼 클릭

## 2️⃣ 각 사이트에서 디버그 스크립트 실행

### ChatGPT (chatgpt.com)
1. https://chatgpt.com 접속
2. F12 (개발자 도구) 열기
3. Console 탭 선택
4. 아래 스크립트 복사/붙여넣기/실행:

```javascript
// ChatGPT 셀렉터 체크
document.querySelectorAll('textarea').forEach(t => {
    console.log('Textarea found:', {
        id: t.id,
        class: t.className,
        placeholder: t.placeholder
    });
    t.style.border = '3px solid red';
});

document.querySelectorAll('[contenteditable="true"]').forEach(c => {
    console.log('ContentEditable found:', {
        tag: c.tagName,
        id: c.id,
        class: c.className,
        dataId: c.getAttribute('data-id')
    });
    c.style.border = '3px solid blue';
});

// 실제 입력창 찾기
const input = document.querySelector('div[contenteditable="true"][data-id="root"]') ||
              document.querySelector('textarea#prompt-textarea') ||
              document.querySelector('div#prompt-textarea') ||
              document.querySelector('[contenteditable="true"]');
              
if (input) {
    console.log('✅ INPUT FOUND:', input);
    input.style.border = '5px solid lime';
} else {
    console.log('❌ NO INPUT FOUND');
}
```

### Perplexity (perplexity.ai)
1. https://www.perplexity.ai 접속
2. F12 (개발자 도구) 열기
3. Console 탭 선택
4. 아래 스크립트 실행:

```javascript
// Perplexity 셀렉터 체크
document.querySelectorAll('textarea').forEach(t => {
    console.log('Textarea:', {
        class: t.className,
        placeholder: t.placeholder,
        dataTestId: t.getAttribute('data-testid')
    });
    t.style.border = '3px solid red';
});

// SearchBar 찾기
const searchBar = document.querySelector('textarea.SearchBar-input') ||
                  document.querySelector('textarea[data-testid="search-bar-input"]') ||
                  document.querySelector('textarea');
                  
if (searchBar) {
    console.log('✅ SEARCHBAR FOUND:', searchBar);
    searchBar.style.border = '5px solid lime';
} else {
    console.log('❌ NO SEARCHBAR FOUND');
}
```

## 3️⃣ Extension 상태 확인

Extension 아이콘 클릭 후:
1. "Check Status" 버튼 클릭
2. 🐛 Debug Console 버튼 클릭
3. Chrome 개발자 도구 Console에서 메시지 확인

## 4️⃣ 수동 테스트

### Test 메시지 전송:
1. Extension 팝업 열기
2. 메시지 입력: "Test message"
3. "Send to All" 클릭
4. 각 플랫폼에서 메시지가 입력되는지 확인

## 5️⃣ 로그 확인 명령어

Chrome Console(F12)에서:
```javascript
// Extension이 로드되었는지 확인
console.log('Badge visible?', document.querySelector('div[style*="position:fixed"][style*="top:20px"]'));

// 현재 플랫폼 확인
console.log('Current platform:', location.hostname);

// Extension content script 상태
chrome.runtime.sendMessage({action: 'status'}, (response) => {
    console.log('Extension response:', response);
});
```

## 📋 체크리스트

- [ ] Extension 새로고침 완료
- [ ] LOADED 배지 표시 확인
- [ ] ChatGPT 입력창 테두리 표시 (lime)
- [ ] Perplexity 입력창 테두리 표시 (lime)
- [ ] Extension 팝업에서 🟢 표시

## 🔧 만약 여전히 빨간 점이면:

1. **전체 디버그 스크립트 실행**:
```bash
# Chrome Console에 복사/붙여넣기
copy(await fetch('chrome-extension://[EXTENSION_ID]/debug_selector.js').then(r => r.text()))
```

2. **결과를 복사해서 공유**

3. **임시 해결책**:
- 페이지 새로고침 (F5)
- 2-3초 기다린 후 다시 체크
- Chrome 재시작