// AI Workspace Controller Popup Script
const dot = (ok) => ok ? "🟢" : "🔴";
const id = (k) => document.getElementById(k);

async function refreshStatus() {
  const statusBar = id("statusBar");
  if (statusBar) statusBar.textContent = "Checking platform status...";
  
  try {
    const res = await chrome.runtime.sendMessage({ action: "statusAll" });
    console.log("Full status response:", res);
    
    if (!res) {
      if (statusBar) statusBar.textContent = "Failed to get status";
      return;
    }
    
    // Debug each platform status
    console.log("ChatGPT status:", res.chatgpt);
    console.log("Claude status:", res.claude);
    console.log("Perplexity status:", res.perplexity);
    console.log("Gemini status:", res.gemini);
    
    // Update dots
    const chatDot = id("dotChatGPT");
    const claudeDot = id("dotClaude");
    const perplexityDot = id("dotPerplexity");
    const geminiDot = id("dotGemini");
    
    if (chatDot) {
      chatDot.textContent = dot(res.chatgpt?.ready);
      console.log("ChatGPT dot set to:", res.chatgpt?.ready ? "🟢" : "🔴");
    }
    if (claudeDot) {
      claudeDot.textContent = dot(res.claude?.ready);
      console.log("Claude dot set to:", res.claude?.ready ? "🟢" : "🔴");
    }
    if (perplexityDot) {
      perplexityDot.textContent = dot(res.perplexity?.ready);
      console.log("Perplexity dot set to:", res.perplexity?.ready ? "🟢" : "🔴");
    }
    if (geminiDot) {
      geminiDot.textContent = dot(res.gemini?.ready);
      console.log("Gemini dot set to:", res.gemini?.ready ? "🟢" : "🔴");
    }
    
    if (statusBar) statusBar.textContent = "Status updated";
  } catch (error) {
    console.error("Status check error:", error);
    if (statusBar) statusBar.textContent = "Error checking status";
  }
}

// Event listeners
const btnOpenAll = id("btnOpenAll");
const btnCheckStatus = id("btnCheckStatus");
const btnSync = id("btnSync");
const btnSendAll = id("btnSendAll");
const btnDebug = id("btnDebug");
const messageInput = id("messageInput");

if (btnOpenAll) {
  btnOpenAll.addEventListener("click", async () => {
    try {
      await chrome.runtime.sendMessage({ action: "openAll" });
      setTimeout(refreshStatus, 2000);
    } catch (error) {
      console.error("Open all error:", error);
    }
  });
}

if (btnCheckStatus) {
  btnCheckStatus.addEventListener("click", refreshStatus);
}

if (btnSync) {
  btnSync.addEventListener("click", async () => {
    try {
      await chrome.runtime.sendMessage({ action: "syncNow" });
      const statusBar = id("statusBar");
      if (statusBar) statusBar.textContent = "✅ Config synced";
    } catch (error) {
      console.error("Sync error:", error);
    }
  });
}

if (btnDebug) {
  btnDebug.addEventListener("click", async () => {
    // Open developer tools for popup
    chrome.tabs.create({ url: 'chrome://extensions/?id=' + chrome.runtime.id });
    
    // Also send a debug test to each platform
    try {
      const tabs = await chrome.tabs.query({});
      const statusBar = id("statusBar");
      
      for (const tab of tabs) {
        if (tab.url && (
          tab.url.includes("chatgpt.com") || 
          tab.url.includes("claude.ai") || 
          tab.url.includes("perplexity.ai") ||
          tab.url.includes("gemini.google.com") ||
          tab.url.includes("aistudio.google.com")
        )) {
          try {
            const response = await chrome.tabs.sendMessage(tab.id, { action: "status" });
            console.log(`Direct test to tab ${tab.id} (${new URL(tab.url).hostname}):`, response);
          } catch (e) {
            console.error(`Failed to send to tab ${tab.id}:`, e);
          }
        }
      }
      
      if (statusBar) statusBar.textContent = "Debug info in console (F12)";
    } catch (error) {
      console.error("Debug error:", error);
    }
  });
}

if (btnSendAll && messageInput) {
  btnSendAll.addEventListener("click", async () => {
    const message = messageInput.value.trim();
    const statusBar = id("statusBar");
    
    if (!message) {
      if (statusBar) statusBar.textContent = "❌ Please enter a message";
      return;
    }
    
    if (statusBar) statusBar.textContent = "📤 Sending to all platforms...";
    
    try {
      const response = await chrome.runtime.sendMessage({ 
        action: "sendToAll", 
        message: message 
      });
      
      if (statusBar) {
        if (response && response.success) {
          statusBar.textContent = "✅ Message sent to all platforms";
          messageInput.value = ""; // Clear input
        } else {
          statusBar.textContent = "⚠️ Some platforms failed";
        }
      }
    } catch (error) {
      console.error("Send error:", error);
      if (statusBar) statusBar.textContent = "❌ Send failed";
    }
  });
}

// Initialize on load
document.addEventListener("DOMContentLoaded", () => {
  console.log("Popup loaded");
  // Initial check after a short delay
  setTimeout(refreshStatus, 1000);
  // Second check for slower loading tabs
  setTimeout(refreshStatus, 2500);
});

// Also check when popup becomes visible
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    refreshStatus();
  }
});
