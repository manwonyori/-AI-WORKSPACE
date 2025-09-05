/**
 * ULTIMATE Background Service Worker v3.0
 * 완벽한 자동 릴레이 시스템
 */

console.log('🚀 ULTIMATE Background Service Worker Starting...');

// ==================== GLOBAL STATE ====================
const SYSTEM = {
    // Platform Management
    platforms: new Map(),
    tabs: new Map(),
    
    // Relay State
    relay: {
        active: false,
        sequence: ['claude', 'chatgpt', 'gemini', 'perplexity'],
        currentIndex: 0,
        currentRound: 0,
        maxRounds: 10,
        messages: [],
        responses: new Map()
    },
    
    // Monitoring
    monitor: {
        startTime: Date.now(),
        successCount: 0,
        failCount: 0,
        lastActivity: Date.now(),
        errors: []
    },
    
    // Storage
    storage: {
        sessions: [],
        currentSession: null
    }
};

// ==================== PLATFORM URLS ====================
const PLATFORM_URLS = {
    chatgpt: 'https://chatgpt.com/',
    claude: 'https://claude.ai/',
    gemini: 'https://gemini.google.com/app',
    perplexity: 'https://www.perplexity.ai/'
};

// ==================== DEBUG HELPER ====================
async function sendToDebugMonitor(action, data = {}) {
    // Send to all tabs that have debug monitor open
    const tabs = await chrome.tabs.query({});
    for (const tab of tabs) {
        if (tab.url && tab.url.includes('debug_relay.html')) {
            chrome.tabs.sendMessage(tab.id, {
                action: 'DEBUG_UPDATE',
                debug: true,
                ...data
            }).catch(() => {}); // Ignore errors
        }
    }
}

// ==================== INITIALIZATION ====================
chrome.runtime.onInstalled.addListener(() => {
    console.log('✅ Extension installed/updated');
    initializeSystem();
});

chrome.runtime.onStartup.addListener(() => {
    console.log('✅ Browser started');
    initializeSystem();
});

async function initializeSystem() {
    console.log('🎯 Initializing system...');
    
    // Clear previous state
    SYSTEM.platforms.clear();
    SYSTEM.tabs.clear();
    
    // Load saved state
    const saved = await chrome.storage.local.get(['relay', 'monitor', 'sessions']);
    if (saved.relay) SYSTEM.relay = { ...SYSTEM.relay, ...saved.relay };
    if (saved.monitor) SYSTEM.monitor = { ...SYSTEM.monitor, ...saved.monitor };
    if (saved.sessions) SYSTEM.storage.sessions = saved.sessions;
    
    // Find existing tabs
    await findExistingTabs();
    
    console.log('✅ System initialized');
}

// ==================== TAB MANAGEMENT ====================
async function findExistingTabs() {
    const tabs = await chrome.tabs.query({});
    
    for (const tab of tabs) {
        const platform = detectPlatformFromUrl(tab.url);
        if (platform) {
            SYSTEM.tabs.set(platform, tab.id);
            SYSTEM.platforms.set(tab.id, platform);
            console.log(`✅ Found ${platform} tab: ${tab.id}`);
        }
    }
    
    return SYSTEM.tabs;
}

function detectPlatformFromUrl(url) {
    if (!url) return null;
    
    if (url.includes('chatgpt.com') || url.includes('chat.openai.com')) return 'chatgpt';
    if (url.includes('claude.ai')) return 'claude';
    if (url.includes('gemini.google.com') || url.includes('aistudio.google.com')) return 'gemini';
    if (url.includes('perplexity.ai')) return 'perplexity';
    
    return null;
}

async function openPlatform(platform) {
    // Check if tab exists
    const existingTabId = SYSTEM.tabs.get(platform);
    
    if (existingTabId) {
        try {
            const tab = await chrome.tabs.get(existingTabId);
            if (tab) {
                await chrome.tabs.update(tab.id, { active: true });
                return tab;
            }
        } catch (e) {
            // Tab doesn't exist anymore
            SYSTEM.tabs.delete(platform);
        }
    }
    
    // Create new tab
    const url = PLATFORM_URLS[platform];
    if (!url) return null;
    
    const tab = await chrome.tabs.create({ url, active: false });
    SYSTEM.tabs.set(platform, tab.id);
    SYSTEM.platforms.set(tab.id, platform);
    
    console.log(`✅ Opened ${platform}: Tab ${tab.id}`);
    
    // Wait for tab to load
    await waitForTabReady(tab.id);
    
    return tab;
}

