// MCP Chrome Extension - Interactive Popup
const SERVER_URL = 'http://localhost:3006/sse';
const MESSAGE_URL = 'http://localhost:3006/message';

let sessionId = null;
let eventSource = null;

// Initialize connection
async function initConnection() {
    return new Promise((resolve) => {
        eventSource = new EventSource(SERVER_URL);
        
        eventSource.addEventListener('endpoint', (event) => {
            const match = event.data.match(/sessionId=([^&]+)/);
            if (match) {
                sessionId = match[1];
                console.log('Session ID:', sessionId);
                updateStatus(true);
                resolve(true);
            }
        });
        
        eventSource.onerror = () => {
            updateStatus(false);
            resolve(false);
        };
        
        setTimeout(() => resolve(false), 5000);
    });
}

// Update connection status
function updateStatus(connected) {
    const indicator = document.getElementById('statusIndicator');
    const text = document.getElementById('statusText');
    
    indicator.className = `status-indicator ${connected ? 'connected' : 'disconnected'}`;
    text.textContent = connected ? 'Connected' : 'Disconnected';
}

// Send MCP request
async function sendMCPRequest(method, params = {}) {
    if (!sessionId) {
        await initConnection();
        if (!sessionId) {
            throw new Error('No connection to MCP server');
        }
    }
    
    const requestId = Date.now();
    const request = {
        jsonrpc: "2.0",
        id: requestId,
        method: `tools/call`,
        params: {
            name: method,
            arguments: params
        }
    };
    
    try {
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
        
        // Wait for response via SSE
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                reject(new Error('Request timeout'));
            }, 10000);
            
            const handleMessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.id === requestId) {
                        clearTimeout(timeout);
                        eventSource.removeEventListener('message', handleMessage);
                        
                        if (data.error) {
                            reject(new Error(data.error.message || 'Request failed'));
                        } else {
                            resolve(data.result);
                        }
                    }
                } catch (e) {
                    // Not JSON or not our response
                }
            };
            
            eventSource.addEventListener('message', handleMessage);
        });
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}

// Show output
function showOutput(tabId, content) {
    const output = document.getElementById(`${tabId}Output`);
    output.style.display = 'block';
    output.textContent = typeof content === 'object' ? JSON.stringify(content, null, 2) : content;
}

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
        
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});

// GitHub Tab Functions
document.getElementById('getRepoInfo').addEventListener('click', async () => {
    const owner = document.getElementById('repoOwner').value;
    const repo = document.getElementById('repoName').value;
    
    try {
        const result = await sendMCPRequest('github.get_repository', {
            owner,
            repo
        });
        showOutput('github', result);
    } catch (error) {
        showOutput('github', `Error: ${error.message}`);
    }
});

document.getElementById('listBranches').addEventListener('click', async () => {
    const owner = document.getElementById('repoOwner').value;
    const repo = document.getElementById('repoName').value;
    
    try {
        const result = await sendMCPRequest('github.list_branches', {
            owner,
            repo
        });
        showOutput('github', result);
    } catch (error) {
        showOutput('github', `Error: ${error.message}`);
    }
});

document.getElementById('listFiles').addEventListener('click', async () => {
    const owner = document.getElementById('repoOwner').value;
    const repo = document.getElementById('repoName').value;
    
    try {
        const result = await sendMCPRequest('github.list_files', {
            owner,
            repo,
            path: ''
        });
        showOutput('github', result);
    } catch (error) {
        showOutput('github', `Error: ${error.message}`);
    }
});

document.getElementById('createFile').addEventListener('click', async () => {
    const owner = document.getElementById('repoOwner').value;
    const repo = document.getElementById('repoName').value;
    const path = document.getElementById('filePath').value;
    const content = document.getElementById('fileContent').value;
    const message = document.getElementById('commitMessage').value;
    
    if (!path || !content || !message) {
        showOutput('github', 'Please fill in all fields');
        return;
    }
    
    try {
        const result = await sendMCPRequest('github.create_or_update_file', {
            owner,
            repo,
            path,
            content: btoa(content), // Base64 encode
            message,
            branch: 'main'
        });
        showOutput('github', 'File created/updated successfully!');
    } catch (error) {
        showOutput('github', `Error: ${error.message}`);
    }
});

// Git Quick Actions
document.getElementById('gitStatus').addEventListener('click', async () => {
    try {
        const result = await sendMCPRequest('filesystem.execute_command', {
            command: 'git status',
            cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
        });
        showOutput('github', result);
    } catch (error) {
        showOutput('github', `Error: ${error.message}`);
    }
});

