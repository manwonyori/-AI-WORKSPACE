/**
 * ChatGPT 실시간 진단 스크립트
 * chatgpt.com에서 F12 콘솔에 실행
 */

console.clear();
console.log('=== CHATGPT DIAGNOSTIC v1.3.0 ===');
console.log('Time:', new Date().toLocaleTimeString());
console.log('URL:', location.href);
console.log('');

// 1. Extension 상태 확인
console.log('📌 EXTENSION STATUS:');
const badge = document.querySelector('div[style*="position:fixed"][style*="background:lime"]');
if (badge) {
    console.log('✅ Green LOADED badge found');
    console.log('   Text:', badge.textContent);
} else {
    console.log('❌ No green LOADED badge found');
}
console.log('');

// 2. 모든 textarea 찾기
console.log('📝 TEXTAREA SEARCH:');
const textareas = document.querySelectorAll('textarea');
console.log(`Found ${textareas.length} textarea(s):`);

textareas.forEach((ta, index) => {
    console.log(`\nTextarea[${index}]:`);
    console.log('  ID:', ta.id || '(no id)');
    console.log('  Class:', ta.className || '(no class)');
    console.log('  Placeholder:', ta.placeholder || '(no placeholder)');
    console.log('  Data-id:', ta.getAttribute('data-id') || '(no data-id)');
    console.log('  Visible:', ta.offsetParent !== null);
    console.log('  ReadOnly:', ta.readOnly);
    console.log('  Disabled:', ta.disabled);
    
    // 하이라이트
    ta.style.border = '3px solid red';
    ta.style.outline = '2px solid yellow';
    ta.style.outlineOffset = '2px';
});

// 3. ID가 prompt-textarea인 요소 직접 확인
console.log('\n🎯 DIRECT ID CHECK:');
const promptTextarea = document.getElementById('prompt-textarea');
if (promptTextarea) {
    console.log('✅ Found element with id="prompt-textarea"');
    console.log('  Tag:', promptTextarea.tagName);
    console.log('  Type:', promptTextarea.type || 'N/A');
    promptTextarea.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
} else {
    console.log('❌ No element with id="prompt-textarea"');
}

// 4. ContentEditable 요소 확인
console.log('\n📄 CONTENTEDITABLE SEARCH:');
const editables = document.querySelectorAll('[contenteditable="true"]');
console.log(`Found ${editables.length} contenteditable element(s)`);

if (editables.length > 0 && editables.length <= 5) {
    editables.forEach((el, index) => {
        console.log(`\nContentEditable[${index}]:`);
        console.log('  Tag:', el.tagName);
        console.log('  ID:', el.id || '(no id)');
        console.log('  Class:', el.className || '(no class)');
        console.log('  Role:', el.getAttribute('role') || '(no role)');
        console.log('  Data-id:', el.getAttribute('data-id') || '(no data-id)');
        console.log('  Visible:', el.offsetParent !== null);
        
        // 하이라이트
        el.style.border = '3px solid blue';
    });
}

// 5. 입력 가능한 모든 요소 찾기
console.log('\n🔍 ALL POSSIBLE INPUT ELEMENTS:');
const possibleInputs = [
    ...document.querySelectorAll('textarea'),
    ...document.querySelectorAll('[contenteditable="true"]'),
    ...document.querySelectorAll('[role="textbox"]'),
    ...document.querySelectorAll('div#prompt-textarea')
];

const uniqueInputs = [...new Set(possibleInputs)];
console.log(`Total unique input elements: ${uniqueInputs.length}`);

// 6. Extension이 찾고 있는 셀렉터 테스트
console.log('\n🧪 TESTING EXTENSION SELECTORS:');
const extensionSelectors = [
    'textarea#prompt-textarea',
    'textarea[data-id="root"]',
    'textarea.m-0.w-full.resize-none',
    'textarea[placeholder*="Message"]',
    'textarea'
];

extensionSelectors.forEach(selector => {
    try {
        const element = document.querySelector(selector);
        if (element) {
            console.log(`✅ "${selector}" -> FOUND`);
            if (element.offsetParent === null) {
                console.log(`   ⚠️ But element is hidden!`);
            }
        } else {
            console.log(`❌ "${selector}" -> NOT FOUND`);
        }
    } catch (e) {
        console.log(`⚠️ "${selector}" -> INVALID SELECTOR`);
    }
});

// 7. 메시지 보내기 버튼 찾기
console.log('\n🔘 SEND BUTTON SEARCH:');
const buttons = document.querySelectorAll('button');
let sendButtonFound = false;

buttons.forEach(btn => {
    const ariaLabel = btn.getAttribute('aria-label');
    const testId = btn.getAttribute('data-testid');
    
    if (testId === 'send-button' || 
        (ariaLabel && ariaLabel.toLowerCase().includes('send'))) {
        if (!sendButtonFound) {
            console.log('✅ Found send button:');
            console.log('  data-testid:', testId);
            console.log('  aria-label:', ariaLabel);
            console.log('  disabled:', btn.disabled);
            console.log('  visible:', btn.offsetParent !== null);
            btn.style.border = '3px solid green';
            sendButtonFound = true;
        }
    }
});

if (!sendButtonFound) {
    console.log('❌ No send button found');
}

// 8. 추천 셀렉터
console.log('\n💡 RECOMMENDED SELECTOR:');
if (promptTextarea) {
    console.log('Use: textarea#prompt-textarea');
} else if (textareas.length > 0) {
    const visibleTextarea = Array.from(textareas).find(ta => ta.offsetParent !== null);
    if (visibleTextarea) {
        if (visibleTextarea.id) {
            console.log(`Use: textarea#${visibleTextarea.id}`);
        } else if (visibleTextarea.className) {
            console.log(`Use: textarea.${visibleTextarea.className.split(' ')[0]}`);
        } else {
            console.log('Use: textarea');
        }
    }
} else if (editables.length > 0) {
    const mainEditable = editables[0];
    if (mainEditable.id) {
        console.log(`Use: [contenteditable="true"]#${mainEditable.id}`);
    } else {
        console.log('Use: [contenteditable="true"]');
    }
}

// 9. 상태 요약
console.log('\n📊 SUMMARY:');
console.log(`- Platform detected: ${location.hostname.includes('chatgpt') ? 'YES' : 'NO'}`);
console.log(`- Textareas found: ${textareas.length}`);
console.log(`- ContentEditables found: ${editables.length}`);
console.log(`- Green badge visible: ${badge ? 'YES' : 'NO'}`);
console.log(`- Input element available: ${textareas.length > 0 || editables.length > 0 ? 'YES' : 'NO'}`);

console.log('\n=== END DIAGNOSTIC ===');
console.log('👉 빨간색 테두리 = textarea');
console.log('👉 파란색 테두리 = contenteditable');
console.log('👉 초록색 테두리 = send button');