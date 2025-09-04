# PowerShell one-shot installer for Chrome extension + GitHub Pages config
$ErrorActionPreference = "Stop"

$root = "C:\Users\8899y\AI-WORKSPACE"
$ext  = Join-Path $root "chrome-extension"
$docs = Join-Path $root "docs"
$cfg  = Join-Path $docs "ai-config"

Write-Host "==&gt; Preparing directories..."
New-Item -ItemType Directory -Path $ext  -Force | Out-Null
New-Item -ItemType Directory -Path $docs -Force | Out-Null
New-Item -ItemType Directory -Path $cfg  -Force | Out-Null

# ---------------------------
# 1) manifest.json (MV3)
# ---------------------------
$manifest = @'
{
  "manifest_version": 3,
  "name": "AI Workspace Controller",
  "version": "1.1.0",
  "description": "AI 협업 릴레이 + 원격 설정 실시간 동기화",
  "permissions": ["storage", "activeTab", "scripting", "alarms", "clipboardWrite", "notifications", "downloads"],
  "host_permissions": [
    "https://chatgpt.com/*",
    "https://claude.ai/*",
    "https://gemini.google.com/*",
    "https://www.perplexity.ai/*",
    "https://manwonyori.github.io/*"
  ],
  "background": { "service_worker": "background.js", "type": "module" },
  "action": { "default_popup": "popup.html" },
  "content_scripts": [
    {
      "matches": [
        "https://chatgpt.com/*",
        "https://claude.ai/*",
        "https://gemini.google.com/*",
        "https://www.perplexity.ai/*"
      ],
      "js": ["content.js"],
      "run_at": "document_idle",
      "all_frames": false
    }
  ]
}
'@
Set-Content -LiteralPath (Join-Path $ext "manifest.json") -Value $manifest -Encoding UTF8

# ---------------------------
# 2) background.js
# ---------------------------
$background = @'
const CFG = {
  base: "https://manwonyori.github.io/-AI-WORKSPACE/ai-config/",
  files: ["agents.json","prompts.json","selectors.json","rules.json"]
};

let etags = {};

async function fetchConfig(name) {
  const url = CFG.base + name;
  const headers = etags[name] ? { "If-None-Match": etags[name] } : {};
  const res = await fetch(url, { headers });
  if (res.status === 304) return null;
  if (!res.ok) throw new Error(`fetch ${name} ${res.status}`);
  const etag = res.headers.get("ETag");
  if (etag) etags[name] = etag;
  return await res.json();
}

async function syncAll() {
  const updated = {};
  for (const f of CFG.files) {
    try {
      const data = await fetchConfig(f);
      if (data) updated[f.replace(".json","")] = data;
    } catch (e) {
      console.warn("sync error:", f, e);
    }
  }
  if (Object.keys(updated).length) {
    await chrome.storage.local.set(updated);
    console.log("Config updated:", Object.keys(updated));
    chrome.runtime.sendMessage({ action: "configUpdated", keys: Object.keys(updated) });
  }
}

chrome.runtime.onInstalled.addListener(() => {
  syncAll();
  chrome.alarms.create("sync", { periodInMinutes: 5 });
});
chrome.runtime.onStartup.addListener(() => {
  syncAll();
  chrome.alarms.create("sync", { periodInMinutes: 5 });
});
chrome.alarms.onAlarm.addListener(alarm => {
  if (alarm.name === "sync") syncAll();
});

const URLS = {
  chatgpt: "https://chatgpt.com/",
  claude: "https://claude.ai/",
  gemini: "https://gemini.google.com/app",
  perplexity: "https://www.perplexity.ai/"
};

async function ensureTabFor(agent) {
  const url = URLS[agent];
  if (!url) throw new Error("Unknown agent: " + agent);
  const tabs = await chrome.tabs.query({ url: url + "*" });
  if (tabs.length) return tabs[0].id;
  const tab = await chrome.tabs.create({ url });
  return tab.id;
}

const ALLOW_TO = new Set(["chatgpt","claude","gemini","perplexity"]);
const ALLOW_ACTION = new Set(["input","send","inputAndSend","clear","getResponse"]);
const lastRun = new Map();