document.getElementById('gitPull').addEventListener('click', async () => {
    try {
        const result = await sendMCPRequest('filesystem.execute_command', {
            command: 'git pull origin main',
            cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
        });
        showOutput('github', result);
    } catch (error) {
        showOutput('github', `Error: ${error.message}`);
    }
});

document.getElementById('gitCommit').addEventListener('click', async () => {
    const message = prompt('Enter commit message:');
    if (!message) return;
    
    try {
        const result = await sendMCPRequest('filesystem.execute_command', {
            command: `git add . && git commit -m "${message}"`,
            cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
        });
        showOutput('github', result);
    } catch (error) {
        showOutput('github', `Error: ${error.message}`);
    }
});

document.getElementById('gitPush').addEventListener('click', async () => {
    try {
        const result = await sendMCPRequest('filesystem.execute_command', {
            command: 'git push origin main',
            cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
        });
        showOutput('github', result);
    } catch (error) {
        showOutput('github', `Error: ${error.message}`);
    }
});

// Files Tab Functions
document.getElementById('listDir').addEventListener('click', async () => {
    const path = document.getElementById('fsPath').value;
    
    try {
        const result = await sendMCPRequest('filesystem.list_directory', {
            path
        });
        showOutput('file', result);
    } catch (error) {
        showOutput('file', `Error: ${error.message}`);
    }
});

document.getElementById('readFile').addEventListener('click', async () => {
    const path = document.getElementById('fsPath').value;
    
    try {
        const result = await sendMCPRequest('filesystem.read_text_file', {
            path
        });
        showOutput('file', result);
    } catch (error) {
        showOutput('file', `Error: ${error.message}`);
    }
});

// Quick Access Buttons
document.querySelectorAll('[data-path]').forEach(button => {
    button.addEventListener('click', async () => {
        const path = `C:\\Users\\8899y\\AI-WORKSPACE\\${button.dataset.path}`;
        document.getElementById('fsPath').value = path;
        
        try {
            const result = await sendMCPRequest('filesystem.list_directory', {
                path
            });
            showOutput('file', result);
        } catch (error) {
            showOutput('file', `Error: ${error.message}`);
        }
    });
});

// Tools Tab Functions
document.getElementById('listTools').addEventListener('click', async () => {
    try {
        // Send a simple list tools request
        const request = {
            jsonrpc: "2.0",
            id: Date.now(),
            method: "tools/list"
        };
        
        const response = await fetch(`${MESSAGE_URL}?sessionId=${sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(request)
        });
        
        showOutput('tool', 'Requesting tools list... Check console for details');
    } catch (error) {
        showOutput('tool', `Error: ${error.message}`);
    }
});

document.getElementById('testConnection').addEventListener('click', async () => {
    try {
        const connected = await initConnection();
        showOutput('tool', connected ? 'Connection successful!' : 'Connection failed');
    } catch (error) {
        showOutput('tool', `Error: ${error.message}`);
    }
});

document.getElementById('listResources').addEventListener('click', async () => {
    try {
        const request = {
            jsonrpc: "2.0",
            id: Date.now(),
            method: "resources/list"
        };
        
        const response = await fetch(`${MESSAGE_URL}?sessionId=${sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(request)
        });
        
        showOutput('tool', 'Requesting resources list...');
    } catch (error) {
        showOutput('tool', `Error: ${error.message}`);
    }
});

document.getElementById('createMemory').addEventListener('click', async () => {
    const name = prompt('Enter memory name:');
    const content = prompt('Enter memory content:');
    
    if (!name || !content) return;
    
    try {
        const result = await sendMCPRequest('memory.create_entities', {
            entities: [{
                name,
                entityType: 'Note',
                observations: [content]
            }]
        });
        showOutput('tool', 'Memory saved!');
    } catch (error) {
        showOutput('tool', `Error: ${error.message}`);
    }
});

document.getElementById('searchFiles').addEventListener('click', async () => {
    const query = prompt('Enter search query:');
    if (!query) return;
    
    try {
        const result = await sendMCPRequest('everything.search', {
            query
        });
        showOutput('tool', result);
    } catch (error) {
        showOutput('tool', `Error: ${error.message}`);
    }
});

document.getElementById('getEnv').addEventListener('click', async () => {
    try {
        const result = await sendMCPRequest('everything.printEnv', {});
        showOutput('tool', result);
    } catch (error) {
        showOutput('tool', `Error: ${error.message}`);
    }
});

// Initialize on load
document.addEventListener('DOMContentLoaded', async () => {
    await initConnection();
});