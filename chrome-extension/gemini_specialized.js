// Gemini Specialized Content Script
// Based on proper Quill editor and Angular Material handling

(function() {
  console.log('🤖 Gemini Specialized script loading...');

  /**
   * Gemini 입력창(Quill Editor)에 텍스트를 입력하는 함수
   * @param {string} text - 입력할 메시지
   */
  function inputTextIntoGemini(text) {
    console.log('📝 Gemini: Inputting text:', text);
    
    // 1. Quill 에디터의 편집 가능 영역을 찾습니다.
    const editor = document.querySelector('div.ql-editor');
    if (!editor) {
      console.error('❌ Gemini 입력창을 찾을 수 없습니다.');
      return false;
    }
    console.log('✅ Found Quill editor');

    // 2. 에디터에 포커스를 줍니다.
    editor.focus();
    console.log('👆 Editor focused');

    // 3. 기존 내용을 지우고 새로운 텍스트를 p 태그로 감싸서 삽입합니다.
    editor.innerHTML = `<p>${text}</p>`;
    console.log('📄 Text inserted with p tag');
    
    // 4. Quill 에디터가 내부적으로 사용하는 Selection을 수동으로 업데이트합니다.
    // 커서를 텍스트 끝으로 이동시킵니다.
    try {
      const range = document.createRange();
      const sel = window.getSelection();
      range.selectNodeContents(editor);
      range.collapse(false); // false는 끝으로 이동
      sel.removeAllRanges();
      sel.addRange(range);
      console.log('🎯 Cursor positioned at end');
    } catch (e) {
      console.warn('⚠️ Selection API failed:', e);
    }

    // 5. React/Angular가 상태 변화를 감지하도록 다양한 이벤트를 발생시킵니다.
    const events = [
      new Event('input', { bubbles: true, cancelable: true }),
      new Event('change', { bubbles: true, cancelable: true }),
      new Event('blur', { bubbles: true, cancelable: true }),
      new InputEvent('input', { 
        inputType: 'insertText', 
        data: text, 
        bubbles: true, 
        cancelable: true 
      })
    ];

    events.forEach(event => {
      editor.dispatchEvent(event);
    });
    console.log('🔄 Events dispatched for Angular detection');

    return true;
  }

  /**
   * 전송 버튼을 찾고 클릭하는 함수
   */
  function clickGeminiSendButton() {
    // 여러 전송 버튼 선택자를 시도합니다 (우선순위 순)
    const buttonSelectors = [
      'button[aria-label="Send message"]',
      'button[aria-label*="전송" i]',
      'button[aria-label*="send" i]',
      'button:has(mat-icon[fonticon="send"])',
      'mat-icon-button[aria-label*="send" i]',
      'button[mattooltip*="send" i]'
    ];

    for (const selector of buttonSelectors) {
      try {
        const button = document.querySelector(selector);
        
        if (button && !button.disabled && !button.hasAttribute('disabled')) {
          // 버튼이 실제로 보이는지 확인
          const rect = button.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            console.log('✅ Found active send button:', selector);
            
            // Enhanced click sequence for Angular Material
            const clickEvents = [
              new PointerEvent('pointerdown', { bubbles: true, cancelable: true }),
              new MouseEvent('mousedown', { bubbles: true, cancelable: true }),
              new PointerEvent('pointerup', { bubbles: true, cancelable: true }),
              new MouseEvent('mouseup', { bubbles: true, cancelable: true }),
              new MouseEvent('click', { bubbles: true, cancelable: true })
            ];

            clickEvents.forEach(event => button.dispatchEvent(event));
            console.log('🖱️ Enhanced click sequence executed');
            return true;
          }
        }
      } catch (e) {
        continue;
      }
    }

    console.log('❌ No active send button found');
    return false;
  }

  /**
   * 전송 버튼이 활성화될 때까지 기다리고 클릭하는 함수
   */
  function waitAndClickSendButton() {
    console.log('⏳ Waiting for send button activation...');
    
    let attempts = 0;
    const maxAttempts = 30; // 30 * 100ms = 3초

    const interval = setInterval(() => {
      attempts++;
      console.log(`🔍 Attempt ${attempts}/${maxAttempts} - Checking button...`);
      
      if (clickGeminiSendButton()) {
        clearInterval(interval);
        console.log('✅ Send button clicked successfully!');
      } else if (attempts >= maxAttempts) {
        clearInterval(interval);
        console.error('❌ 전송 버튼을 활성화하고 클릭하는 데 실패했습니다.');
      }
    }, 100);
  }

  /**
   * 메인 함수: 텍스트를 입력하고 전송하는 전체 과정
   * @param {string} text - 전송할 메시지
   */
  async function sendMessageToGemini(text) {
    console.log('🚀 Starting Gemini message send process...');
    console.log('📝 Message:', text);
    
    // 1. 텍스트 입력
    const inputSuccess = inputTextIntoGemini(text);
    if (!inputSuccess) {
      console.error('❌ Text input failed');
      return false;
    }
    
    // 2. 잠시 대기 (Angular 상태 업데이트를 위해)
    console.log('⏳ Waiting for Angular state update...');
    await new Promise(resolve => setTimeout(resolve, 200));
    
    // 3. 버튼 클릭
    waitAndClickSendButton();
    
    return true;
  }

  /**
   * MutationObserver를 사용한 더 신뢰성 있는 버튼 대기
   */
  function waitForButtonWithObserver(timeout = 5000) {
    return new Promise((resolve, reject) => {
      console.log('👁️ Using MutationObserver for button detection...');
      
      // 즉시 체크
      if (clickGeminiSendButton()) {
        resolve(true);
        return;
      }

      const observer = new MutationObserver((mutations) => {
        // DOM 변화나 속성 변화 감지 시 버튼 상태 재체크
        if (clickGeminiSendButton()) {
          observer.disconnect();
          resolve(true);
        }
      });

      // DOM 변화 관찰 시작
      observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['disabled', 'aria-disabled', 'class']
      });

      // 타임아웃 설정
      setTimeout(() => {
        observer.disconnect();
        console.error('⏰ Button detection timeout');
        reject(new Error('Button detection timeout'));
      }, timeout);
    });
  }

  /**
   * 고급 버전: MutationObserver 사용
   */
  async function sendMessageToGeminiAdvanced(text) {
    console.log('🚀 Advanced Gemini send process...');
    
    try {
      // 1. 텍스트 입력
      const inputSuccess = inputTextIntoGemini(text);
      if (!inputSuccess) throw new Error('Text input failed');
      
      // 2. MutationObserver로 버튼 대기
      await waitForButtonWithObserver(10000);
      console.log('✅ Message sent via advanced method!');
      return true;
      
    } catch (error) {
      console.error('❌ Advanced send failed:', error);
      return false;
    }
  }

  // Chrome extension message listener
  if (typeof chrome !== 'undefined' && chrome.runtime?.onMessage) {
    chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
      if (msg?.type === 'gemini_send') {
        sendMessageToGeminiAdvanced(msg.text)
          .then(success => sendResponse({ success }))
          .catch(error => sendResponse({ success: false, error: error.message }));
        return true; // async response
      }
    });
  }

  // 디버그용 전역 함수들
  window.__geminiSendTest = (text = "[GEMINI TEST] " + new Date().toISOString()) => {
    return sendMessageToGemini(text);
  };

  window.__geminiAdvancedTest = (text = "[ADVANCED TEST] " + new Date().toISOString()) => {
    return sendMessageToGeminiAdvanced(text);
  };

  window.__geminiInputTest = (text = "Input test") => {
    return inputTextIntoGemini(text);
  };

  window.__geminiButtonTest = () => {
    return clickGeminiSendButton();
  };

  console.log('✅ Gemini Specialized script loaded successfully!');
  console.log('💡 Available test functions:');
  console.log('  - __geminiSendTest("message")');
  console.log('  - __geminiAdvancedTest("message")');
  console.log('  - __geminiInputTest("text")');
  console.log('  - __geminiButtonTest()');
})();