async function routeCommand(cmd) {
  const stored = await chrome.storage.local.get("rules");
  const rules = stored?.rules || {};
  const rate = rules.rateLimitMs ?? 2000;

  if (!ALLOW_TO.has(cmd.to) || !ALLOW_ACTION.has(cmd.action)) return { ok:false, reason:"blocked" };

  const now = Date.now();
  const prev = lastRun.get(cmd.to) || 0;
  if (now - prev &lt; rate) return { ok:false, reason:"rate-limit" };
  lastRun.set(cmd.to, now);

  const tabId = await ensureTabFor(cmd.to);
  const payload = cmd.payload || {};
  const res = await chrome.tabs.sendMessage(tabId, { action: cmd.action, text: payload.text });
  return { ok: !!res?.success, platform: res?.platform };
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  (async () => {
    if (msg?.action === "commandDetected") {
      const result = await routeCommand(msg.command);
      sendResponse(result);
    }
    if (msg?.action === "syncNow") {
      await syncAll();
      sendResponse({ ok: true });
    }
    if (msg?.action === "getConfig") {
      const data = await chrome.storage.local.get(["agents","prompts","selectors","rules"]);
      sendResponse(data);
    }
  })();
  return true;
});
'@
Set-Content -LiteralPath (Join-Path $ext "background.js") -Value $background -Encoding UTF8

# ---------------------------
# 3) content.js (enhanced)
# ---------------------------
$content = @'
const platform = detectPlatform();

function detectPlatform() {
  const hostname = window.location.hostname;
  if (hostname.includes("chatgpt.com")) return "chatgpt";
  if (hostname.includes("claude.ai")) return "claude";
  if (hostname.includes("gemini.google.com")) return "gemini";
  if (hostname.includes("perplexity.ai")) return "perplexity";
  return null;
}

// Platform-specific selectors (externalizable)
const SELECTORS = {
  chatgpt: {
    input: "#prompt-textarea, textarea[data-id=\\"root\\"]",
    button: "button[data-testid=\\"send-button\\"], button[aria-label=\\"Send message\\"], form button[type=\\"submit\\"]",
    container: "main"
  },
  claude: {
    input: "div[contenteditable=\\"true\\"].ProseMirror, div[contenteditable=\\"true\\"]",
    button: "button[aria-label=\\"Send Message\\"], form button[type=\\"submit\\"]",
    container: "main"
  },
  gemini: {
    input: "textarea, [contenteditable=\\"true\\"]",
    button: "button[aria-label*=\\"Send\\"], form button[type=\\"submit\\"], button[aria-label*=\\"작성\\"]",
    container: "main"
  },
  perplexity: {
    input: "textarea[placeholder*=\\"Ask\\"], textarea, [contenteditable=\\"true\\"]",
    button: "button[aria-label=\\"Submit\\"], button.bg-super, form button[type=\\"submit\\"]",
    container: "main"
  }
};

// Chunk size per platform (raised)
const CHUNK_LIMIT = {
  chatgpt: 4500,
  claude: 4500,
  gemini: 3200,
  perplexity: 3800,
  default: 3000
};

async function chunkedInsert(inputEl, text, limit) {
  const chunks = [];
  for (let i = 0; i &lt; text.length; i += limit) chunks.push(text.slice(i, i + limit));
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
    await new Promise(r =&gt; setTimeout(r, 180));
  }
  return true;
}

async function autoInput(text) {
  const selector = SELECTORS[platform];
  if (!selector) return false;
  const input = document.querySelector(selector.input);
  if (!input) return false;
  const limit = CHUNK_LIMIT[platform] || CHUNK_LIMIT.default;
  return await chunkedInsert(input, text, limit);
}

function sendMessage() {
  const selector = SELECTORS[platform];
  if (!selector) return false;

  const button = document.querySelector(selector.button);
  if (button &amp;&amp; !button.disabled) {
    button.click();
    return true;
  }

  const input = document.querySelector(selector.input);
  if (input) {
    const enterEvent = new KeyboardEvent("keydown", {
      key: "Enter",
      code: "Enter",
      keyCode: 13,
      which: 13,
      bubbles: true,
      cancelable: true
    });
    input.dispatchEvent(enterEvent);
    return true;
  }
  return false;
}

