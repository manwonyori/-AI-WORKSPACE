const puppeteer = require('puppeteer');

async function testPlatform(platformName, url, selectors) {
    console.log(`\n========== Testing ${platformName} ==========`);
    console.log(`URL: ${url}`);
    
    try {
        const browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        const page = await browser.newPage();
        
        // Set viewport
        await page.setViewport({ width: 1280, height: 800 });
        
        // Navigate to the page
        console.log('Navigating to page...');
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
        
        // Wait a bit for dynamic content
        await new Promise(r => setTimeout(r, 3000));
        
        // Test input selectors
        console.log('\nTesting INPUT selectors:');
        let inputFound = null;
        for (const selector of selectors.input) {
            try {
                const element = await page.$(selector);
                if (element) {
                    console.log(`  [OK] Found: ${selector}`);
                    
                    // Get element details
                    const details = await page.evaluate(el => {
                        return {
                            tagName: el.tagName.toLowerCase(),
                            className: el.className,
                            id: el.id,
                            placeholder: el.placeholder || el.getAttribute('placeholder'),
                            ariaLabel: el.getAttribute('aria-label'),
                            dataTestId: el.getAttribute('data-testid'),
                            contentEditable: el.contentEditable
                        };
                    }, element);
                    
                    console.log('    Details:', JSON.stringify(details));
                    inputFound = selector;
                    break;
                }
            } catch (e) {
                console.log(`  [FAIL] ${selector} - ${e.message}`);
            }
        }
        
        if (!inputFound) {
            console.log('  [WARNING] No input element found!');
            
            // Try to find ANY input-like element
            console.log('\n  Searching for any textarea or contenteditable...');
            const anyTextarea = await page.$$eval('textarea', els => 
                els.map(el => ({
                    class: el.className,
                    id: el.id,
                    placeholder: el.placeholder,
                    visible: el.offsetParent !== null
                }))
            );
            console.log('  Textareas found:', anyTextarea);
            
            const anyContentEditable = await page.$$eval('[contenteditable="true"]', els => 
                els.map(el => ({
                    tagName: el.tagName,
                    class: el.className,
                    id: el.id,
                    visible: el.offsetParent !== null
                }))
            );
            console.log('  ContentEditables found:', anyContentEditable);
        }
        
        // Test button selectors
        console.log('\nTesting BUTTON selectors:');
        let buttonFound = null;
        for (const selector of selectors.button) {
            try {
                const element = await page.$(selector);
                if (element) {
                    console.log(`  [OK] Found: ${selector}`);
                    buttonFound = selector;
                    break;
                }
            } catch (e) {
                console.log(`  [FAIL] ${selector}`);
            }
        }
        
        if (!buttonFound) {
            console.log('  [WARNING] No button element found!');
            
            // Try to find ANY button
            console.log('\n  Searching for any button...');
            const anyButton = await page.$$eval('button', els => 
                els.slice(0, 5).map(el => ({
                    text: el.textContent.trim().substring(0, 20),
                    ariaLabel: el.getAttribute('aria-label'),
                    type: el.type,
                    visible: el.offsetParent !== null
                }))
            );
            console.log('  Buttons found:', anyButton);
        }
        
        // Take screenshot
        const screenshotPath = `${platformName.toLowerCase()}_test.png`;
        await page.screenshot({ path: screenshotPath });
        console.log(`\n[SCREENSHOT] Saved: ${screenshotPath}`);
        
        await browser.close();
        
        return { inputFound, buttonFound };
        
    } catch (error) {
        console.error(`[ERROR] Failed to test ${platformName}: ${error.message}`);
        return { error: error.message };
    }
}

// Platform configurations
const platforms = {
    chatgpt: {
        url: 'https://chatgpt.com',
        selectors: {
            input: [
                'div[contenteditable="true"][data-id="root"]',
                'div[contenteditable="true"][data-placeholder*="Message"]',
                'div[contenteditable="true"][aria-label*="Message"]',
                'div.m-0.w-full.resize-none[contenteditable="true"]',
                'textarea[data-id="root"]',
                'textarea.m-0.w-full.resize-none'
            ],
            button: [
                'button[data-testid="send-button"]',
                'button[aria-label*="Send"]',
                'button[type="submit"]'
            ]
        }
    },
    claude: {
        url: 'https://claude.ai',
        selectors: {
            input: [
                'div[contenteditable="true"].ProseMirror',
                'div[contenteditable="true"][data-placeholder]',
                'div[role="textbox"][contenteditable="true"]',
                'div[contenteditable="true"]'
            ],
            button: [
                'button[aria-label="Send Message"]',
                'button[data-testid="send-button"]',
                'button[aria-label*="Send"]'
            ]
        }
    },
    perplexity: {
        url: 'https://www.perplexity.ai',
        selectors: {
            input: [
                'textarea.SearchBar-input[data-testid="search-bar-input"]',
                'textarea.SearchBar-input',
                'textarea[data-testid="search-bar-input"]',
                'textarea[aria-label*="Ask anything"]',
                'textarea[placeholder*="Ask"]',
                'textarea'
            ],
            button: [
                'button.SearchBar-sendButton[data-testid="send-btn"]',
                'button.SearchBar-sendButton',
                'button[data-testid="send-btn"]',
                'button[aria-label*="Send"]'
            ]
        }
    },
    gemini: {
        url: 'https://gemini.google.com',
        selectors: {
            input: [
                'rich-textarea textarea',
                'textarea[aria-label*="Enter a prompt"]',
                'textarea[aria-label*="Type something"]',
                'textarea[data-test-id="text-input"]',
                'textarea.ql-editor',
                'textarea'
            ],
            button: [
                'button[aria-label*="Send"]',
                'button[aria-label*="Run"]',
                'button[data-test-id="send-button"]',
                'button[mattooltip*="Send"]'
            ]
        }
    }
};

// Main execution
(async () => {
    console.log('AI Platform Selector Test - Direct Execution');
    console.log('=' * 50);
    
    const results = {};
    
    // Test each platform
    for (const [name, config] of Object.entries(platforms)) {
        const result = await testPlatform(name.toUpperCase(), config.url, config.selectors);
        results[name] = result;
        console.log('\n' + '=' * 50);
    }
    
    // Summary
    console.log('\n\n========== SUMMARY ==========');
    for (const [name, result] of Object.entries(results)) {
        if (result.error) {
            console.log(`${name.toUpperCase()}: ERROR - ${result.error}`);
        } else {
            const inputStatus = result.inputFound ? 'OK' : 'FAIL';
            const buttonStatus = result.buttonFound ? 'OK' : 'FAIL';
            console.log(`${name.toUpperCase()}: Input=${inputStatus}, Button=${buttonStatus}`);
        }
    }
})();