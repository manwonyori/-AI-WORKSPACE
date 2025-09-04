/**
 * Comprehensive Extension Diagnostic Tool
 * 
 * 이 도구를 각 AI 플랫폼에서 실행하여 extension의 실제 작동 상태를 확인하고
 * 문제를 정확히 진단할 수 있습니다.
 * 
 * 사용법: 각 AI 플랫폼에서 F12 → Console에 이 코드를 붙여넣고 실행
 */

(function() {
  console.clear();
  console.log("%c🔧 AI Workspace Extension - Comprehensive Diagnostic Tool", 
    "color: #ff6b35; font-size: 18px; font-weight: bold; background: #fff3cd; padding: 10px; border-radius: 5px;");
  
  console.log("=" + "=".repeat(80));
  
  // Platform Detection
  function detectCurrentPlatform() {
    const hostname = location.hostname;
    const pathname = location.pathname;
    const url = location.href;
    
    console.log("%c📍 Platform Detection", "font-weight: bold; font-size: 14px; color: #0066cc;");
    console.log(`   Hostname: ${hostname}`);
    console.log(`   Pathname: ${pathname}`);
    console.log(`   Full URL: ${url}`);
    
    let platform = "Unknown";
    if (hostname.includes("chatgpt.com") || hostname.includes("chat.openai.com")) {
      platform = "ChatGPT";
    } else if (hostname.includes("claude.ai")) {
      platform = "Claude";
    } else if (hostname.includes("perplexity.ai")) {
      platform = "Perplexity";
    } else if (hostname.includes("aistudio.google.com")) {
      platform = "Google AI Studio";
      if (pathname.includes("/500") || pathname === "/" || pathname.includes("/app")) {
        console.log("%c⚠️ WARNING: Problematic URL detected!", "color: #ff9800; font-weight: bold;");
        console.log("   Should be on: https://aistudio.google.com/prompts/new_chat");
      }
    } else if (hostname.includes("gemini.google.com")) {
      platform = "Gemini";
    }
    
    console.log(`%c   Detected: ${platform}`, `color: ${platform === "Unknown" ? "#ff0000" : "#00cc00"}; font-weight: bold;`);
    return platform;
  }
  
  // Extension Status Check
  function checkExtensionStatus() {
    console.log("\n%c🔌 Chrome Extension Status", "font-weight: bold; font-size: 14px; color: #0066cc;");
    
    // Check if extension runtime is available
    const hasChrome = typeof chrome !== 'undefined';
    const hasRuntime = hasChrome && chrome.runtime;
    
    console.log(`   Chrome API available: ${hasChrome ? "✅ Yes" : "❌ No"}`);
    console.log(`   Runtime available: ${hasRuntime ? "✅ Yes" : "❌ No"}`);
    
    if (hasRuntime) {
      try {
        const extensionId = chrome.runtime.id;
        console.log(`   Extension ID: ${extensionId}`);
        
        // Try to send a test message
        chrome.runtime.sendMessage({ action: "status" }, (response) => {
          if (chrome.runtime.lastError) {
            console.log(`   Message Test: ❌ Error - ${chrome.runtime.lastError.message}`);
          } else {
            console.log(`   Message Test: ✅ Success`);
            if (response) {
              console.log(`   Extension Response:`, response);
            }
          }
        });
      } catch (e) {
        console.log(`   Extension Error: ❌ ${e.message}`);
      }
    }
    
    return { hasChrome, hasRuntime };
  }
  
  // Input Elements Analysis
  function analyzeInputElements(platform) {
    console.log("\n%c📝 Input Elements Analysis", "font-weight: bold; font-size: 14px; color: #0066cc;");
    
    const inputSelectors = {
      ChatGPT: [
        "#prompt-textarea",
        "textarea[aria-label*='message' i]",
        "textarea[placeholder*='message' i]",
        "textarea",
        "[contenteditable='true'][data-testid]",
        "[contenteditable='true'][aria-label*='message' i]",
        "[contenteditable='true']"
      ],
      "Google AI Studio": [
        "div.ql-editor",
        "textarea[aria-label*='prompt' i]",
        "textarea",
        "[contenteditable='true']"
      ],
      Gemini: [
        "div.ql-editor",
        "textarea[aria-label*='prompt' i]",
        "textarea",
        "[contenteditable='true']"
      ],
      Claude: [
        "div.ProseMirror",
        "[contenteditable='true'][data-placeholder]",
        "[contenteditable='true']"
      ],
      Perplexity: [
        "textarea[placeholder*='Ask' i]",
        "textarea",
        "[contenteditable='true']"
      ]
    };
    
    const selectors = inputSelectors[platform] || [];
    let foundElements = [];
    
    console.log(`   Testing ${selectors.length} selectors for ${platform}:`);
    
    selectors.forEach((selector, index) => {
      try {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
          elements.forEach((el, elIndex) => {
            const rect = el.getBoundingClientRect();
            const isVisible = rect.width > 0 && rect.height > 0;
            const id = el.id || `no-id-${elIndex}`;
            const className = el.className || 'no-class';
            
            foundElements.push({
              selector,
              element: el,
              visible: isVisible,
              id,
              className: className.slice(0, 50)
            });
            
            console.log(`      ${index + 1}.${elIndex + 1} ${isVisible ? '✅' : '❌'} ${el.tagName}#${id}.${className.slice(0, 30)}`);
            console.log(`           Selector: "${selector}"`);
            console.log(`           Size: ${Math.round(rect.width)}x${Math.round(rect.height)}`);
            console.log(`           Visible: ${isVisible}, Editable: ${el.contentEditable || 'N/A'}`);
          });
        } else {
          console.log(`      ${index + 1}. ❌ No elements found for "${selector}"`);
        }
      } catch (e) {
        console.log(`      ${index + 1}. 💥 Error with selector "${selector}": ${e.message}`);
      }
    });
    
    console.log(`\n   Summary: Found ${foundElements.length} input elements total`);
    const visibleElements = foundElements.filter(el => el.visible);
    console.log(`   Visible: ${visibleElements.length} elements`);
    
    return foundElements;
  }
  
  // Send Button Analysis
  function analyzeSendButtons(platform) {
    console.log("\n%c🚀 Send Button Analysis", "font-weight: bold; font-size: 14px; color: #0066cc;");
    
    const buttonSelectors = {
      ChatGPT: [
        "button[data-testid='send-button']",
        "button[aria-label*='send' i]",
        "button[title*='send' i]",
        "form button[type='submit']",
        "button:has(path[d*='16V6.414'])"
      ],
      "Google AI Studio": [
        "button[aria-label='Send message']",
        "button[aria-label*='전송' i]",
        "button[aria-label*='send' i]",
        "button:has(mat-icon[fonticon='send'])",
        "mat-icon-button[aria-label*='send' i]"
      ],
      Gemini: [
        "button[aria-label='Send message']",
        "button[aria-label*='전송' i]",
        "button[aria-label*='send' i]",
        "button:has(mat-icon[fonticon='send'])",
        "mat-icon-button[aria-label*='send' i]"
      ],
      Claude: [
        "button[aria-label='Send Message']",
        "button[aria-label*='Send']",
        "form button[type='submit']"
      ],
      Perplexity: [
        "button[aria-label='Submit']",
        "button.bg-super",
        "form button[type='submit']"
      ]
    };
    
    const selectors = buttonSelectors[platform] || [];
    let foundButtons = [];
    
    console.log(`   Testing ${selectors.length} button selectors for ${platform}:`);
    
    selectors.forEach((selector, index) => {
      try {
        const buttons = document.querySelectorAll(selector);
        if (buttons.length > 0) {
          buttons.forEach((btn, btnIndex) => {
            const rect = btn.getBoundingClientRect();
            const isVisible = rect.width > 0 && rect.height > 0;
            const isDisabled = btn.disabled || btn.hasAttribute('disabled');
            const ariaLabel = btn.getAttribute('aria-label') || 'no-label';
            
            foundButtons.push({
              selector,
              button: btn,
              visible: isVisible,
              disabled: isDisabled,
              ariaLabel
            });
            
            const status = isVisible && !isDisabled ? '✅' : (isDisabled ? '🚫' : '❌');
            console.log(`      ${index + 1}.${btnIndex + 1} ${status} "${ariaLabel.slice(0, 20)}"`);
            console.log(`           Selector: "${selector}"`);
            console.log(`           Visible: ${isVisible}, Disabled: ${isDisabled}`);
            
            // Check for SVG/Icon content
            const hasIcon = btn.querySelector('svg, mat-icon, path');
            if (hasIcon) {
              console.log(`           Has Icon: ✅ ${hasIcon.tagName}`);
            }
          });
        } else {
          console.log(`      ${index + 1}. ❌ No buttons found for "${selector}"`);
        }
      } catch (e) {
        console.log(`      ${index + 1}. 💥 Error with selector "${selector}": ${e.message}`);
      }
    });
    
    console.log(`\n   Summary: Found ${foundButtons.length} buttons total`);
    const activeButtons = foundButtons.filter(btn => btn.visible && !btn.disabled);
    console.log(`   Active: ${activeButtons.length} buttons`);
    
    return foundButtons;
  }
  
  // Network & API Status
  function checkNetworkStatus() {
    console.log("\n%c🌐 Network & API Status", "font-weight: bold; font-size: 14px; color: #0066cc;");
    
    // Check if we can make network requests
    const canFetch = typeof fetch !== 'undefined';
    console.log(`   Fetch API available: ${canFetch ? '✅ Yes' : '❌ No'}`);
    
    // Check online status
    const isOnline = navigator.onLine;
    console.log(`   Network status: ${isOnline ? '✅ Online' : '❌ Offline'}`);
    
    // Try a test request to check CORS/permissions
    if (canFetch && isOnline) {
      console.log("   Testing network connectivity...");
      
      // Test with a simple request
      fetch('https://httpbin.org/get', { method: 'GET' })
        .then(response => {
          console.log(`   Network test: ✅ Success (${response.status})`);
        })
        .catch(error => {
          console.log(`   Network test: ❌ Failed - ${error.message}`);
        });
    }
  }
  
  // Live Test Functions
  function createTestFunctions(platform, inputElements, sendButtons) {
    console.log("\n%c🧪 Live Test Functions", "font-weight: bold; font-size: 14px; color: #0066cc;");
    
    const visibleInputs = inputElements.filter(el => el.visible);
    const activeButtons = sendButtons.filter(btn => btn.visible && !btn.disabled);
    
    if (visibleInputs.length === 0) {
      console.log("   ❌ No visible input elements found - cannot create test functions");
      return;
    }
    
    if (activeButtons.length === 0) {
      console.log("   ⚠️ No active send buttons found - input test only");
    }
    
    // Create input test function
    window.__diagnosticInputTest = (text = `Test input ${Date.now()}`) => {
      console.log(`\n🧪 Testing input on ${platform}...`);
      const input = visibleInputs[0].element;
      
      try {
        input.focus();
        
        if (platform === "ChatGPT") {
          // ChatGPT specific method
          if (input.tagName === 'TEXTAREA') {
            const win = input.ownerDocument?.defaultView || window;
            const desc = Object.getOwnPropertyDescriptor(win.HTMLTextAreaElement.prototype, 'value');
            if (desc?.set) {
              desc.set.call(input, text);
            } else {
              input.value = text;
            }
          } else {
            input.textContent = text;
          }
          
          // Fire events
          input.dispatchEvent(new Event('beforeinput', { bubbles: true }));
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('compositionend', { bubbles: true }));
          
        } else if (platform === "Google AI Studio" || platform === "Gemini") {
          // Gemini specific method
          if (input.classList.contains('ql-editor')) {
            input.innerHTML = `<p>${text}</p>`;
            
            // Selection API
            const range = document.createRange();
            const sel = window.getSelection();
            range.selectNodeContents(input);
            range.collapse(false);
            sel.removeAllRanges();
            sel.addRange(range);
          } else {
            input.value = text;
          }
          
          // Fire events
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
          input.dispatchEvent(new Event('blur', { bubbles: true }));
          
        } else {
          // Generic method
          if (input.tagName === 'TEXTAREA') {
            input.value = text;
          } else {
            input.textContent = text;
          }
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        
        console.log(`✅ Input test successful: "${text}"`);
        return true;
      } catch (e) {
        console.log(`❌ Input test failed: ${e.message}`);
        return false;
      }
    };
    
    // Create send test function
    if (activeButtons.length > 0) {
      window.__diagnosticSendTest = () => {
        console.log(`\n🧪 Testing send button on ${platform}...`);
        const button = activeButtons[0].button;
        
        try {
          // Enhanced click sequence
          const events = [
            new PointerEvent('pointerdown', { bubbles: true }),
            new MouseEvent('mousedown', { bubbles: true }),
            new PointerEvent('pointerup', { bubbles: true }),
            new MouseEvent('mouseup', { bubbles: true }),
            new MouseEvent('click', { bubbles: true })
          ];
          
          events.forEach(event => button.dispatchEvent(event));
          console.log(`✅ Send button clicked successfully`);
          return true;
        } catch (e) {
          console.log(`❌ Send button test failed: ${e.message}`);
          return false;
        }
      };
      
      // Complete test function
      window.__diagnosticCompleteTest = async (text = `Complete test ${Date.now()}`) => {
        console.log(`\n🧪 Running complete test on ${platform}...`);
        
        const inputSuccess = window.__diagnosticInputTest(text);
        if (!inputSuccess) return false;
        
        // Wait for button activation
        console.log("⏳ Waiting for button activation...");
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const sendSuccess = window.__diagnosticSendTest();
        
        const success = inputSuccess && sendSuccess;
        console.log(`\n📊 Complete Test Result: ${success ? '✅ SUCCESS' : '❌ FAILED'}`);
        return success;
      };
    }
    
    console.log("   Created test functions:");
    console.log("   - __diagnosticInputTest('text')");
    if (activeButtons.length > 0) {
      console.log("   - __diagnosticSendTest()");
      console.log("   - __diagnosticCompleteTest('text')");
    }
  }
  
  // Main diagnostic execution
  function runDiagnostic() {
    const platform = detectCurrentPlatform();
    const extensionStatus = checkExtensionStatus();
    const inputElements = analyzeInputElements(platform);
    const sendButtons = analyzeSendButtons(platform);
    
    checkNetworkStatus();
    createTestFunctions(platform, inputElements, sendButtons);
    
    // Final summary
    console.log("\n%c📋 Diagnostic Summary", "font-weight: bold; font-size: 16px; color: #ff6b35; background: #fff3cd; padding: 5px;");
    console.log(`   Platform: ${platform}`);
    console.log(`   Extension: ${extensionStatus.hasRuntime ? '✅ Working' : '❌ Not Working'}`);
    console.log(`   Input Elements: ${inputElements.filter(el => el.visible).length} visible`);
    console.log(`   Send Buttons: ${sendButtons.filter(btn => btn.visible && !btn.disabled).length} active`);
    
    const canWork = extensionStatus.hasRuntime && 
                   inputElements.some(el => el.visible) && 
                   sendButtons.some(btn => btn.visible && !btn.disabled);
    
    console.log(`\n%c🎯 Overall Status: ${canWork ? '✅ SHOULD WORK' : '❌ ISSUES DETECTED'}`, 
      `font-weight: bold; color: ${canWork ? '#00cc00' : '#ff0000'}; font-size: 14px;`);
    
    if (!canWork) {
      console.log("\n%c🔧 Recommended Actions:", "font-weight: bold; color: #ff9800;");
      if (!extensionStatus.hasRuntime) {
        console.log("   1. Check if extension is loaded in chrome://extensions");
        console.log("   2. Reload the extension");
        console.log("   3. Check manifest.json for correct permissions");
      }
      if (!inputElements.some(el => el.visible)) {
        console.log("   1. Check if you're on the correct page");
        console.log("   2. Wait for page to fully load");
        console.log("   3. Update input selectors in extension code");
      }
      if (!sendButtons.some(btn => btn.visible && !btn.disabled)) {
        console.log("   1. Try typing in the input field first");
        console.log("   2. Check if send buttons appear after input");
        console.log("   3. Update button selectors in extension code");
      }
    }
    
    console.log("\n" + "=".repeat(80));
    console.log("💡 Use the created test functions to verify functionality");
  }
  
  // Run the diagnostic
  runDiagnostic();
  
})();