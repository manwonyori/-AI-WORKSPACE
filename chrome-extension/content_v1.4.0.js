// Enhanced Content Script v1.3.9 with URL handling and debugging
// Complete implementation for ChatGPT arrow button and Gemini Quill.js integration

function detectPlatform() {
  const h = location.hostname;
  const pathname = location.pathname;
  const fullUrl = location.href;
  
  console.log("🔍 Platform detection:");
  console.log("  Hostname:", h);
  console.log("  Pathname:", pathname);
  console.log("  Full URL:", fullUrl);
  
  if (h.includes("chatgpt.com") || h.includes("chat.openai.com")) {
    console.log("✅ Detected ChatGPT");
    return "chatgpt";
  }
  if (h.includes("claude.ai")) {
    console.log("✅ Detected Claude");
    return "claude";
  }
  if (h.includes("perplexity.ai")) {
    console.log("✅ Detected Perplexity");
    return "perplexity";
  }
  if (h.includes("aistudio.google.com")) {
    // Handle Google AI Studio URL issues
    if (pathname.includes("/500") || pathname === "/" || pathname.includes("/app")) {
      console.log("⚠️ AI Studio problematic URL detected:", fullUrl);
      console.log("🔄 Redirecting to proper chat page in 2 seconds...");
      setTimeout(() => {
        window.location.href = "https://aistudio.google.com/prompts/new_chat";
      }, 2000);
      return "gemini"; // Still return gemini to allow initialization
    }
    
    if (pathname.includes("/prompts/")) {
      console.log("✅ Detected Google AI Studio (proper URL)");
      return "gemini";
    } else {
      console.log("⚠️ AI Studio detected but not on prompts page:", pathname);
      return "gemini";
    }
  }
  if (h.includes("gemini.google.com")) {
    console.log("✅ Detected Gemini");
    return "gemini";
  }
  
  console.log("❓ Unknown platform");
  return null;
}

const platform = detectPlatform();

// Updated selectors with dynamic button patterns
const SELECTORS = {
  chatgpt: {
    input: "textarea#prompt-textarea, div#prompt-textarea, textarea[data-id=\"root\"], div[data-id=\"root\"][contenteditable=\"true\"], textarea.m-0, textarea.w-full, textarea[placeholder*=\"Message\"], textarea[placeholder*=\"message\"], div[contenteditable=\"true\"][role=\"textbox\"], textarea, div[contenteditable=\"true\"]",
    // Added path-based selector for arrow button
    button: "button[data-testid=\"send-button\"], button path[d*=\"M8.99992 16V6.41407\"], button:has(path[d*=\"M8.99992\"]), button[aria-label*=\"Send\"], button[aria-label*=\"send\"], button svg.icon-2xl, button[type=\"submit\"]:not([disabled])",
    container: "main, #__next",
    useCtrlEnter: false,
    waitForButton: true  // Wait for button to appear after input
  },
  claude: {
    input: "div[contenteditable=\"true\"].ProseMirror, div[contenteditable=\"true\"][data-placeholder], div[contenteditable=\"true\"][aria-label*=\"Message\"], div.DraftEditor-editorContainer div[contenteditable=\"true\"], div[role=\"textbox\"][contenteditable=\"true\"], div[contenteditable=\"true\"]",
    button: "button[aria-label=\"Send Message\"], button[aria-label*=\"Send\"], button[data-testid=\"send-button\"], form button[type=\"submit\"], button.send-button",
    container: "main, .chat-container",
    useCtrlEnter: false,
    waitForButton: false
  },
  gemini: {
    input: "div.ql-editor, div[contenteditable=\"true\"].ql-editor, rich-textarea textarea, textarea[aria-label*=\"Enter a prompt\"], textarea[aria-label*=\"prompt\"], textarea[placeholder*=\"Enter a prompt\"], textarea.textarea, textarea[rows], textarea",
    // Prioritize aria-label for robustness
    button: 'button[aria-label="Send message"], button[aria-label*="Send"], button.mat-icon-button:has(mat-icon[fonticon="send"]), button:has(mat-icon[fonticon="send"]), mat-icon-button[aria-label*="Send"], button[mattooltip*="Send"]',
    container: "main, c-wiz, mat-sidenav-content, .main-content",
    useCtrlEnter: false,
    waitForButton: true,
    useAngularEvents: true  // Flag for Angular-specific event handling
  },
  perplexity: {
    input: "textarea[placeholder*=\"Ask\"], textarea, [contenteditable=\"true\"]",
    button: "button[aria-label=\"Submit\"], button.bg-super, form button[type=\"submit\"]",
    container: "main",
    useCtrlEnter: false,
    waitForButton: false
  }
};

const CHUNK_LIMIT = { 
  chatgpt: 4500, 
  claude: 4500, 
  gemini: 3200, 
  perplexity: 3800, 
  default: 3000 
};

