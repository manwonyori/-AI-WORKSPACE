// AI Workspace Controller Background Script
console.log("🚀 Background script starting...");

// Simple tab management - Updated with real URLs (5 total)
const URLS = {
  chatgpt: "https://chatgpt.com/",
  claude: "https://claude.ai/",
  gemini: "https://gemini.google.com/app",
  aistudio: "https://aistudio.google.com/app", 
  perplexity: "https://www.perplexity.ai/"
};

// URL patterns for finding existing tabs - Updated with real patterns  
const URL_PATTERNS = {
  chatgpt: ["*://chatgpt.com/*", "*://chat.openai.com/*", "*://*.chatgpt.com/*"],
  claude: ["*://claude.ai/*", "*://*.claude.ai/*"],
  gemini: ["*://aistudio.google.com/*", "*://gemini.google.com/*", "*://*.google.com/app*", "*://*.google.com/prompts*"],
  perplexity: ["*://www.perplexity.ai/*", "*://perplexity.ai/*", "*://*.perplexity.ai/*"]
};

// Open all platforms
async function openAll() {
  console.log("📂 Opening all platforms...");
  const results = {};
  
  for (const [platform, url] of Object.entries(URLS)) {
    try {
      const tab = await chrome.tabs.create({ url, active: false });
      results[platform] = { success: true, tabId: tab.id };
      console.log(`✅ ${platform} opened: tab ${tab.id}`);
    } catch (error) {
      results[platform] = { success: false, error: error.message };
      console.error(`❌ ${platform} failed:`, error);
    }
  }
  
  return results;
}

// Check status of all platforms by scanning all tabs
async function statusAll() {
  console.log("🔍 Checking status of all platforms...");
  const status = {
    chatgpt: { ready: false, reason: "no-tab" },
    claude: { ready: false, reason: "no-tab" },
    gemini: { ready: false, reason: "no-tab" },
    perplexity: { ready: false, reason: "no-tab" }
  };
  
  try {
    // Get all tabs
    const allTabs = await chrome.tabs.query({});
    console.log(`📊 Scanning ${allTabs.length} total tabs`);
    
    for (const tab of allTabs) {
      console.log(`🔍 Checking tab ${tab.id}: ${tab.url}`);
      
      // Determine platform from URL
      let platform = null;
      const url = tab.url || "";
      
      if (url.includes("chatgpt.com") || url.includes("chat.openai.com")) {
        platform = "chatgpt";
      } else if (url.includes("claude.ai")) {
        platform = "claude";
      } else if (url.includes("aistudio.google.com") || url.includes("gemini.google.com") || (url.includes("google.com") && (url.includes("prompts") || url.includes("app")))) {
        platform = "gemini";
        console.log(`🔍 Gemini variant detected: ${url}`);
      } else if (url.includes("perplexity.ai")) {
        platform = "perplexity";
      }
      
      if (platform) {
        console.log(`🎯 Found ${platform} tab: ${tab.id}`);
        
        try {
          // Try to ping the content script
          const response = await chrome.tabs.sendMessage(tab.id, { action: "status" });
          console.log(`📨 Response from ${platform}:`, response);
          
          if (response && response.ready) {
            // If platform is already ready, don't overwrite - just log
            if (!status[platform].ready) {
              status[platform] = {
                ready: true,
                platform: response.platform,
                url: tab.url,
                tabId: tab.id
              };
              console.log(`🟢 ${platform} is ready!`);
            } else {
              console.log(`🟢 ${platform} already ready, found additional tab`);
            }
          }
        } catch (error) {
          console.log(`🔴 ${platform} content script error:`, error.message);
          // Only set error status if platform isn't already ready
          if (!status[platform].ready) {
            status[platform] = { 
              ready: false, 
              reason: "no-content-script", 
              url: tab.url,
              tabId: tab.id,
              error: error.message
            };
          }
        }
      }
    }
    
  } catch (error) {
    console.error("❌ Error scanning tabs:", error);
  }
  
  console.log("📋 Final status:", status);
  return status;
}

// Sync configuration (placeholder)
async function syncNow() {
  console.log("⚙️ Syncing configuration...");
  // TODO: Implement actual config sync
  return { success: true };
}

// Send message to all platforms
async function sendToAllPlatforms(message) {
  console.log("📤 Sending to all platforms:", message);
  const results = {};
  let successCount = 0;
  
  try {
    const allTabs = await chrome.tabs.query({});
    
    for (const tab of allTabs) {
      const url = tab.url || "";
      let platform = null;
      
      if (url.includes("chatgpt.com") || url.includes("chat.openai.com")) {
        platform = "chatgpt";
      } else if (url.includes("claude.ai")) {
        platform = "claude";
      } else if (url.includes("aistudio.google.com") || url.includes("gemini.google.com")) {
        platform = "gemini";
      } else if (url.includes("perplexity.ai")) {
        platform = "perplexity";
      }
      
      if (platform && !results[platform]) {
        try {
          console.log(`📤 Sending to ${platform} tab ${tab.id}`);
          const response = await chrome.tabs.sendMessage(tab.id, { 
            action: "inputAndSend", 
            text: message 
          });
          
          if (response && response.success) {
            results[platform] = { success: true };
            successCount++;
            console.log(`✅ ${platform} success`);
          } else {
            results[platform] = { success: false, reason: "send-failed" };
            console.log(`❌ ${platform} send failed`);
          }
        } catch (error) {
          results[platform] = { success: false, error: error.message };
          console.log(`❌ ${platform} error:`, error.message);
        }
      }
    }
    
  } catch (error) {
    console.error("❌ sendToAllPlatforms error:", error);
    return { success: false, error: error.message };
  }
  
  console.log(`📊 Send results: ${successCount} successes`, results);
  return { success: successCount > 0, results, successCount };
}

// Message handler
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("📨 Message received:", message);
  
  (async () => {
    try {
      switch (message?.action) {
        case "openAll":
          const openResults = await openAll();
          sendResponse(openResults);
          break;
          
        case "statusAll":
          const statusResults = await statusAll();
          sendResponse(statusResults);
          break;
          
        case "syncNow":
          const syncResults = await syncNow();
          sendResponse(syncResults);
          break;
          
        case "sendToAll":
          const sendResults = await sendToAllPlatforms(message.message);
          sendResponse(sendResults);
          break;
          
        default:
          console.warn("❓ Unknown action:", message?.action);
          sendResponse({ error: "Unknown action" });
      }
    } catch (error) {
      console.error("❌ Message handler error:", error);
      sendResponse({ error: error.message });
    }
  })();
  
  return true; // Keep message channel open for async response
});

// Initialize
chrome.runtime.onInstalled.addListener(() => {
  console.log("🎉 AI Workspace Controller installed!");
});

console.log("✅ Background script ready!");