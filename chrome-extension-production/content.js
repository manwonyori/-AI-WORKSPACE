/**
 * ULTIMATE Content Script v3.0
 * 완벽한 작동을 보장하는 최종 버전
 */

console.log('🚀 ULTIMATE AI Auto-Relay Content Script Starting...');

// ==================== GLOBAL STATE ====================
const STATE = {
    platform: null,
    initialized: false,
    lastMessage: '',
    lastResponse: '',
    isProcessing: false,
    retryCount: 0,
    maxRetries: 3,
    elements: {
        input: null,
        button: null,
        stopButton: null
    }
};

// ==================== PLATFORM CONFIGURATIONS ====================
const PLATFORMS = {
    chatgpt: {
        name: 'ChatGPT',
        hostname: ['chatgpt.com', 'chat.openai.com'],
        selectors: {
            input: [
                '#prompt-textarea',
                'textarea#prompt-textarea',
                'div#prompt-textarea[contenteditable="true"]',
                'textarea[data-id="root"]',
                'div.ProseMirror[contenteditable="true"]',
                'div[contenteditable="true"][role="textbox"]'
            ],
            button: [
                'button[data-testid="send-button"]',
                'button[aria-label*="Send message"]',
                'button[aria-label*="Send"]',
                'form button[type="submit"]:not([disabled])',
                'button:has(svg.icon-2xl)',
                'button.absolute.p-1.rounded-md'
            ],
            stop: [
                'button[aria-label*="Stop generating"]',
                'button[aria-label*="Stop"]',
                'button:has(svg rect[width="10"])',
                'button.btn-neutral'
            ],
            response: [
                'div[data-message-author-role="assistant"]',
                '.markdown.prose',
                '.text-base .items-start'
            ]
        },
        inputMethod: 'react',
        needsUnlock: true
    },
    
    claude: {
        name: 'Claude',
        hostname: ['claude.ai'],
        selectors: {
            input: [
                'div.ProseMirror[contenteditable="true"]',
                'div[contenteditable="true"][data-placeholder]',
                'div[contenteditable="true"].text-input',
                'div[role="textbox"][contenteditable="true"]'
            ],
            button: [
                'button[aria-label="Send Message"]',
                'button[aria-label*="Send"]',
                'button.send-button',
                'button[type="submit"]:not([disabled])'
            ],
            stop: [
                'button[aria-label*="Stop"]',
                'button.stop-button'
            ],
            response: [
                'div.font-claude-message',
                'div[data-is-streaming]',
                '.assistant-message'
            ]
        },
        inputMethod: 'contenteditable',
        needsUnlock: false
    },
    
    gemini: {
        name: 'Gemini',
        hostname: ['gemini.google.com', 'aistudio.google.com', 'makersuite.google.com'],
        selectors: {
            input: [
                'div.ql-editor[contenteditable="true"]',
                'div.ql-editor',
                'rich-textarea textarea',
                'textarea[aria-label*="Enter a prompt"]',
                'textarea[placeholder*="Enter a prompt"]',
                'div[contenteditable="true"][role="textbox"]'
            ],
            button: [
                'button[aria-label="Send message"]',
                'button[aria-label*="Send"]',
                'button[aria-label*="Run"]',
                'button:has(mat-icon[fonticon="send"])',
                'button.send-button',
                'button[mattooltip*="Send"]'
            ],
            stop: [
                'button[aria-label*="Stop"]',
                'button:has(mat-icon[fonticon="stop"])'
            ],
            response: [
                'message-content.model-response',
                '.model-response-text',
                '.message-content',
                'model-response'
            ]
        },
        inputMethod: 'quill',
        needsUnlock: false
    },
    
    perplexity: {
        name: 'Perplexity',
        hostname: ['perplexity.ai', 'www.perplexity.ai'],
        selectors: {
            input: [
                'textarea[placeholder*="Ask"]',
                'textarea[placeholder*="follow"]',
                'textarea.max-h-52',
                'textarea',
                'div[contenteditable="true"]'
            ],
            button: [
                'button[aria-label="Submit"]',
                'button[aria-label*="Send"]',
                'button.bg-super',
                'button[type="submit"]',
                'button:has(svg path[d*="m21"])'
            ],
            stop: [
                'button[aria-label*="Stop"]'
            ],
            response: [
                '.prose',
                '.answer',
                '.response-content',
                '.markdown'
            ]
        },
        inputMethod: 'standard',
        needsUnlock: false
    }
};

