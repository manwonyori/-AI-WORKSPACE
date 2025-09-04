# 🎯 AI Platform Selectors Guide (2025)

## 📋 **전체 셀렉터 현황 (v1.1.5)**

### 1️⃣ **ChatGPT**
```javascript
input: 
  div[contenteditable="true"][data-id="root"]           // React root element
  div[contenteditable="true"][data-placeholder*="Message"]  // Placeholder attribute
  div[contenteditable="true"][aria-label*="Message"]    // Accessibility label
  div.m-0.w-full.resize-none[contenteditable="true"]    // TailwindCSS classes

button:
  button[data-testid="send-button"]                     // Test ID
  button[aria-label*="Send"]                            // ARIA label
  button[type="submit"]                                 // Form submit button
```

### 2️⃣ **Claude**  
```javascript
input:
  div[contenteditable="true"].ProseMirror               // ProseMirror editor
  div[contenteditable="true"][data-placeholder]         // Placeholder div
  div[contenteditable="true"][aria-label*="Message"]    // ARIA label
  div.DraftEditor-editorContainer div[contenteditable="true"]  // Draft.js
  div[role="textbox"][contenteditable="true"]          // ARIA role

button:
  button[aria-label="Send Message"]                     // Exact match
  button[aria-label*="Send"]                            // Partial match
  button[data-testid="send-button"]                     // Test ID
```

### 3️⃣ **Gemini / AI Studio**
```javascript
input:
  rich-textarea textarea                                // Custom element
  textarea[aria-label*="Enter a prompt"]                // ARIA label
  textarea[aria-label*="prompt"]                        // Shorter match
  div[contenteditable="true"][role="textbox"]          // Editable div
  textarea.textarea                                     // Class selector
  div[data-placeholder]                                 // Placeholder div

button:
  button[aria-label*="Send"]                            // ARIA label
  button[data-test-id="send-button"]                    // Test ID
  mat-icon-button[aria-label*="Send"]                   // Material Angular
  button[mattooltip*="Send"]                            // Material tooltip
```

### 4️⃣ **Perplexity**
```javascript
input:
  .PromptTextarea textarea                              // Class-based
  #chat-input                                           // ID selector
  textarea[data-testid="chat-input"]                    // Test ID
  textarea[aria-label*="Message"]                       // ARIA label
  div.ComposerInput[contenteditable="true"]            // Composer class
  textarea[placeholder*="Ask anything"]                 // Placeholder text

button:
  button[aria-label*="Submit"]                          // Submit label
  button[aria-label*="Send"]                            // Send label  
  button[data-testid="send-button"]                     // Test ID
  button.bg-super                                       // Tailwind class
```

## 🔍 **셀렉터 우선순위 전략**

### **우선순위 1: 고유 식별자**
- `id` 속성 (예: `#chat-input`)
- `data-id` 속성 (예: `[data-id="root"]`)
- `data-testid` 속성 (예: `[data-testid="chat-input"]`)

### **우선순위 2: 의미론적 속성**
- `aria-label` (예: `[aria-label*="Message"]`)
- `role` 속성 (예: `[role="textbox"]`)
- `placeholder` 속성

### **우선순위 3: 프레임워크 특화**
- ProseMirror: `.ProseMirror`
- Draft.js: `.DraftEditor-editorContainer`
- Material Angular: `mat-icon-button`
- Rich Text: `rich-textarea`

### **우선순위 4: 클래스 기반**
- 컴포넌트 클래스: `.PromptTextarea`, `.ComposerInput`
- 유틸리티 클래스: `.resize-none`, `.bg-super`

## 📊 **플랫폼별 특징**

| 플랫폼 | 프레임워크 | 입력 타입 | 특이사항 |
|--------|-----------|-----------|---------|
| ChatGPT | React | contenteditable div | TailwindCSS, data-id 사용 |
| Claude | ProseMirror/Draft.js | contenteditable div | 다양한 에디터 라이브러리 |
| Gemini | Angular/Material | textarea + rich-textarea | Material 컴포넌트 |
| Perplexity | React | textarea 또는 contenteditable | 클래스 기반 셀렉터 |

## 🛠️ **디버깅 팁**

### **셀렉터가 작동하지 않을 때**

1. **DevTools Console에서 테스트**
```javascript
// 입력 요소 찾기
document.querySelector('div[contenteditable="true"]')
document.querySelectorAll('textarea')

// 버튼 찾기  
document.querySelector('button[type="submit"]')
```

2. **동적 로딩 대응**
```javascript
// MutationObserver로 DOM 변경 감지
const observer = new MutationObserver((mutations) => {
  const input = document.querySelector(SELECTORS[platform].input);
  if (input) {
    console.log('Input element found:', input);
    observer.disconnect();
  }
});
observer.observe(document.body, { childList: true, subtree: true });
```

3. **Fallback 체인 구현**
```javascript
function findInput(selectors) {
  const selectorList = selectors.split(',');
  for (const selector of selectorList) {
    const element = document.querySelector(selector.trim());
    if (element) return element;
  }
  return null;
}
```

## 🔄 **업데이트 감지 방법**

### **UI 변경 모니터링**
1. Chrome DevTools → Elements 탭
2. 입력창에서 우클릭 → Inspect
3. 속성 변경사항 확인
4. 새로운 셀렉터 추가

### **자동 리포트**
```javascript
// 셀렉터 검증 스크립트
function validateSelectors() {
  const results = {};
  for (const [platform, selectors] of Object.entries(SELECTORS)) {
    const input = document.querySelector(selectors.input);
    const button = document.querySelector(selectors.button);
    results[platform] = {
      inputFound: !!input,
      buttonFound: !!button,
      inputSelector: input ? selectors.input.split(',')[0] : null,
      buttonSelector: button ? selectors.button.split(',')[0] : null
    };
  }
  console.table(results);
}
```

## 📝 **변경 이력**

| 날짜 | 플랫폼 | 변경사항 |
|------|--------|---------|
| 2025-09-04 | Perplexity | `.PromptTextarea`, `#chat-input` 추가 |
| 2025-09-04 | Claude | Draft.js, `role="textbox"` 지원 |
| 2025-09-04 | Gemini | Material Angular 컴포넌트 대응 |
| 2025-09-04 | ChatGPT | `data-id="root"`, TailwindCSS 클래스 |

---
📅 **마지막 업데이트**: 2025-09-04  
🏷️ **현재 버전**: v1.1.5  
🔧 **총 셀렉터 수**: 50+ (모든 플랫폼 합계)