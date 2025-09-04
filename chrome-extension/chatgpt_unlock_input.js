/**
 * ChatGPT 입력창 잠금 해제 및 강제 활성화
 * 
 * 진단 결과: 모든 입력창이 ReadOnly + Disabled 상태
 * 이를 강제로 활성화하여 입력 가능하게 만듭니다.
 */

console.clear();
console.log("%c🔓 ChatGPT 입력창 잠금 해제", "color: #ff0000; font-size: 18px; font-weight: bold;");

// 1. 입력창 상태 강제 변경
function unlockInputs() {
    console.log("\n🔓 입력창 잠금 해제 시작...");
    
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
                const originalState = {
                    readonly: element.readOnly,
                    disabled: element.disabled,
                    contentEditable: element.contentEditable
                };
                
                console.log(`🔧 처리 중: ${element.tagName}#${element.id || 'no-id'}`);
                console.log(`   원래 상태: readonly=${originalState.readonly}, disabled=${originalState.disabled}, contentEditable=${originalState.contentEditable}`);
                
                // 강제 활성화
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
                
                // 추가 속성들 제거
                element.removeAttribute('aria-disabled');
                element.removeAttribute('data-readonly');
                
                // 스타일 속성 수정
                element.style.pointerEvents = 'auto';
                element.style.userSelect = 'text';
                element.style.cursor = 'text';
                
                console.log(`   ✅ 활성화 완료: readonly=false, disabled=false, contentEditable=true`);
                unlockedCount++;
            });
        } catch (e) {
            console.log(`❌ ${selector} 처리 실패: ${e.message}`);
        }
    });
    
    console.log(`🎉 총 ${unlockedCount}개 입력창 활성화 완료!`);
    return unlockedCount > 0;
}

// 2. ChatGPT 상태 체크 및 초기화
function resetChatGPTState() {
    console.log("\n🔄 ChatGPT 상태 초기화...");
    
    // Stop 버튼이 있다면 클릭 (처리 중 상태 해제)
    const stopButtons = document.querySelectorAll('button[aria-label*="stop" i], button[aria-label*="Stop" i], button.stop-button');
    if (stopButtons.length > 0) {
        console.log(`🛑 Stop 버튼 ${stopButtons.length}개 발견, 클릭 시도...`);
        stopButtons.forEach(btn => {
            try {
                btn.click();
                console.log("   ✅ Stop 버튼 클릭 완료");
            } catch (e) {
                console.log("   ❌ Stop 버튼 클릭 실패:", e.message);
            }
        });
    }
    
    // Regenerate나 Continue 버튼 체크
    const actionButtons = document.querySelectorAll('button[aria-label*="regenerate" i], button[aria-label*="continue" i]');
    if (actionButtons.length > 0) {
        console.log(`🔄 액션 버튼 ${actionButtons.length}개 발견`);
        actionButtons.forEach(btn => {
            console.log(`   버튼: ${btn.getAttribute('aria-label') || btn.textContent?.slice(0, 20)}`);
        });
    }
    
    // 오류 메시지 체크
    const errorMessages = document.querySelectorAll('.error, .warning, [role="alert"]');
    if (errorMessages.length > 0) {
        console.log(`⚠️ 오류 메시지 ${errorMessages.length}개 발견:`);
        errorMessages.forEach((msg, i) => {
            console.log(`   ${i+1}. ${msg.textContent?.slice(0, 100)}`);
        });
    }
}

