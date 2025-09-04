// Background service worker for AI Workspace MCP Chrome Extension

const SERVER_URL = 'http://localhost:3006/sse';
const MESSAGE_URL = 'http://localhost:3006/message';

let eventSource = null;
let sessionId = null;
let serverInfo = {
    connected: false,
    tools: 0,
    resources: 0
};

// Initialize MCP connection
async function initializeConnection() {
    try {
        if (eventSource) {
            eventSource.close();
        }
        
        // Create new EventSource connection
        eventSource = new EventSource(SERVER_URL);
        
        eventSource.onopen = () => {
            console.log('Connected to MCP server');
            serverInfo.connected = true;
            updateBadge(true);
        };
        
        eventSource.onmessage = (event) => {
            console.log('Message from server:', event.data);
            handleServerMessage(event.data);
        };
        
        eventSource.onerror = (error) => {
            console.error('Connection error:', error);
            serverInfo.connected = false;
            updateBadge(false);
        };
        
        // Listen for endpoint event to get session ID
        eventSource.addEventListener('endpoint', (event) => {
            const match = event.data.match(/sessionId=([^&]+)/);
            if (match) {
                sessionId = match[1];
                console.log('Session ID:', sessionId);
                sendInitializeRequest();
            }
        });
        
        return true;
    } catch (error) {
        console.error('Failed to initialize connection:', error);
        return false;
    }
}

// Send initialize request to MCP server
async function sendInitializeRequest() {
    if (!sessionId) return;
    
    const initRequest = {
        jsonrpc: "2.0",
        id: 0,
        method: "initialize",
        params: {
            protocolVersion: "2025-06-18",
            capabilities: {},
            clientInfo: {
                name: "ai-workspace-chrome",
                version: "1.0.0"
            }
        }
    };
    
    try {
        const response = await fetch(`${MESSAGE_URL}?sessionId=${sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(initRequest)
        });
        
        if (response.ok) {
            console.log('Initialize request sent successfully');
            // Request tools list
            requestToolsList();
        }
    } catch (error) {
        console.error('Failed to send initialize request:', error);
    }
}

// Request tools list from server
async function requestToolsList() {
    if (!sessionId) return;
    
    const toolsRequest = {
        jsonrpc: "2.0",
        id: 1,
        method: "tools/list"
    };
    
    try {
        const response = await fetch(`${MESSAGE_URL}?sessionId=${sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(toolsRequest)
        });
        
        if (response.ok) {
            console.log('Tools list requested');
        }
    } catch (error) {
        console.error('Failed to request tools list:', error);
    }
}

// Handle messages from server
function handleServerMessage(data) {
    try {
        const message = JSON.parse(data);
        
        if (message.result && message.result.tools) {
            serverInfo.tools = message.result.tools.length;
            console.log(`Server has ${serverInfo.tools} tools available`);
        }
        
        if (message.result && message.result.resources) {
            serverInfo.resources = message.result.resources.length;
            console.log(`Server has ${serverInfo.resources} resources available`);
        }
    } catch (error) {
        // Not JSON, ignore
    }
}

// Update extension badge
function updateBadge(connected) {
    const color = connected ? '#4ade80' : '#ef4444';
    const text = connected ? 'ON' : 'OFF';
    
    chrome.action.setBadgeBackgroundColor({ color });
    chrome.action.setBadgeText({ text });
}

// Handle messages from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'connect') {
        initializeConnection().then((success) => {
            sendResponse({ success });
        });
        return true; // Keep message channel open for async response
    }
    
    if (request.action === 'getServerInfo') {
        sendResponse(serverInfo);
        return true;
    }
    
    if (request.action === 'disconnect') {
        if (eventSource) {
            eventSource.close();
            eventSource = null;
            sessionId = null;
            serverInfo.connected = false;
            updateBadge(false);
        }
        sendResponse({ success: true });
        return true;
    }
    
    // MCP tool calls
    if (request.action === 'mcp_call') {
        executeMCPTool(request.tool, request.params)
            .then(result => sendResponse({result}))
            .catch(error => sendResponse({error: error.message}));
        return true;
    }
    
    // Platform status updates
    if (request.type === 'PLATFORM_READY') {
        console.log(`Platform ${request.platform} is ready`);
        chrome.storage.local.get(['platform_status'], (data) => {
            const status = data.platform_status || {};
            status[request.platform] = true;
            chrome.storage.local.set({platform_status: status});
        });
    }
    
    // Auto command results
    if (request.type === 'AUTO_COMMAND_RESULT') {
        console.log('Auto command completed:', request.result);
        chrome.storage.local.get(['command_results'], (data) => {
            const results = data.command_results || [];
            results.push(request.result);
            chrome.storage.local.set({command_results: results});
        });
    }
    
    // Open MCP panel
    if (request.type === 'OPEN_MCP_PANEL') {
        chrome.action.openPopup();
    }
    
    // Send command to AI platform
    if (request.action === 'send_to_platform') {
        const { platform, command, context } = request;
        
        // Find or open the platform tab
        chrome.tabs.query({url: `https://${platform}*/*`}, async (tabs) => {
            if (tabs.length > 0) {
                // Send message to existing tab
                chrome.tabs.sendMessage(tabs[0].id, {
                    type: 'AI_COMMAND',
                    command,
                    context
                }, (response) => {
                    sendResponse(response || { error: 'No response from platform' });
                });
            } else {
                // Open new tab
                chrome.tabs.create({url: `https://${platform}.com`}, (tab) => {
                    // Wait for tab to load
                    setTimeout(() => {
                        chrome.tabs.sendMessage(tab.id, {
                            type: 'AI_COMMAND',
                            command,
                            context
                        }, (response) => {
                            sendResponse(response || { error: 'Platform loading' });
                        });
                    }, 3000);
                });
            }
        });
        return true; // Keep channel open for async response
    }
});

// Execute MCP tool
async function executeMCPTool(toolName, params) {
    if (!sessionId) {
        await initializeConnection();
        if (!sessionId) {
            throw new Error('No MCP connection');
        }
    }
    
    const request = {
        jsonrpc: "2.0",
        id: Date.now(),
        method: "tools/call",
        params: {
            name: toolName,
            arguments: params
        }
    };
    
    const response = await fetch(`${MESSAGE_URL}?sessionId=${sessionId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // For simplicity, return success
    // In production, you'd wait for the SSE response
    return {success: true, tool: toolName, params};
}

// Initialize connection on extension load
chrome.runtime.onInstalled.addListener(() => {
    console.log('AI Workspace MCP Extension installed');
    initializeConnection();
});

// Reconnect on startup
chrome.runtime.onStartup.addListener(() => {
    console.log('AI Workspace MCP Extension started');
    initializeConnection();
});

// Keep service worker alive
setInterval(() => {
    if (serverInfo.connected && eventSource && eventSource.readyState === EventSource.CLOSED) {
        console.log('Reconnecting to server...');
        initializeConnection();
    }
}, 30000);