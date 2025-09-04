// Background service worker for AI Workspace Controller

const PLATFORMS = {
    chatgpt: 'https://chatgpt.com',
    claude: 'https://claude.ai',
    perplexity: 'https://perplexity.ai'
};

let platformTabs = {
    chatgpt: null,
    claude: null,
    perplexity: null
};

// Open all AI platforms in arranged windows
async function openAllPlatforms() {
    const displays = await chrome.system.display.getInfo();
    const primaryDisplay = displays[0];
    const screenWidth = primaryDisplay.bounds.width;
    const screenHeight = primaryDisplay.bounds.height;
    
    // Calculate window positions (3 columns)
    const windowWidth = Math.floor(screenWidth / 3);
    const windowHeight = screenHeight - 100; // Leave space for taskbar
    
    const positions = [
        { left: 0, top: 0 },                          // Left - ChatGPT
        { left: windowWidth, top: 0 },                // Center - Claude
        { left: windowWidth * 2, top: 0 }             // Right - Perplexity
    ];
    
    let index = 0;
    for (const [platform, url] of Object.entries(PLATFORMS)) {
        const window = await chrome.windows.create({
            url: url,
            type: 'normal',
            state: 'normal',
            left: positions[index].left,
            top: positions[index].top,
            width: windowWidth,
            height: windowHeight
        });
        
        if (window.tabs && window.tabs[0]) {
            platformTabs[platform] = window.tabs[0].id;
        }
        
        index++;
        
        // Wait a bit between opening windows
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    return platformTabs;
}

// Send text to specific platform
async function sendToPlatform(platform, text) {
    let tabId = platformTabs[platform];
    
    // Check if tab exists and is valid
    if (tabId) {
        try {
            await chrome.tabs.get(tabId);
        } catch (e) {
            tabId = null;
        }
    }
    
    // If no tab, find or create one
    if (!tabId) {
        const tabs = await chrome.tabs.query({ url: PLATFORMS[platform] + '/*' });
        if (tabs.length > 0) {
            tabId = tabs[0].id;
            platformTabs[platform] = tabId;
        } else {
            // Create new tab
            const tab = await chrome.tabs.create({ url: PLATFORMS[platform] });
            tabId = tab.id;
            platformTabs[platform] = tabId;
            
            // Wait for page to load
            await new Promise(resolve => setTimeout(resolve, 3000));
        }
    }
    
    // Send message to content script
    return new Promise((resolve) => {
        chrome.tabs.sendMessage(tabId, {
            action: 'inputAndSend',
            text: text
        }, response => {
            resolve(response || { error: 'No response' });
        });
    });
}

// Send to all platforms
async function sendToAll(text) {
    const results = {};
    
    for (const platform of Object.keys(PLATFORMS)) {
        try {
            results[platform] = await sendToPlatform(platform, text);
        } catch (error) {
            results[platform] = { error: error.message };
        }
    }
    
    return results;
}

// Get responses from all platforms
async function getAllResponses() {
    const responses = {};
    
    for (const [platform, tabId] of Object.entries(platformTabs)) {
        if (tabId) {
            try {
                const response = await new Promise((resolve) => {
                    chrome.tabs.sendMessage(tabId, {
                        action: 'getResponse'
                    }, resolve);
                });
                responses[platform] = response?.response || '';
            } catch (error) {
                responses[platform] = '';
            }
        }
    }
    
    return responses;
}

// Check platform status
async function checkPlatformStatus() {
    const status = {};
    
    for (const platform of Object.keys(PLATFORMS)) {
        const tabId = platformTabs[platform];
        if (tabId) {
            try {
                await chrome.tabs.get(tabId);
                status[platform] = 'active';
            } catch (e) {
                status[platform] = 'closed';
                platformTabs[platform] = null;
            }
        } else {
            status[platform] = 'closed';
        }
    }
    
    return status;
}

// Message handler
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Background received:', request);
    
    if (request.action === 'openAll') {
        openAllPlatforms().then(sendResponse);
        return true;
    }
    
    if (request.action === 'sendToPlatform') {
        sendToPlatform(request.platform, request.text).then(sendResponse);
        return true;
    }
    
    if (request.action === 'sendToAll') {
        sendToAll(request.text).then(sendResponse);
        return true;
    }
    
    if (request.action === 'getResponses') {
        getAllResponses().then(sendResponse);
        return true;
    }
    
    if (request.action === 'checkStatus') {
        checkPlatformStatus().then(sendResponse);
        return true;
    }
    
    if (request.action === 'openPopup') {
        chrome.action.openPopup();
        sendResponse({ success: true });
    }
});

// Tab update listener
chrome.tabs.onRemoved.addListener((tabId) => {
    for (const [platform, storedTabId] of Object.entries(platformTabs)) {
        if (storedTabId === tabId) {
            console.log(`${platform} tab closed`);
            platformTabs[platform] = null;
        }
    }
});

console.log('AI Workspace Controller background script loaded');