// Platform-specific input methods with better event handling
async function inputForChatGPT(inputEl, text) {
  console.log("[ChatGPT] Input element type:", inputEl.tagName, inputEl.id, inputEl.className);
  
  if (inputEl.tagName === "TEXTAREA") {
    console.log("[ChatGPT] Using React-style setter for textarea");
    
    try {
      inputEl.focus();
      
      // Use React-compatible setter
      const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(
        window.HTMLTextAreaElement.prototype, 
        'value'
      ).set;
      
      if (nativeTextAreaValueSetter) {
        // Clear first
        nativeTextAreaValueSetter.call(inputEl, '');
        inputEl.dispatchEvent(new Event('input', { bubbles: true }));
        
        // Set new value
        nativeTextAreaValueSetter.call(inputEl, text);
        
        // Dispatch multiple events for better compatibility
        inputEl.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
        inputEl.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Also dispatch InputEvent for completeness
        inputEl.dispatchEvent(new InputEvent('input', {
          data: text,
          inputType: 'insertText',
          bubbles: true
        }));
        
        console.log("[ChatGPT] Text set successfully using React setter");
        return true;
      } else {
        // Fallback
        inputEl.value = text;
        inputEl.dispatchEvent(new Event('input', { bubbles: true }));
        return true;
      }
    } catch (e) {
      console.error("[ChatGPT] Textarea input error:", e);
      return false;
    }
  } else if (inputEl.tagName === "DIV" && (inputEl.contentEditable === "true" || inputEl.id === "prompt-textarea")) {
    console.log("[ChatGPT] Using contenteditable method for div");
    
    try {
      inputEl.focus();
      
      // Clear and set content
      inputEl.textContent = '';
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      
      inputEl.textContent = text;
      
      // Multiple event types
      inputEl.dispatchEvent(new InputEvent('input', {
        data: text,
        inputType: 'insertText',
        bubbles: true,
        composed: true
      }));
      
      inputEl.dispatchEvent(new Event('change', { bubbles: true }));
      
      console.log("[ChatGPT] Div content set successfully");
      return true;
    } catch (e) {
      console.error("[ChatGPT] Div input error:", e);
      return false;
    }
  }
  
  console.warn("[ChatGPT] Unknown element type:", inputEl.tagName);
  return false;
}

async function inputForGemini(inputEl, text) {
  console.log("[Gemini] Step 1: Text input - Detected element type:", inputEl.tagName, inputEl.className);
  
  // Handle Quill Editor with finalized approach
  if (inputEl.classList && inputEl.classList.contains("ql-editor")) {
    console.log("[Gemini] Using optimized Quill editor method");
    
    try {
      // Try Quill API first if available
      const quill = inputEl.__quill;
      
      if (quill && typeof quill.setText === 'function') {
        console.log("[Gemini] ✅ Found Quill instance, using API");
        quill.setText(text);
        
        // Set cursor position to end
        const textLength = quill.getText().length;
        quill.setSelection(textLength, 0);
        
        console.log("[Gemini] Text input via Quill API complete");
      } else {
        // Primary method: Direct innerHTML manipulation (most reliable in practice)
        console.log("[Gemini] Using direct DOM manipulation (primary method)");
        
        // Clear and set content
        inputEl.innerHTML = `<p>${text}</p>`;
        console.log("[Gemini] Text set via innerHTML:", text);
      }
      
      // Critical: Dispatch events for Angular change detection
      // This sequence simulates real user interaction
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      inputEl.dispatchEvent(new Event('change', { bubbles: true })); // Angular listens to 'change'
      inputEl.dispatchEvent(new Event('blur', { bubbles: true }));   // Triggers final updates
      
      console.log("[Gemini] Event dispatch complete (input, change, blur)");
      return true;
      
    } catch (e) {
      console.error("[Gemini] Text input error:", e);
      return false;
    }
  }
  
  // Handle regular textarea
  if (inputEl.tagName === "TEXTAREA") {
    console.log("[Gemini] Using textarea method");
    
    try {
      inputEl.focus();
      inputEl.value = text;
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      inputEl.dispatchEvent(new Event('change', { bubbles: true }));
      
      console.log("[Gemini] Textarea text set successfully");
      return true;
    } catch (e) {
      console.error("[Gemini] Textarea error:", e);
      return false;
    }
  }
  
  // Handle other contenteditable
  if (inputEl.contentEditable === "true" || inputEl.isContentEditable) {
    console.log("[Gemini] Using contenteditable method");
    
    try {
      inputEl.focus();
      inputEl.textContent = text;
      inputEl.dispatchEvent(new InputEvent('input', {
        data: text,
        inputType: 'insertText',
        bubbles: true
      }));
      
      console.log("[Gemini] ContentEditable text set successfully");
      return true;
    } catch (e) {
      console.error("[Gemini] ContentEditable error:", e);
      return false;
    }
  }
  
  console.warn("[Gemini] Unknown element type");
  return false;
}

async function inputForClaude(inputEl, text) {
  console.log("[Claude] Using standard contenteditable method");
  
  try {
    inputEl.focus();
    inputEl.textContent = text;
    inputEl.dispatchEvent(new InputEvent('input', { 
      bubbles: true, 
      inputType: 'insertText', 
      data: text 
    }));
    
    console.log("[Claude] Text set successfully");
    return true;
  } catch (e) {
    console.error("[Claude] Input error:", e);
    return false;
  }
}

