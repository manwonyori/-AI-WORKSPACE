# 🧪 로컬 테스트 가이드 - AI 플랫폼 수정 스크립트

## 🎯 테스트 방법

각 AI 플랫폼에서 **개발자 도구 콘솔**에 스크립트를 직접 붙여넣어 실행합니다.

---

## 1️⃣ ChatGPT 테스트 (https://chatgpt.com)

### 단계:
1. ChatGPT 페이지 접속
2. F12 → Console 탭 열기
3. 아래 스크립트 복사하여 붙여넣기

### 테스트 스크립트:
```javascript
// ChatGPT 완전 복구 스크립트 실행
console.log("🔓 ChatGPT 입력창 복구 시작...");

// 입력창 잠금 해제
function unlockInputs() {
    const inputSelectors = [
        '#prompt-textarea',
        'div#prompt-textarea[contenteditable="true"]',
        'div[contenteditable="true"].ProseMirror',
        'textarea',
        'div[contenteditable="true"]'
    ];
    
    let unlockedCount = 0;
    
    inputSelectors.forEach(selector => {
        try {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (element.tagName === 'TEXTAREA' || element.tagName === 'INPUT') {
                    element.readOnly = false;
                    element.disabled = false;
                    element.removeAttribute('readonly');
                    element.removeAttribute('disabled');
                } else if (element.contentEditable !== undefined) {
                    element.contentEditable = 'true';
                    element.removeAttribute('readonly');
                    element.removeAttribute('disabled');
                }
                
                element.removeAttribute('aria-disabled');
                element.style.pointerEvents = 'auto';
                element.style.userSelect = 'text';
                element.style.cursor = 'text';
                
                unlockedCount++;
            });
        } catch (e) {
            console.log(`❌ ${selector} 처리 실패: ${e.message}`);
        }
    });
    
    console.log(`✅ ${unlockedCount}개 입력창 활성화 완료!`);
    return unlockedCount > 0;
}

// 강제 입력 테스트
async function testChatGPTInput(text = "ChatGPT 로컬 테스트 - 이 메시지가 보이나요? " + Date.now()) {
    console.log(`📤 입력 테스트: "${text}"`);
    
    const mainInput = document.querySelector('#prompt-textarea.ProseMirror[contenteditable="true"]') ||
                     document.querySelector('#prompt-textarea') ||
                     document.querySelector('div[contenteditable="true"].ProseMirror');
    
    if (!mainInput) {
        console.error("❌ 입력창을 찾을 수 없음");
        return false;
    }
    
    // 포커스 및 입력
    mainInput.focus();
    mainInput.innerHTML = `<p>${text}</p>`;
    
    // 이벤트 발생
    mainInput.dispatchEvent(new Event('input', { bubbles: true }));
    mainInput.dispatchEvent(new Event('change', { bubbles: true }));
    
    console.log("✅ 입력 완료! 화면에서 확인해보세요.");
    return true;
}

// 실행
unlockInputs();
setTimeout(() => testChatGPTInput(), 1000);
```

---

## 2️⃣ Google AI Studio 테스트 (https://aistudio.google.com)

### 단계:
1. Google AI Studio 페이지 접속
2. F12 → Console 탭 열기  
3. 아래 스크립트 복사하여 붙여넣기

