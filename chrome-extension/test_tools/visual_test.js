const puppeteer = require('puppeteer');

async function visualTest() {
    console.log('Starting Visual Browser Test...\n');
    
    const browser = await puppeteer.launch({
        headless: false,  // Show the browser
        defaultViewport: null,
        args: [
            '--start-maximized',
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ]
    });
    
    const page = await browser.newPage();
    
    // Test configuration
    const tests = [
        {
            name: 'Gemini',
            url: 'https://gemini.google.com',
            wait: 5000,
            selectors: {
                input: [
                    'div.ql-editor',
                    'div[contenteditable="true"].ql-editor',
                    'rich-textarea textarea',
                    'textarea[aria-label*="Enter a prompt"]'
                ],
                button: [
                    'button[aria-label*="Send"]',
                    'button[mattooltip*="Send"]',
                    'button[jsaction*="send"]'
                ]
            }
        },
        {
            name: 'Perplexity',
            url: 'https://www.perplexity.ai',
            wait: 5000,
            selectors: {
                input: [
                    'textarea',
                    'textarea[placeholder*="Ask"]',
                    'textarea.SearchBar-input',
                    'input[type="text"]'
                ],
                button: [
                    'button[type="submit"]',
                    'button[aria-label*="Submit"]',
                    'button.SearchBar-sendButton'
                ]
            }
        }
    ];
    
    for (const test of tests) {
        console.log(`\n========== Testing ${test.name} ==========`);
        console.log(`Opening: ${test.url}`);
        console.log('Please login if needed and navigate to the chat interface.');
        console.log(`Waiting ${test.wait/1000} seconds for you to login...\n`);
        
        await page.goto(test.url);
        
        // Wait for user to login
        await new Promise(r => setTimeout(r, test.wait));
        
        // Now test selectors
        console.log('Testing selectors...');
        
        // Find any input elements
        const foundInputs = await page.evaluate(() => {
            const inputs = [];
            
            // Find all textareas
            document.querySelectorAll('textarea').forEach(el => {
                inputs.push({
                    type: 'textarea',
                    class: el.className,
                    id: el.id,
                    placeholder: el.placeholder,
                    ariaLabel: el.getAttribute('aria-label'),
                    visible: el.offsetParent !== null
                });
            });
            
            // Find all contenteditable
            document.querySelectorAll('[contenteditable="true"]').forEach(el => {
                inputs.push({
                    type: 'contenteditable',
                    tagName: el.tagName,
                    class: el.className,
                    id: el.id,
                    role: el.getAttribute('role'),
                    visible: el.offsetParent !== null
                });
            });
            
            // Find all input[type="text"]
            document.querySelectorAll('input[type="text"]').forEach(el => {
                inputs.push({
                    type: 'input-text',
                    class: el.className,
                    id: el.id,
                    placeholder: el.placeholder,
                    visible: el.offsetParent !== null
                });
            });
            
            return inputs;
        });
        
        console.log('Found Input Elements:', JSON.stringify(foundInputs, null, 2));
        
        // Find buttons
        const foundButtons = await page.evaluate(() => {
            const buttons = [];
            document.querySelectorAll('button').forEach((el, idx) => {
                if (idx < 10) {  // First 10 buttons
                    buttons.push({
                        text: el.textContent.trim().substring(0, 30),
                        class: el.className,
                        ariaLabel: el.getAttribute('aria-label'),
                        type: el.type,
                        dataTestId: el.getAttribute('data-testid'),
                        visible: el.offsetParent !== null
                    });
                }
            });
            return buttons;
        });
        
        console.log('\nFound Buttons:', JSON.stringify(foundButtons, null, 2));
        
        // Test specific selectors
        console.log('\nTesting specific selectors:');
        for (const selector of test.selectors.input) {
            const found = await page.$(selector);
            console.log(`  Input "${selector}": ${found ? 'FOUND' : 'NOT FOUND'}`);
        }
        
        for (const selector of test.selectors.button) {
            const found = await page.$(selector);
            console.log(`  Button "${selector}": ${found ? 'FOUND' : 'NOT FOUND'}`);
        }
        
        // Take screenshot
        const screenshotName = `${test.name.toLowerCase()}_visual.png`;
        await page.screenshot({ path: screenshotName });
        console.log(`\nScreenshot saved: ${screenshotName}`);
    }
    
    console.log('\n========================================');
    console.log('Test Complete! Check the screenshots.');
    console.log('Browser will remain open. Close it manually when done.');
    console.log('========================================');
}

visualTest().catch(console.error);