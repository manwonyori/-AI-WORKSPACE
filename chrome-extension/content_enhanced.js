// Enhanced Content Script with platform-specific input methods
// Based on investigation findings from chatgpt_simple_test.js and platform_investigation.js

function detectPlatform() {
  const h = location.hostname;
  console.log("🔍 Platform detection - hostname:", h, "pathname:", location.pathname);
  
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
  if (h.includes("aistudio.google.com") || h.includes("gemini.google.com") || 
      (h.includes("google.com") && (location.pathname.includes("prompts") || location.pathname.includes("app")))) {
    console.log("✅ Detected Gemini/AI Studio - hostname:", h, "pathname:", location.pathname);
    return "gemini";
  }
  
  console.log("❓ Unknown platform");
  return null;
}

const platform = detectPlatform();

const SELECTORS = {
  chatgpt: {
    input: "textarea#prompt-textarea, textarea[data-id=\"root\"], textarea.m-0.w-full.resize-none, textarea[placeholder*=\"Message\"], textarea",
    button: "button[data-testid=\"send-button\"], button[aria-label*=\"Send\"], button[aria-label*=\"send\"], button[type=\"submit\"]:not([disabled])",
    container: "main"
  },
  claude: {
    input: "div[contenteditable=\"true\"].ProseMirror, div[contenteditable=\"true\"][data-placeholder], div[contenteditable=\"true\"][aria-label*=\"Message\"], div.DraftEditor-editorContainer div[contenteditable=\"true\"], div[role=\"textbox\"][contenteditable=\"true\"], div[contenteditable=\"true\"]",
    button: "button[aria-label=\"Send Message\"], button[aria-label*=\"Send\"], button[data-testid=\"send-button\"], form button[type=\"submit\"], button.send-button",
    container: "main, .chat-container"
  },
  gemini: {
    input: "div.ql-editor, div[contenteditable=\"true\"].ql-editor, rich-textarea textarea, textarea[aria-label*=\"Enter a prompt\"], textarea[aria-label*=\"prompt\"], textarea[placeholder*=\"Enter a prompt\"], textarea.textarea, textarea[rows], textarea",
    button: "button[aria-label*=\"Send\"], button[aria-label*=\"send\"], button[aria-label*=\"Run\"], button[title*=\"Send\"], button[title*=\"Run\"], button.send-button, mat-icon-button[aria-label*=\"Send\"], button[mattooltip*=\"Send\"]",
    container: "main, c-wiz, mat-sidenav-content, .main-content"
  },
  perplexity: {
    input: "textarea[placeholder*=\"Ask\"], textarea, [contenteditable=\"true\"]",
    button: "button[aria-label=\"Submit\"], button.bg-super, form button[type=\"submit\"]",
    container: "main"
  }
};

const CHUNK_LIMIT = { 
  chatgpt: 4500, 
  claude: 4500, 
  gemini: 3200, 
  perplexity: 3800, 
  default: 3000 
};

// Platform-specific input methods
async function inputForChatGPT(inputEl, text) {
  console.log("[ChatGPT] Using React-style setter method");
  
  if (inputEl.tagName !== "TEXTAREA") {
    console.warn("[ChatGPT] Expected textarea, got:", inputEl.tagName);
    return false;
  }
  
  try {
    // Focus the element
    inputEl.focus();
    
    // Use React-compatible setter (Method C from investigation)
    const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype, 
      'value'
    ).set;
    
    if (nativeTextAreaValueSetter) {
      // Clear existing value
      nativeTextAreaValueSetter.call(inputEl, '');
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      
      // Set new value
      nativeTextAreaValueSetter.call(inputEl, text);
      
      // Dispatch both input and change events
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      inputEl.dispatchEvent(new Event('change', { bubbles: true }));
      
      console.log("[ChatGPT] Text set successfully using React setter");
      return true;
    } else {
      console.warn("[ChatGPT] Native setter not found, falling back to direct value");
      inputEl.value = text;
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      return true;
    }
  } catch (e) {
    console.error("[ChatGPT] Input error:", e);
    return false;
  }
}

