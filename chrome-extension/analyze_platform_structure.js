// Universal Platform Structure Analyzer
// 이 코드를 각 AI 플랫폼 콘솔에서 실행하여 정확한 구조 파악

(function() {
  console.clear();
  console.log("%c🔍 AI Platform Structure Analyzer", "font-size: 16px; font-weight: bold; color: #4CAF50");
  console.log("=" + "=".repeat(50));
  
  // 1. Platform Detection
  const platform = (() => {
    const h = location.hostname;
    if (h.includes("chatgpt.com") || h.includes("chat.openai.com")) return "ChatGPT";
    if (h.includes("claude.ai")) return "Claude";
    if (h.includes("perplexity.ai")) return "Perplexity";
    if (h.includes("aistudio.google.com")) return "Google AI Studio";
    if (h.includes("gemini.google.com")) return "Gemini";
    return "Unknown";
  })();
  
  console.log(`📍 Platform: ${platform}`);
  console.log(`🌐 URL: ${location.href}`);
  console.log("");
  
  // 2. Find Input Elements
  console.log("%c📝 Input Elements:", "font-weight: bold; color: #2196F3");
  const inputSelectors = [
    'textarea',
    'div[contenteditable="true"]',
    '[contenteditable="true"]',
    '.ql-editor',
    'div[role="textbox"]',
    '[role="textbox"]',
    '#prompt-textarea',
    '.ProseMirror',
    'rich-textarea'
  ];
  
  const foundInputs = new Set();
  inputSelectors.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      if (!foundInputs.has(el)) {
        foundInputs.add(el);
        const rect = el.getBoundingClientRect();
        const visible = rect.width > 0 && rect.height > 0;
        
        console.log(`  ✓ ${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}${el.className ? '.' + el.className.split(' ').join('.') : ''}`);
        console.log(`    Selector: "${selector}"`);
        console.log(`    Visible: ${visible ? '✅' : '❌'}, Size: ${Math.round(rect.width)}x${Math.round(rect.height)}`);
        console.log(`    Editable: ${el.contentEditable || 'N/A'}, Type: ${el.type || 'N/A'}`);
        
        // Check for React
        const reactProps = Object.keys(el).filter(k => k.startsWith('__react'));
        if (reactProps.length > 0) {
          console.log(`    %c⚛️ React component detected`, "color: #61DAFB");
        }
        
        // Check for Angular
        const ngVersion = el.getAttribute('ng-version');
        if (ngVersion || el.hasAttribute('_ngcontent')) {
          console.log(`    %c🅰️ Angular component detected`, "color: #DD0031");
        }
        
        console.log("");
      }
    });
  });
  
  // 3. Find Send Buttons
  console.log("%c🚀 Send Buttons:", "font-weight: bold; color: #4CAF50");
  const buttonSelectors = [
    'button[aria-label*="send" i]',
    'button[aria-label*="submit" i]',
    'button[data-testid*="send"]',
    'button:has(svg)',
    'button:has(mat-icon)',
    'mat-icon[fonticon="send"]',
    'mat-icon-button',
    '[role="button"]',
    'button[type="submit"]'
  ];
  
  const foundButtons = new Set();
  buttonSelectors.forEach(selector => {
    try {
      const elements = document.querySelectorAll(selector);
      elements.forEach(el => {
        if (!foundButtons.has(el)) {
          foundButtons.add(el);
          const rect = el.getBoundingClientRect();
          const visible = rect.width > 0 && rect.height > 0;
          
          console.log(`  ✓ ${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}${el.className ? '.' + el.className.split(' ').join('.') : ''}`);
          console.log(`    Selector: "${selector}"`);
          console.log(`    Visible: ${visible ? '✅' : '❌'}, Disabled: ${el.disabled ? '🚫' : '✅'}`);
          
          // Check for SVG/Icon
          const svg = el.querySelector('svg');
          const path = el.querySelector('path');
          const matIcon = el.querySelector('mat-icon') || (el.tagName === 'MAT-ICON' ? el : null);
          
          if (svg) console.log(`    Contains SVG ✓`);
          if (path) {
            const d = path.getAttribute('d');
            if (d) console.log(`    Path: "${d.substring(0, 30)}..."`);
          }
          if (matIcon) {
            console.log(`    Mat-Icon: ${matIcon.getAttribute('fonticon') || matIcon.textContent}`);
          }
          
          console.log("");
        }
      });
    } catch (e) {
      // Ignore selector errors
    }
  });
  
  // 4. Test Input Simulation
  console.log("%c🧪 Input Simulation Test:", "font-weight: bold; color: #FF9800");
  console.log("Paste this code to test input:");
  
  const testCode = `
// Test input simulation
(async function() {
  const input = document.querySelector('${platform === 'ChatGPT' ? '#prompt-textarea' : 
                                        platform === 'Claude' ? '.ProseMirror' :
                                        platform === 'Gemini' ? '.ql-editor' :
                                        platform === 'Google AI Studio' ? '.ql-editor' :
                                        'textarea'}');
  
  if (input) {
    console.log('Testing input on:', input);
    
    // Save original value
    const original = input.value || input.textContent || input.innerHTML;
    
    // Try different input methods
    const testText = "Test message from analyzer";
    
    if (input.tagName === 'TEXTAREA') {
      // Method 1: Direct value
      input.value = testText;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      console.log('Method 1 (direct): ', input.value === testText ? '✅' : '❌');
      
      // Method 2: React setter
      const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value')?.set;
      if (setter) {
        setter.call(input, testText);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        console.log('Method 2 (React): ', input.value === testText ? '✅' : '❌');
      }
    } else if (input.contentEditable === 'true') {
      // ContentEditable
      input.textContent = testText;
      input.dispatchEvent(new InputEvent('input', { 
        bubbles: true, 
        inputType: 'insertText',
        data: testText 
      }));
      console.log('ContentEditable: ', input.textContent === testText ? '✅' : '❌');
    } else if (input.classList.contains('ql-editor')) {
      // Quill editor
      input.innerHTML = '<p>' + testText + '</p>';
      input.dispatchEvent(new Event('input', { bubbles: true }));
      console.log('Quill: ', input.textContent.includes(testText) ? '✅' : '❌');
    }
    
    // Watch for button appearance
    console.log('Watching for button appearance...');
    const startTime = Date.now();
    const checkInterval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      if (elapsed > 3000) {
        clearInterval(checkInterval);
        console.log('No button appeared in 3 seconds');
        // Restore original
        if (input.tagName === 'TEXTAREA') {
          input.value = original;
        } else {
          input.textContent = original;
          input.innerHTML = original;
        }
        input.dispatchEvent(new Event('input', { bubbles: true }));
        return;
      }
      
      // Check for send button
      const sendButton = document.querySelector('button:has(path[d*="M8.99992"])') || 
                        document.querySelector('mat-icon[fonticon="send"]')?.closest('button') ||
                        document.querySelector('button[aria-label*="send" i]:not([disabled])');
      
      if (sendButton) {
        clearInterval(checkInterval);
        console.log('✅ Button appeared after ' + elapsed + 'ms:', sendButton);
        
        // Clear input
        if (input.tagName === 'TEXTAREA') {
          input.value = '';
        } else {
          input.textContent = '';
          input.innerHTML = '';
        }
        input.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }, 100);
  } else {
    console.log('❌ No input element found');
  }
})();`;
  
  console.log(testCode);
  
  // 5. Monitor DOM Changes
  console.log("");
  console.log("%c👁️ Starting DOM Monitor...", "font-weight: bold; color: #9C27B0");
  console.log("Type in the input field to see what changes...");
  
  const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      if (mutation.type === 'childList') {
        mutation.addedNodes.forEach(node => {
          if (node.nodeType === 1) { // Element node
            if (node.tagName === 'BUTTON' || node.querySelector?.('button')) {
              console.log('%c➕ Button added:', 'color: #4CAF50', node);
            }
            if (node.tagName === 'MAT-ICON' || node.querySelector?.('mat-icon')) {
              console.log('%c➕ Mat-icon added:', 'color: #4CAF50', node);
            }
          }
        });
      }
      if (mutation.type === 'attributes' && mutation.target.tagName === 'BUTTON') {
        console.log('%c🔄 Button attribute changed:', 'color: #FF9800', 
                    mutation.attributeName, '→', mutation.target.getAttribute(mutation.attributeName));
      }
    });
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['disabled', 'aria-disabled', 'class']
  });
  
  // Store observer for cleanup
  window.__platformAnalyzerObserver = observer;
  
  console.log("");
  console.log("%c📋 Analysis Complete!", "font-size: 14px; font-weight: bold; color: #4CAF50");
  console.log("To stop monitoring: window.__platformAnalyzerObserver.disconnect()");
})();