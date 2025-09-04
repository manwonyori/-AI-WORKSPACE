// AI Workspace Controller Popup Script

let platformStatus = {
    chatgpt: false,
    claude: false,
    perplexity: false,
    gemini: false
};

let responses = {
    chatgpt: '',
    claude: '',
    perplexity: '',
    gemini: ''
};

let activeResponseTab = 'chatgpt';

// Update platform status display
function updatePlatformStatus(platform, isActive) {
    const card = document.getElementById(`${platform}-card`);
    const status = document.getElementById(`${platform}-status`);
    
    if (card) {
        card.className = `platform-card ${isActive ? 'active' : 'inactive'}`;
    }
    if (status) {
        status.className = `platform-status ${isActive ? 'active' : 'inactive'}`;
    }
    
    platformStatus[platform] = isActive;
}

// Update status bar
function updateStatusBar(message) {
    const statusBar = document.getElementById('statusBar');
    if (statusBar) {
        statusBar.textContent = message;
    }
}

// Check all platforms status
async function checkAllPlatforms() {
    updateStatusBar('Checking platform status...');
    
    chrome.runtime.sendMessage({action: 'checkStatus'}, (response) => {
        if (chrome.runtime.lastError) {
            console.error('Error checking status:', chrome.runtime.lastError);
            updateStatusBar('Error checking status');
            return;
        }
        
        if (response) {
            for (const [platform, status] of Object.entries(response)) {
                updatePlatformStatus(platform, status === 'active');
            }
            
            const activeCount = Object.values(response).filter(s => s === 'active').length;
            updateStatusBar(`${activeCount}/4 platforms active`);
        }
    });
}

// Open all platforms
function openAllPlatforms() {
    updateStatusBar('Opening all platforms...');
    
    chrome.runtime.sendMessage({action: 'openAll'}, (response) => {
        if (chrome.runtime.lastError) {
            console.error('Error opening platforms:', chrome.runtime.lastError);
            updateStatusBar('Error opening platforms');
            return;
        }
        
        updateStatusBar('All platforms opened');
        setTimeout(checkAllPlatforms, 2000);
    });
}

// Send message to all platforms
function sendToAllPlatforms() {
    const messageInput = document.getElementById('messageInput');
    const text = messageInput.value.trim();
    
    if (!text) {
        updateStatusBar('Please enter a message');
        return;
    }
    
    updateStatusBar('Sending to all platforms...');
    
    chrome.runtime.sendMessage({action: 'sendToAll', text: text}, (response) => {
        if (chrome.runtime.lastError) {
            console.error('Error sending message:', chrome.runtime.lastError);
            updateStatusBar('Error sending message');
            return;
        }
        
        console.log('Send results:', response);
        updateStatusBar('Message sent to all platforms');
        
        // Clear input
        messageInput.value = '';
    });
}

// Get responses from all platforms
function getResponses() {
    updateStatusBar('Getting responses...');
    
    chrome.runtime.sendMessage({action: 'getResponses'}, (response) => {
        if (chrome.runtime.lastError) {
            console.error('Error getting responses:', chrome.runtime.lastError);
            updateStatusBar('Error getting responses');
            return;
        }
        
        if (response) {
            responses = response;
            showResponseSection();
            displayResponse(activeResponseTab);
            updateStatusBar('Responses received');
        }
    });
}

// Show response section
function showResponseSection() {
    const responseSection = document.getElementById('responseSection');
    if (responseSection) {
        responseSection.classList.add('visible');
    }
}

// Display response for specific platform
function displayResponse(platform) {
    const responseContent = document.getElementById('responseContent');
    if (responseContent) {
        const response = responses[platform] || 'No response from ' + platform;
        responseContent.textContent = response;
    }
    
    // Update active tab
    document.querySelectorAll('.response-tab').forEach(tab => {
        if (tab.dataset.platform === platform) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
    
    activeResponseTab = platform;
}

// Clear all inputs
function clearAll() {
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.value = '';
    }
    
    responses = {
        chatgpt: '',
        claude: '',
        perplexity: '',
        gemini: ''
    };
    
    const responseContent = document.getElementById('responseContent');
    if (responseContent) {
        responseContent.textContent = 'No responses yet...';
    }
    
    updateStatusBar('Cleared');
}

// Sync configuration from GitHub Pages
function syncConfig() {
    updateStatusBar('Syncing configuration...');
    
    chrome.runtime.sendMessage({action: 'syncConfig'}, (response) => {
        if (chrome.runtime.lastError) {
            console.error('Error syncing config:', chrome.runtime.lastError);
            updateStatusBar('❌ Config sync failed');
            return;
        }
        
        if (response && response.success) {
            updateStatusBar('✅ Config synced successfully!');
            console.log('Config synced:', response.config);
        } else {
            updateStatusBar('❌ Config sync failed');
        }
    });
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log('AI Workspace Controller popup loaded');
    
    // Button event listeners
    document.getElementById('openAllBtn')?.addEventListener('click', openAllPlatforms);
    document.getElementById('checkStatusBtn')?.addEventListener('click', checkAllPlatforms);
    document.getElementById('syncConfigBtn')?.addEventListener('click', syncConfig);
    document.getElementById('sendAllBtn')?.addEventListener('click', sendToAllPlatforms);
    document.getElementById('getResponsesBtn')?.addEventListener('click', getResponses);
    document.getElementById('clearAllBtn')?.addEventListener('click', clearAll);
    
    // Response tab listeners
    document.querySelectorAll('.response-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            displayResponse(tab.dataset.platform);
        });
    });
    
    // Enter key to send
    document.getElementById('messageInput')?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendToAllPlatforms();
        }
    });
    
    // Initial status check
    checkAllPlatforms();
});

// Auto-check status every 5 seconds
setInterval(checkAllPlatforms, 5000);