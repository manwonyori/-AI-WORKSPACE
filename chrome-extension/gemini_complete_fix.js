/**
 * Google AI Studio / Gemini 완전 복구 시스템
 * 
 * ChatGPT에서 성공한 방식을 Google AI Studio에 적용하여
 * 모든 입력 문제를 해결합니다.
 */

console.clear();
console.log("%c🤖 Google AI Studio 완전 복구", "color: #4285f4; font-size: 20px; font-weight: bold;");
console.log("ChatGPT 성공 방식을 적용하여 Google AI Studio를 완전히 복구합니다.\n");

// 현재 환경 확인
const currentURL = location.href;
const hostname = location.hostname;
let isGemini = hostname.includes('aistudio.google.com') || hostname.includes('gemini.google.com');

console.log(`🎯 현재 사이트: ${hostname}`);
console.log(`📍 Google AI Studio 여부: ${isGemini ? '✅' : '❌'}`);
console.log(`🔗 현재 URL: ${currentURL}\n`);

// 1. Google AI Studio 입력창 정밀 진단
function diagnoseGeminiInputs() {
    console.log("📋 Google AI Studio 입력창 정밀 진단");
    console.log("-".repeat(50));
    
    const inputSelectors = [
        'textarea.textarea',
        'textarea[aria-label*="Type something"]',
        'textarea[placeholder]',
        'rich-textarea textarea',
        '.ql-editor',
        'div[contenteditable="true"].ql-editor',
        'textarea[rows]',
        'textarea',
        'div[contenteditable="true"]',
        'input[type="text"]'
    ];
    
    let foundInputs = [];
    
    inputSelectors.forEach((selector, i) => {
        try {
            const elements = document.querySelectorAll(selector);
            elements.forEach((element, j) => {
                const rect = element.getBoundingClientRect();
                const isVisible = rect.width > 0 && rect.height > 0 && 
                                window.getComputedStyle(element).display !== 'none';
                
                const inputInfo = {
                    index: `${i+1}-${j+1}`,
                    selector,
                    element,
                    visible: isVisible,
                    tagName: element.tagName,
                    id: element.id,
                    className: element.className,
                    rect: { width: rect.width, height: rect.height },
                    placeholder: element.placeholder || element.getAttribute('placeholder'),
                    ariaLabel: element.getAttribute('aria-label'),
                    readonly: element.readOnly,
                    disabled: element.disabled
                };
                
                foundInputs.push(inputInfo);
                
                console.log(`${i+1}-${j+1}. ${selector}`);
                console.log(`    태그: ${element.tagName}`);
                console.log(`    ID: ${element.id || 'none'}`);
                console.log(`    클래스: ${element.className.slice(0, 50) || 'none'}`);
                console.log(`    보임: ${isVisible ? '✅' : '❌'}`);
                console.log(`    크기: ${rect.width}x${rect.height}`);
                console.log(`    Placeholder: ${inputInfo.placeholder || 'none'}`);
                console.log(`    AriaLabel: ${inputInfo.ariaLabel || 'none'}`);
                console.log(`    ReadOnly: ${element.readOnly ? '❌' : '✅'}`);
                console.log(`    Disabled: ${element.disabled ? '❌' : '✅'}`);
                console.log("");
            });
        } catch (e) {
            console.log(`${i+1}. ${selector} - 선택자 오류: ${e.message}`);
        }
    });
    
    // 가장 적합한 입력창 선택
    const bestInput = foundInputs.find(input => 
        input.visible && !input.readonly && !input.disabled && 
        (input.className.includes('textarea') || input.ariaLabel?.includes('Type'))
    ) || foundInputs.find(input => input.visible && !input.readonly && !input.disabled);
    
    console.log(`🎯 최적 입력창: ${bestInput ? `${bestInput.tagName}.${bestInput.className.split(' ')[0]}` : '찾을 수 없음'}`);
    
    return { foundInputs, bestInput };
}

