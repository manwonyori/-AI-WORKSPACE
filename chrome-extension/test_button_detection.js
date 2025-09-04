// Button Detection Test Script for v1.3.4
// Tests improved dynamic button detection with MutationObserver

console.log("🧪 Button Detection Test v1.3.4 Starting...");

// Platform detection
const platform = (() => {
  const h = location.hostname;
  if (h.includes("chatgpt.com") || h.includes("chat.openai.com")) return "chatgpt";
  if (h.includes("claude.ai")) return "claude";
  if (h.includes("perplexity.ai")) return "perplexity";
  if (h.includes("aistudio.google.com") || h.includes("gemini.google.com")) return "gemini";
  return "unknown";
})();

console.log(`📍 Platform: ${platform}`);

// Test 1: Find input element
function testInputElement() {
  console.log("\n=== Test 1: Input Element Detection ===");
  
  const selectors = {
    chatgpt: ["textarea#prompt-textarea", "div#prompt-textarea", "textarea[data-id='root']", "div[contenteditable='true']"],
    gemini: ["div.ql-editor", "textarea[aria-label*='prompt']", "rich-textarea textarea"],
    claude: ["div.ProseMirror", "div[contenteditable='true'][data-placeholder]"],
    perplexity: ["textarea[placeholder*='Ask']", "textarea", "[contenteditable='true']"]
  };
  
  const platformSelectors = selectors[platform] || [];
  let found = false;
  
  for (const sel of platformSelectors) {
    const el = document.querySelector(sel);
    if (el) {
      const rect = el.getBoundingClientRect();
      console.log(`✅ Found input: ${sel}`);
      console.log(`   Type: ${el.tagName}, Visible: ${rect.width > 0 && rect.height > 0}`);
      found = true;
      break;
    }
  }
  
  if (!found) {
    console.log("❌ No input element found");
  }
  
  return found;
}

// Test 2: Simulate text input and watch for button
async function testButtonAppearance() {
  console.log("\n=== Test 2: Button Appearance After Input ===");
  
  // Find input
  let inputEl = null;
  
  if (platform === "chatgpt") {
    inputEl = document.querySelector("textarea#prompt-textarea") || 
              document.querySelector("div#prompt-textarea") ||
              document.querySelector("textarea[data-id='root']");
  } else if (platform === "gemini") {
    inputEl = document.querySelector("div.ql-editor") ||
              document.querySelector("textarea[aria-label*='prompt']");
  }
  
  if (!inputEl) {
    console.log("❌ No input element to test with");
    return;
  }
  
  console.log(`📝 Found input element: ${inputEl.tagName}.${inputEl.className}`);
  
  // Setup MutationObserver to watch for button
  console.log("👁️ Setting up MutationObserver to watch for button appearance...");
  
  const buttonAppeared = new Promise((resolve) => {
    let found = false;
    
    const checkButton = () => {
      if (found) return null;
      
      // Check for ChatGPT arrow button
      if (platform === "chatgpt") {
        const buttons = document.querySelectorAll("button");
        for (const btn of buttons) {
          const paths = btn.querySelectorAll("path");
          for (const path of paths) {
            const d = path.getAttribute("d");
            if (d && d.includes("M8.99992 16V6.41407")) {
              console.log("✅ Found ChatGPT send button!");
              console.log(`   Button state: ${btn.disabled ? 'disabled' : 'enabled'}`);
              found = true;
              return btn;
            }
          }
        }
      }
      
      // Check for Gemini mat-icon
      if (platform === "gemini") {
        const icons = document.querySelectorAll('mat-icon[fonticon="send"]');
        for (const icon of icons) {
          const btn = icon.closest("button, [role='button']");
          if (btn || icon) {
            console.log("✅ Found Gemini send button!");
            const target = btn || icon;
            console.log(`   Element: ${target.tagName}, Disabled: ${target.hasAttribute('disabled')}`);
            found = true;
            return target;
          }
        }
      }
      
      return null;
    };
    
    const observer = new MutationObserver(() => {
      const btn = checkButton();
      if (btn) {
        observer.disconnect();
        resolve(btn);
      }
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['disabled', 'class', 'style']
    });
    
    // Also check immediately
    const immediate = checkButton();
    if (immediate) {
      observer.disconnect();
      resolve(immediate);
    }
    
    // Timeout
    setTimeout(() => {
      observer.disconnect();
      if (!found) {
        console.log("⏱️ Timeout: No button appeared within 5 seconds");
        resolve(null);
      }
    }, 5000);
  });
  
  // Simulate input
  console.log("💬 Simulating text input...");
  
  inputEl.focus();
  
  if (platform === "chatgpt") {
    if (inputEl.tagName === "TEXTAREA") {
      const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value')?.set;
      if (setter) {
        setter.call(inputEl, "Test message for button detection");
        inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      }
    } else {
      inputEl.textContent = "Test message for button detection";
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
    }
  } else if (platform === "gemini") {
    if (inputEl.classList.contains("ql-editor")) {
      inputEl.innerHTML = "<p>Test message for button detection</p>";
    } else {
      inputEl.value = "Test message for button detection";
    }
    inputEl.dispatchEvent(new Event('input', { bubbles: true }));
  }
  
  // Wait for button
  const button = await buttonAppeared;
  
  if (button) {
    console.log("🎯 Button detection successful!");
    console.log(`   Button details: ${button.tagName}, Clickable: ${!button.disabled}`);
    
    // Clear input
    if (inputEl.tagName === "TEXTAREA") {
      inputEl.value = "";
    } else {
      inputEl.textContent = "";
      inputEl.innerHTML = "";
    }
    inputEl.dispatchEvent(new Event('input', { bubbles: true }));
  } else {
    console.log("❌ Button did not appear after input");
  }
}

// Test 3: Check existing buttons
function testExistingButtons() {
  console.log("\n=== Test 3: Existing Button Detection ===");
  
  if (platform === "chatgpt") {
    // Look for any send buttons
    const buttons = document.querySelectorAll('button[data-testid="send-button"], button[aria-label*="Send"]');
    console.log(`Found ${buttons.length} potential send buttons`);
    
    // Check for arrow path buttons
    const pathButtons = Array.from(document.querySelectorAll("button")).filter(btn => {
      const path = btn.querySelector('path[d*="M8.99992"]');
      return path !== null;
    });
    console.log(`Found ${pathButtons.length} buttons with arrow path`);
  } else if (platform === "gemini") {
    const matIcons = document.querySelectorAll('mat-icon[fonticon="send"]');
    console.log(`Found ${matIcons.length} mat-icon send elements`);
    
    const sendButtons = document.querySelectorAll('button[aria-label*="Send"], button[title*="Send"]');
    console.log(`Found ${sendButtons.length} buttons with Send label/title`);
  }
}

// Run tests
(async () => {
  console.log("\n🚀 Starting all tests...\n");
  
  testInputElement();
  testExistingButtons();
  
  if (platform === "chatgpt" || platform === "gemini") {
    await testButtonAppearance();
  }
  
  console.log("\n✅ All tests completed!");
  console.log("\n💡 Summary:");
  console.log(`- Platform: ${platform}`);
  console.log(`- URL: ${location.href}`);
  console.log("- Check console for detailed results");
})();