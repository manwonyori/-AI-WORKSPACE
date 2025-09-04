// ChatGPT Specialized Content Script
// Based on proven solutions for ChatGPT DOM/Event issues

(function() {
  const RETRY_MS = 300;
  const TIMEOUT_MS = 8000;

  function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

  function findComposer() {
    const ta = document.querySelector('#prompt-textarea') ||
               document.querySelector('textarea[aria-label*="message" i]') ||
               document.querySelector('textarea[placeholder*="message" i]') ||
               document.querySelector('textarea');
    if (ta) return { type: 'textarea', el: ta };

    const ed = document.querySelector('[contenteditable="true"][data-testid]') ||
               document.querySelector('[contenteditable="true"][aria-label*="message" i]') ||
               document.querySelector('[contenteditable="true"]');
    if (ed) return { type: 'editable', el: ed };

    return null;
  }

  function nativeSetValue(el, text) {
    const win = el.ownerDocument?.defaultView || window;
    if (el.tagName === 'TEXTAREA') {
      const desc = Object.getOwnPropertyDescriptor(win.HTMLTextAreaElement.prototype, 'value');
      desc?.set?.call(el, text);
    } else {
      el.textContent = text;
    }
  }

  function fireTypingEvents(el) {
    const ev = (type, opts={}) => el.dispatchEvent(new Event(type, { bubbles: true, cancelable: true, ...opts }));
    const kev = (type, init={}) => el.dispatchEvent(new KeyboardEvent(type, { bubbles: true, cancelable: true, ...init }));
    el.focus();
    ev('beforeinput');
    ev('input');
    ev('compositionend');
    kev('keydown', { key: 'Unidentified' });
    kev('keyup', { key: 'Unidentified' });
  }

  function findSendButton() {
    const candidates = [
      'button[data-testid="send-button"]',
      'button[aria-label*="send" i]',
      'button[title*="send" i]',
      'form button[type="submit"]',
    ];
    for (const sel of candidates) {
      const b = document.querySelector(sel);
      if (b) return b;
    }
    const svg = Array.from(document.querySelectorAll('svg,path')).find(n => (n.getAttribute('d') || '').includes('16V6.414'));
    if (svg) {
      const btn = svg.closest('button');
      if (btn) return btn;
    }
    return document.querySelector('[role="button"]');
  }

  function clickSend(btn) {
    const ev = (type) => btn.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true, view: window }));
    ev('pointerdown'); ev('mousedown'); ev('pointerup'); ev('mouseup'); ev('click');
  }

  async function ensureReady(selector, timeoutMs = TIMEOUT_MS) {
    const start = Date.now();
    while (Date.now() - start < timeoutMs) {
      const el = typeof selector === 'function' ? selector() : document.querySelector(selector);
      if (el) return el;
      await delay(RETRY_MS);
    }
    return null;
  }

  // 외부(background/popup)에서 메시지 받기: { type: 'gpt_send', text: '...' }
  chrome.runtime?.onMessage?.addListener((msg, _sender, sendResponse) => {
    if (msg?.type === 'gpt_send') {
      sendText(msg.text).then(ok => sendResponse({ ok })).catch(e => sendResponse({ ok:false, error: String(e) }));
      return true; // async
    }
  });

  async function sendText(text) {
    console.log('🚀 ChatGPT Specialized: Sending text:', text);
    
    // 오버레이 닫기 시도 (선택적으로 커스텀)
    const overlayClose = document.querySelector('button[aria-label*="close" i], [data-testid*="close"]');
    if (overlayClose) {
      console.log('📱 Closing overlay/modal');
      overlayClose.click();
      await delay(200);
    }

    const comp = await ensureReady(findComposer);
    if (!comp) throw new Error('Composer not found');
    
    console.log('✅ Found composer:', comp.type, comp.el);

    nativeSetValue(comp.el, text);
    fireTypingEvents(comp.el);
    console.log('📝 Text set and events fired');
    
    await delay(150);

    const btn = await ensureReady(findSendButton);
    if (!btn) throw new Error('Send button not found');
    
    console.log('✅ Found send button:', btn);

    clickSend(btn);
    console.log('🎯 Send button clicked');
    
    return true;
  }

  // 디버그용: 콘솔에서 테스트
  window.__gptSendTest = (t = "[SPECIALIZED TEST] " + new Date().toISOString()) => sendText(t);
  
  console.log('🤖 ChatGPT Specialized script loaded');
  console.log('💡 Test with: __gptSendTest("Hello World")');
})();