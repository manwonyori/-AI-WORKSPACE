// Content script (robust domain detection + chunked input)
function detectPlatform() {
  const h = location.hostname;
  if (h.includes("chatgpt.com")) return "chatgpt";
  if (h.includes("claude.ai")) return "claude";
  if (h.includes("perplexity.ai")) return "perplexity";
  if (h === "gemini.google.com" || (h.endsWith(".google.com") && location.pathname.startsWith("/app"))) return "gemini";
  return null;
}
const platform = detectPlatform();

const SELECTORS = {
  chatgpt: {
    input: "#prompt-textarea, textarea[data-id=\"root\"]",
    button: "button[data-testid=\"send-button\"], button[aria-label=\"Send message\"], form button[type=\"submit\"]",
    container: "main"
  },
  claude: {
    input: "div[contenteditable=\"true\"].ProseMirror, div[contenteditable=\"true\"]",
    button: "button[aria-label=\"Send Message\"], form button[type=\"submit\"]",
    container: "main"
  },
  gemini: {
    input: "textarea, [contenteditable=\"true\"]",
    button: "button[aria-label*=\"Send\"], form button[type=\"submit\"], button[aria-label*=\"작성\"]",
    container: "main"
  },
  perplexity: {
    input: "textarea[placeholder*=\"Ask\"], textarea, [contenteditable=\"true\"]",
    button: "button[aria-label=\"Submit\"], button.bg-super, form button[type=\"submit\"]",
    container: "main"
  }
};

const CHUNK_LIMIT = { chatgpt: 4500, claude: 4500, gemini: 3200, perplexity: 3800, default: 3000 };

async function chunkedInsert(inputEl, text, limit) {
  const chunks = [];
  for (let i = 0; i < text.length; i += limit) chunks.push(text.slice(i, i + limit));
  for (const part of chunks) {
    if (inputEl.tagName === "TEXTAREA") {
      const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
      setter.call(inputEl, (inputEl.value || "") + part);
      inputEl.dispatchEvent(new Event("input", { bubbles: true }));
      inputEl.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      inputEl.focus();
      document.execCommand("insertText", false, part);
      inputEl.dispatchEvent(new InputEvent("input", { bubbles: true, data: part, inputType: "insertText" }));
    }
    await new Promise(r => setTimeout(r, 180));
  }
  return true;
}

async function autoInput(text) {
  const sel = SELECTORS[platform];
  if (!sel) return false;
  const input = document.querySelector(sel.input);
  if (!input) return false;
  const limit = CHUNK_LIMIT[platform] || CHUNK_LIMIT.default;
  return await chunkedInsert(input, text, limit);
}

function sendMessage() {
  const sel = SELECTORS[platform];
  if (!sel) return false;
  const btn = document.querySelector(sel.button);
  if (btn && !btn.disabled) { btn.click(); return true; }
  const input = document.querySelector(sel.input);
  if (input) {
    const e = new KeyboardEvent("keydown", { key: "Enter", code: "Enter", keyCode: 13, which: 13, bubbles: true, cancelable: true });
    input.dispatchEvent(e);
    return true;
  }
  return false;
}

function getLastResponse() {
  let t = "";
  if (platform === "chatgpt") {
    const m = document.querySelectorAll('[data-message-author-role="assistant"]'); if (m.length) t = m[m.length-1].textContent || "";
  } else if (platform === "claude") {
    const m = document.querySelectorAll("[data-test-render-count]"); if (m.length) t = m[m.length-1].textContent || "";
  } else if (platform === "gemini") {
    const m = document.querySelectorAll("main, c-wiz, div[aria-live]"); if (m.length) t = m[m.length-1].textContent || "";
  } else if (platform === "perplexity") {
    const m = document.querySelectorAll(".prose"); if (m.length) t = m[m.length-1].textContent || "";
  }
  return t;
}

function extractCommandFromText(s) {
  const m = s.match(/```json([\s\S]*?)```/);
  const raw = (m ? m[1] : s).trim();
  try { const o = JSON.parse(raw); if (o && o.type === "command" && o.to && o.action) return o; } catch {}
  return null;
}

async function detectAndRelayCommand() {
  const r = getLastResponse();
  if (!r) return;
  const cmd = extractCommandFromText(r);
  if (cmd) chrome.runtime.sendMessage({ action: "commandDetected", command: cmd }, () => {});
}

chrome.runtime.onMessage.addListener((req, _sender, sendResponse) => {
  (async () => {
    if (req.action === "input") { const ok = await autoInput(req.text); sendResponse({ success: ok, platform }); return; }
    if (req.action === "send") { const ok = sendMessage(); sendResponse({ success: ok, platform }); return; }
    if (req.action === "inputAndSend") {
      const ok1 = await autoInput(req.text);
      setTimeout(() => { const ok2 = sendMessage(); sendResponse({ success: ok1 && ok2, platform }); }, 400);
      return true;
    }
    if (req.action === "getResponse") { const response = getLastResponse(); sendResponse({ response, platform }); setTimeout(detectAndRelayCommand, 300); return; }
    if (req.action === "clear") {
      const input = document.querySelector(SELECTORS[platform]?.input);
      if (input) { if (platform === "claude") input.innerHTML = ""; else input.value = ""; input.dispatchEvent(new Event("input", { bubbles: true })); }
      sendResponse({ success: true, platform });
      return;
    }
    if (req.action === "status") { sendResponse({ platform, ready: !!document.querySelector(SELECTORS[platform]?.input), url: location.href }); return; }
    if (req.action === "configUpdate") {
      console.log(`[${platform}] Config updated:`, req.config);
      sendResponse({ success: true, platform });
      return;
    }
  })();
  return true;
});

// Badge (ready)
(function () {
  const badge = document.createElement("div");
  badge.style.cssText = "position:fixed;bottom:20px;right:20px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:8px 15px;border-radius:20px;font-size:12px;z-index:999999;opacity:.9;cursor:pointer;font-family:system-ui;";
  badge.textContent = "🤖 " + (platform ? platform.toUpperCase() : "AI") + " Ready";
  badge.title = "AI Workspace Controller Active";
  badge.addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "openPopup" });
  });
  document.addEventListener("DOMContentLoaded", () => { try { document.body.appendChild(badge); } catch {} });
  // Fallback for already loaded pages
  if (document.readyState === "complete") {
    try { document.body.appendChild(badge); } catch {}
  }
})();

console.log(`[${platform}] Content script loaded (chunk-safe) and ready`);