// ==================== PLATFORM DETECTION ====================
function detectPlatform() {
    const hostname = location.hostname.toLowerCase();
    
    for (const [key, config] of Object.entries(PLATFORMS)) {
        if (config.hostname.some(h => hostname.includes(h))) {
            console.log(`✅ Platform detected: ${config.name}`);
            return key;
        }
    }
    
    console.warn('⚠️ Unknown platform:', hostname);
    return null;
}

// ==================== ELEMENT FINDING ====================
function findElement(selectors, retryCount = 0) {
    if (!selectors || !Array.isArray(selectors)) return null;
    
    for (const selector of selectors) {
        try {
            const elements = document.querySelectorAll(selector);
            
            for (const element of elements) {
                const rect = element.getBoundingClientRect();
                const isVisible = rect.width > 0 && rect.height > 0;
                const isInViewport = rect.top < window.innerHeight && rect.bottom > 0;
                
                if (isVisible && isInViewport) {
                    // Additional visibility check
                    const style = window.getComputedStyle(element);
                    if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                        console.log(`✅ Found element: ${selector}`);
                        return element;
                    }
                }
            }
        } catch (e) {
            // Selector error, continue
        }
    }
    
    if (retryCount < 3) {
        console.log(`⏳ Retrying element search... (${retryCount + 1}/3)`);
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(findElement(selectors, retryCount + 1));
            }, 1000);
        });
    }
    
    return null;
}

// ==================== INPUT UNLOCK (ChatGPT) ====================
function unlockInputs() {
    if (STATE.platform !== 'chatgpt') return;
    
    console.log('🔓 Unlocking ChatGPT inputs...');
    
    const elements = document.querySelectorAll('textarea, div[contenteditable], input');
    let unlocked = 0;
    
    elements.forEach(el => {
        // Remove all restrictions
        el.readOnly = false;
        el.disabled = false;
        el.removeAttribute('readonly');
        el.removeAttribute('disabled');
        el.removeAttribute('aria-disabled');
        el.removeAttribute('data-disabled');
        
        // Force contenteditable
        if (el.hasAttribute('contenteditable')) {
            el.contentEditable = 'true';
        }
        
        // Remove pointer-events restrictions
        el.style.pointerEvents = 'auto';
        el.style.userSelect = 'text';
        el.style.cursor = 'text';
        
        // Remove any disabled classes
        el.classList.remove('disabled', 'readonly', 'locked');
        
        unlocked++;
    });
    
    console.log(`✅ Unlocked ${unlocked} elements`);
}

// ==================== INPUT METHODS ====================
async function setInputText(text) {
    const config = PLATFORMS[STATE.platform];
    if (!config) return false;
    
    // Unlock if needed
    if (config.needsUnlock) {
        unlockInputs();
        await wait(300);
    }
    
    // Find input element
    const input = await findElement(config.selectors.input);
    if (!input) {
        console.error('❌ Input element not found');
        return false;
    }
    
    STATE.elements.input = input;
    
    try {
        input.focus();
        input.click();
        
        // Clear existing content
        if (input.tagName === 'TEXTAREA' || input.tagName === 'INPUT') {
            input.value = '';
        } else {
            input.innerHTML = '';
            input.textContent = '';
        }
        
        await wait(100);
        
        // Set new content based on input method
        switch (config.inputMethod) {
            case 'react':
                await setReactInput(input, text);
                break;
            case 'quill':
                await setQuillInput(input, text);
                break;
            case 'contenteditable':
                await setContentEditableInput(input, text);
                break;
            default:
                await setStandardInput(input, text);
        }
        
        // Trigger events to ensure UI updates
        await triggerInputEvents(input);
        
        console.log('✅ Input text set successfully');
        STATE.lastMessage = text;
        return true;
        
    } catch (error) {
        console.error('❌ Input error:', error);
        return false;
    }
}