async function inputForGemini(inputEl, text) {
  console.log("[Gemini] Detected element type:", inputEl.tagName, inputEl.className);
  
  // Handle Quill Editor
  if (inputEl.classList && inputEl.classList.contains("ql-editor")) {
    console.log("[Gemini] Using Quill editor method");
    
    try {
      inputEl.focus();
      
      // Method 2 from investigation: innerHTML with focus events
      inputEl.innerHTML = `<p>${text}</p>`;
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      
      // Trigger blur/focus cycle for Quill
      inputEl.dispatchEvent(new Event('blur', { bubbles: true }));
      await new Promise(r => setTimeout(r, 100));
      inputEl.dispatchEvent(new Event('focus', { bubbles: true }));
      
      console.log("[Gemini] Quill editor text set successfully");
      return true;
    } catch (e) {
      console.error("[Gemini] Quill editor error:", e);
      return false;
    }
  }
  
  // Handle regular textarea (AI Studio might use this)
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
  } else if (inputEl.contentEditable === "true") {
    inputEl.textContent = '';
  }
  
  for (let i = 0; i < chunks.length; i++) {
    const part = chunks[i];
    console.log(`[${platform}] Inserting chunk ${i+1}/${chunks.length}: ${part.substring(0, 50)}...`);
    
    // Append chunk based on platform
    if (platform === "chatgpt" && inputEl.tagName === "TEXTAREA") {
      const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
      if (setter) {
        setter.call(inputEl, inputEl.value + part);
        inputEl.dispatchEvent(new Event('input', { bubbles: true }));
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
  
  for (const selector of selectors) {
    try {
      const element = document.querySelector(selector.trim());
      if (element) {
        // Verify it's visible and interactable
        if (element.offsetParent !== null) {
          input = element;
          console.log(`[${platform}] Found input element with selector:`, selector.trim());
          break;
        }
      }
    } catch (e) {
      continue;
    }
  }
  
  if (!input) {
    console.warn(`[${platform}] No input element found`);
    return false;
  }
  
  const limit = CHUNK_LIMIT[platform] || CHUNK_LIMIT.default;
  return await chunkedInsert(input, text, limit);
}

function sendMessage() {
  const sel = SELECTORS[platform];
  if (!sel) return false;
  
  // Try each button selector
  const buttonSelectors = sel.button.split(',');
  for (const selector of buttonSelectors) {
    try {
      const btn = document.querySelector(selector.trim());
      if (btn && !btn.disabled && btn.offsetParent !== null) {
        btn.click();
        console.log(`[${platform}] Clicked button with selector:`, selector.trim());
        return true;
      }
    } catch (e) {
      continue;
    }
  }
  
  // Fallback: Try Enter key on input
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
          const sendOk = sendMessage();
          sendResponse({ success: sendOk, platform });
          break;
          
        case "inputAndSend":
          const ok1 = await autoInput(req.text);
          await new Promise(resolve => setTimeout(resolve, 400));
          const ok2 = sendMessage();
          sendResponse({ success: ok1 && ok2, platform });
          break;
          
        case "getResponse":
          const response = getLastResponse();
          sendResponse({ response, platform });
          setTimeout(detectAndRelayCommand, 300);
          break;
          
        case "clear":
          const input = document.querySelector(SELECTORS[platform]?.input);
          if (input) {
            if (platform === "chatgpt" && input.tagName === "TEXTAREA") {
              // Use React setter to clear
              const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
              if (setter) {
                setter.call(input, '');
                input.dispatchEvent(new Event('input', { bubbles: true }));
              } else {
                input.value = '';
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
          }
          sendResponse({ success: true, platform });
          break;
          
        case "status":
          let inputFound = false;
          if (platform && SELECTORS[platform]) {
            const selectors = SELECTORS[platform].input.split(',');
            for (const selector of selectors) {
              try {
                const element = document.querySelector(selector.trim());
                if (element && element.offsetParent !== null) {
                  inputFound = true;
                  console.log(`[${platform}] Status check - found input with selector:`, selector.trim());
                  break;
                }
              } catch (e) {
                continue;
              }
            }
          }
          
          sendResponse({ 
            platform, 
            ready: inputFound, 
            url: location.href 
          });
          console.log(`[${platform}] Status response:`, { ready: inputFound });
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

console.log(`[${platform}] Enhanced content script loaded`);
console.log(`[${platform}] URL: ${location.href}`);

// Check selectors on ready
function checkSelectors() {
  if (platform && SELECTORS[platform]) {
    const inputSelectors = SELECTORS[platform].input.split(',');
    let found = false;
    
    for (const selector of inputSelectors) {
      try {
        const inputEl = document.querySelector(selector.trim());
        if (inputEl && inputEl.offsetParent !== null) {
          console.log(`[${platform}] Input found: ${selector.trim()}`);
          console.log(`[${platform}] Element type:`, inputEl.tagName, inputEl.className);
          found = true;
          break;
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

// Wait for page ready
function waitForReady() {
  if (document.readyState === 'complete') {
    const found = checkSelectors();
    if (!found) {
      // Retry for dynamic content
      setTimeout(checkSelectors, 2000);
      setTimeout(checkSelectors, 4000);
    }
  } else {
    document.addEventListener('readystatechange', () => {
      if (document.readyState === 'complete') {
        waitForReady();
      }
    });
  }
}

waitForReady();