/**
 * Gemini 3-Step Message Sending Test
 * 이 코드를 Gemini/AI Studio 콘솔에서 실행하여 테스트
 */

console.clear();
console.log("🚀 Gemini 3-Step Message Sending Test");
console.log("=" + "=".repeat(50));

// Utility function
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

/**
 * Gemini 입력창(Quill Editor)에 텍스트를 입력하고 전송합니다.
 * @param {string} message - 전송할 메시지 텍스트
 */
async function sendGeminiMessage(message) {
  console.log("\n📝 Step 1: Text Input");
  console.log("Message:", message);
  
  // 1단계: 텍스트 입력
  const editorElement = document.querySelector('div.ql-editor');
  if (!editorElement) {
    console.error('❌ Gemini 입력창을 찾을 수 없습니다.');
    return false;
  }
  console.log('✅ Found Quill editor:', editorElement);

  // 에디터 요소에 연결된 Quill 인스턴스를 가져옵니다.
  const quillInstance = editorElement.__quill;

  if (quillInstance) {
    // Quill API를 사용해 텍스트를 설정합니다. (가장 안정적인 방법)
    console.log('✅ Found Quill instance, using API');
    
    // Clear any existing text
    quillInstance.setText('');
    await sleep(100);
    
    // Set new text
    quillInstance.setText(message);
    console.log('✅ Text set via Quill API');
    
    // Optional: Check if text was actually set
    const currentText = quillInstance.getText();
    console.log('Verification - Current text:', currentText.trim());
  } else {
    // Quill 인스턴스를 찾지 못했을 경우의 대체 방법
    console.warn('⚠️ Quill instance not found, using fallback method');
    editorElement.innerHTML = `<p>${message}</p>`;
    editorElement.dispatchEvent(new Event('input', { bubbles: true }));
    editorElement.dispatchEvent(new Event('change', { bubbles: true }));
  }

  // 2단계: 전송 버튼 활성화 대기
  console.log("\n⏳ Step 2: Waiting for button activation");
  
  // Find send button with multiple selectors
  let sendButton = null;
  const buttonSelectors = [
    'button[aria-label="Send message"]',
    'button[aria-label*="Send"]',
    'button.mat-icon-button:has(mat-icon[fonticon="send"])',
    'button:has(mat-icon[fonticon="send"])',
    'button[mattooltip*="Send"]'
  ];

  // Wait for button to become enabled
  const maxWaitTime = 5000; // 5 seconds
  const startTime = Date.now();
  
  while (Date.now() - startTime < maxWaitTime) {
    for (const selector of buttonSelectors) {
      const btn = document.querySelector(selector);
      if (btn && !btn.disabled && !btn.hasAttribute('disabled')) {
        sendButton = btn;
        break;
      }
    }
    
    if (sendButton) {
      console.log('✅ Send button found and enabled:', sendButton);
      break;
    }
    
    await sleep(100);
  }

  if (!sendButton) {
    console.error('❌ Send button not found or still disabled after', maxWaitTime, 'ms');
    return false;
  }

  // 3단계: 전송 버튼 클릭
  console.log("\n🖱️ Step 3: Clicking send button");
  
  try {
    // Try pointer events first (more natural)
    const opts = { bubbles: true, cancelable: true, composed: true };
    sendButton.dispatchEvent(new PointerEvent('pointerdown', opts));
    sendButton.dispatchEvent(new MouseEvent('mousedown', opts));
    sendButton.dispatchEvent(new PointerEvent('pointerup', opts));
    sendButton.dispatchEvent(new MouseEvent('mouseup', opts));
    sendButton.dispatchEvent(new MouseEvent('click', opts));
    console.log('✅ Button clicked with pointer events');
  } catch (e) {
    // Fallback to simple click
    sendButton.click();
    console.log('✅ Button clicked with fallback method');
  }

  console.log("\n✅ Message sending process complete!");
  return true;
}

// Test function with monitoring
async function testGeminiSending() {
  console.log("\n" + "=".repeat(50));
  console.log("🧪 Starting automated test...");
  
  // Save original content
  const editor = document.querySelector('div.ql-editor');
  const originalContent = editor ? (editor.innerHTML || '') : '';
  
  // Test message
  const testMessage = "Test message from 3-step process at " + new Date().toLocaleTimeString();
  
  // Monitor DOM changes
  console.log("\n👁️ Starting DOM monitor...");
  const mutations = [];
  const observer = new MutationObserver((mutationsList) => {
    mutationsList.forEach(mutation => {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        mutation.addedNodes.forEach(node => {
          if (node.nodeType === 1) { // Element node
            if (node.tagName === 'BUTTON' || (node.querySelector && node.querySelector('button'))) {
              console.log('  📌 Button added to DOM:', node);
              mutations.push({ type: 'button-added', element: node });
            }
          }
        });
      }
      if (mutation.type === 'attributes' && mutation.target.tagName === 'BUTTON') {
        if (mutation.attributeName === 'disabled' || mutation.attributeName === 'aria-disabled') {
          console.log('  🔄 Button state changed:', mutation.attributeName, '→', mutation.target.getAttribute(mutation.attributeName));
          mutations.push({ 
            type: 'button-state-change', 
            attribute: mutation.attributeName,
            value: mutation.target.getAttribute(mutation.attributeName)
          });
        }
      }
    });
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['disabled', 'aria-disabled', 'class']
  });
  
  // Run the test
  const success = await sendGeminiMessage(testMessage);
  
  // Stop monitoring
  observer.disconnect();
  
  // Report results
  console.log("\n" + "=".repeat(50));
  console.log("📊 Test Results:");
  console.log("- Success:", success ? "✅ Yes" : "❌ No");
  console.log("- DOM mutations observed:", mutations.length);
  console.log("- Test message:", testMessage);
  
  if (!success && editor) {
    // Clean up if failed
    console.log("\n🧹 Cleaning up...");
    if (editor.__quill) {
      editor.__quill.setText('');
    } else {
      editor.innerHTML = originalContent;
    }
    editor.dispatchEvent(new Event('input', { bubbles: true }));
  }
  
  console.log("\n✅ Test complete!");
}

// Run test
console.log("\n💡 Commands:");
console.log("- sendGeminiMessage('Your message here')  // Send a message");
console.log("- testGeminiSending()                      // Run automated test");
console.log("\nExample: await sendGeminiMessage('안녕하세요, 오늘 날씨 어때요?')");

// Auto-run test after 2 seconds
console.log("\n⏰ Auto-running test in 2 seconds...");
setTimeout(() => {
  testGeminiSending();
}, 2000);