// 2. Google AI Studio 입력창 잠금 해제
function unlockGeminiInputs() {
    console.log("\n🔓 Google AI Studio 입력창 잠금 해제...");
    
    const inputSelectors = [
        'textarea.textarea',
        'textarea[aria-label*="Type something"]',
        'textarea',
        '.ql-editor',
        'div[contenteditable="true"]'
    ];
    
    let unlockedCount = 0;
    
    inputSelectors.forEach(selector => {
        try {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                console.log(`🔧 처리 중: ${element.tagName}.${element.className.split(' ')[0]}`);
                
                // 강제 활성화
                if (element.tagName === 'TEXTAREA') {
                    element.readOnly = false;
                    element.disabled = false;
                    element.removeAttribute('readonly');
                    element.removeAttribute('disabled');
                } else if (element.classList.contains('ql-editor')) {
                    element.contentEditable = 'true';
                    element.removeAttribute('readonly');
                    element.removeAttribute('disabled');
                }
                
                // Angular/Material 속성들 정리
                element.removeAttribute('aria-disabled');
                element.removeAttribute('data-readonly');
                element.style.pointerEvents = 'auto';
                element.style.userSelect = 'text';
                element.style.cursor = 'text';
                
                console.log(`   ✅ 활성화 완료`);
                unlockedCount++;
            });
        } catch (e) {
            console.log(`❌ ${selector} 처리 실패: ${e.message}`);
        }
    });
    
    console.log(`🎉 총 ${unlockedCount}개 입력창 활성화 완료!`);
    return unlockedCount > 0;
}

// 3. Google AI Studio 상태 초기화
function resetGeminiState() {
    console.log("\n🔄 Google AI Studio 상태 초기화...");
    
    // Stop 버튼이 있다면 클릭
    const stopSelectors = [
        'button[aria-label*="stop" i]',
        'button[aria-label*="Stop" i]',
        '.stop-button',
        'button:has(mat-icon[fonticon="stop"])'
    ];
    
    let stoppedCount = 0;
    stopSelectors.forEach(selector => {
        try {
            const buttons = document.querySelectorAll(selector);
            buttons.forEach(btn => {
                if (!btn.disabled) {
                    btn.click();
                    console.log(`🛑 Stop 버튼 클릭: ${selector}`);
                    stoppedCount++;
                }
            });
        } catch (e) {}
    });
    
    if (stoppedCount === 0) {
        console.log("ℹ️ 활성 Stop 버튼 없음");
    }
    
    // 오류 메시지 체크
    const errorSelectors = ['.error', '.warning', '[role="alert"]', '.mat-error'];
    const errors = [];
    errorSelectors.forEach(selector => {
        try {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                if (el.textContent?.trim()) {
                    errors.push(el.textContent.trim().slice(0, 100));
                }
            });
        } catch (e) {}
    });
    
    if (errors.length > 0) {
        console.log(`⚠️ 오류 메시지 ${errors.length}개 발견:`);
        errors.forEach((msg, i) => console.log(`   ${i+1}. ${msg}`));
    } else {
        console.log("✅ 오류 메시지 없음");
    }
}

