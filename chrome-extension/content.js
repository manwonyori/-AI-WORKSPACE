// Content script for AI platforms auto-input (chunk-safe + multi-site)
// Updated: add Gemini support, chunked insertion, robust events, minor UI fixes

const platform = detectPlatform();

function detectPlatform() {
  const h = window.location.hostname;
  if (h.includes('chatgpt.com')) return 'chatgpt';
  if (h.includes('claude.ai')) return 'claude';
  if (h.includes('perplexity.ai')) return 'perplexity';
  if (h.includes('gemini.google.com')) return 'gemini';
  return null;
}

// Platform-specific selectors (2025-09 baseline)
const SELECTORS = {
  chatgpt: {
    input: '#prompt-textarea, textarea[data-id=\"root\"]',
    button: 'button[data-testid=\"send-button\"], button[aria-label=\"Send message\"], form button[type=\"submit\"]',
    container: 'main'
  },
  claude: {
    input: 'div[contenteditable=\"true\"].ProseMirror, div[contenteditable=\"true\"]',
    button: 'button[aria-label=\"Send Message\"], form button[type=\"submit\"]',
    container: 'main'
  },
  gemini: {
    input: 'textarea, [contenteditable=\"true\"]',
    button: 'button[aria-label*=\"Send\"], form button[type=\"submit\"], button[aria-label*=\"작성\"]',
    container: 'main'
  },
  perplexity: {
    input: 'textarea[placeholder*=\"Ask\"], textarea, [contenteditable=\"true\"]',
    button: 'button[aria-label=\"Submit\"], button.bg-super, form button[type=\"submit\"]',
    container: 'main'
  }
};

// Reasonable per-platform chunk caps (defensive; services can change)
const CHUNK_LIMIT = {
  chatgpt: 3500,
  claude: 3500,
  gemini: 2500,
  perplexity: 3000,
  default: 2500
};