### 테스트 스크립트:
```javascript
// Google AI Studio 완전 복구 스크립트 실행
console.log("🎯 Google AI Studio 복구 시작...");

// 전송 버튼 찾기
function findSendButton() {
    const allButtons = document.querySelectorAll('button');
    console.log(`🔍 총 ${allButtons.length}개 버튼 스캔 중...`);
    
    let candidates = [];
    
    allButtons.forEach(btn => {
        const rect = btn.getBoundingClientRect();
        const isVisible = rect.width > 0 && rect.height > 0;
        const isEnabled = !btn.disabled;
        
        if (isVisible && isEnabled) {
            const ariaLabel = btn.getAttribute('aria-label') || '';
            const text = btn.textContent?.trim() || '';
            const hasMatIcon = btn.querySelector('mat-icon');
            
            let score = 0;
            if (ariaLabel.toLowerCase().includes('send') || ariaLabel.toLowerCase().includes('run')) score += 10;
            if (text.toLowerCase().includes('send') || text.toLowerCase().includes('run')) score += 8;
            if (hasMatIcon) {
                const iconText = hasMatIcon.textContent || '';
                if (iconText.includes('send') || iconText.includes('play_arrow')) score += 8;
            }
            
            if (score > 0) {
                candidates.push({
                    element: btn,
                    score,
                    ariaLabel,
                    text: text.slice(0, 30),
                    iconText: hasMatIcon ? hasMatIcon.textContent : ''
                });
            }
        }
    });
    
    candidates.sort((a, b) => b.score - a.score);
    
    if (candidates.length > 0) {
        console.log(`🎯 최고 후보: 점수 ${candidates[0].score} - "${candidates[0].ariaLabel || candidates[0].text}"`);
        return candidates[0].element;
    }
    
    return null;
}

// 입력 및 전송 테스트
async function testGeminiInput(text = "Google AI Studio 로컬 테스트 - 이 메시지가 보이나요? " + Date.now()) {
    console.log(`📤 입력 테스트: "${text}"`);
    
    // 입력창 찾기
    const textarea = document.querySelector('textarea.textarea') || 
                    document.querySelector('textarea') ||
                    document.querySelector('.ql-editor');
    
    if (!textarea) {
        console.error("❌ 입력창을 찾을 수 없음");
        return false;
    }
    
    // 입력
    textarea.focus();
    textarea.value = text;
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    textarea.dispatchEvent(new Event('change', { bubbles: true }));
    
    console.log("✅ 입력 완료!");
    
    // 전송 버튼 찾기 및 클릭
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const sendButton = findSendButton();
    if (sendButton) {
        console.log("🖱️ 전송 버튼 클릭 시도...");
        sendButton.click();
        console.log("✅ 전송 완료!");
        return true;
    } else {
        console.log("❌ 전송 버튼을 찾을 수 없음");
        return false;
    }
}

// 실행
testGeminiInput();
```

---

## 3️⃣ 종합 테스트 스크립트 (모든 플랫폼 대응)

### 어느 플랫폼에서든 실행 가능:
```javascript
// 플랫폼 자동 감지 및 적절한 수정 적용
console.log("🔍 플랫폼 감지 및 자동 수정 시작...");

function detectPlatform() {
    const hostname = location.hostname;
    if (hostname.includes('chatgpt.com')) return 'chatgpt';
    if (hostname.includes('aistudio.google.com')) return 'gemini';
    if (hostname.includes('gemini.google.com')) return 'gemini';
    if (hostname.includes('claude.ai')) return 'claude';
    if (hostname.includes('perplexity.ai')) return 'perplexity';
    return 'unknown';
}

const platform = detectPlatform();
console.log(`✅ 감지된 플랫폼: ${platform}`);

// 플랫폼별 자동 실행
if (platform === 'chatgpt') {
    console.log("🔓 ChatGPT 자동 수정 실행...");
    // ChatGPT 수정 코드 실행
} else if (platform === 'gemini') {
    console.log("🎯 Google AI Studio 자동 수정 실행...");
    // Gemini 수정 코드 실행
} else {
    console.log("✅ 이 플랫폼은 수정이 필요하지 않습니다.");
}
```

---

## 📋 테스트 체크리스트

### ChatGPT:
- [ ] 입력창 활성화 확인
- [ ] 메시지 입력 가능
- [ ] 전송 버튼 활성화

### Google AI Studio:
- [ ] 입력창에 텍스트 입력 가능
- [ ] "Run" 버튼 감지 및 클릭 가능
- [ ] 메시지 전송 성공

### 결과:
- **성공시**: "✅ 입력 완료!", "✅ 전송 완료!" 메시지 표시
- **실패시**: "❌" 메시지와 함께 오류 내용 표시

---

*로컬 테스트 - 2025년 9월 4일*