async function inputForPerplexity(inputEl, text) {
  console.log("[Perplexity] Detected element type:", inputEl.tagName);
  
  if (inputEl.tagName === "TEXTAREA") {
    try {
      inputEl.focus();
      inputEl.value = text;
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      
      console.log("[Perplexity] Textarea text set successfully");
      return true;
    } catch (e) {
      console.error("[Perplexity] Textarea error:", e);
      return false;
    }
  }
  
  // Handle contenteditable
  if (inputEl.contentEditable === "true" || inputEl.isContentEditable) {
    try {
      inputEl.focus();
      inputEl.textContent = text;
      inputEl.dispatchEvent(new InputEvent('input', {
        bubbles: true,
        inputType: 'insertText',
        data: text
      }));
      
      console.log("[Perplexity] ContentEditable text set successfully");
      return true;
    } catch (e) {
      console.error("[Perplexity] ContentEditable error:", e);
      return false;
    }
  }
  
  return false;
}

// Enhanced chunked insert with platform-specific methods
async function chunkedInsert(inputEl, text, limit) {
  console.log(`[${platform}] Starting chunked insert for:`, inputEl.tagName, inputEl.className);
  
  const chunks = [];
  for (let i = 0; i < text.length; i += limit) {
    chunks.push(text.slice(i, i + limit));
  }
  
  // For single chunk, use platform-specific method directly
  if (chunks.length === 1) {
    let success = false;
    
    switch(platform) {
      case "chatgpt":
        success = await inputForChatGPT(inputEl, text);
        break;
      case "gemini":
        success = await inputForGemini(inputEl, text);
        break;
      case "claude":
        success = await inputForClaude(inputEl, text);
        break;
      case "perplexity":
        success = await inputForPerplexity(inputEl, text);
        break;
      default:
        // Fallback to generic method
        if (inputEl.tagName === "TEXTAREA") {
          inputEl.value = text;
          inputEl.dispatchEvent(new Event('input', { bubbles: true }));
          success = true;
        } else if (inputEl.contentEditable === "true") {
          inputEl.textContent = text;
          inputEl.dispatchEvent(new InputEvent('input', { bubbles: true }));
          success = true;
        }
    }
    
    return success;
  }
  
  // For multiple chunks, handle accordingly
  console.log(`[${platform}] Processing ${chunks.length} chunks`);
  
  // Clear first
  if (inputEl.tagName === "TEXTAREA") {
    if (platform === "chatgpt") {
      const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
      if (setter) setter.call(inputEl, '');
    } else {
      inputEl.value = '';
    }
  } else if (inputEl.contentEditable === "true" || inputEl.id === "prompt-textarea") {
    inputEl.textContent = '';
  }
  
  for (let i = 0; i < chunks.length; i++) {
    const part = chunks[i];
    console.log(`[${platform}] Inserting chunk ${i+1}/${chunks.length}: ${part.substring(0, 50)}...`);
    
    // Append chunk based on platform
    if (platform === "chatgpt") {
      if (inputEl.tagName === "TEXTAREA") {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        if (setter) {
          setter.call(inputEl, inputEl.value + part);
          inputEl.dispatchEvent(new Event('input', { bubbles: true }));
        }
      } else if (inputEl.tagName === "DIV") {
        inputEl.textContent += part;
        inputEl.dispatchEvent(new InputEvent('input', { bubbles: true }));
      }
    } else if (platform === "gemini" && inputEl.classList.contains("ql-editor")) {
      inputEl.innerHTML += `<p>${part}</p>`;
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (inputEl.tagName === "TEXTAREA") {
      inputEl.value += part;
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (inputEl.contentEditable === "true") {
      inputEl.textContent += part;
      inputEl.dispatchEvent(new InputEvent('input', { bubbles: true }));
    }
    
    await new Promise(r => setTimeout(r, 200));
  }
  
  console.log(`[${platform}] Chunked insert completed`);
  return true;
}

async function autoInput(text) {
  const sel = SELECTORS[platform];
  if (!sel) return false;
  
  // Try each selector until we find a valid input element
  let input = null;
  const selectors = sel.input.split(',');
  
  console.log(`[${platform}] Trying ${selectors.length} selectors...`);
  
  for (const selector of selectors) {
    try {
      const trimmedSelector = selector.trim();
      const element = document.querySelector(trimmedSelector);
      
      if (element) {
        // Verify it's visible and interactable
        const isVisible = element.offsetParent !== null || 
                         element.offsetHeight > 0 || 
                         element.offsetWidth > 0 ||
                         window.getComputedStyle(element).display !== 'none';
                         
        if (isVisible) {
          input = element;
          console.log(`[${platform}] Found input element with selector:`, trimmedSelector);
          console.log(`[${platform}] Element details:`, {
            tag: element.tagName,
            id: element.id,
            className: element.className,
            visible: isVisible
          });
          break;
        } else {
          console.log(`[${platform}] Element found but not visible:`, trimmedSelector);
        }
      }
    } catch (e) {
      // Skip invalid selectors
      continue;
    }
  }
  
  if (!input) {
    console.warn(`[${platform}] No input element found after trying all selectors`);
    return false;
  }
  
  const limit = CHUNK_LIMIT[platform] || CHUNK_LIMIT.default;
  return await chunkedInsert(input, text, limit);
}

// Utility functions
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function waitFor(fn, {timeout=8000, interval=80} = {}) {
  const start = performance.now();
  while (performance.now() - start < timeout) {
    const el = fn();
    if (el) return el;
    await sleep(interval);
  }
  throw new Error('Timeout waiting for element');
}

function clickWithPointer(el) {
  const opts = { bubbles: true, cancelable: true, composed: true };
  el.dispatchEvent(new PointerEvent('pointerdown', opts));
  el.dispatchEvent(new MouseEvent('mousedown', opts));
  el.dispatchEvent(new PointerEvent('pointerup', opts));
  el.dispatchEvent(new MouseEvent('mouseup', opts));
  el.dispatchEvent(new MouseEvent('click', opts));
}

// Enhanced wait for dynamic button with MutationObserver
async function waitForButton(maxWait = 5000) {  // Increased to 5s for Gemini
  const sel = SELECTORS[platform];
  if (!sel || !sel.waitForButton) return null;
  
  if (platform === 'gemini') {
    console.log(`[Gemini] Step 2: Waiting for send button activation...`);
    maxWait = 10000;  // Give Gemini more time (10s)
  } else {
    console.log(`[${platform}] Waiting for send button to appear...`);
  }
  
  return new Promise((resolve, reject) => {
    let resolved = false;
    const startTime = Date.now();
    
    // Function to check for button
    const checkForButton = () => {
      if (resolved) return null;
      
      const buttonSelectors = sel.button.split(',');
      
      for (const selector of buttonSelectors) {
        try {
          const trimmedSelector = selector.trim();
          
          // Special handling for ChatGPT arrow path
          if (trimmedSelector.includes('path[d*=') || platform === 'chatgpt') {
            // Find all buttons and check for arrow path
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
              // Check for the specific arrow path
              const paths = btn.querySelectorAll('path');
              for (const path of paths) {
                const d = path.getAttribute('d');
                if (d && d.includes('M8.99992 16V6.41407')) {
                  // Verify button is enabled and visible
                  const rect = btn.getBoundingClientRect();
                  const isVisible = !btn.disabled && 
                                  rect.width > 0 && 
                                  rect.height > 0 &&
                                  window.getComputedStyle(btn).display !== 'none';
                  
                  if (isVisible) {
                    console.log(`[${platform}] Found ChatGPT send button with arrow path`);
                    resolved = true;
                    return btn;
                  }
                }
              }
            }
          }
          
          // Special handling for Gemini mat-icon with exact selectors from reliable code
          if (trimmedSelector.includes('mat-icon') || trimmedSelector.includes('mat-icon-button') || platform === 'gemini') {
            // Use exact selector priority from sendGeminiMessageReliably
            let sendBtn = document.querySelector('button[aria-label="Send message"]');
            
            if (!sendBtn) {
              // Secondary: mat-icon-button with nested mat-icon
              sendBtn = document.querySelector('button.mat-icon-button:has(mat-icon[fonticon="send"])');
            }
            
            // Additional fallbacks
            if (!sendBtn) {
              sendBtn = document.querySelector('button[aria-label*="Send" i]') ||
                        document.querySelector('button:has(mat-icon[fonticon="send"])') ||
                        document.querySelector('button[mattooltip*="Send" i]');
            }
            
            if (sendBtn) {
              const rect = sendBtn.getBoundingClientRect();
              const isVisible = rect.width > 0 && 
                              rect.height > 0 &&
                              window.getComputedStyle(sendBtn).display !== 'none';
              
              if (isVisible) {
                // Check if button is enabled
                const isDisabled = sendBtn.hasAttribute('disabled') || 
                                  sendBtn.disabled ||
                                  sendBtn.classList.contains('disabled') ||
                                  sendBtn.getAttribute('aria-disabled') === 'true';
                
                if (!isDisabled) {
                  console.log(`[${platform}] Step 2 complete: Send button is now active`);
                  resolved = true;
                  return sendBtn;
                }
              }
            }
          }
          
          // Standard selector check
          const btn = document.querySelector(trimmedSelector);
          if (btn && !btn.disabled) {
            const rect = btn.getBoundingClientRect();
            const isVisible = btn.offsetParent !== null || 
                            rect.height > 0 || 
                            rect.width > 0;
            
            if (isVisible) {
              console.log(`[${platform}] Found button with selector:`, trimmedSelector);
              resolved = true;
              return btn;
            }
          }
        } catch (e) {
          continue;
        }
      }
      
      return null;
    };
    
    // Initial check
    const initialButton = checkForButton();
    if (initialButton) {
      resolve(initialButton);
      return;
    }
    
    // Setup MutationObserver to watch for button appearance and state changes
    const observer = new MutationObserver((mutations) => {
      if (!resolved) {
        // For Gemini, specifically look for disabled attribute changes
        mutations.forEach(mutation => {
          if (platform === 'gemini' && 
              mutation.type === 'attributes' && 
              mutation.attributeName === 'disabled' &&
              mutation.target.tagName === 'BUTTON') {
            console.log(`[Gemini] Button disabled state changed`);
          }
        });
        
        // Check for button on any DOM change
        const button = checkForButton();
        if (button) {
          // Double-check button is not disabled
          const isDisabled = button.hasAttribute('disabled') || 
                            button.disabled ||
                            button.getAttribute('aria-disabled') === 'true';
          
          if (!isDisabled) {
            observer.disconnect();
            console.log(`[${platform}] Button found and active`);
            resolve(button);
          } else if (platform === 'gemini') {
            console.log(`[Gemini] Button found but still disabled, continuing to wait...`);
          }
        }
      }
    });
    
    // Start observing with comprehensive options
    // For Gemini, focus especially on 'disabled' attribute changes
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: platform === 'gemini' ? 
        ['disabled', 'aria-disabled'] : 
        ['disabled', 'aria-disabled', 'class', 'style', 'aria-label']
    });
    
    // Timeout handling with reject for Gemini
    setTimeout(() => {
      if (!resolved) {
        resolved = true;
        observer.disconnect();
        
        if (platform === 'gemini') {
          console.error(`[Gemini] Timeout: Send button did not become active within ${maxWait}ms`);
          reject(new Error('Gemini send button timeout'));
        } else {
          console.log(`[${platform}] No button appeared within ${maxWait}ms`);
          resolve(null);
        }
      }
    }, maxWait);
    
    // Also do periodic checks as fallback
    const intervalId = setInterval(() => {
      if (resolved || Date.now() - startTime > maxWait) {
        clearInterval(intervalId);
        return;
      }
      
      const button = checkForButton();
      if (button) {
        clearInterval(intervalId);
        observer.disconnect();
        resolve(button);
      }
    }, 100);
  });
}

