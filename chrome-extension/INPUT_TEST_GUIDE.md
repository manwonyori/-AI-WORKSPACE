# 🔍 ChatGPT & Gemini 입력 문제 조사 가이드

## 🚨 현재 상황
- ✅ Claude: 정상 작동
- ✅ Perplexity: 정상 작동  
- ❌ ChatGPT: 입력 안됨
- ❌ Gemini/AI Studio: 입력 안됨

## 🧪 조사 방법

### 1. ChatGPT 조사 (chatgpt.com)

#### Step 1: 입력창 확인
```javascript
// F12 콘솔에 실행
const ta = document.querySelector('textarea#prompt-textarea');
if (ta) {
    console.log('✅ Textarea found:', ta);
    ta.style.border = '5px solid red';
    console.log('Properties:', {
        id: ta.id,
        class: ta.className,
        readOnly: ta.readOnly,
        disabled: ta.disabled
    });
} else {
    console.log('❌ No textarea#prompt-textarea found');
    // 다른 textarea 찾기
    document.querySelectorAll('textarea').forEach((t, i) => {
        console.log(`Textarea[${i}]:`, t);
        t.style.border = '3px solid yellow';
    });
}
```

#### Step 2: 입력 테스트
```javascript
// 여러 방법으로 텍스트 입력 시도
const textarea = document.querySelector('textarea#prompt-textarea') || document.querySelector('textarea');

// Test 1: Direct value
console.log('Test 1: Direct value');
textarea.value = 'Test 1';

// Test 2: Focus and type
setTimeout(() => {
    console.log('Test 2: Focus and type');
    textarea.focus();
    textarea.value = 'Test 2';
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
}, 2000);

// Test 3: React style
setTimeout(() => {
    console.log('Test 3: React style');
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
        window.HTMLTextAreaElement.prototype, 'value'
    ).set;
    nativeInputValueSetter.call(textarea, 'Test 3');
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
}, 4000);

// Test 4: Keyboard event
setTimeout(() => {
    console.log('Test 4: Keyboard event');
    textarea.focus();
    textarea.value = 'Test 4';
    textarea.dispatchEvent(new KeyboardEvent('keydown', { key: 'a' }));
    textarea.dispatchEvent(new KeyboardEvent('keyup', { key: 'a' }));
}, 6000);
```

### 2. Gemini/AI Studio 조사

#### Google AI Studio URL:
**https://aistudio.google.com/prompts/new_chat**

#### Step 1: 입력창 확인
```javascript
// F12 콘솔에 실행
const editor = document.querySelector('.ql-editor');
if (editor) {
    console.log('✅ Quill editor found:', editor);
    editor.style.border = '5px solid red';
    console.log('Properties:', {
        class: editor.className,
        contentEditable: editor.contentEditable,
        innerHTML: editor.innerHTML
    });
} else {
    console.log('❌ No .ql-editor found');
    // contenteditable 찾기
    document.querySelectorAll('[contenteditable="true"]').forEach((el, i) => {
        console.log(`ContentEditable[${i}]:`, el);
        el.style.border = '3px solid yellow';
    });
}
```

#### Step 2: 입력 테스트
```javascript
// Quill Editor 입력 테스트
const editor = document.querySelector('.ql-editor');

// Test 1: innerHTML
console.log('Test 1: innerHTML');
editor.innerHTML = '<p>Test 1</p>';

// Test 2: Focus and innerHTML
setTimeout(() => {
    console.log('Test 2: Focus and innerHTML');
    editor.focus();
    editor.innerHTML = '<p>Test 2</p>';
    editor.dispatchEvent(new Event('input', { bubbles: true }));
}, 2000);

// Test 3: textContent
setTimeout(() => {
    console.log('Test 3: textContent');
    editor.focus();
    editor.textContent = 'Test 3';
    editor.dispatchEvent(new InputEvent('input', { 
        bubbles: true,
        inputType: 'insertText'
    }));
}, 4000);

// Test 4: execCommand
setTimeout(() => {
    console.log('Test 4: execCommand');
    editor.focus();
    document.execCommand('insertText', false, 'Test 4');
}, 6000);
```

## 📊 조사 결과 기록

### ChatGPT
```
작동하는 방법: [기록하세요]
셀렉터: [기록하세요]
이벤트 타입: [기록하세요]
```

### Gemini
```
작동하는 방법: [기록하세요]
셀렉터: [기록하세요]
이벤트 타입: [기록하세요]
```

## 🔧 Extension 수정 방향

조사 결과를 바탕으로:
1. 정확한 셀렉터 사용
2. 올바른 입력 메소드 적용
3. 필요한 이벤트 발생

## 📝 완전 조사 스크립트

더 자세한 조사가 필요하면:
```javascript
// platform_investigation.js 파일 내용을 F12 콘솔에 복사/붙여넣기
// 자동으로 모든 테스트 실행
```

## ❓ 핵심 질문

1. **ChatGPT**
   - textarea의 정확한 id는?
   - React 컴포넌트인가?
   - 어떤 이벤트를 listen하는가?

2. **Gemini**
   - Quill Editor를 사용하는가?
   - contentEditable div인가?
   - 어떤 이벤트가 필요한가?

각 플랫폼에서 위 테스트를 실행하고 결과를 기록해주세요!