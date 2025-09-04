/**
 * ChatGPT 입력 문제 진단 및 해결
 * 
 * Real Working Fix가 로드되었지만 대화창에 실제 입력이 안 되는 문제를 해결합니다.
 */

console.clear();
console.log("%c🔍 ChatGPT 입력 문제 진단", "color: #ff6600; font-size: 18px; font-weight: bold;");

// 1. 현재 입력창 상태 정밀 진단
console.log("\n📋 1단계: 입력창 정밀 진단");
console.log("-".repeat(50));

const inputSelectors = [
    '#prompt-textarea',
    'textarea#prompt-textarea', 
    'div#prompt-textarea[contenteditable="true"]',
    'div[contenteditable="true"].ProseMirror',
    'textarea[placeholder*="Message"]',
    'div[contenteditable="true"][data-placeholder]',
    'textarea.m-0',
    'textarea',
    'div[contenteditable="true"]'
];

let foundInputs = [];

inputSelectors.forEach((selector, i) => {
    try {
        const elements = document.querySelectorAll(selector);
        elements.forEach((element, j) => {
            const rect = element.getBoundingClientRect();
            const isVisible = rect.width > 0 && rect.height > 0 && 
                            window.getComputedStyle(element).display !== 'none';
            
            foundInputs.push({
                index: `${i+1}-${j+1}`,
                selector,
                element,
                visible: isVisible,
                tagName: element.tagName,
                id: element.id,
                className: element.className,
                rect: { width: rect.width, height: rect.height },
                placeholder: element.placeholder || element.getAttribute('data-placeholder'),
                readonly: element.readOnly,
                disabled: element.disabled
            });
            
            console.log(`${i+1}-${j+1}. ${selector}`);
            console.log(`    태그: ${element.tagName}`);
            console.log(`    ID: ${element.id || 'none'}`);
            console.log(`    클래스: ${element.className.slice(0, 50) || 'none'}`);
            console.log(`    보임: ${isVisible ? '✅' : '❌'}`);
            console.log(`    크기: ${rect.width}x${rect.height}`);
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
    (input.id === 'prompt-textarea' || input.className.includes('ProseMirror'))
);

console.log(`\n🎯 최적 입력창: ${bestInput ? `${bestInput.tagName}#${bestInput.id}` : '찾을 수 없음'}`);

// 2. 실제 입력 테스트 함수
async function testRealInput(text = `입력 테스트 ${Date.now()}`) {
    console.log(`\n📤 실제 입력 테스트: "${text}"`);
    
    if (!bestInput) {
        console.error("❌ 사용 가능한 입력창이 없음");
        return false;
    }
    
    const element = bestInput.element;
    console.log(`🎯 사용할 입력창: ${element.tagName}#${element.id}`);
    
    try {
        // 단계별 입력 시도
        console.log("1️⃣ 포커스 설정...");
        element.focus();
        await new Promise(resolve => setTimeout(resolve, 500));
        
        console.log("2️⃣ 기존 내용 클리어...");
        if (element.tagName === 'TEXTAREA') {
            // React 방식 클리어
            const nativeValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            )?.set;
            
            if (nativeValueSetter) {
                nativeValueSetter.call(element, '');
                element.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
                console.log("   ✅ React setter로 클리어 완료");
            } else {
                element.value = '';
                element.dispatchEvent(new Event('input', { bubbles: true }));
                console.log("   ✅ 표준 방식으로 클리어 완료");
            }
        } else {
            element.textContent = '';
            element.innerHTML = '';
            element.dispatchEvent(new Event('input', { bubbles: true }));
            console.log("   ✅ ContentEditable 클리어 완료");
        }
        
        await new Promise(resolve => setTimeout(resolve, 500));
        
        console.log("3️⃣ 새 텍스트 입력...");
        if (element.tagName === 'TEXTAREA') {
            const nativeValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            )?.set;
            
            if (nativeValueSetter) {
                nativeValueSetter.call(element, text);
                console.log("   ✅ React setter로 입력");
            } else {
                element.value = text;
                console.log("   ✅ 표준 방식으로 입력");
            }
        } else {
            element.textContent = text;
            console.log("   ✅ ContentEditable로 입력");
        }
        
        console.log("4️⃣ 이벤트 발생...");
        const events = [
            new Event('beforeinput', { bubbles: true }),
            new InputEvent('input', { 
                bubbles: true, 
                inputType: 'insertText',
                data: text,
                composed: true
            }),
            new Event('change', { bubbles: true }),
            new KeyboardEvent('keydown', { key: 'Unidentified', bubbles: true }),
            new KeyboardEvent('keyup', { key: 'Unidentified', bubbles: true }),
            new Event('blur', { bubbles: true }),
            new Event('focus', { bubbles: true })
        ];
        
        events.forEach((event, i) => {
            try {
                element.dispatchEvent(event);
                console.log(`   ✅ 이벤트 ${i+1}: ${event.type}`);
            } catch (e) {
                console.log(`   ❌ 이벤트 ${i+1}: ${event.type} 실패 - ${e.message}`);
            }
        });
        
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        console.log("5️⃣ 입력 결과 확인...");
        const currentValue = element.value || element.textContent || element.innerHTML;
        console.log(`   현재 값: "${currentValue}"`);
        
        if (currentValue.includes(text)) {
            console.log("✅ 입력 성공!");
            return true;
        } else {
            console.log("❌ 입력 실패 - 텍스트가 반영되지 않음");
            return false;
        }
        
    } catch (error) {
        console.error("❌ 입력 테스트 중 오류:", error);
        return false;
    }
}

// 3. 다양한 입력 방식 테스트
async function testAllInputMethods() {
    console.log("\n🧪 모든 입력 방식 테스트");
    console.log("-".repeat(50));
    
    if (!bestInput) {
        console.error("❌ 테스트할 입력창이 없음");
        return;
    }
    
    const element = bestInput.element;
    const testText = `멀티 테스트 ${Date.now()}`;
    
    // 방법 1: 직접 입력
    console.log("🔄 방법 1: 직접 property 설정");
    element.focus();
    if (element.tagName === 'TEXTAREA') {
        element.value = testText + " (직접)";
    } else {
        element.textContent = testText + " (직접)";
    }
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 방법 2: 시뮬레이션된 타이핑
    console.log("🔄 방법 2: 시뮬레이션된 타이핑");
    element.focus();
    const typingText = testText + " (타이핑)";
    
    // 한 글자씩 타이핑 시뮬레이션
    for (let i = 0; i < typingText.length; i++) {
        const currentText = typingText.substring(0, i + 1);
        
        if (element.tagName === 'TEXTAREA') {
            const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
            if (setter) {
                setter.call(element, currentText);
            } else {
                element.value = currentText;
            }
        } else {
            element.textContent = currentText;
        }
        
        element.dispatchEvent(new InputEvent('input', {
            data: typingText[i],
            inputType: 'insertText',
            bubbles: true
        }));
        
        await new Promise(resolve => setTimeout(resolve, 50));
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 방법 3: 클립보드 시뮬레이션
    console.log("🔄 방법 3: 클립보드 시뮬레이션");
    element.focus();
    const pasteText = testText + " (붙여넣기)";
    
    if (element.tagName === 'TEXTAREA') {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
        if (setter) setter.call(element, pasteText);
        else element.value = pasteText;
    } else {
        element.textContent = pasteText;
    }
    
    element.dispatchEvent(new Event('paste', { bubbles: true }));
    element.dispatchEvent(new InputEvent('input', {
        inputType: 'insertFromPaste',
        data: pasteText,
        bubbles: true
    }));
    
    console.log("🎯 모든 테스트 완료. 어떤 방법이 화면에 나타나나요?");
}

// 전역 함수 등록
window.testRealInput = testRealInput;
window.testAllInputMethods = testAllInputMethods;
window.foundInputs = foundInputs;
window.bestInput = bestInput;

console.log("\n💡 사용법:");
console.log("1. testRealInput('내 테스트 메시지')     - 정교한 입력 테스트");
console.log("2. testAllInputMethods()               - 모든 입력 방식 테스트");
console.log("3. foundInputs                         - 발견된 모든 입력창 정보");

if (bestInput) {
    console.log("\n🎯 지금 바로 테스트해보세요:");
    console.log("testRealInput('ChatGPT 입력 테스트 - 이 메시지가 보이나요?')");
} else {
    console.log("\n❌ 사용 가능한 입력창이 없습니다!");
    console.log("페이지를 새로고침하거나 ChatGPT 대화 페이지로 이동해보세요.");
}