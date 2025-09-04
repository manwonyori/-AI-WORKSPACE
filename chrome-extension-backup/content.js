// Content script for AI Workspace MCP Chrome Extension

console.log('AI Workspace MCP Extension loaded');

// Listen for messages from the webpage
window.addEventListener('message', (event) => {
    // Only accept messages from the same origin
    if (event.origin !== window.location.origin) return;
    
    if (event.data && event.data.type === 'MCP_REQUEST') {
        // Forward MCP requests to background script
        chrome.runtime.sendMessage({
            action: 'mcpRequest',
            data: event.data.payload
        }, (response) => {
            // Send response back to webpage
            window.postMessage({
                type: 'MCP_RESPONSE',
                id: event.data.id,
                payload: response
            }, '*');
        });
    }
});

// Inject MCP client API into the page
const script = document.createElement('script');
script.textContent = `
    // MCP Client API for web pages
    window.MCPClient = {
        connected: false,
        pendingRequests: new Map(),
        
        // Send MCP request
        request: function(method, params) {
            return new Promise((resolve, reject) => {
                const id = Date.now() + Math.random();
                
                this.pendingRequests.set(id, { resolve, reject });
                
                window.postMessage({
                    type: 'MCP_REQUEST',
                    id: id,
                    payload: { method, params }
                }, '*');
                
                // Timeout after 10 seconds
                setTimeout(() => {
                    if (this.pendingRequests.has(id)) {
                        this.pendingRequests.delete(id);
                        reject(new Error('Request timeout'));
                    }
                }, 10000);
            });
        },
        
        // Check if extension is connected
        isConnected: async function() {
            try {
                const response = await this.request('ping', {});
                return response.success === true;
            } catch {
                return false;
            }
        }
    };
    
    // Listen for responses
    window.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'MCP_RESPONSE') {
            const request = window.MCPClient.pendingRequests.get(event.data.id);
            if (request) {
                window.MCPClient.pendingRequests.delete(event.data.id);
                if (event.data.payload.error) {
                    request.reject(new Error(event.data.payload.error));
                } else {
                    request.resolve(event.data.payload);
                }
            }
        }
    });
    
    console.log('MCP Client API injected. Use window.MCPClient to interact with MCP servers.');
`;

document.documentElement.appendChild(script);
script.remove();

// Add visual indicator when on supported sites
if (window.location.hostname === 'chatgpt.com' || 
    window.location.hostname === 'claude.ai' ||
    window.location.hostname === 'perplexity.ai') {
    
    const indicator = document.createElement('div');
    indicator.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 12px;
        z-index: 999999;
        opacity: 0.9;
        cursor: pointer;
        transition: all 0.3s ease;
    `;
    indicator.textContent = '🚀 MCP Connected';
    indicator.title = 'AI Workspace MCP Extension';
    
    indicator.addEventListener('mouseenter', () => {
        indicator.style.transform = 'scale(1.05)';
        indicator.style.opacity = '1';
    });
    
    indicator.addEventListener('mouseleave', () => {
        indicator.style.transform = 'scale(1)';
        indicator.style.opacity = '0.9';
    });
    
    indicator.addEventListener('click', () => {
        chrome.runtime.sendMessage({action: 'openPopup'});
    });
    
    document.body.appendChild(indicator);
}