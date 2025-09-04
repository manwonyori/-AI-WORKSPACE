# 🔧 Perplexity 문제 해결 가이드 v1.2.3

## 📌 중요: 계정 로그인
- **모든 플랫폼에서 `8899you@gmail.com`으로 로그인해야 연동됩니다**

## 1️⃣ Extension 업데이트 확인
1. Chrome에서 `chrome://extensions/` 열기
2. AI Workspace Controller v1.2.3 확인
3. 🔄 새로고침 버튼 클릭

## 2️⃣ Perplexity 테스트

### A. 로그인 확인
1. https://www.perplexity.ai 접속
2. 8899you@gmail.com으로 로그인
3. 홈 화면 또는 채팅 화면으로 이동

### B. 디버그 스크립트 실행
1. F12 (개발자 도구) 열기
2. Console 탭에서 아래 스크립트 실행:

```javascript
// Perplexity 입력창 찾기
const textarea = document.querySelector('textarea:not([aria-label*="mic"])');
if (textarea) {
    console.log('✅ Textarea found!');
    textarea.style.border = '5px solid lime';
    
    // 테스트 입력
    textarea.click();
    textarea.focus();
    textarea.value = 'Test message from debug';
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    
    console.log('Properties:', {
        class: textarea.className,
        placeholder: textarea.placeholder,
        value: textarea.value
    });
} else {
    console.log('❌ No textarea found');
    
    // 모든 textarea 표시
    document.querySelectorAll('textarea').forEach((ta, i) => {
        console.log(`Textarea[${i}]:`, ta);
        ta.style.border = '3px solid red';
    });
}

// 버튼 찾기
const button = document.querySelector('button[type="submit"]:not([aria-label*="mic"])');
if (button) {
    console.log('✅ Submit button found!');
    button.style.border = '5px solid blue';
} else {
    console.log('❌ No submit button found');
}
```

### C. Extension 테스트
1. Extension 아이콘 클릭
2. Perplexity 항목이 🟢 인지 확인
3. 메시지 입력: "Test from extension"
4. "Send to All" 클릭

## 3️⃣ 마이크 모드 문제 해결

### 증상
- 텍스트 입력 시 마이크 모드로 전환
- 음성 인식 팝업이 나타남

### 해결 방법
v1.2.3에서 자동으로 처리되지만, 수동으로 해결하려면:

```javascript
// 마이크 버튼 비활성화
const micButton = document.querySelector('[aria-label*="mic"], [aria-label*="voice"]');
if (micButton) {
    micButton.style.display = 'none';
    console.log('Mic button hidden');
}

// 텍스트 입력 모드 강제
const input = document.querySelector('textarea');
if (input) {
    input.click();
    input.focus();
    console.log('Text mode activated');
}
```

## 4️⃣ 입력이 안 되는 경우

### Extension 팝업에서:
1. 🐛 Debug Console 클릭
2. Chrome 개발자 도구에서 오류 확인

### Perplexity 페이지에서:
```javascript
// 수동 입력 테스트
const ta = document.querySelector('textarea');
if (ta) {
    // 방법 1: 직접 값 설정
    ta.value = 'Test 1';
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    
    setTimeout(() => {
        // 방법 2: Native setter 사용
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLTextAreaElement.prototype, 'value'
        ).set;
        setter.call(ta, 'Test 2');
        ta.dispatchEvent(new Event('input', { bubbles: true }));
    }, 1000);
    
    setTimeout(() => {
        // 방법 3: 시뮬레이션 타이핑
        ta.focus();
        document.execCommand('insertText', false, 'Test 3');
    }, 2000);
    
    console.log('All methods tested - check which one worked');
}
```

## 5️⃣ 완전한 디버그 정보 수집

`perplexity_debug.js` 파일 내용을 Console에 복사/붙여넣기:
```bash
C:\Users\8899y\AI-WORKSPACE\chrome-extension\perplexity_debug.js
```

결과를 복사하여 공유

## ✅ 체크리스트

- [ ] 8899you@gmail.com으로 로그인
- [ ] Extension v1.2.3 설치
- [ ] LOADED 배지 표시
- [ ] Perplexity 🟢 상태
- [ ] 텍스트 입력 가능
- [ ] 마이크 모드 비활성
- [ ] 메시지 전송 가능

## 🆘 여전히 문제가 있다면

1. **Chrome 재시작**
2. **Extension 재설치**:
   - Extensions 페이지에서 제거
   - 폴더 다시 로드
3. **시크릿 모드에서 테스트**
4. **다른 브라우저에서 테스트**