// 4. Google AI Studio 강제 입력 테스트
async function forceGeminiInput(text = `Gemini 복구 테스트 ${Date.now()}`) {
    console.log(`\n💪 Google AI Studio 강제 입력: "${text}"`);
    
    // 먼저 잠금 해제
    unlockGeminiInputs();
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 최적 입력창 찾기
    const diagnosis = diagnoseGeminiInputs();
    const mainInput = diagnosis.bestInput?.element;
    
    if (!mainInput) {
        console.error("❌ 사용 가능한 입력창을 찾을 수 없음");
        return false;
    }
    
    console.log(`🎯 사용할 입력창: ${mainInput.tagName}.${mainInput.className.split(' ')[0]}`);
    
    try {
        // 1. 포커스
        console.log("1️⃣ 포커스 설정...");
        mainInput.focus();
        mainInput.click();
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 2. 기존 내용 클리어
        console.log("2️⃣ 기존 내용 클리어...");
        if (mainInput.tagName === 'TEXTAREA') {
            mainInput.value = '';
        } else if (mainInput.classList.contains('ql-editor')) {
            mainInput.innerHTML = '<p><br></p>'; // Quill 기본 구조
        } else {
            mainInput.textContent = '';
        }
        
        mainInput.dispatchEvent(new Event('input', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 3. 새 텍스트 입력
        console.log("3️⃣ 새 텍스트 입력...");
        if (mainInput.tagName === 'TEXTAREA') {
            mainInput.value = text;
            console.log("   ✅ Textarea 입력 완료");
        } else if (mainInput.classList.contains('ql-editor')) {
            mainInput.innerHTML = `<p>${text}</p>`;
            console.log("   ✅ Quill Editor 입력 완료");
        } else {
            mainInput.textContent = text;
            console.log("   ✅ ContentEditable 입력 완료");
        }
        
        // 4. Angular/Material 친화적 이벤트들
        console.log("4️⃣ Angular 이벤트 발생...");
        const angularEvents = [
            new Event('focus', { bubbles: true }),
            new Event('beforeinput', { bubbles: true }),
            new InputEvent('input', { 
                bubbles: true, 
                inputType: 'insertText',
                data: text
            }),
            new Event('change', { bubbles: true }),
            new Event('blur', { bubbles: true }),  // Angular change detection 중요
            new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }),
            new KeyboardEvent('keyup', { key: 'Enter', bubbles: true })
        ];
        
        angularEvents.forEach((event, i) => {
            try {
                mainInput.dispatchEvent(event);
                console.log(`   ✅ Angular 이벤트 ${i+1}: ${event.type}`);
            } catch (e) {
                console.log(`   ❌ Angular 이벤트 ${i+1}: ${event.type} 실패`);
            }
        });
        
        // 5. Angular Zone 강제 트리거 (가능한 경우)
        console.log("5️⃣ Angular Zone 트리거...");
        try {
            if (window.ng) {
                console.log("   Angular 감지됨, Zone 트리거 시도...");
                // Angular의 NgZone.run() 시뮬레이션
                setTimeout(() => {
                    mainInput.dispatchEvent(new Event('ngModelChange', { bubbles: true }));
                }, 100);
            }
        } catch (e) {
            console.log("   Angular Zone 트리거 실패:", e.message);
        }
        
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 6. 결과 확인
        console.log("6️⃣ 입력 결과 확인...");
        const currentValue = mainInput.value || mainInput.textContent || mainInput.innerText;
        const currentHTML = mainInput.innerHTML;
        
        console.log(`   현재 값: "${currentValue}"`);
        console.log(`   HTML: ${currentHTML.slice(0, 100)}`);
        
        const success = currentValue.includes(text) || currentHTML.includes(text);
        console.log(`   결과: ${success ? '✅ 성공' : '❌ 실패'}`);
        
        if (success) {
            console.log("🎉 Gemini 입력 성공! 이제 전송 버튼을 확인해보세요.");
            
            // 전송 버튼 상태 체크
            setTimeout(() => {
                checkGeminiSendButtons();
            }, 1000);
        }
        
        return success;
        
    } catch (error) {
        console.error("❌ Gemini 강제 입력 중 오류:", error);
        return false;
    }
}