async function waitForTabReady(tabId, timeout = 10000) {
    return new Promise((resolve) => {
        const startTime = Date.now();
        
        const checkTab = setInterval(async () => {
            try {
                const tab = await chrome.tabs.get(tabId);
                
                if (tab.status === 'complete') {
                    clearInterval(checkTab);
                    
                    // Additional wait for content script
                    setTimeout(() => resolve(true), 1000);
                }
                
                if (Date.now() - startTime > timeout) {
                    clearInterval(checkTab);
                    resolve(false);
                }
            } catch (e) {
                clearInterval(checkTab);
                resolve(false);
            }
        }, 500);
    });
}

// ==================== MESSAGE SENDING ====================
async function sendToTab(tabId, action, data = {}) {
    try {
        const response = await chrome.tabs.sendMessage(tabId, {
            action,
            ...data,
            timestamp: Date.now()
        });
        
        console.log(`✅ Sent to tab ${tabId}: ${action}`);
        SYSTEM.monitor.successCount++;
        
        return response;
    } catch (error) {
        console.error(`❌ Failed to send to tab ${tabId}:`, error);
        SYSTEM.monitor.failCount++;
        SYSTEM.monitor.errors.push({
            time: Date.now(),
            action,
            error: error.message
        });
        
        return null;
    }
}

async function sendToPlatform(platform, action, data = {}) {
    const tabId = SYSTEM.tabs.get(platform);
    
    if (!tabId) {
        console.warn(`⚠️ No tab for ${platform}, opening...`);
        const tab = await openPlatform(platform);
        if (!tab) return null;
        return sendToTab(tab.id, action, data);
    }
    
    return sendToTab(tabId, action, data);
}

// ==================== RELAY SYSTEM ====================
async function startRelay(objective) {
    console.log('🚀 Starting Auto Relay:', objective);
    
    SYSTEM.relay.active = true;
    SYSTEM.relay.currentRound = 0;
    SYSTEM.relay.messages = [];
    SYSTEM.relay.responses.clear();
    
    // Create new session
    SYSTEM.storage.currentSession = {
        id: Date.now(),
        objective,
        startTime: Date.now(),
        messages: [],
        platforms: []
    };
    
    // Save state
    await saveState();
    
    // Send initial message to first platform
    const firstPlatform = SYSTEM.relay.sequence[0];
    const initialMessage = `[AUTO-RELAY PROJECT START]
목표: ${objective}

이 프로젝트는 여러 AI가 협업합니다.
당신의 응답은 자동으로 다음 AI에게 전달됩니다.

시작해주세요.`;
    
    await relayToPlatform(firstPlatform, initialMessage);
    
    return true;
}

async function stopRelay() {
    console.log('⏹️ Stopping Auto Relay');
    
    SYSTEM.relay.active = false;
    
    // Save session
    if (SYSTEM.storage.currentSession) {
        SYSTEM.storage.currentSession.endTime = Date.now();
        SYSTEM.storage.sessions.push(SYSTEM.storage.currentSession);
        SYSTEM.storage.currentSession = null;
    }
    
    await saveState();
    
    return true;
}

async function relayToPlatform(platform, message) {
    console.log(`🔄 Relaying to ${platform}...`);
    
    // Send debug update
    await sendToDebugMonitor('RELAY_SENDING', {
        platform,
        messageLength: message.length
    });
    
    // Ensure tab exists and is active
    let tabId = SYSTEM.tabs.get(platform);
    if (!tabId) {
        console.log(`📂 Opening ${platform} tab...`);
        const tab = await openPlatform(platform);
        if (!tab) {
            console.error(`❌ Failed to open ${platform}`);
            await sendToDebugMonitor('RELAY_ERROR', {
                platform,
                error: 'Failed to open tab'
            });
            return false;
        }
        tabId = tab.id;
    }
    
    // Make tab active
    try {
        await chrome.tabs.update(tabId, { active: true });
        console.log(`✅ Activated ${platform} tab`);
    } catch (e) {
        console.warn(`⚠️ Could not activate tab: ${e.message}`);
    }
    
    // Wait a bit for tab to be ready
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Send relay message
    const result = await sendToTab(tabId, 'AUTO_RELAY', { message });
    
    if (result && result.success) {
        console.log(`✅ Message sent to ${platform}`);
        
        // Record in session
        if (SYSTEM.storage.currentSession) {
            SYSTEM.storage.currentSession.messages.push({
                platform,
                message,
                timestamp: Date.now(),
                type: 'sent'
            });
        }
        
        SYSTEM.monitor.lastActivity = Date.now();
        
        await sendToDebugMonitor('RELAY_SENT', {
            platform,
            success: true
        });
        
        return true;
    } else {
        console.error(`❌ Failed to send message to ${platform}:`, result?.error);
        
        await sendToDebugMonitor('RELAY_ERROR', {
            platform,
            error: result?.error || 'Unknown error'
        });
        
        return false;
    }
}

