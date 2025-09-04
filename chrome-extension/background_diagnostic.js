/**
 * Background Script Diagnostic Tool
 * 
 * 이 코드를 background.js나 service worker에 추가하여
 * extension의 백그라운드 동작을 진단할 수 있습니다.
 * 
 * 또는 chrome://extensions → 서비스 워커 → Console에서 실행
 */

(function() {
  console.clear();
  console.log("%c🔧 AI Workspace Extension - Background Diagnostic", 
    "color: #ff6b35; font-size: 16px; font-weight: bold; background: #fff3cd; padding: 8px;");
  
  // Extension Info
  function getExtensionInfo() {
    console.log("\n%c📋 Extension Information", "font-weight: bold; color: #0066cc;");
    
    try {
      const manifest = chrome.runtime.getManifest();
      console.log(`   Name: ${manifest.name}`);
      console.log(`   Version: ${manifest.version}`);
      console.log(`   Manifest Version: ${manifest.manifest_version}`);
      console.log(`   Extension ID: ${chrome.runtime.id}`);
      
      // Check permissions
      if (manifest.permissions) {
        console.log(`   Permissions: ${manifest.permissions.join(', ')}`);
      }
      
      if (manifest.host_permissions) {
        console.log(`   Host Permissions: ${manifest.host_permissions.join(', ')}`);
      }
      
      // Check content scripts
      if (manifest.content_scripts) {
        console.log(`   Content Scripts: ${manifest.content_scripts.length} configured`);
        manifest.content_scripts.forEach((script, i) => {
          console.log(`      ${i+1}. Matches: ${script.matches.join(', ')}`);
          console.log(`         Files: ${script.js?.join(', ') || 'none'}`);
        });
      }
      
      return manifest;
    } catch (e) {
      console.error("   ❌ Failed to get extension info:", e);
      return null;
    }
  }
  
  // Test Message Passing
  function testMessagePassing() {
    console.log("\n%c💬 Message Passing Test", "font-weight: bold; color: #0066cc;");
    
    // Set up message listener
    if (chrome.runtime.onMessage) {
      chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        console.log(`   📨 Received message:`, message);
        console.log(`   👤 From sender:`, sender);
        
        if (message.action === 'diagnostic_test') {
          console.log(`   ✅ Diagnostic test message received successfully`);
          sendResponse({ success: true, timestamp: Date.now() });
          return true;
        }
      });
      console.log("   ✅ Message listener set up");
    } else {
      console.log("   ❌ chrome.runtime.onMessage not available");
    }
    
    // Test sending to active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length > 0) {
        const activeTab = tabs[0];
        console.log(`   🎯 Active tab: ${activeTab.url}`);
        
        chrome.tabs.sendMessage(activeTab.id, {
          action: 'diagnostic_ping',
          timestamp: Date.now()
        }, (response) => {
          if (chrome.runtime.lastError) {
            console.log(`   ❌ Failed to send to content script: ${chrome.runtime.lastError.message}`);
          } else {
            console.log(`   ✅ Content script responded:`, response);
          }
        });
      } else {
        console.log("   ⚠️ No active tabs found");
      }
    });
  }
  
  // Check Storage
  function testStorage() {
    console.log("\n%c💾 Storage Test", "font-weight: bold; color: #0066cc;");
    
    const testData = {
      diagnostic_test: true,
      timestamp: Date.now(),
      version: "diagnostic_v1"
    };
    
    // Test chrome.storage.local
    if (chrome.storage && chrome.storage.local) {
      chrome.storage.local.set(testData, () => {
        if (chrome.runtime.lastError) {
          console.log(`   ❌ Storage.local set failed: ${chrome.runtime.lastError.message}`);
        } else {
          console.log(`   ✅ Storage.local set successful`);
          
          // Test get
          chrome.storage.local.get(['diagnostic_test'], (result) => {
            if (chrome.runtime.lastError) {
              console.log(`   ❌ Storage.local get failed: ${chrome.runtime.lastError.message}`);
            } else {
              console.log(`   ✅ Storage.local get successful:`, result);
            }
          });
        }
      });
    } else {
      console.log("   ❌ chrome.storage.local not available");
    }
    
    // Test chrome.storage.sync (if available)
    if (chrome.storage && chrome.storage.sync) {
      chrome.storage.sync.set({ sync_test: Date.now() }, () => {
        if (chrome.runtime.lastError) {
          console.log(`   ⚠️ Storage.sync failed: ${chrome.runtime.lastError.message}`);
        } else {
          console.log(`   ✅ Storage.sync available and working`);
        }
      });
    }
  }
  
  // Network Test
  function testNetworkAccess() {
    console.log("\n%c🌐 Network Access Test", "font-weight: bold; color: #0066cc;");
    
    const testUrls = [
      'https://httpbin.org/get',
      'https://api.github.com',
      'https://generativelanguage.googleapis.com/v1beta/models' // Gemini API base
    ];
    
    testUrls.forEach((url, index) => {
      fetch(url, { 
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      })
      .then(response => {
        console.log(`   ${index + 1}. ✅ ${url} - Status: ${response.status}`);
      })
      .catch(error => {
        console.log(`   ${index + 1}. ❌ ${url} - Error: ${error.message}`);
      });
    });
  }
  
  // Monitor Errors
  function setupErrorMonitoring() {
    console.log("\n%c🚨 Error Monitoring", "font-weight: bold; color: #0066cc;");
    
    // Global error handler
    self.addEventListener('error', (event) => {
      console.log(`   💥 Global Error:`, event.error);
      console.log(`   📍 Source: ${event.filename}:${event.lineno}:${event.colno}`);
    });
    
    // Unhandled promise rejection handler
    self.addEventListener('unhandledrejection', (event) => {
      console.log(`   💥 Unhandled Promise Rejection:`, event.reason);
    });
    
    console.log("   ✅ Error monitoring set up");
  }
  
  // API Test Functions
  function createAPITestFunctions() {
    console.log("\n%c🧪 API Test Functions", "font-weight: bold; color: #0066cc;");
    
    // Test function for Gemini API
    self.__testGeminiAPI = (apiKey, text = "Hello, this is a test.") => {
      if (!apiKey) {
        console.log("   ❌ API key required. Usage: __testGeminiAPI('your-api-key', 'test text')");
        return;
      }
      
      console.log("   🧪 Testing Gemini API...");
      
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`;
      
      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{
            parts: [{ text: text }]
          }]
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.log("   ❌ API Error:", data.error);
        } else {
          console.log("   ✅ API Success:", data);
        }
      })
      .catch(error => {
        console.log("   ❌ Network Error:", error);
      });
    };
    
    // Test content script injection
    self.__testContentScriptInjection = () => {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length > 0) {
          const tabId = tabs[0].id;
          
          chrome.scripting.executeScript({
            target: { tabId: tabId },
            func: () => {
              console.log("🧪 Content script injection test successful!");
              return { 
                success: true, 
                url: location.href, 
                title: document.title 
              };
            }
          }, (results) => {
            if (chrome.runtime.lastError) {
              console.log("   ❌ Script injection failed:", chrome.runtime.lastError.message);
            } else {
              console.log("   ✅ Script injection successful:", results[0].result);
            }
          });
        }
      });
    };
    
    console.log("   Created test functions:");
    console.log("   - __testGeminiAPI('api-key', 'text')");
    console.log("   - __testContentScriptInjection()");
  }
  
  // Main diagnostic execution
  function runBackgroundDiagnostic() {
    console.log("🚀 Starting background diagnostic...\n");
    
    const manifest = getExtensionInfo();
    testMessagePassing();
    testStorage();
    testNetworkAccess();
    setupErrorMonitoring();
    createAPITestFunctions();
    
    console.log("\n%c📋 Background Diagnostic Complete", 
      "font-weight: bold; font-size: 14px; color: #00cc00; background: #d4edda; padding: 5px;");
    
    console.log("💡 Available test functions:");
    console.log("   - __testGeminiAPI('your-api-key')");
    console.log("   - __testContentScriptInjection()");
    
    return manifest;
  }
  
  // Auto-run or expose for manual execution
  if (typeof window === 'undefined') {
    // We're in service worker context
    runBackgroundDiagnostic();
  } else {
    // We're in window context, expose for manual execution
    window.__runBackgroundDiagnostic = runBackgroundDiagnostic;
    console.log("💡 Run: __runBackgroundDiagnostic()");
  }
  
})();