// 5. Google AI Studio 전송 버튼 체크
function checkGeminiSendButtons() {
    console.log("\n📤 Google AI Studio 전송 버튼 체크...");
    
    const buttonSelectors = [
        'button[aria-label="Send message"]',
        'button[aria-label*="Send" i]',
        'button.mat-icon-button:has(mat-icon[fonticon="send"])',
        'button:has(mat-icon[fonticon="send"])',
        'mat-icon-button[aria-label*="Send" i]',
        'button[mattooltip*="Send" i]'
    ];
    
    let foundButtons = [];
    
    buttonSelectors.forEach(selector => {
        try {
            const buttons = document.querySelectorAll(selector);
            buttons.forEach(btn => {
                const rect = btn.getBoundingClientRect();
                const isVisible = rect.width > 0 && rect.height > 0;
                const isEnabled = !btn.disabled && !btn.hasAttribute('disabled');
                
                if (isVisible) {
                    foundButtons.push({
                        element: btn,
                        selector,
                        enabled: isEnabled,
                        ariaLabel: btn.getAttribute('aria-label') || 'no-label'
                    });
                }
            });
        } catch (e) {}
    });
    
    console.log(`📊 발견된 전송 버튼: ${foundButtons.length}개`);
    foundButtons.forEach((btn, i) => {
        console.log(`   ${i+1}. "${btn.ariaLabel}" (${btn.enabled ? '활성' : '비활성'})`);
    });
    
    const activeButtons = foundButtons.filter(btn => btn.enabled);
    console.log(`🎯 활성 전송 버튼: ${activeButtons.length}개`);
    
    return activeButtons;
}

// 6. 완전한 Google AI Studio 복구
async function fullGeminiRestore() {
    console.log("\n🛠️ 완전한 Google AI Studio 복구 시작...");
    
    if (!isGemini) {
        console.error("❌ Google AI Studio가 아닙니다!");
        console.log("https://aistudio.google.com/prompts/new_chat 로 이동해주세요.");
        return false;
    }
    
    // 1단계: 상태 초기화
    resetGeminiState();
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 2단계: 입력창 진단
    const diagnosis = diagnoseGeminiInputs();
    
    // 3단계: 입력창 잠금 해제
    unlockGeminiInputs();
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 4단계: 강제 입력 테스트
    const inputSuccess = await forceGeminiInput("Google AI Studio 복구 테스트 - 이 메시지가 보이나요?");
    
    console.log(`\n🎯 복구 결과: ${inputSuccess ? '✅ 성공' : '❌ 실패'}`);
    
    if (inputSuccess) {
        console.log("🎉 Google AI Studio가 정상적으로 복구되었습니다!");
        console.log("이제 메시지를 입력하고 전송할 수 있습니다.");
        
        // 전송 버튼 최종 체크
        const sendButtons = checkGeminiSendButtons();
        if (sendButtons.length > 0) {
            console.log("✅ 전송 가능한 상태입니다!");
        }
    } else {
        console.log("❌ 복구에 실패했습니다.");
        console.log("💡 해결책:");
        console.log("1. 페이지 새로고침");
        console.log("2. https://aistudio.google.com/prompts/new_chat 새로 시작");
        console.log("3. 다른 브라우저에서 시도");
    }
    
    return inputSuccess;
}

// 전역 함수 등록
window.diagnoseGeminiInputs = diagnoseGeminiInputs;
window.unlockGeminiInputs = unlockGeminiInputs;
window.resetGeminiState = resetGeminiState;
window.forceGeminiInput = forceGeminiInput;
window.checkGeminiSendButtons = checkGeminiSendButtons;
window.fullGeminiRestore = fullGeminiRestore;

console.log("💡 사용법:");
console.log("1. fullGeminiRestore()              - 완전한 Google AI Studio 복구 (권장)");
console.log("2. diagnoseGeminiInputs()           - 입력창 상태 진단");
console.log("3. forceGeminiInput('메시지')       - 강제 입력 테스트");
console.log("4. checkGeminiSendButtons()         - 전송 버튼 상태 확인");

if (isGemini) {
    console.log("\n🎯 지금 바로 실행해보세요:");
    console.log("fullGeminiRestore()");
} else {
    console.log("\n⚠️ Google AI Studio로 이동 후 실행하세요:");
    console.log("https://aistudio.google.com/prompts/new_chat");
}

console.log("\n" + "=".repeat(60));
console.log("🤖 ChatGPT 성공 방식을 Google AI Studio에 적용했습니다!");
console.log("Angular/Material UI 환경에 최적화된 복구 시스템입니다.");
console.log("=".repeat(60));