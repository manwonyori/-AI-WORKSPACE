// Debug script - paste this in F12 console on each platform

console.clear();
console.log('=== SELECTOR DEBUG TOOL ===');
console.log('Platform:', location.hostname);
console.log('URL:', location.href);

// ChatGPT selectors
if (location.hostname.includes('chatgpt.com')) {
    console.log('\n--- Testing ChatGPT Selectors ---');
    const chatgptSelectors = [
        'div[contenteditable="true"][data-id="root"]',
        'div[contenteditable="true"][data-placeholder*="Message"]',
        'div[contenteditable="true"][placeholder*="Message"]',
        'div[contenteditable="true"][aria-label*="Message"]',
        'div[contenteditable="true"].resize-none',
        'div.m-0.w-full.resize-none[contenteditable="true"]',
        // Additional possibilities
        'textarea#prompt-textarea',
        'textarea[data-id="root"]',
        'div#prompt-textarea',
        'textarea.m-0.w-full.resize-none'
    ];
    
    for (const selector of chatgptSelectors) {
        try {
            const el = document.querySelector(selector);
            if (el) {
                console.log(`✅ FOUND: ${selector}`);
                console.log('  Element:', el);
                console.log('  Tag:', el.tagName);
                console.log('  Classes:', el.className);
                console.log('  ID:', el.id);
                console.log('  ContentEditable:', el.contentEditable);
                console.log('  Attributes:', Array.from(el.attributes).map(a => `${a.name}="${a.value}"`).join(', '));
                el.style.outline = '3px solid lime';
                break;
            } else {
                console.log(`❌ Not found: ${selector}`);
            }
        } catch(e) {
            console.log(`⚠️ Invalid selector: ${selector}`);
        }
    }
    
    // Find ANY input-like element
    console.log('\n--- Finding ANY input elements ---');
    const textareas = document.querySelectorAll('textarea');
    console.log(`Textareas found: ${textareas.length}`);
    textareas.forEach((el, i) => {
        console.log(`  Textarea[${i}]:`, {
            id: el.id,
            class: el.className,
            placeholder: el.placeholder,
            ariaLabel: el.getAttribute('aria-label'),
            dataId: el.getAttribute('data-id')
        });
    });
    
    const contentEditables = document.querySelectorAll('[contenteditable="true"]');
    console.log(`\nContentEditables found: ${contentEditables.length}`);
    contentEditables.forEach((el, i) => {
        if (i < 5) {
            console.log(`  ContentEditable[${i}]:`, {
                tag: el.tagName,
                id: el.id,
                class: el.className,
                dataId: el.getAttribute('data-id'),
                role: el.getAttribute('role')
            });
        }
    });
}

// Perplexity selectors
if (location.hostname.includes('perplexity.ai')) {
    console.log('\n--- Testing Perplexity Selectors ---');
    const perplexitySelectors = [
        'textarea.SearchBar-input[data-testid="search-bar-input"]',
        'textarea.SearchBar-input',
        'textarea[data-testid="search-bar-input"]',
        'textarea[aria-label*="Ask anything"]',
        'textarea[placeholder*="Ask"]',
        '.PromptTextarea textarea',
        '#chat-input',
        'textarea[data-testid="chat-input"]',
        'textarea',
        'input[type="text"]'
    ];
    
    for (const selector of perplexitySelectors) {
        try {
            const el = document.querySelector(selector);
            if (el) {
                console.log(`✅ FOUND: ${selector}`);
                console.log('  Element:', el);
                console.log('  Tag:', el.tagName);
                console.log('  Classes:', el.className);
                console.log('  ID:', el.id);
                console.log('  Placeholder:', el.placeholder);
                console.log('  Attributes:', Array.from(el.attributes).map(a => `${a.name}="${a.value}"`).join(', '));
                el.style.outline = '3px solid lime';
                break;
            } else {
                console.log(`❌ Not found: ${selector}`);
            }
        } catch(e) {
            console.log(`⚠️ Invalid selector: ${selector}`);
        }
    }
    
    // Find ANY input
    console.log('\n--- Finding ANY input elements ---');
    const allTextareas = document.querySelectorAll('textarea');
    console.log(`All textareas: ${allTextareas.length}`);
    allTextareas.forEach((el, i) => {
        console.log(`  Textarea[${i}]:`, {
            class: el.className,
            id: el.id,
            placeholder: el.placeholder,
            dataTestId: el.getAttribute('data-testid')
        });
    });
    
    const allInputs = document.querySelectorAll('input[type="text"]');
    console.log(`\nText inputs: ${allInputs.length}`);
    allInputs.forEach((el, i) => {
        if (i < 5) {
            console.log(`  Input[${i}]:`, {
                class: el.className,
                id: el.id,
                placeholder: el.placeholder
            });
        }
    });
}

console.log('\n=== END DEBUG ===');
console.log('Copy this output and share for debugging!');