async function processRelayResponse(platform, response) {
    console.log(`📨 Response from ${platform}: ${response.substring(0, 100)}...`);
    
    // Send debug update
    await sendToDebugMonitor('RELAY_RESPONSE', {
        platform,
        responseLength: response.length,
        preview: response.substring(0, 200)
    });
    
    // Record response
    SYSTEM.relay.responses.set(platform, response);
    
    if (SYSTEM.storage.currentSession) {
        SYSTEM.storage.currentSession.messages.push({
            platform,
            message: response,
            timestamp: Date.now(),
            type: 'received'
        });
    }
    
    // Check if relay should continue
    if (!SYSTEM.relay.active) {
        console.log('⏸️ Relay stopped');
        return;
    }
    
    // Check round limit
    if (SYSTEM.relay.currentRound >= SYSTEM.relay.maxRounds) {
        console.log('🏁 Max rounds reached');
        await stopRelay();
        return;
    }
    
    // Find next platform
    const currentIndex = SYSTEM.relay.sequence.indexOf(platform);
    const nextIndex = (currentIndex + 1) % SYSTEM.relay.sequence.length;
    const nextPlatform = SYSTEM.relay.sequence[nextIndex];
    
    console.log(`🔄 Relay flow: ${platform} (${currentIndex}) -> ${nextPlatform} (${nextIndex})`);
    
    // Increment round if cycling back
    if (nextIndex === 0) {
        SYSTEM.relay.currentRound++;
        console.log(`📊 Starting Round ${SYSTEM.relay.currentRound + 1}`);
    }
    
    // Update current index
    SYSTEM.relay.currentIndex = nextIndex;
    
    // Prepare relay message
    const relayMessage = `[AUTO-RELAY from ${platform}]

${response}

[Please continue with your analysis and provide your perspective]`;
    
    console.log(`⏳ Waiting 5 seconds before relaying to ${nextPlatform}...`);
    
    // Delay before relay with retry logic
    setTimeout(async () => {
        const success = await relayToPlatform(nextPlatform, relayMessage);
        
        if (!success) {
            console.warn(`❌ Failed to relay to ${nextPlatform}, retrying in 3 seconds...`);
            setTimeout(() => {
                relayToPlatform(nextPlatform, relayMessage);
            }, 3000);
        }
    }, 5000);
}

// ==================== STORAGE MANAGEMENT ====================
async function saveState() {
    await chrome.storage.local.set({
        relay: {
            active: SYSTEM.relay.active,
            currentIndex: SYSTEM.relay.currentIndex,
            currentRound: SYSTEM.relay.currentRound
        },
        monitor: SYSTEM.monitor,
        sessions: SYSTEM.storage.sessions
    });
}

