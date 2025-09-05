# Patch manifest/background/popup to fix red status dots
$ErrorActionPreference = "Stop"
$root = "C:\Users\8899y\AI-WORKSPACE\chrome-extension"

if (!(Test-Path $root)) { throw "chrome-extension folder not found: $root" }

# 1) manifest.json — add "tabs" permission
$manifest = @'
{
  "manifest_version": 3,
  "name": "AI Workspace Controller",
  "version": "1.1.2",
  "description": "AI 협업 릴레이 + 원격 설정 실시간 동기화",
  "permissions": ["storage", "activeTab", "scripting", "alarms", "clipboardWrite", "notifications", "downloads", "tabs"],
  "host_permissions": [
    "https://chat.openai.com/*",
    "https://chatgpt.com/*",
    "https://*.chatgpt.com/*",
    "https://claude.ai/*",
    "https://*.claude.ai/*",
    "https://gemini.google.com/*",
    "https://*.google.com/*",
    "https://perplexity.ai/*",
    "https://www.perplexity.ai/*",
    "https://*.perplexity.ai/*",
    "https://manwonyori.github.io/*"
  ],
  "background": { "service_worker": "background.js", "type": "module" },
  "action": { "default_popup": "popup.html" },
  "content_scripts": [
    {
      "matches": [
        "https://chat.openai.com/*",
        "https://chatgpt.com/*",
        "https://*.chatgpt.com/*",
        "https://claude.ai/*",
        "https://*.claude.ai/*",
        "https://gemini.google.com/*",
        "https://*.google.com/*",
        "https://perplexity.ai/*",
        "https://www.perplexity.ai/*",
        "https://*.perplexity.ai/*"
      ],
      "js": ["content.js"],
      "run_at": "document_end",
      "all_frames": true
    }
  ]
}
'@
Set-Content -LiteralPath (Join-Path $root "manifest.json") -Value $manifest -Encoding UTF8

# 2) background.js — add openAll/statusAll
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
    } catch (e) { console.warn("sync error:", f, e); }
  }
  if (Object.keys(updated).length) {
    await chrome.storage.local.set(updated);
    chrome.runtime.sendMessage({ action: "configUpdated", keys: Object.keys(updated) });
  }
}
chrome.runtime.onInstalled.addListener(() => { syncAll(); chrome.alarms.create("sync", { periodInMinutes: 5 }); });
chrome.runtime.onStartup.addListener(() => { syncAll(); chrome.alarms.create("sync", { periodInMinutes: 5 }); });
chrome.alarms.onAlarm.addListener(a => { if (a.name === "sync") syncAll(); });

const URLS = {
  chatgpt: "https://chatgpt.com/",
  openai:  "https://chat.openai.com/",
  claude:  "https://claude.ai/",
  gemini:  "https://gemini.google.com/app",
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
  const rules = (await chrome.storage.local.get("rules"))?.rules || {};
  const rate = rules.rateLimitMs ?? 2000;
  if (!ALLOW_TO.has(cmd.to) || !ALLOW_ACTION.has(cmd.action)) return { ok:false, reason:"blocked" };
  const now = Date.now(); const prev = lastRun.get(cmd.to) || 0;
  if (now - prev &lt; rate) return { ok:false, reason:"rate-limit" };
  lastRun.set(cmd.to, now);
  const tabId = await ensureTabFor(cmd.to);
  const payload = cmd.payload || {};
  const res = await chrome.tabs.sendMessage(tabId, { action: cmd.action, text: payload.text });
  return { ok: !!res?.success, platform: res?.platform };
}

async function openAll() {
  const agents = ["chatgpt","claude","gemini","perplexity"];
  const results = {};
  for (const a of agents) {
    try { results[a] = { ok: true, tabId: await ensureTabFor(a) }; }
    catch (e) { results[a] = { ok: false, error: String(e) }; }
  }
  return results;
}

async function statusAll() {
  const agents = ["chatgpt","claude","gemini","perplexity"];
  const statuses = {};
  for (const a of agents) {
    const url = URLS[a];
    const tabs = await chrome.tabs.query({ url: url + "*" });
    if (!tabs.length) { statuses[a] = { ready:false, reason:"no-tab" }; continue; }
    try {
      const res = await chrome.tabs.sendMessage(tabs[0].id, { action: "status" });
      statuses[a] = { ready: !!res?.ready, platform: res?.platform, url: res?.url || url };
    } catch (e) {
      statuses[a] = { ready:false, reason: "no-content-script" };
    }
  }
  return statuses;
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  (async () => {
    if (msg?.action === "commandDetected") { sendResponse(await routeCommand(msg.command)); }
    if (msg?.action === "syncNow")        { await syncAll(); sendResponse({ ok: true }); }
    if (msg?.action === "getConfig")      { sendResponse(await chrome.storage.local.get(["agents","prompts","selectors","rules"])); }
    if (msg?.action === "openAll")        { sendResponse(await openAll()); }
    if (msg?.action === "statusAll")      { sendResponse(await statusAll()); }
  })();
  return true;
});
'@
Set-Content -LiteralPath (Join-Path $root "background.js") -Value $background -Encoding UTF8

# 3) popup.js — use openAll/statusAll to paint real status
$popup = @'
const dot = (ok) => ok ? "🟢" : "🔴";
const id = (k) => document.getElementById(k);

async function refreshStatus() {
  id("statusBar").textContent = "Checking platform status...";
  const res = await chrome.runtime.sendMessage({ action: "statusAll" });
  if (!res) { id("statusBar").textContent = "Failed to get status"; return; }
  id("dotChatGPT").textContent = dot(res.chatgpt?.ready);
  id("dotClaude").textContent = dot(res.claude?.ready);
  id("dotPerplexity").textContent = dot(res.perplexity?.ready);
  id("dotGemini").textContent = dot(res.gemini?.ready);
  id("statusBar").textContent = "Status updated";
}

id("btnOpenAll")?.addEventListener("click", async () => {
  await chrome.runtime.sendMessage({ action: "openAll" });
  setTimeout(refreshStatus, 1500);
});
id("btnCheckStatus")?.addEventListener("click", refreshStatus);
id("btnSync")?.addEventListener("click", async () => {
  await chrome.runtime.sendMessage({ action: "syncNow" });
  id("statusBar").textContent = "✅ Config synced";
});

// initial
setTimeout(refreshStatus, 400);
'@
# Note: assumes popup.html has elements: dotChatGPT/dotClaude/dotPerplexity/dotGemini, btnOpenAll/btnCheckStatus/btnSync, statusBar
Set-Content -LiteralPath (Join-Path $root "popup.js") -Value $popup -Encoding UTF8

Write-Host "Patched manifest/background/popup. Reload the extension in chrome://extensions ."