function getLastResponse() {
  let response = "";
  if (platform === "chatgpt") {
    const messages = document.querySelectorAll('[data-message-author-role="assistant"]');
    if (messages.length) response = messages[messages.length - 1].textContent || "";
  } else if (platform === "claude") {
    const messages = document.querySelectorAll("[data-test-render-count]");
    if (messages.length) response = messages[messages.length - 1].textContent || "";
  } else if (platform === "gemini") {
    // best-effort selector (may change)
    const messages = document.querySelectorAll("main, c-wiz, div");
    if (messages.length) response = messages[messages.length - 1].textContent || "";
  } else if (platform === "perplexity") {
    const messages = document.querySelectorAll(".prose");
    if (messages.length) response = messages[messages.length - 1].textContent || "";
  }
  return response;
}

function extractCommandFromText(txt) {
  const m = txt.match(/```json([\\s\\S]*?)```/);
  const raw = (m ? m[1] : txt).trim();
  try {
    const obj = JSON.parse(raw);
    if (obj &amp;&amp; obj.type === "command" &amp;&amp; obj.to &amp;&amp; obj.action) return obj;
  } catch {}
  return null;
}

async function detectAndRelayCommand() {
  const resp = getLastResponse();
  if (!resp) return;
  const cmd = extractCommandFromText(resp);
  if (cmd) {
    chrome.runtime.sendMessage({ action: "commandDetected", command: cmd }, () =&gt; {});
  }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) =&gt; {
  (async () =&gt; {
    if (request.action === "input") {
      const ok = await autoInput(request.text);
      sendResponse({ success: ok, platform });
      return;
    }
    if (request.action === "send") {
      const ok = sendMessage();
      sendResponse({ success: ok, platform });
      return;
    }
    if (request.action === "inputAndSend") {
      const ok1 = await autoInput(request.text);
      setTimeout(() =&gt; {
        const ok2 = sendMessage();
        sendResponse({ success: ok1 &amp;&amp; ok2, platform });
      }, 400);
      return true;
    }
    if (request.action === "getResponse") {
      const response = getLastResponse();
      sendResponse({ response, platform });
      setTimeout(detectAndRelayCommand, 300);
      return;
    }
    if (request.action === "clear") {
      const input = document.querySelector(SELECTORS[platform]?.input);
      if (input) {
        if (platform === "claude") input.innerHTML = "";
        else input.value = "";
        input.dispatchEvent(new Event("input", { bubbles: true }));
      }
      sendResponse({ success: true, platform });
      return;
    }
    if (request.action === "status") {
      sendResponse({ platform, ready: !!document.querySelector(SELECTORS[platform]?.input), url: location.href });
      return;
    }
  })();
  return true;
});