// Enhanced send message with dynamic button detection
async function sendMessage() {
  const sel = SELECTORS[platform];
  if (!sel) return false;
  
  // Wait for button if platform requires it
  if (sel.waitForButton) {
    const button = await waitForButton();
    if (button) {
      if (platform === 'gemini') {
        console.log(`[Gemini] Step 3: Clicking activated send button...`);
      }
      
      // Use enhanced click for better compatibility
      try {
        clickWithPointer(button);
        if (platform === 'gemini') {
          console.log(`[Gemini] ✅ Step 3 complete: Message sent successfully!`);
        } else {
          console.log(`[${platform}] Clicked dynamic button with pointer events`);
        }
      } catch (e) {
        button.click();
        if (platform === 'gemini') {
          console.log(`[Gemini] ✅ Step 3 complete: Message sent (fallback click)`);
        } else {
          console.log(`[${platform}] Clicked dynamic button with fallback`);
        }
      }
      return true;
    }
  }
  
  // Try Ctrl+Enter if configured
  if (sel.useCtrlEnter) {
    console.log(`[${platform}] Trying Ctrl+Enter...`);
    
    const inputSelectors = sel.input.split(',');
    for (const selector of inputSelectors) {
      try {
        const input = document.querySelector(selector.trim());
        if (input && input.offsetParent !== null) {
          input.focus();
          
          // Send Ctrl+Enter
          const ctrlEnterEvent = new KeyboardEvent('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13,
            ctrlKey: true,
            bubbles: true,
            cancelable: true,
            composed: true
          });
          
          const dispatched = input.dispatchEvent(ctrlEnterEvent);
          console.log(`[${platform}] Ctrl+Enter dispatched:`, dispatched);
          
          // Also send keyup
          setTimeout(() => {
            const keyupEvent = new KeyboardEvent('keyup', {
              key: 'Enter',
              code: 'Enter',
              keyCode: 13,
              which: 13,
              ctrlKey: true,
              bubbles: true
            });
            input.dispatchEvent(keyupEvent);
          }, 50);
          
          return true;
        }
      } catch (e) {
        continue;
      }
    }
  }
  
  // Try standard button selectors
  const buttonSelectors = sel.button.split(',');
  for (const selector of buttonSelectors) {
    try {
      const trimmedSelector = selector.trim();
      
      // Special handling for ChatGPT path-based selectors
      if (trimmedSelector.includes('path[d*=') || platform === 'chatgpt') {
        // Use the same multi-strategy approach as in waitForButton
        const candidates = [
          'button[data-testid="send-button"]',
          'button[aria-label*="send" i]',
          'button[title*="send" i]',
          'form button[type="submit"]'
        ];
        
        // Try standard selectors first
        for (const sel of candidates) {
          const btn = document.querySelector(sel);
          if (btn && !btn.disabled) {
            try {
              clickWithPointer(btn);
              console.log(`[${platform}] Clicked ChatGPT button via ${sel}`);
            } catch (e) {
              btn.click();
              console.log(`[${platform}] Clicked ChatGPT button (fallback)`);
            }
            return true;
          }
        }
        
        // Fallback to SVG path detection
        const svgElements = document.querySelectorAll('svg, path');
        for (const svg of svgElements) {
          const d = svg.getAttribute('d') || '';
          if (d.includes('16V6.414') || d.includes('M8.99992')) {
            const btn = svg.closest('button');
            if (btn && !btn.disabled) {
              try {
                clickWithPointer(btn);
                console.log(`[${platform}] Clicked ChatGPT SVG path button`);
              } catch (e) {
                btn.click();
                console.log(`[${platform}] Clicked ChatGPT SVG button (fallback)`);
              }
              return true;
            }
          }
        }
      } else if (trimmedSelector.includes('mat-icon') || trimmedSelector.includes('aria-label')) {
        // Prioritize aria-label="Send message" for Gemini
        let sendBtn = document.querySelector('button[aria-label="Send message"]');
        
        if (!sendBtn) {
          sendBtn = document.querySelector('button.mat-icon-button:has(mat-icon[fonticon="send"])') ||
                    document.querySelector('button[aria-label*="Send" i]') ||
                    document.querySelector('button:has(mat-icon[fonticon="send"])') ||
                    document.querySelector('button[mattooltip*="Send" i]');
        }
        
        if (sendBtn && !sendBtn.disabled && !sendBtn.hasAttribute('disabled')) {
          try {
            clickWithPointer(sendBtn);
            console.log(`[${platform}] Clicked Gemini button with pointer events`);
          } catch (e) {
            sendBtn.click();
            console.log(`[${platform}] Clicked Gemini button with fallback`);
          }
          return true;
        }
      } else {
        const btn = document.querySelector(trimmedSelector);
        if (btn && !btn.disabled) {
          const isVisible = btn.offsetParent !== null || 
                          btn.offsetHeight > 0 || 
                          btn.offsetWidth > 0;
          
          if (isVisible) {
            btn.click();
            console.log(`[${platform}] Clicked button with selector:`, trimmedSelector);
            return true;
          }
        }
      }
    } catch (e) {
      continue;
    }
  }
  
  // Final fallback: Try Enter key on input
  const inputSelectors = sel.input.split(',');
  for (const selector of inputSelectors) {
    try {
      const input = document.querySelector(selector.trim());
      if (input) {
        const e = new KeyboardEvent("keydown", { 
          key: "Enter", 
          code: "Enter", 
          keyCode: 13, 
          which: 13, 
          bubbles: true, 
          cancelable: true 
        });
        input.dispatchEvent(e);
        console.log(`[${platform}] Sent Enter key to input:`, selector.trim());
        return true;
      }
    } catch (e) {
      continue;
    }
  }
  
  return false;
}

