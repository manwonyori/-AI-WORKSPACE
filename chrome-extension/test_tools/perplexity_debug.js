// Perplexity 전용 디버그 스크립트
// perplexity.ai에서 F12 콘솔에 실행

console.clear();
console.log('=== PERPLEXITY DEBUG ===');
console.log('URL:', location.href);
console.log('Logged in as: 8899you@gmail.com');

// 모든 textarea 찾기
console.log('\n--- All Textareas ---');
const textareas = document.querySelectorAll('textarea');
console.log(`Found ${textareas.length} textareas:`);

textareas.forEach((ta, idx) => {
    console.log(`\nTextarea[${idx}]:`);
    console.log('  Tag:', ta.tagName);
    console.log('  Class:', ta.className);
    console.log('  ID:', ta.id);
    console.log('  Placeholder:', ta.placeholder);
    console.log('  Aria-label:', ta.getAttribute('aria-label'));
    console.log('  Data-testid:', ta.getAttribute('data-testid'));
    console.log('  Visible:', ta.offsetParent !== null);
    console.log('  Parent classes:', ta.parentElement?.className);
    console.log('  Grandparent classes:', ta.parentElement?.parentElement?.className);
    
    // 하이라이트
    ta.style.border = `3px solid ${idx === 0 ? 'lime' : 'red'}`;
    ta.style.borderRadius = '8px';
});

// 모든 입력 관련 요소 찾기
console.log('\n--- All Input Elements ---');
const inputs = document.querySelectorAll('input[type="text"], input[type="search"], [contenteditable="true"]');
console.log(`Found ${inputs.length} input elements:`);

inputs.forEach((input, idx) => {
    if (idx < 5) {
        console.log(`\nInput[${idx}]:`);
        console.log('  Type:', input.type || 'contenteditable');
        console.log('  Class:', input.className);
        console.log('  Placeholder:', input.placeholder);
        console.log('  ContentEditable:', input.contentEditable);
    }
});

// 버튼 찾기
console.log('\n--- Send/Submit Buttons ---');
const buttons = document.querySelectorAll('button');
console.log(`Found ${buttons.length} buttons`);

// 전송 관련 버튼만
const sendButtons = Array.from(buttons).filter(btn => {
    const text = btn.textContent.toLowerCase();
    const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
    const testId = btn.getAttribute('data-testid') || '';
    
    return text.includes('send') || 
           text.includes('submit') || 
           text.includes('ask') ||
           ariaLabel.includes('send') || 
           ariaLabel.includes('submit') ||
           testId.includes('send') ||
           testId.includes('submit') ||
           btn.type === 'submit';
});

console.log(`\nFound ${sendButtons.length} send buttons:`);
sendButtons.forEach((btn, idx) => {
    console.log(`\nButton[${idx}]:`);
    console.log('  Text:', btn.textContent.trim());
    console.log('  Class:', btn.className);
    console.log('  Type:', btn.type);
    console.log('  Aria-label:', btn.getAttribute('aria-label'));
    console.log('  Data-testid:', btn.getAttribute('data-testid'));
    console.log('  Visible:', btn.offsetParent !== null);
    
    btn.style.border = '3px solid blue';
});

// 마이크 버튼 찾기
console.log('\n--- Microphone Button ---');
const micButtons = Array.from(buttons).filter(btn => {
    const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
    return ariaLabel.includes('mic') || 
           ariaLabel.includes('voice') || 
           btn.innerHTML.includes('mic') ||
           btn.innerHTML.includes('Mic');
});

if (micButtons.length > 0) {
    console.log('⚠️ MICROPHONE BUTTON FOUND - This might be interfering!');
    micButtons.forEach(mic => {
        console.log('  Mic button:', mic);
        console.log('  Aria-label:', mic.getAttribute('aria-label'));
        mic.style.border = '3px solid orange';
    });
}

// 실제 작동 테스트
console.log('\n--- FUNCTIONAL TEST ---');
const mainTextarea = textareas[0];
if (mainTextarea) {
    console.log('Testing main textarea...');
    
    // Focus
    mainTextarea.focus();
    console.log('✓ Focused');
    
    // Try to set value
    const testText = 'Test from debug script';
    
    // Method 1: Direct value
    mainTextarea.value = testText;
    console.log('Method 1 (direct value):', mainTextarea.value === testText ? '✓' : '✗');
    
    // Method 2: Using setter
    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
    setter.call(mainTextarea, testText);
    mainTextarea.dispatchEvent(new Event('input', { bubbles: true }));
    console.log('Method 2 (setter + event):', mainTextarea.value === testText ? '✓' : '✗');
    
    // Clear for user
    setTimeout(() => {
        mainTextarea.value = '';
        mainTextarea.dispatchEvent(new Event('input', { bubbles: true }));
        console.log('Cleared test text');
    }, 2000);
}

console.log('\n=== SUMMARY ===');
console.log('Textareas found:', textareas.length);
console.log('Send buttons found:', sendButtons.length);
console.log('Microphone interference:', micButtons.length > 0 ? 'YES ⚠️' : 'No');

// 추천 셀렉터
if (textareas.length > 0) {
    const ta = textareas[0];
    console.log('\n📌 RECOMMENDED SELECTORS:');
    
    if (ta.className) {
        console.log(`  textarea.${ta.className.split(' ')[0]}`);
    }
    if (ta.id) {
        console.log(`  textarea#${ta.id}`);
    }
    if (ta.getAttribute('data-testid')) {
        console.log(`  textarea[data-testid="${ta.getAttribute('data-testid')}"]`);
    }
    console.log('  textarea (generic fallback)');
}

console.log('\n=== END DEBUG ===');