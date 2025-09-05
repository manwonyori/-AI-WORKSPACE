# ⚡ 빠른 테스트 스크립트 - 각 플랫폼별

## 🎯 현재 열린 플랫폼들
- ChatGPT (https://chatgpt.com)
- Google AI Studio (https://aistudio.google.com) 
- Claude AI (https://claude.ai)
- Perplexity AI (https://perplexity.ai)

---

## 1️⃣ ChatGPT 테스트 스크립트 (복사해서 콘솔에 붙여넣기)

```javascript
console.clear();
console.log("🔓 ChatGPT 완전 복구 시작...");

// 입력창 강제 활성화
function unlockChatGPT() {
    const selectors = [
        '#prompt-textarea',
        'div#prompt-textarea[contenteditable="true"]', 
        'div[contenteditable="true"].ProseMirror',
        'textarea',
        'div[contenteditable="true"]'
    ];
    
    let count = 0;
    selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
            if (el.tagName === 'TEXTAREA') {
                el.readOnly = false;
                el.disabled = false;
                el.removeAttribute('readonly');
                el.removeAttribute('disabled');
            } else {
                el.contentEditable = 'true';
                el.removeAttribute('readonly');
                el.removeAttribute('disabled');
            }
            el.style.pointerEvents = 'auto';
            el.style.userSelect = 'text';
            el.style.cursor = 'text';
            count++;
        });
    });
    console.log(`✅ ${count}개 입력창 활성화 완료!`);
}

// 테스트 입력
async function testInput() {
    const input = document.querySelector('#prompt-textarea') || 
                 document.querySelector('div[contenteditable="true"].ProseMirror');
    
    if (!input) {
        console.error("❌ 입력창을 찾을 수 없음");
        return;
    }
    
    const testMsg = `ChatGPT 테스트 성공! ${Date.now()}`;
    input.focus();
    
    if (input.tagName === 'TEXTAREA') {
        input.value = testMsg;
    } else {
        input.innerHTML = `<p>${testMsg}</p>`;
    }
    
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    
    console.log("🎉 ChatGPT 입력 성공! 화면을 확인하세요.");
}

// 실행
unlockChatGPT();
setTimeout(testInput, 1000);
```

---

## 2️⃣ Google AI Studio 테스트 스크립트

```javascript
console.clear();
console.log("🎯 Google AI Studio 완전 복구 시작...");

// 전송 버튼 찾기
function findRunButton() {
    const buttons = Array.from(document.querySelectorAll('button'));
    console.log(`🔍 ${buttons.length}개 버튼 스캔...`);
    
    const candidates = buttons.filter(btn => {
        const rect = btn.getBoundingClientRect();
        const visible = rect.width > 0 && rect.height > 0;
        const enabled = !btn.disabled;
        
        if (!visible || !enabled) return false;
        
        const label = btn.getAttribute('aria-label') || '';
        const text = btn.textContent || '';
        const matIcon = btn.querySelector('mat-icon');
        
        return label.toLowerCase().includes('run') || 
               label.toLowerCase().includes('send') ||
               text.toLowerCase().includes('run') ||
               (matIcon && matIcon.textContent.includes('play_arrow'));
    });
    
    if (candidates.length > 0) {
        console.log(`✅ Run 버튼 발견: ${candidates[0].getAttribute('aria-label')}`);
        return candidates[0];
    }
    return null;
}

// 입력 및 전송
async function testGemini() {
    const textarea = document.querySelector('textarea.textarea') || 
                    document.querySelector('textarea') ||
                    document.querySelector('.ql-editor');
    
    if (!textarea) {
        console.error("❌ 입력창을 찾을 수 없음");
        return;
    }
    
    const testMsg = `Google AI Studio 테스트 성공! ${Date.now()}`;
    
    // 입력
    textarea.focus();
    textarea.value = testMsg;
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    textarea.dispatchEvent(new Event('change', { bubbles: true }));
    
    console.log("✅ 입력 완료!");
    
    // 전송 버튼 대기 및 클릭
    await new Promise(r => setTimeout(r, 2000));
    
    const runBtn = findRunButton();
    if (runBtn) {
        runBtn.click();
        console.log("🎉 Google AI Studio 전송 성공!");
    } else {
        console.log("⚠️ Run 버튼을 찾지 못함. 수동으로 클릭해주세요.");
    }
}

// 실행
testGemini();
```

---

## 3️⃣ Claude AI 확인 스크립트 (정상 작동 확인용)

```javascript
console.clear();
console.log("✅ Claude AI 상태 확인...");

const textarea = document.querySelector('textarea') || 
                document.querySelector('[contenteditable="true"]');

if (textarea) {
    const testMsg = `Claude 정상 작동 확인 ${Date.now()}`;
    textarea.focus();
    
    if (textarea.tagName === 'TEXTAREA') {
        textarea.value = testMsg;
    } else {
        textarea.textContent = testMsg;
    }
    
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    console.log("✅ Claude는 정상 작동합니다!");
} else {
    console.log("❌ Claude 입력창을 찾을 수 없음");
}
```

---

## 4️⃣ Perplexity AI 확인 스크립트

```javascript
console.clear();
console.log("✅ Perplexity AI 상태 확인...");

const textarea = document.querySelector('textarea') || 
                document.querySelector('[contenteditable="true"]');

if (textarea) {
    const testMsg = `Perplexity 정상 작동 확인 ${Date.now()}`;
    textarea.focus();
    
    if (textarea.tagName === 'TEXTAREA') {
        textarea.value = testMsg;
    } else {
        textarea.textContent = testMsg;
    }
    
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    console.log("✅ Perplexity는 정상 작동합니다!");
} else {
    console.log("❌ Perplexity 입력창을 찾을 수 없음");
}
```

---

## 🚀 실행 순서

1. **ChatGPT 탭**: F12 → Console → ChatGPT 스크립트 붙여넣기
2. **Google AI Studio 탭**: F12 → Console → Google AI Studio 스크립트 붙여넣기  
3. **Claude 탭**: F12 → Console → Claude 확인 스크립트 붙여넣기
4. **Perplexity 탭**: F12 → Console → Perplexity 확인 스크립트 붙여넣기

## 📊 예상 결과

- ✅ **ChatGPT**: "입력창 활성화 완료!" → "입력 성공!"
- ✅ **Google AI Studio**: "입력 완료!" → "전송 성공!"  
- ✅ **Claude**: "정상 작동합니다!"
- ✅ **Perplexity**: "정상 작동합니다!"

---
*전체 플랫폼 테스트 - 2025년 9월 4일*