function getLastResponse() {
  let t = "";
  if (platform === "chatgpt") {
    const m = document.querySelectorAll('[data-message-author-role="assistant"]'); 
    if (m.length) t = m[m.length-1].textContent || "";
  } else if (platform === "claude") {
    const m = document.querySelectorAll("[data-test-render-count]"); 
    if (m.length) t = m[m.length-1].textContent || "";
  } else if (platform === "gemini") {
    const m = document.querySelectorAll("main, c-wiz, div[aria-live]"); 
    if (m.length) t = m[m.length-1].textContent || "";
  } else if (platform === "perplexity") {
    const m = document.querySelectorAll(".prose"); 
    if (m.length) t = m[m.length-1].textContent || "";
  }
  return t;
}

function extractCommandFromText(s) {
  const m = s.match(/```json([\s\S]*?)```/);
  const raw = (m ? m[1] : s).trim();
  try { 
    const o = JSON.parse(raw); 
    if (o && o.type === "command" && o.to && o.action) return o; 
  } catch {}
  return null;
}

async function detectAndRelayCommand() {
  const r = getLastResponse();
  if (!r) return;
  const cmd = extractCommandFromText(r);
  if (cmd) chrome.runtime.sendMessage({ action: "commandDetected", command: cmd }, () => {});
}