async function exportSessions() {
    const data = {
        exportTime: Date.now(),
        sessions: SYSTEM.storage.sessions,
        monitor: SYSTEM.monitor
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    await chrome.downloads.download({
        url,
        filename: `ai_relay_export_${Date.now()}.json`,
        saveAs: true
    });
    
    return true;
}

// ==================== MESSAGE HANDLERS ====================
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 Message received:', request.action);
    
    (async () => {
        let result = { success: false };
        
        try {
            switch (request.action) {
                // From Content Scripts
                case 'CONTENT_READY':
                    if (sender.tab) {
                        const platform = request.platform;
                        SYSTEM.platforms.set(sender.tab.id, platform);
                        SYSTEM.tabs.set(platform, sender.tab.id);
                        console.log(`✅ ${platform} content script ready`);
                        result.success = true;
                    }
                    break;
                    
                case 'RELAY_RESPONSE':
                    console.log(`📥 Received relay response from ${request.platform}`);
                    if (request.platform && request.response) {
                        // Validate response
                        if (request.response.length < 10) {
                            console.warn(`⚠️ Response too short from ${request.platform}: ${request.response}`);
                        } else {
                            console.log(`✅ Valid response from ${request.platform}, processing...`);
                            await processRelayResponse(request.platform, request.response);
                            result.success = true;
                        }
                    } else {
                        console.error(`❌ Invalid relay response:`, request);
                        result.error = 'Missing platform or response';
                    }
                    break;
                    
                // From Popup
                case 'GET_STATUS':
                    await findExistingTabs();
                    result = {
                        success: true,
                        platforms: Object.fromEntries(SYSTEM.tabs),
                        relay: {
                            active: SYSTEM.relay.active,
                            currentRound: SYSTEM.relay.currentRound
                        },
                        monitor: SYSTEM.monitor
                    };
                    break;
                    
                case 'OPEN_ALL':
                    for (const platform of Object.keys(PLATFORM_URLS)) {
                        await openPlatform(platform);
                    }
                    result.success = true;
                    break;
                    
                case 'SEND_TO_ALL':
                    const message = request.message || request.text;
                    result.platforms = {};
                    
                    for (const platform of SYSTEM.tabs.keys()) {
                        const response = await sendToPlatform(platform, 'INPUT_AND_SEND', { message });
                        result.platforms[platform] = !!response?.success;
                    }
                    
                    result.success = true;
                    break;
                    
                case 'START_RELAY':
                    result.success = await startRelay(request.objective);
                    break;
                    
                case 'STOP_RELAY':
                    result.success = await stopRelay();
                    break;
                    
                case 'EXPORT_DATA':
                    result.success = await exportSessions();
                    break;
                    
                case 'CLEAR_DATA':
                    SYSTEM.storage.sessions = [];
                    SYSTEM.monitor.errors = [];
                    await saveState();
                    result.success = true;
                    break;
                    
                case 'TEST_PLATFORM':
                    const testResult = await sendToPlatform(request.platform, 'CHECK_STATUS');
                    result = testResult || { success: false };
                    break;
                    
                default:
                    result.error = 'Unknown action';
            }
        } catch (error) {
            console.error('❌ Handler error:', error);
            result.error = error.message;
        }
        
        sendResponse(result);
    })();
    
    return true;
});

// ==================== TAB MONITORING ====================
chrome.tabs.onRemoved.addListener((tabId) => {
    const platform = SYSTEM.platforms.get(tabId);
    if (platform) {
        console.log(`❌ ${platform} tab closed`);
        SYSTEM.platforms.delete(tabId);
        SYSTEM.tabs.delete(platform);
    }
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete') {
        const platform = detectPlatformFromUrl(tab.url);
        const oldPlatform = SYSTEM.platforms.get(tabId);
        
        if (platform && platform !== oldPlatform) {
            // Platform changed
            if (oldPlatform) {
                SYSTEM.tabs.delete(oldPlatform);
            }
            
            SYSTEM.platforms.set(tabId, platform);
            SYSTEM.tabs.set(platform, tabId);
            console.log(`✅ Tab ${tabId} is now ${platform}`);
        }
    }
});

// ==================== HEARTBEAT MONITOR ====================
setInterval(() => {
    const now = Date.now();
    const inactive = now - SYSTEM.monitor.lastActivity;
    
    if (SYSTEM.relay.active && inactive > 120000) {
        console.warn('⚠️ Relay inactive for 2 minutes');
        
        // Auto-restart if stuck
        const currentPlatform = SYSTEM.relay.sequence[SYSTEM.relay.currentIndex];
        const lastResponse = SYSTEM.relay.responses.get(currentPlatform);
        
        if (lastResponse) {
            console.log('🔄 Attempting to restart relay...');
            processRelayResponse(currentPlatform, lastResponse);
        }
    }
    
    // Save state periodically
    if (inactive < 60000) {
        saveState();
    }
}, 30000);

// ==================== INITIALIZATION ====================
initializeSystem();

console.log('✅ Ultimate Background Service Worker Ready');