// 3. 강제 입력 테스트 (잠금 해제 후)
async function forceInputTest(text = `강제 입력 테스트 ${Date.now()}`) {
    console.log(`\n💪 강제 입력 테스트: "${text}"`);
    
    // 먼저 잠금 해제
    const unlocked = unlockInputs();
    if (!unlocked) {
        console.error("❌ 활성화할 입력창이 없음");
        return false;
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 메인 입력창 찾기
    const mainInput = document.querySelector('#prompt-textarea.ProseMirror[contenteditable="true"]') ||
                     document.querySelector('#prompt-textarea') ||
                     document.querySelector('div[contenteditable="true"].ProseMirror');
    
    if (!mainInput) {
        console.error("❌ 메인 입력창을 찾을 수 없음");
        return false;
    }
    
    console.log(`🎯 사용할 입력창: ${mainInput.tagName}#${mainInput.id}`);
    
    try {
        // 1. 포커스
        console.log("1️⃣ 포커스 설정...");
        mainInput.focus();
        mainInput.click(); // 클릭도 시도
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 2. 클리어 (ProseMirror 방식)
        console.log("2️⃣ ProseMirror 클리어...");
        mainInput.innerHTML = '<p><br></p>'; // ProseMirror 기본 구조
        mainInput.dispatchEvent(new Event('input', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 3. 텍스트 입력 (ProseMirror 방식)
        console.log("3️⃣ ProseMirror 텍스트 입력...");
        mainInput.innerHTML = `<p>${text}</p>`;
        
        // 4. ProseMirror 전용 이벤트들
        console.log("4️⃣ ProseMirror 이벤트 발생...");
        const proseMirrorEvents = [
            new Event('focus', { bubbles: true }),
            new Event('beforeinput', { bubbles: true }),
            new InputEvent('input', { 
                bubbles: true, 
                inputType: 'insertText',
                data: text,
                composed: true
            }),
            new Event('change', { bubbles: true }),
            new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }),
            new KeyboardEvent('keyup', { key: 'Enter', bubbles: true }),
            new Event('compositionend', { bubbles: true }),
            new Event('textInput', { bubbles: true })
        ];
        
        proseMirrorEvents.forEach((event, i) => {
            try {
                mainInput.dispatchEvent(event);
                console.log(`   ✅ ProseMirror 이벤트 ${i+1}: ${event.type}`);
            } catch (e) {
                console.log(`   ❌ ProseMirror 이벤트 ${i+1}: ${event.type} 실패`);
            }
        });
        
        // 5. 강제 DOM 업데이트
        console.log("5️⃣ 강제 DOM 업데이트...");
        mainInput.setAttribute('data-content', text);
        mainInput.style.minHeight = '40px';
        
        // 6. React/Vue 업데이트 트리거 시도
        console.log("6️⃣ React 업데이트 트리거...");
        if (window.React && window.React.version) {
            console.log("   React 감지됨, 강제 업데이트 시도...");
            // React DevTools가 있다면 활용
            if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
                try {
                    window.__REACT_DEVTOOLS_GLOBAL_HOOK__.onCommitFiberRoot();
                } catch (e) {}
            }
        }
        
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 7. 결과 확인
        console.log("7️⃣ 입력 결과 확인...");
        const currentValue = mainInput.textContent || mainInput.innerText || mainInput.innerHTML;
        console.log(`   현재 내용: "${currentValue}"`);
        console.log(`   HTML: ${mainInput.innerHTML.slice(0, 100)}`);
        
        const success = currentValue.includes(text) || mainInput.innerHTML.includes(text);
        console.log(`   결과: ${success ? '✅ 성공' : '❌ 실패'}`);
        
        if (success) {
            console.log("🎉 강제 입력 성공! 이제 전송 버튼을 찾아보세요.");
            
            // 전송 버튼 상태도 체크
            setTimeout(() => {
                const sendButtons = document.querySelectorAll('button[data-testid="send-button"], button[aria-label*="send" i]');
                console.log(`📤 전송 버튼 ${sendButtons.length}개 발견:`);
                sendButtons.forEach((btn, i) => {
                    console.log(`   ${i+1}. Disabled: ${btn.disabled}, 보임: ${btn.offsetParent !== null}`);
                });
            }, 1000);
        }
        
        return success;
        
    } catch (error) {
        console.error("❌ 강제 입력 테스트 중 오류:", error);
        return false;
    }
}

// 4. 완전한 ChatGPT 복구
async function fullChatGPTRestore() {
    console.log("\n🛠️ 완전한 ChatGPT 복구 시작...");
    
    // 1단계: 상태 초기화
    resetChatGPTState();
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 2단계: 입력창 잠금 해제
    unlockInputs();
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 3단계: 강제 입력 테스트
    const inputSuccess = await forceInputTest("ChatGPT 복구 테스트 - 이 메시지가 보이나요?");
    
    console.log(`\n🎯 복구 결과: ${inputSuccess ? '✅ 성공' : '❌ 실패'}`);
    
    if (inputSuccess) {
        console.log("🎉 ChatGPT가 정상적으로 복구되었습니다!");
        console.log("이제 메시지를 입력하고 전송할 수 있습니다.");
    } else {
        console.log("❌ 복구에 실패했습니다. 페이지를 새로고침해보세요.");
    }
    
    return inputSuccess;
}

// 전역 함수 등록
window.unlockInputs = unlockInputs;
window.resetChatGPTState = resetChatGPTState;
window.forceInputTest = forceInputTest;
window.fullChatGPTRestore = fullChatGPTRestore;

console.log("\n💡 사용법:");
console.log("1. fullChatGPTRestore()           - 완전한 ChatGPT 복구 (권장)");
console.log("2. unlockInputs()                 - 입력창만 잠금 해제");
console.log("3. forceInputTest('메시지')       - 강제 입력 테스트");
console.log("4. resetChatGPTState()            - ChatGPT 상태만 초기화");

console.log("\n🎯 지금 바로 실행해보세요:");
console.log("fullChatGPTRestore()");

console.log("\n" + "=".repeat(60));
console.log("🔓 ChatGPT 입력창이 비활성화되어 있는 문제를 해결합니다!");
console.log("ReadOnly/Disabled 상태를 강제로 해제하고 입력을 가능하게 만듭니다.");
console.log("=".repeat(60));