// Message handler
chrome.runtime.onMessage.addListener((req, _sender, sendResponse) => {
  (async () => {
    try {
      switch(req.action) {
        case "input":
          const inputOk = await autoInput(req.text);
          sendResponse({ success: inputOk, platform });
          break;
          
        case "send":
          const sendOk = await sendMessage();
          sendResponse({ success: sendOk, platform });
          break;
          
        case "inputAndSend":
          if (platform === 'gemini') {
            console.log(`[Gemini] Starting optimized message sending...`);
          }
          
          const ok1 = await autoInput(req.text);
          if (ok1) {
            // Small initial delay to allow DOM updates
            if (platform === 'gemini') {
              console.log(`[Gemini] Text input complete, initiating button wait...`);
              await new Promise(resolve => setTimeout(resolve, 100));
            } else if (SELECTORS[platform]?.waitForButton) {
              await new Promise(resolve => setTimeout(resolve, 300));
            }
            
            let ok2 = false;
            try {
              ok2 = await sendMessage();
            } catch (error) {
              if (platform === 'gemini') {
                console.error(`[Gemini] Send failed:`, error.message);
                // Retry once for Gemini
                console.log(`[Gemini] Retrying send...`);
                await new Promise(resolve => setTimeout(resolve, 500));
                try {
                  ok2 = await sendMessage();
                } catch (retryError) {
                  console.error(`[Gemini] Retry failed:`, retryError.message);
                }
              }
            }
            
            if (platform === 'gemini') {
              if (ok1 && ok2) {
                console.log(`[Gemini] ✅ Message sent successfully!`);
              } else {
                console.error(`[Gemini] ❌ Send failed - Input: ${ok1}, Send: ${ok2}`);
              }
            }
            
            sendResponse({ success: ok1 && ok2, platform });
          } else {
            if (platform === 'gemini') {
              console.error(`[Gemini] ❌ Text input failed`);
            }
            sendResponse({ success: false, platform });
          }
          break;
          
        case "getResponse":
          const response = getLastResponse();
          sendResponse({ response, platform });
          setTimeout(detectAndRelayCommand, 300);
          break;
          
        case "clear":
          const selectors = SELECTORS[platform]?.input.split(',') || [];
          let cleared = false;
          
          for (const selector of selectors) {
            try {
              const input = document.querySelector(selector.trim());
              if (input) {
                if (platform === "chatgpt") {
                  if (input.tagName === "TEXTAREA") {
                    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                    if (setter) {
                      setter.call(input, '');
                      input.dispatchEvent(new Event('input', { bubbles: true }));
                    } else {
                      input.value = '';
                    }
                  } else if (input.tagName === "DIV") {
                    input.textContent = '';
                    input.innerHTML = '';
                  }
                } else if (platform === "gemini" && input.classList.contains("ql-editor")) {
                  input.innerHTML = '';
                } else if (platform === "claude") {
                  input.innerHTML = '';
                } else if (input.tagName === "TEXTAREA") {
                  input.value = '';
                } else if (input.contentEditable === "true") {
                  input.innerText = '';
                }
                input.dispatchEvent(new Event('input', { bubbles: true }));
                cleared = true;
                break;
              }
            } catch (e) {
              continue;
            }
          }
          
          sendResponse({ success: cleared, platform });
          break;
          
        case "status":
          let inputFound = false;
          let debugInfo = {};
          
          if (platform && SELECTORS[platform]) {
            const selectors = SELECTORS[platform].input.split(',');
            debugInfo.totalSelectors = selectors.length;
            debugInfo.testedSelectors = [];
            
            for (const selector of selectors) {
              try {
                const element = document.querySelector(selector.trim());
                const selectorInfo = {
                  selector: selector.trim(),
                  found: !!element,
                  visible: false
                };
                
                if (element) {
                  // More comprehensive visibility check
                  const rect = element.getBoundingClientRect();
                  const isVisible = element.offsetParent !== null || 
                                   rect.height > 0 || 
                                   rect.width > 0 ||
                                   window.getComputedStyle(element).display !== 'none';
                  
                  selectorInfo.visible = isVisible;
                  selectorInfo.rect = { width: rect.width, height: rect.height };
                  
                  if (isVisible) {
                    inputFound = true;
                    console.log(`[${platform}] Status check - found input with selector:`, selector.trim());
                  }
                }
                
                debugInfo.testedSelectors.push(selectorInfo);
                if (inputFound) break;
              } catch (e) {
                debugInfo.testedSelectors.push({
                  selector: selector.trim(),
                  error: e.message
                });
                continue;
              }
            }
            
            // If still not found, try a delay and retry (for dynamic loading)
            if (!inputFound && (platform === "chatgpt" || platform === "gemini")) {
              await new Promise(resolve => setTimeout(resolve, 1000));
              
              // Retry with simple selector
              const fallbackElement = document.querySelector('textarea') || 
                                    document.querySelector('div[contenteditable="true"]') ||
                                    document.querySelector('[role="textbox"]') ||
                                    document.querySelector('.ql-editor');
              
              if (fallbackElement) {
                inputFound = true;
                console.log(`[${platform}] Found input on retry with fallback`);
              }
            }
          }
          
          // Enhanced debugging for problematic platforms
          if (!inputFound && (platform === 'chatgpt' || platform === 'gemini')) {
            console.log(`[${platform}] 🔍 No input found - debugging info:`, debugInfo);
            
            // Try fallback detection
            const fallbackInputs = document.querySelectorAll('textarea, [contenteditable="true"], .ql-editor');
            if (fallbackInputs.length > 0) {
              console.log(`[${platform}] 📝 Fallback found ${fallbackInputs.length} inputs:`);
              fallbackInputs.forEach((el, i) => {
                console.log(`  ${i+1}. ${el.tagName}.${el.className} #${el.id}`);
              });
            }
          }
          
          sendResponse({ 
            platform, 
            ready: inputFound, 
            url: location.href,
            debug: debugInfo
          });
          console.log(`[${platform}] Status response:`, { ready: inputFound, debugInfo });
          break;
          
        case "configUpdate":
          console.log(`[${platform}] Config updated:`, req.config);
          sendResponse({ success: true, platform });
          break;
          
        default:
          console.warn(`[${platform}] Unknown action:`, req.action);
          sendResponse({ success: false, error: "Unknown action", platform });
      }
    } catch (error) {
      console.error(`[${platform}] Message handler error:`, error);
      sendResponse({ success: false, error: error.message, platform });
    }
  })();
  
  return true; // Async response
});