async function setReactInput(input, text) {
    if (input.tagName === 'TEXTAREA' || input.tagName === 'INPUT') {
        // React-compatible setter
        const nativeSetter = Object.getOwnPropertyDescriptor(
            input.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype,
            'value'
        )?.set;
        
        if (nativeSetter) {
            nativeSetter.call(input, text);
        } else {
            input.value = text;
        }
    } else {
        // ProseMirror or contenteditable
        input.innerHTML = `<p>${text}</p>`;
    }
}

async function setQuillInput(input, text) {
    // Quill editor specific
    input.innerHTML = `<p>${text}</p>`;
    
    // Try to access Quill instance
    if (input.__quill) {
        input.__quill.setText(text);
    }
}

async function setContentEditableInput(input, text) {
    input.textContent = text;
    
    // Set cursor to end
    const range = document.createRange();
    const sel = window.getSelection();
    range.selectNodeContents(input);
    range.collapse(false);
    sel.removeAllRanges();
    sel.addRange(range);
}

async function setStandardInput(input, text) {
    if (input.tagName === 'TEXTAREA' || input.tagName === 'INPUT') {
        input.value = text;
    } else {
        input.textContent = text;
    }
}

async function triggerInputEvents(input) {
    const events = [
        new Event('input', { bubbles: true, cancelable: true }),
        new Event('change', { bubbles: true }),
        new InputEvent('input', { bubbles: true, inputType: 'insertText', data: STATE.lastMessage }),
        new Event('blur', { bubbles: true }),
        new Event('focus', { bubbles: true }),
        new CompositionEvent('compositionend', { bubbles: true }),
        new KeyboardEvent('keydown', { bubbles: true, key: 'Enter', code: 'Enter' }),
        new KeyboardEvent('keyup', { bubbles: true, key: 'Enter', code: 'Enter' })
    ];
    
    for (const event of events) {
        input.dispatchEvent(event);
        await wait(50);
    }
}

// ==================== BUTTON OPERATIONS ====================
async function clickSendButton() {
    const config = PLATFORMS[STATE.platform];
    if (!config) return false;
    
    // Wait for button to be enabled
    await wait(1000);
    
    // Find send button
    const button = await findElement(config.selectors.button);
    if (!button) {
        console.error('❌ Send button not found');
        return false;
    }
    
    STATE.elements.button = button;
    
    // Wait if button is disabled
    let waitCount = 0;
    while (button.disabled && waitCount < 10) {
        console.log('⏳ Waiting for button to enable...');
        await wait(500);
        waitCount++;
    }
    
    try {
        // Multiple click methods for reliability
        button.click();
        button.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        button.dispatchEvent(new Event('click', { bubbles: true }));
        
        console.log('✅ Send button clicked');
        STATE.isProcessing = true;
        return true;
    } catch (error) {
        console.error('❌ Click error:', error);
        return false;
    }
}

async function clickStopButton() {
    const config = PLATFORMS[STATE.platform];
    if (!config) return false;
    
    const button = await findElement(config.selectors.stop);
    if (!button) return false;
    
    try {
        button.click();
        console.log('⏹️ Stop button clicked');
        STATE.isProcessing = false;
        return true;
    } catch (error) {
        return false;
    }
}

// ==================== RESPONSE HANDLING ====================
function getLastResponse() {
    const config = PLATFORMS[STATE.platform];
    if (!config) return '';
    
    for (const selector of config.selectors.response) {
        try {
            const elements = document.querySelectorAll(selector);
            if (elements.length > 0) {
                const lastElement = elements[elements.length - 1];
                const text = lastElement.textContent || lastElement.innerText || '';
                if (text && text.length > 0) {
                    return text.trim();
                }
            }
        } catch (e) {
            // Continue to next selector
        }
    }
    
    return '';
}

function watchForResponse(callback) {
    console.log('👁️ Watching for response...');
    
    let lastLength = 0;
    let stableCount = 0;
    let checkCount = 0;
    
    const interval = setInterval(() => {
        const response = getLastResponse();
        const currentLength = response.length;
        
        checkCount++;
        
        // Check if response is stable
        if (currentLength > 50 && currentLength === lastLength) {
            stableCount++;
            
            if (stableCount >= 3) {
                clearInterval(interval);
                STATE.lastResponse = response;
                STATE.isProcessing = false;
                console.log('✅ Response complete');
                if (callback) callback(response);
            }
        } else {
            stableCount = 0;
            lastLength = currentLength;
        }
        
        // Timeout after 30 checks (60 seconds)
        if (checkCount >= 30) {
            clearInterval(interval);
            STATE.isProcessing = false;
            console.log('⏱️ Response watch timeout');
            if (callback && currentLength > 50) callback(response);
        }
    }, 2000);
}