// Visual indicator
(function () {
  const indicator = document.createElement("div");
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
  indicator.textContent = \`🤖 \${(platform||"AI").toUpperCase()} Ready\`;
  indicator.title = "AI Workspace Controller Active";
  indicator.addEventListener("click", () =&gt; chrome.runtime.sendMessage({ action: "openPopup" }));
  document.addEventListener("DOMContentLoaded", () =&gt; {
    try { document.body.appendChild(indicator); } catch {}
  });
})();
'@
Set-Content -LiteralPath (Join-Path $ext "content.js") -Value $content -Encoding UTF8

# ---------------------------
# 4) popup.html
# ---------------------------
$popupHtml = @'
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>AI Workspace</title>
<style>
  body { font-family: system-ui; width: 320px; padding: 12px; }
  button { padding: 8px 10px; border-radius: 8px; border: 1px solid #ddd; cursor: pointer; margin-right: 6px; margin-bottom: 8px; }
  #status { font-size: 12px; opacity: 0.8; margin-top: 8px; white-space: pre-line; }
  .row { margin-bottom: 8px; }
</style>
</head>
<body>
  <h3>AI Workspace</h3>
  <div class="row">
    <button id="btnSync">Sync Config</button>
    <button id="btnStatus">Status</button>
    <button id="btnExport">Export Logs</button>
  </div>
  <div id="status">준비됨</div>
  <script src="popup.js"></script>
</body>
</html>
'@
Set-Content -LiteralPath (Join-Path $ext "popup.html") -Value $popupHtml -Encoding UTF8

# ---------------------------
# 5) popup.js
# ---------------------------
$popupJs = @'
async function sendToActive(action, payload = {}) {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) return { ok: false };
  try {
    const res = await chrome.tabs.sendMessage(tab.id, { action, ...payload });
    return res;
  } catch {
    return { ok: false };
  }
}

document.getElementById("btnSync").addEventListener("click", async () => {
  const res = await chrome.runtime.sendMessage({ action: "syncNow" });
  document.getElementById("status").textContent = res?.ok ? "✅ Config synced" : "❌ Sync failed";
});

document.getElementById("btnStatus").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) return;
  const res = await chrome.tabs.sendMessage(tab.id, { action: "status" });
  document.getElementById("status").textContent = res?.ready ? `🟢 ${res.platform} ready\n${res.url}` : `🔴 Not ready`;
});

document.getElementById("btnExport").addEventListener("click", async () => {
  const cfg = await chrome.runtime.sendMessage({ action: "getConfig" });
  const blob = new Blob([JSON.stringify({ exportedAt: new Date().toISOString(), cfg }, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  // Requires "downloads" permission if you want to avoid saveAs prompt by policy
  chrome.downloads?.download?.({ url, filename: "ai-workspace-export.json", saveAs: true });
});
'@
Set-Content -LiteralPath (Join-Path $ext "popup.js") -Value $popupJs -Encoding UTF8

# ---------------------------
# 6) GitHub Pages 준비 배치 (선택 실행)
# ---------------------------
$setupBat = @'
@echo off
chcp 65001 >nul
cd /d "C:\Users\8899y\AI-WORKSPACE"

if not exist docs mkdir docs
if not exist docs\ai-config mkdir docs\ai-config

> docs\index.md echo ---
>> docs\index.md echo layout: default
>> docs\index.md echo title: AI-WORKSPACE Config
>> docs\index.md echo ---
>> docs\index.md echo.
>> docs\index.md echo # AI-WORKSPACE Remote Config
>> docs\index.md echo - [agents.json](./ai-config/agents.json)
>> docs\index.md echo - [prompts.json](./ai-config/prompts.json)
>> docs\index.md echo - [rules.json](./ai-config/rules.json)
>> docs\index.md echo - [selectors.json](./ai-config/selectors.json)

> docs\ai-config\agents.json echo {^
"order":["chatgpt","claude","gemini","perplexity"],^
"maxTurns":24,^
"backoffMs":{"min":2000,"max":6000},^
"loopGuard":{"window":5,"similarity":0.96}^
}

> docs\ai-config\prompts.json echo {^
"primary":"프리미엄 상세페이지 템플릿 기준으로 요약 후 다음 질문 1개만 제시.",^
"secondary":"톤은 고급·희소성·신뢰 중심. CTA 3안.",^
"handoff":"[turn:{turn}] from:{from} → to:{to} | 최근 요약(1~2줄) 후 다음 질문 1개만."^
}

> docs\ai-config\rules.json echo {^
"allow":{"to":["chatgpt","claude","gemini","perplexity"],"actions":["input","send","inputAndSend","clear","getResponse"]},^
"rateLimitMs":2000,^
"stop":{"maxTurns":24,"stopWords":["ERROR:","TERMS VIOLATION"],"timeoutMs":45000}^
}

> docs\ai-config\selectors.json echo {^
"chatgpt":{"input":"#prompt-textarea, textarea[data-id=\\"root\\"]","button":"button[data-testid=\\"send-button\\"], button[aria-label=\\"Send message\\"], form button[type=\\"submit\\"]"},^
"claude":{"input":"div[contenteditable=\\"true\\"].ProseMirror, div[contenteditable=\\"true\\"]","button":"button[aria-label=\\"Send Message\\"], form button[type=\\"submit\\"]"},^
"gemini":{"input":"textarea, [contenteditable=\\"true\\"]","button":"button[aria-label*=\\"Send\\"], form button[type=\\"submit\\"], button[aria-label*=\\"작성\\"]"},^
"perplexity":{"input":"textarea[placeholder*=\\"Ask\\"], textarea, [contenteditable=\\"true\\"]","button":"button[aria-label=\\"Submit\\"], button.bg-super, form button[type=\\"submit\\"]"}^
}

git add docs
git commit -m "chore(pages): add /docs + /docs/ai-config for extension remote config"
git push -u origin main

echo.
echo ✅ /docs 세트가 커밋/푸시되었습니다. 
echo ➜ 레포 Settings → Pages → Branch: main / Folder: /docs 설정 후 'Your site is live' 상태를 확인하세요.
'@
Set-Content -LiteralPath (Join-Path $root "setup_pages.bat") -Value $setupBat -Encoding UTF8

Write-Host "==&gt; Done. Files written:"
Get-ChildItem $ext | Select-Object Name, Length, LastWriteTime
Write-Host "==&gt; Also wrote: $($root)\setup_pages.bat"
'