// Badge with better visibility
(function () {
  const badge = document.createElement("div");
  badge.style.cssText = "position:fixed;top:20px;left:20px;background:lime;color:black;padding:8px 15px;border-radius:8px;font-size:14px;font-weight:bold;z-index:999999;border:2px solid black;cursor:pointer;font-family:system-ui;";
  badge.textContent = "🟢 " + (platform ? platform.toUpperCase() : "AI") + " LOADED";
  badge.title = `AI Workspace Controller Active on ${location.hostname}`;
  
  badge.addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "openPopup" });
  });
  
  // Add with delay and retry
  setTimeout(() => {
    try {
      document.body.appendChild(badge);
      console.log("✅ Badge added successfully for", platform);
    } catch (e) {
      console.log("❌ Failed to add badge:", e);
      setTimeout(() => {
        try {
          document.body.appendChild(badge);
          console.log("✅ Badge added on retry for", platform);
        } catch (e2) {
          console.log("❌ Badge failed again:", e2);
        }
      }, 2000);
    }
  }, 1000);
})();

console.log(`[${platform}] Enhanced content script v1.4.0 loaded - ChatGPT fixes & advanced debugging`);
console.log(`[${platform}] URL: ${location.href}`);

// Enhanced debugging for non-working platforms
if (platform === 'chatgpt' || platform === 'gemini') {
  console.log(`[${platform}] 🔍 Debugging mode active - this platform currently has issues`);
  
  // Immediate element detection
  setTimeout(() => {
    console.log(`[${platform}] 🔍 Initial element scan:`);
    
    // Check for input elements
    const inputs = document.querySelectorAll('textarea, div[contenteditable="true"], .ql-editor');
    console.log(`  📝 Found ${inputs.length} potential input elements`);
    inputs.forEach((el, i) => {
      console.log(`    ${i+1}. ${el.tagName}.${el.className} #${el.id}`);
    });
    
    // Check for send buttons
    const buttons = document.querySelectorAll('button');
    const sendButtons = Array.from(buttons).filter(btn => {
      const text = btn.textContent?.toLowerCase() || '';
      const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
      return text.includes('send') || ariaLabel.includes('send') || btn.querySelector('svg, mat-icon');
    });
    console.log(`  🚀 Found ${sendButtons.length} potential send buttons`);
    sendButtons.forEach((btn, i) => {
      console.log(`    ${i+1}. ${btn.tagName} - "${btn.getAttribute('aria-label') || btn.textContent?.slice(0, 20)}"`);
    });
  }, 2000);
}

