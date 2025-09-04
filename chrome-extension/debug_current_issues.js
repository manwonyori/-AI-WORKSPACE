/**
 * Debug Current Issues - ChatGPT & Gemini
 * 
 * 각 플랫폼에서 이 코드를 실행하여 현재 상태를 확인하고
 * 실제 작동하는 코드를 찾아보세요
 */

console.clear();
console.log("%c🐛 Debug Current Issues - AI Platform Analysis", "color: #ff5722; font-size: 16px; font-weight: bold");
console.log("=" + "=".repeat(60));

// Platform detection
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
console.log(`📄 Title: ${document.title}`);

// Function to test text input
async function testInput(text = "Test message") {
  console.log(`\n📝 Testing text input on ${platform}...`);
  
  let success = false;
  
  if (platform === "ChatGPT") {
    // ChatGPT input methods
    console.log("Trying ChatGPT input methods...");
    
    // Method 1: Find textarea
    let textarea = document.querySelector("textarea#prompt-textarea") ||
                   document.querySelector("textarea[data-id='root']") ||
                   document.querySelector("textarea[placeholder*='Message']") ||
                   document.querySelector("textarea");
    
    if (textarea) {
      console.log("✅ Found textarea:", textarea);
      
      try {
        // React setter method
        const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value')?.set;
        if (setter) {
          setter.call(textarea, text);
          textarea.dispatchEvent(new Event('input', { bubbles: true }));
          console.log("✅ Text set via React setter");
          success = true;
        } else {
          textarea.value = text;
          textarea.dispatchEvent(new Event('input', { bubbles: true }));
          console.log("✅ Text set via direct value");
          success = true;
        }
      } catch (e) {
        console.error("❌ TextArea input failed:", e);
      }
    }
    
    // Method 2: Find contenteditable div
    if (!success) {
      let div = document.querySelector("div#prompt-textarea") ||
                document.querySelector("div[contenteditable='true']") ||
                document.querySelector("div[role='textbox']");
      
      if (div) {
        console.log("✅ Found contenteditable div:", div);
        try {
          div.textContent = text;
          div.dispatchEvent(new Event('input', { bubbles: true }));
          console.log("✅ Text set via contenteditable");
          success = true;
        } catch (e) {
          console.error("❌ ContentEditable input failed:", e);
        }
      }
    }
    
  } else if (platform === "Google AI Studio" || platform === "Gemini") {
    // Gemini input methods
    console.log("Trying Gemini input methods...");
    
    const editor = document.querySelector("div.ql-editor");
    if (editor) {
      console.log("✅ Found Quill editor:", editor);
      
      try {
        // Method 1: Quill API
        const quill = editor.__quill;
        if (quill) {
          quill.setText(text);
          console.log("✅ Text set via Quill API");
          success = true;
        } else {
          // Method 2: innerHTML
          editor.innerHTML = `<p>${text}</p>`;
          editor.dispatchEvent(new Event('input', { bubbles: true }));
          editor.dispatchEvent(new Event('change', { bubbles: true }));
          editor.dispatchEvent(new Event('blur', { bubbles: true }));
          console.log("✅ Text set via innerHTML");
          success = true;
        }
      } catch (e) {
        console.error("❌ Gemini input failed:", e);
      }
    } else {
      // Try other selectors
      const fallback = document.querySelector("textarea") || 
                      document.querySelector("div[contenteditable='true']");
      if (fallback) {
        console.log("✅ Found fallback input:", fallback);
        try {
          if (fallback.tagName === 'TEXTAREA') {
            fallback.value = text;
          } else {
            fallback.textContent = text;
          }
          fallback.dispatchEvent(new Event('input', { bubbles: true }));
          success = true;
        } catch (e) {
          console.error("❌ Fallback input failed:", e);
        }
      }
    }
  }
  
  if (!success) {
    console.error("❌ All input methods failed");
  }
  
  return success;
}