// ==================== UTILITY FUNCTIONS ====================
function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ==================== INITIALIZATION ====================
async function initialize() {
    console.log('🎯 Initializing Ultimate Content Script...');
    
    // Detect platform
    STATE.platform = detectPlatform();
    
    if (!STATE.platform) {
        console.error('❌ Platform not supported');
        return false;
    }
    
    // Platform-specific initialization
    if (STATE.platform === 'chatgpt') {
        // Wait for React to load
        await wait(2000);
        unlockInputs();
    }
    
    STATE.initialized = true;
    console.log(`✅ Initialized for ${PLATFORMS[STATE.platform].name}`);
    
    // Notify background
    chrome.runtime.sendMessage({
        action: 'CONTENT_READY',
        platform: STATE.platform,
        url: location.href
    });
    
    return true;
}

// ==================== MESSAGE HANDLER ====================
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 Message received:', request.action);
    
    // Async handler
    (async () => {
        // Initialize if needed
        if (!STATE.initialized) {
            await initialize();
        }
        
        let result = { success: false, platform: STATE.platform };
        
        try {
            switch (request.action) {
                case 'CHECK_STATUS':
                    result = {
                        success: true,
                        platform: STATE.platform,
                        initialized: STATE.initialized,
                        processing: STATE.isProcessing,
                        elements: {
                            input: !!STATE.elements.input,
                            button: !!STATE.elements.button
                        }
                    };
                    break;
                    
                case 'INPUT':
                    result.success = await setInputText(request.text || request.message);
                    break;
                    
                case 'SEND':
                    result.success = await clickSendButton();
                    break;
                    
                case 'INPUT_AND_SEND':
                    const inputOk = await setInputText(request.text || request.message);
                    if (inputOk) {
                        await wait(1000);
                        const sendOk = await clickSendButton();
                        result.success = inputOk && sendOk;
                    }
                    break;
                    
                case 'STOP':
                    result.success = await clickStopButton();
                    break;
                    
                case 'GET_RESPONSE':
                    result.response = getLastResponse();
                    result.success = true;
                    break;
                    
                case 'AUTO_RELAY':
                    console.log('🔄 Auto relay message');
                    
                    // Stop any current processing
                    await clickStopButton();
                    await wait(1000);
                    
                    // Input and send
                    const relayInput = await setInputText(request.message);
                    if (relayInput) {
                        await wait(1500);
                        const relaySend = await clickSendButton();
                        
                        if (relaySend) {
                            // Watch for response
                            watchForResponse((response) => {
                                chrome.runtime.sendMessage({
                                    action: 'RELAY_RESPONSE',
                                    platform: STATE.platform,
                                    response: response,
                                    timestamp: Date.now()
                                });
                            });
                            
                            result.success = true;
                            result.status = 'processing';
                        }
                    }
                    break;
                    
                case 'REINITIALIZE':
                    STATE.initialized = false;
                    result.success = await initialize();
                    break;
                    
                default:
                    result.error = 'Unknown action';
            }
        } catch (error) {
            console.error('❌ Handler error:', error);
            result.error = error.message;
        }
        
        sendResponse(result);
    })();
    
    // Return true for async response
    return true;
});

// ==================== AUTO-INITIALIZATION ====================
(async function() {
    // Wait for page load
    if (document.readyState === 'loading') {
        await new Promise(resolve => {
            document.addEventListener('DOMContentLoaded', resolve);
        });
    }
    
    // Additional wait for SPA frameworks
    await wait(1500);
    
    // Initialize
    await initialize();
    
    // Monitor for page changes (SPA navigation)
    let lastUrl = location.href;
    setInterval(() => {
        if (location.href !== lastUrl) {
            console.log('📍 Page changed, reinitializing...');
            lastUrl = location.href;
            STATE.initialized = false;
            initialize();
        }
    }, 1000);
})();

console.log('✅ Ultimate Content Script Loaded');