if (SELECTORS[platform]?.waitForButton) {
  console.log(`[${platform}] Note: Will wait for send button after input`);
}

// Enhanced selector checking with multiple retries
function checkSelectors() {
  if (platform && SELECTORS[platform]) {
    const inputSelectors = SELECTORS[platform].input.split(',');
    let found = false;
    
    for (const selector of inputSelectors) {
      try {
        const inputEl = document.querySelector(selector.trim());
        if (inputEl) {
          const rect = inputEl.getBoundingClientRect();
          const isVisible = inputEl.offsetParent !== null || 
                           rect.height > 0 || 
                           rect.width > 0 ||
                           window.getComputedStyle(inputEl).display !== 'none';
          
          if (isVisible) {
            console.log(`[${platform}] Input found: ${selector.trim()}`);
            console.log(`[${platform}] Element type:`, inputEl.tagName, inputEl.className);
            found = true;
            break;
          }
        }
      } catch (e) {
        continue;
      }
    }
    
    if (!found) {
      console.log(`[${platform}] No input element found on initial check`);
    }
    
    return found;
  }
  return false;
}

// Wait for page ready with enhanced retries
function waitForReady() {
  let retryCount = 0;
  const maxRetries = 5;
  
  function tryCheck() {
    const found = checkSelectors();
    
    if (!found && retryCount < maxRetries) {
      retryCount++;
      console.log(`[${platform}] Retry ${retryCount}/${maxRetries} in ${retryCount}s...`);
      setTimeout(tryCheck, retryCount * 1000);
    } else if (found) {
      console.log(`[${platform}] Input element found and ready!`);
    } else {
      console.log(`[${platform}] Input element not found after ${maxRetries} retries`);
    }
  }
  
  if (document.readyState === 'complete') {
    tryCheck();
  } else {
    document.addEventListener('readystatechange', () => {
      if (document.readyState === 'complete') {
        tryCheck();
      }
    });
  }
}

waitForReady();