function getChunkLimit() {
  return CHUNK_LIMIT[platform] || CHUNK_LIMIT.default;
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function splitText(text, limit) {
  // split on paragraph boundaries where possible
  const chunks = [];
  let remaining = text;
  while (remaining.length > limit) {
    // try to cut on newline near limit
    const slice = remaining.slice(0, limit);
    let cut = slice.lastIndexOf('\\n\\n');
    if (cut < limit * 0.6) cut = slice.lastIndexOf('\\n');
    if (cut < limit * 0.4) cut = slice.lastIndexOf(' ');
    if (cut <= 0) cut = limit;
    chunks.push(remaining.slice(0, cut));
    remaining = remaining.slice(cut);
  }
  if (remaining) chunks.push(remaining);
  return chunks;
}

// React-controlled textarea safe setter
function setReactTextareaValue(el, value) {
  const proto = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value');
  if (proto && proto.set) {
    proto.set.call(el, value);
  } else {
    el.value = value;
  }
  el.dispatchEvent(new Event('input', { bubbles: true }));
}

// Insert text into contenteditable using InputEvent
function insertIntoContentEditable(el, text) {
  el.focus();
  // fallback: selection insert
  const sel = window.getSelection();
  if (sel && sel.rangeCount) {
    const range = sel.getRangeAt(0);
    range.deleteContents();
    range.insertNode(document.createTextNode(text));
    range.collapse(false);
  } else {
    // execCommand is deprecated but still widely supported
    document.execCommand('insertText', false, text);
  }
  el.dispatchEvent(new InputEvent('input', { bubbles: true, cancelable: true, inputType: 'insertText', data: text }));
}

async function clearInput(el) {
  if (!el) return;
  if (el.tagName === 'TEXTAREA') {
    setReactTextareaValue(el, '');
  } else {
    el.innerHTML = '';
    el.dispatchEvent(new Event('input', { bubbles: true }));
  }
  await sleep(50);
}

// Chunked insertion core
async function chunkedInsert(el, text) {
  const limit = getChunkLimit();
  const chunks = splitText(text, limit);

  // Always start clean
  await clearInput(el);

  for (let i = 0; i < chunks.length; i++) {
    const part = chunks[i];
    if (el.tagName === 'TEXTAREA') {
      // Append in pieces for React-controlled inputs
      const current = el.value ?? '';
      setReactTextareaValue(el, current + part);
    } else {
      // contenteditable
      insertIntoContentEditable(el, part);
    }
    // small pacing to avoid throttling
    await sleep(80 + Math.min(220, Math.round(part.length / 10)));
  }

  // Force a final input/change event
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
  return true;
}

// Auto-input (now chunk safe)
async function autoInput(text) {
  try {
    if (!platform) throw new Error('Platform not detected');
    const selector = SELECTORS[platform];
    if (!selector) throw new Error('Platform not supported');

    // Find input element (with short polling for late-mount UIs)
    const started = performance.now();
    let input = null;
    while (performance.now() - started < 2500) {
      input = document.querySelector(selector.input);
      if (input) break;
      await sleep(120);
    }
    if (!input) throw new Error('Input field not found');

    // Decide mode
    const isTextarea = input.tagName === 'TEXTAREA';
    await chunkedInsert(input, text);

    return true;
  } catch (err) {
    console.error('[autoInput] error:', err);
    return false;
  }
}

// Send message
function sendMessage() {
  const selector = SELECTORS[platform];
  if (!selector) return false;
  const button = document.querySelector(selector.button);
  if (button && !button.disabled) {
    button.click();
    return true;
  }
  // Fallback: simulate Enter
  const input = document.querySelector(selector.input);
  if (input) {
    const evt = new KeyboardEvent('keydown', {
      key: 'Enter', code: 'Enter', keyCode: 13, which: 13,
      bubbles: true, cancelable: true
    });
    input.dispatchEvent(evt);
    return true;
  }
  return false;
}

// Get response (simple last assistant bubble text)
function getLastResponse() {
  let response = '';
  try {
    if (platform === 'chatgpt') {
      const msgs = document.querySelectorAll('[data-message-author-role=\"assistant\"]');
      if (msgs.length) response = msgs[msgs.length - 1].textContent || '';
    } else if (platform === 'claude') {
      const msgs = document.querySelectorAll('[data-test-render-count]');
      if (msgs.length) response = msgs[msgs.length - 1].textContent || '';
    } else if (platform === 'perplexity') {
      const msgs = document.querySelectorAll('.prose');
      if (msgs.length) response = msgs[msgs.length - 1].textContent || '';
    } else if (platform === 'gemini') {
      const msgs = document.querySelectorAll('[data-md-component], article, .response, .prose');
      if (msgs.length) response = msgs[msgs.length - 1].textContent || '';
    }
  } catch (e) {
    console.warn('[getLastResponse] failed:', e);
  }
  return response;
}

// Listen for commands from extension (now supports async input)
chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
  (async () => {
    try {
      if (request?.action === 'input') {
        const success = await autoInput(request.text || '');
        return sendResponse({ success, platform });
      }
      if (request?.action === 'send') {
        const success = sendMessage();
        return sendResponse({ success, platform });
      }
      if (request?.action === 'inputAndSend') {
        const ok = await autoInput(request.text || '');
        await sleep(300);
        const sent = ok ? sendMessage() : false;
        return sendResponse({ success: ok && sent, platform });
      }
      if (request?.action === 'getResponse') {
        const response = getLastResponse();
        return sendResponse({ response, platform });
      }
      if (request?.action === 'clear') {
        const input = document.querySelector(SELECTORS[platform]?.input);
        await clearInput(input);
        return sendResponse({ success: true, platform });
      }
      if (request?.action === 'status') {
        return sendResponse({
          platform,
          ready: !!document.querySelector(SELECTORS[platform]?.input),
          url: window.location.href
        });
      }
      if (request?.action === 'configUpdate') {
        console.log(`[${platform}] Config updated:`, request.config);
        // Could use config to update selectors, prompts, etc.
        return sendResponse({ success: true, platform });
      }
    } catch (err) {
      console.error('handler error:', err);
      return sendResponse({ success: false, error: String(err), platform });
    }
  })();
  return true; // keep channel open for async
});

// Visual indicator (guard if unsupported)
if (platform) {
  const indicator = document.createElement('div');
  indicator.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 12px;
    z-index: 999999;
    opacity: 0.9;
    cursor: pointer;
    font-family: system-ui;
  `;
  indicator.textContent = \`🤖 \${platform.toUpperCase()} Ready\`;
  indicator.title = 'AI Workspace Controller Active';
  indicator.addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'openPopup' });
  });
  document.addEventListener('DOMContentLoaded', () => {
    document.body.appendChild(indicator);
  });
}

console.log(\`[\${platform}] Content script loaded (chunk-safe) and ready\`);