// Function to test send button
async function testSend() {
  console.log(`\n🚀 Testing send button on ${platform}...`);
  
  let success = false;
  
  if (platform === "ChatGPT") {
    console.log("Looking for ChatGPT send button...");
    
    // Method 1: Look for arrow path button
    const buttons = document.querySelectorAll("button");
    for (const btn of buttons) {
      const path = btn.querySelector("path");
      if (path && path.getAttribute("d")?.includes("M8.99992")) {
        console.log("✅ Found arrow path button:", btn);
        if (!btn.disabled) {
          btn.click();
          console.log("✅ Clicked arrow button");
          success = true;
          break;
        } else {
          console.log("⚠️ Arrow button is disabled");
        }
      }
    }
    
    // Method 2: Standard selectors
    if (!success) {
      const sendBtn = document.querySelector('button[data-testid="send-button"]') ||
                     document.querySelector('button[aria-label*="Send"]');
      if (sendBtn && !sendBtn.disabled) {
        sendBtn.click();
        console.log("✅ Clicked standard send button");
        success = true;
      }
    }
    
  } else if (platform === "Google AI Studio" || platform === "Gemini") {
    console.log("Looking for Gemini send button...");
    
    // Method 1: aria-label priority
    let sendBtn = document.querySelector('button[aria-label="Send message"]');
    
    if (!sendBtn) {
      // Method 2: mat-icon button
      sendBtn = document.querySelector('button.mat-icon-button:has(mat-icon[fonticon="send"])') ||
                document.querySelector('button:has(mat-icon[fonticon="send"])');
    }
    
    if (!sendBtn) {
      // Method 3: Any Send button
      sendBtn = document.querySelector('button[aria-label*="Send"]');
    }
    
    if (sendBtn) {
      console.log("✅ Found send button:", sendBtn);
      if (!sendBtn.disabled && !sendBtn.hasAttribute('disabled')) {
        sendBtn.click();
        console.log("✅ Clicked send button");
        success = true;
      } else {
        console.log("⚠️ Send button is disabled");
      }
    }
  }
  
  if (!success) {
    console.error("❌ No working send button found");
  }
  
  return success;
}

// Function to run complete test
async function runCompleteTest() {
  console.log("\n" + "=".repeat(60));
  console.log("🧪 Running Complete Test");
  console.log("-".repeat(60));
  
  const testMessage = `Debug test ${Date.now()}`;
  
  // Step 1: Input test
  const inputSuccess = await testInput(testMessage);
  
  if (inputSuccess) {
    // Step 2: Wait and send
    console.log("\n⏳ Waiting 2 seconds for button activation...");
    await new Promise(r => setTimeout(r, 2000));
    
    const sendSuccess = await testSend();
    
    console.log("\n" + "=".repeat(60));
    console.log("📊 Test Results:");
    console.log(`Input: ${inputSuccess ? '✅ Success' : '❌ Failed'}`);
    console.log(`Send: ${sendSuccess ? '✅ Success' : '❌ Failed'}`);
    console.log(`Overall: ${inputSuccess && sendSuccess ? '✅ Working' : '❌ Not Working'}`);
    
  } else {
    console.log("\n❌ Skipping send test due to input failure");
  }
}

// Function to analyze current state
function analyzeCurrentState() {
  console.log("\n" + "=".repeat(60));
  console.log("🔍 Current State Analysis");
  console.log("-".repeat(60));
  
  // Count elements
  const textareas = document.querySelectorAll('textarea');
  const contentEditables = document.querySelectorAll('[contenteditable="true"]');
  const quillEditors = document.querySelectorAll('.ql-editor');
  const buttons = document.querySelectorAll('button');
  
  console.log(`📝 Input Elements Found:`);
  console.log(`  - Textareas: ${textareas.length}`);
  console.log(`  - ContentEditable: ${contentEditables.length}`);
  console.log(`  - Quill Editors: ${quillEditors.length}`);
  
  console.log(`\n🚀 Button Elements Found:`);
  console.log(`  - Total Buttons: ${buttons.length}`);
  
  // Analyze send buttons
  const potentialSendButtons = Array.from(buttons).filter(btn => {
    const text = btn.textContent?.toLowerCase() || '';
    const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
    const hasIcon = btn.querySelector('svg, mat-icon');
    
    return text.includes('send') || 
           ariaLabel.includes('send') || 
           hasIcon ||
           btn.querySelector('path[d*="M8.99992"]');
  });
  
  console.log(`  - Potential Send Buttons: ${potentialSendButtons.length}`);
  
  potentialSendButtons.forEach((btn, i) => {
    const disabled = btn.disabled || btn.hasAttribute('disabled');
    const ariaLabel = btn.getAttribute('aria-label') || 'no-label';
    const hasPath = !!btn.querySelector('path[d*="M8.99992"]');
    const hasMatIcon = !!btn.querySelector('mat-icon');
    
    console.log(`    ${i+1}. ${disabled ? '🚫' : '✅'} "${ariaLabel}" ${hasPath ? '(arrow)' : ''} ${hasMatIcon ? '(mat-icon)' : ''}`);
  });
}

// Auto-run analysis
console.log("\n💡 Available Commands:");
console.log("- analyzeCurrentState()  // Analyze current page");
console.log("- testInput('message')   // Test text input");
console.log("- testSend()            // Test send button");
console.log("- runCompleteTest()     // Run full test");

console.log("\n⏰ Running automatic analysis in 2 seconds...");
setTimeout(() => {
  analyzeCurrentState();
  
  // Also run test if on ChatGPT or Gemini
  if (platform === "ChatGPT" || platform === "Google AI Studio" || platform === "Gemini") {
    console.log("\n⏰ Running complete test in 5 seconds...");
    setTimeout(runCompleteTest, 5000);
  }
}, 2000);