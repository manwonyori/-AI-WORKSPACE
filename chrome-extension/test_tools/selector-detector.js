// Selector Auto-Detection Script for AI Platforms
// Based on ChatGPT's provided script, enhanced for all platforms

function detectInputElement() {
  // 1) Find candidates: textarea, contenteditable div
  const candidates = Array.from(document.querySelectorAll(`
    textarea,
    div[contenteditable="true"][role="textbox"],
    div[contenteditable="true"],
    rich-textarea textarea,
    .PromptTextarea textarea,
    .SearchBar-input
  `));

  // 2) Filter visible elements only
  const isVisible = el => {
    if (!el) return false;
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return (
      el.offsetParent !== null &&
      style.visibility !== 'hidden' &&
      style.display !== 'none' &&
      rect.width > 0 && rect.height > 0
    );
  };

  // 3) Score candidates to find most likely input
  const score = el => {
    let s = 0;
    if (el.matches('textarea')) s += 3;
    if (el.matches('div[contenteditable="true"]')) s += 2;
    if (el.getAttribute('role') === 'textbox') s += 2;
    if (el.hasAttribute('aria-label')) s += 2;
    if (el.hasAttribute('placeholder')) s += 2;
    if (el.hasAttribute('data-testid')) s += 2;
    if (el.hasAttribute('data-id')) s += 1; // React root
    // Larger elements more likely to be main input
    const r = el.getBoundingClientRect();
    s += Math.min(4, Math.round((r.width * r.height) / 15000));
    return s;
  };

  const visible = candidates.filter(isVisible);
  const inputEl = visible.sort((a,b) => score(b) - score(a))[0] || document.activeElement;

  // 4) Collect data-* attributes
  const dataAttrs = {};
  for (const {name, value} of Array.from(inputEl.attributes)) {
    if (name.startsWith('data-')) dataAttrs[name] = value;
  }

  // 5) Generate unique CSS selector
  const cssEscape = s => CSS && CSS.escape ? CSS.escape(s) : s.replace(/([ !"#$%&'()*+,.\/:;<=>?@[\\\]^`{|}~])/g,'\\$1');
  
  function uniqueSelector(el) {
    if (!el || el.nodeType !== 1) return '';
    if (el.id) return `#${cssEscape(el.id)}`;
    
    const parts = [];
    while (el && el.nodeType === 1 && parts.length < 5) {
      let part = el.tagName.toLowerCase();
      if (el.id) { 
        part += `#${cssEscape(el.id)}`; 
        parts.unshift(part); 
        break; 
      }
      if (el.classList.length) {
        part += '.' + Array.from(el.classList).slice(0,3).map(cssEscape).join('.');
      }
      const sibs = Array.from(el.parentNode ? el.parentNode.children : []);
      const sameTag = sibs.filter(s => s.tagName === el.tagName);
      if (sameTag.length > 1) {
        const idx = sameTag.indexOf(el) + 1;
        part += `:nth-of-type(${idx})`;
      }
      parts.unshift(part);
      el = el.parentElement;
    }
    return parts.join(' > ');
  }

  // 6) Compile information
  const info = {
    // Core attributes
    tagName: inputEl.tagName.toLowerCase(),
    class: inputEl.className || '',
    id: inputEl.id || '',
    contenteditable: inputEl.getAttribute('contenteditable'),
    dataAttributes: dataAttrs,
    ariaLabel: inputEl.getAttribute('aria-label'),
    placeholder: inputEl.getAttribute('placeholder'),
    // Additional useful attributes
    role: inputEl.getAttribute('role'),
    dataTestid: inputEl.getAttribute('data-testid'),
    dataId: inputEl.getAttribute('data-id'),
    dataPlaceholder: inputEl.getAttribute('data-placeholder'),
    // Generated selectors
    uniqueSelector: uniqueSelector(inputEl),
    // Platform detection
    platform: detectPlatform(),
    url: location.href,
    timestamp: new Date().toISOString()
  };

  // Generate helpful selectors based on attributes
  info.helpfulSelectors = generateHelpfulSelectors(inputEl, info);
  
  return info;
}

function generateHelpfulSelectors(el, info) {
  const selectors = [];
  const cssEscape = s => CSS && CSS.escape ? CSS.escape(s) : s.replace(/([ !"#$%&'()*+,.\/:;<=>?@[\\\]^`{|}~])/g,'\\$1');
  
  // ID selector
  if (info.id) {
    selectors.push(`#${cssEscape(info.id)}`);
  }
  
  // Class selector
  if (info.class) {
    const classes = info.class.split(' ').filter(c => c && !c.includes(':'));
    if (classes.length > 0) {
      selectors.push(`${info.tagName}.${classes.slice(0, 3).map(cssEscape).join('.')}`);
    }
  }
  
  // Data attributes
  if (info.dataTestid) {
    selectors.push(`[data-testid="${info.dataTestid}"]`);
  }
  if (info.dataId) {
    selectors.push(`[data-id="${info.dataId}"]`);
  }
  
  // ContentEditable + role
  if (info.contenteditable === 'true') {
    if (info.role) {
      selectors.push(`${info.tagName}[contenteditable="true"][role="${info.role}"]`);
    } else {
      selectors.push(`${info.tagName}[contenteditable="true"]`);
    }
  }
  
  // Aria label
  if (info.ariaLabel) {
    selectors.push(`[aria-label*="${info.ariaLabel.substring(0, 20)}"]`);
  }
  
  // Placeholder
  if (info.placeholder) {
    selectors.push(`[placeholder*="${info.placeholder.substring(0, 20)}"]`);
  }
  
  return selectors.filter(Boolean);
}

function detectPlatform() {
  const hostname = location.hostname;
  if (hostname.includes('chatgpt.com') || hostname.includes('chat.openai.com')) {
    return 'chatgpt';
  }
  if (hostname.includes('claude.ai')) {
    return 'claude';
  }
  if (hostname.includes('perplexity.ai')) {
    return 'perplexity';
  }
  if (hostname.includes('aistudio.google.com') || hostname.includes('gemini.google.com')) {
    return 'gemini';
  }
  return 'unknown';
}

function detectSendButton() {
  const buttonCandidates = Array.from(document.querySelectorAll(`
    button[aria-label*="Send"],
    button[aria-label*="Submit"],
    button[data-testid*="send"],
    button[data-testid*="submit"],
    button[type="submit"],
    button.send-button,
    button.SendButton,
    button.SearchBar-sendButton,
    button svg[data-icon="send"]
  `));
  
  const isVisible = el => {
    if (!el) return false;
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return (
      el.offsetParent !== null &&
      style.visibility !== 'hidden' &&
      style.display !== 'none' &&
      rect.width > 0 && rect.height > 0 &&
      !el.disabled
    );
  };
  
  const visible = buttonCandidates.filter(isVisible);
  const button = visible[0];
  
  if (!button) return null;
  
  return {
    tagName: button.tagName.toLowerCase(),
    class: button.className || '',
    id: button.id || '',
    ariaLabel: button.getAttribute('aria-label'),
    dataTestid: button.getAttribute('data-testid'),
    type: button.getAttribute('type'),
    disabled: button.disabled,
    selector: generateButtonSelector(button)
  };
}

function generateButtonSelector(button) {
  const selectors = [];
  
  if (button.id) {
    selectors.push(`#${CSS.escape(button.id)}`);
  }
  
  if (button.className) {
    const classes = button.className.split(' ').filter(c => c && !c.includes(':'));
    if (classes.length > 0) {
      selectors.push(`button.${classes[0]}`);
    }
  }
  
  const ariaLabel = button.getAttribute('aria-label');
  if (ariaLabel) {
    selectors.push(`button[aria-label="${ariaLabel}"]`);
  }
  
  const dataTestid = button.getAttribute('data-testid');
  if (dataTestid) {
    selectors.push(`button[data-testid="${dataTestid}"]`);
  }
  
  return selectors[0] || 'button[type="submit"]';
}

// Main detection function
function runFullDetection() {
  const results = {
    input: detectInputElement(),
    button: detectSendButton(),
    platform: detectPlatform(),
    url: location.href,
    timestamp: new Date().toISOString()
  };
  
  console.clear();
  console.log('=== AI Platform Selector Detection Results ===');
  console.log('Platform:', results.platform);
  console.log('URL:', results.url);
  console.log('\n📝 INPUT ELEMENT:');
  console.table(results.input);
  console.log('Suggested selectors:', results.input.helpfulSelectors);
  console.log('\n🔘 SEND BUTTON:');
  if (results.button) {
    console.table(results.button);
  } else {
    console.log('No send button found');
  }
  
  // Highlight elements
  const inputEl = document.querySelector(results.input.uniqueSelector);
  if (inputEl) {
    inputEl.style.outline = '3px solid #4CAF50';
    inputEl.style.outlineOffset = '2px';
    console.log('✅ Input element highlighted in GREEN');
  }
  
  if (results.button) {
    const buttonEl = document.querySelector(results.button.selector);
    if (buttonEl) {
      buttonEl.style.outline = '3px solid #2196F3';
      buttonEl.style.outlineOffset = '2px';
      console.log('✅ Send button highlighted in BLUE');
    }
  }
  
  return results;
}

// Export for use in extension
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { runFullDetection, detectInputElement, detectSendButton };
} else {
  window.selectorDetector = { runFullDetection, detectInputElement, detectSendButton };
}

// Auto-run if called directly
if (typeof window !== 'undefined' && window.location) {
  runFullDetection();
}