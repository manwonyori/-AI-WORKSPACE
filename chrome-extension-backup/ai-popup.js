/**
 * AI Popup JavaScript
 * Complete integration with all AI platforms
 */

// AI Integration class definition (simplified for popup context)
class AIIntegration {
    constructor() {
        this.platforms = {
            chatgpt: { name: 'ChatGPT', url: 'https://chatgpt.com' },
            claude: { name: 'Claude', url: 'https://claude.ai' },
            perplexity: { name: 'Perplexity', url: 'https://perplexity.ai' }
        };
    }
    
    async sendCommand(platform, command, context = {}) {
        return new Promise((resolve, reject) => {
            chrome.runtime.sendMessage({
                action: 'send_to_platform',
                platform,
                command,
                context
            }, response => {
                if (chrome.runtime.lastError) {
                    reject(chrome.runtime.lastError);
                } else {
                    resolve(response);
                }
            });
        });
    }
    
    async callMCPTool(toolName, params) {
        return new Promise((resolve, reject) => {
            chrome.runtime.sendMessage({
                action: 'mcp_call',
                tool: toolName,
                params: params
            }, response => {
                if (chrome.runtime.lastError) {
                    reject(chrome.runtime.lastError);
                } else {
                    resolve(response);
                }
            });
        });
    }
    
    async executeWorkflow(workflow) {
        const results = [];
        for (const step of workflow.steps) {
            try {
                const result = await this.executeStep(step);
                results.push(result);
            } catch (error) {
                console.error('Step failed:', error);
                results.push({ error: error.message });
            }
        }
        return results;
    }
    
    async executeStep(step) {
        switch (step.type) {
            case 'ai_command':
                return await this.sendCommand(step.platform, step.command, step.context || {});
            case 'mcp_tool':
                return await this.callMCPTool(step.tool, step.params);
            case 'file_operation':
                return await this.handleFileOperation(step.operation, step.params);
            case 'github_action':
                return await this.handleGitHubAction(step.action, step.params);
            default:
                throw new Error(`Unknown step type: ${step.type}`);
        }
    }
    
    async handleFileOperation(operation, params) {
        const operations = {
            read: 'filesystem.read_text_file',
            write: 'filesystem.write_file',
            list: 'filesystem.list_directory'
        };
        return await this.callMCPTool(operations[operation], params);
    }
    
    async handleGitHubAction(action, params) {
        const actions = {
            commit: 'filesystem.execute_command',
            push: 'filesystem.execute_command',
            pull: 'filesystem.execute_command'
        };
        
        const commands = {
            commit: `git add . && git commit -m "${params.message}"`,
            push: 'git push origin main',
            pull: 'git pull origin main'
        };
        
        return await this.callMCPTool(actions[action], {
            command: commands[action],
            cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
        });
    }
    
    async multiAIAnalysis(task) {
        const results = {};
        for (const platform of ['chatgpt', 'claude', 'perplexity']) {
            try {
                results[platform] = await this.sendCommand(platform, task.query, task.context);
            } catch (error) {
                results[platform] = { error: error.message };
            }
        }
        return results;
    }
}

// Initialize AI Integration
const ai = new AIIntegration();

// Platform status check
async function checkPlatformStatus() {
    const platforms = ['chatgpt', 'claude', 'perplexity'];
    
    for (const platform of platforms) {
        chrome.tabs.query({url: `https://${platform}*/*`}, (tabs) => {
            const statusDot = document.getElementById(`${platform}-status`);
            if (statusDot) {
                if (tabs.length > 0) {
                    statusDot.classList.add('active');
                } else {
                    statusDot.classList.remove('active');
                }
            }
        });
    }
}

// Tab switching
document.querySelectorAll('.main-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active from all tabs and contents
        document.querySelectorAll('.main-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active to clicked tab and corresponding content
        tab.classList.add('active');
        const contentId = tab.dataset.tab;
        document.getElementById(contentId).classList.add('active');
    });
});

// Workflow functions
async function startWorkflow(type) {
    const workflows = {
        research: {
            name: 'Research & Analysis',
            steps: [
                {
                    type: 'ai_command',
                    platform: 'perplexity',
                    command: 'Search for the latest information on the topic'
                },
                {
                    type: 'ai_command',
                    platform: 'chatgpt',
                    command: 'Analyze the search results and provide insights'
                },
                {
                    type: 'ai_command',
                    platform: 'claude',
                    command: 'Synthesize all findings into a comprehensive report'
                }
            ]
        },
        code: {
            name: 'Code Generation',
            steps: [
                {
                    type: 'ai_command',
                    platform: 'claude',
                    command: 'Generate the requested code'
                },
                {
                    type: 'ai_command',
                    platform: 'chatgpt',
                    command: 'Review the code for improvements'
                },
                {
                    type: 'github_action',
                    action: 'commit',
                    params: {message: 'Add generated code'}
                }
            ]
        },
        debug: {
            name: 'Debug & Fix',
            steps: [
                {
                    type: 'file_operation',
                    operation: 'read',
                    params: {path: 'current_file.js'}
                },
                {
                    type: 'ai_command',
                    platform: 'claude',
                    command: 'Debug this code and find issues'
                },
                {
                    type: 'ai_command',
                    platform: 'chatgpt',
                    command: 'Validate the bug fixes'
                },
                {
                    type: 'github_action',
                    action: 'commit',
                    params: {message: 'Fix bugs'}
                }
            ]
        },
        document: {
            name: 'Documentation',
            steps: [
                {
                    type: 'file_operation',
                    operation: 'read',
                    params: {path: 'src/'}
                },
                {
                    type: 'ai_command',
                    platform: 'claude',
                    command: 'Generate documentation for this code'
                },
                {
                    type: 'file_operation',
                    operation: 'write',
                    params: {path: 'README.md'}
                },
                {
                    type: 'github_action',
                    action: 'push'
                }
            ]
        }
    };
    
    const workflow = workflows[type];
    if (workflow) {
        addActivityLog(`Starting workflow: ${workflow.name}`);
        const results = await ai.executeWorkflow(workflow);
        addActivityLog(`Workflow completed: ${workflow.name}`);
        showResults(results);
    }
}

// Custom workflow execution
async function executeCustomWorkflow() {
    const steps = [];
    document.querySelectorAll('#custom-workflow .workflow-step').forEach((stepEl, index) => {
        const platformEl = stepEl.querySelector('.step-platform');
        const inputEl = stepEl.querySelector('input');
        
        if (platformEl && inputEl && inputEl.value) {
            steps.push({
                type: 'ai_command',
                platform: platformEl.textContent.toLowerCase(),
                command: inputEl.value
            });
        }
    });
    
    if (steps.length > 0) {
        addActivityLog('Executing custom workflow...');
        const results = await ai.executeWorkflow({steps});
        showResults(results);
    }
}

// Send direct command
async function sendCommand() {
    const platform = document.getElementById('platform-select').value;
    const command = document.getElementById('command-text').value;
    
    if (!command) return;
    
    addActivityLog(`Sending command to ${platform}: ${command.substring(0, 50)}...`);
    
    if (platform === 'all') {
        const results = await ai.multiAIAnalysis({
            query: command,
            context: {}
        });
        showResults(results);
    } else {
        const result = await ai.sendCommand(platform, command);
        showResults([result]);
    }
    
    document.getElementById('command-text').value = '';
}

// Template commands
async function sendTemplate(type) {
    const templates = {
        review: 'Review this code and provide detailed feedback on improvements',
        optimize: 'Optimize this code for better performance and readability',
        explain: 'Explain this code in detail, including its purpose and how it works',
        test: 'Generate comprehensive unit tests for this code'
    };
    
    document.getElementById('command-text').value = templates[type];
    await sendCommand();
}

// GitHub actions
async function gitAction(action) {
    addActivityLog(`Executing git ${action}...`);
    
    const actions = {
        status: async () => {
            const result = await ai.callMCPTool('filesystem.execute_command', {
                command: 'git status',
                cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
            });
            showGitResult(result);
        },
        pull: async () => {
            const result = await ai.callMCPTool('filesystem.execute_command', {
                command: 'git pull origin main',
                cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
            });
            showGitResult(result);
        },
        commit: async () => {
            const message = prompt('Commit message:') || 'Update files';
            const result = await ai.callMCPTool('filesystem.execute_command', {
                command: `git add . && git commit -m "${message}"`,
                cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
            });
            showGitResult(result);
        },
        push: async () => {
            const result = await ai.callMCPTool('filesystem.execute_command', {
                command: 'git push origin main',
                cwd: 'C:\\Users\\8899y\\AI-WORKSPACE'
            });
            showGitResult(result);
        }
    };
    
    if (actions[action]) {
        await actions[action]();
    }
}

// Save file
async function saveFile() {
    const path = document.getElementById('file-path').value;
    const content = document.getElementById('file-content').value;
    
    if (!path || !content) {
        alert('Please enter file path and content');
        return;
    }
    
    addActivityLog(`Saving file: ${path}`);
    
    const result = await ai.handleFileOperation('write', {
        path: `C:\\Users\\8899y\\AI-WORKSPACE\\${path}`,
        content
    });
    
    if (result) {
        const commitResult = await ai.handleGitHubAction('commit', {
            message: `Update ${path}`
        });
        showGitResult(commitResult);
    }
}

// UI Helper Functions
function addActivityLog(message) {
    const log = document.getElementById('activity-log');
    if (log) {
        const item = document.createElement('div');
        item.className = 'result-item';
        item.innerHTML = `
            <span style="color: #888; font-size: 11px;">${new Date().toLocaleTimeString()}</span>
            ${message}
        `;
        log.insertBefore(item, log.firstChild);
    }
}

function showResults(results) {
    const resultsEl = document.getElementById('command-results');
    if (resultsEl) {
        resultsEl.innerHTML = '';
        if (Array.isArray(results)) {
            results.forEach(result => {
                const item = document.createElement('div');
                item.className = 'result-item';
                item.textContent = JSON.stringify(result, null, 2);
                resultsEl.appendChild(item);
            });
        } else {
            resultsEl.textContent = JSON.stringify(results, null, 2);
        }
    }
}

function showGitResult(result) {
    const resultsEl = document.getElementById('github-results');
    if (resultsEl) {
        resultsEl.innerHTML = `<div class="result-item">${result || 'Command executed'}</div>`;
    }
}

// Update counts
function updateCounts() {
    chrome.storage.local.get(['ai_sessions', 'task_results'], (data) => {
        const sessions = data.ai_sessions || [];
        const tasks = data.task_results || [];
        
        document.getElementById('session-count').textContent = sessions.length;
        document.getElementById('task-count').textContent = tasks.filter(t => 
            new Date(t.created).toDateString() === new Date().toDateString()
        ).length;
    });
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    checkPlatformStatus();
    updateCounts();
    addActivityLog('AI Workspace MCP Hub initialized');
    
    // Refresh status every 2 seconds
    setInterval(() => {
        checkPlatformStatus();
        updateCounts();
    }, 2000);
});

// Make functions available globally
window.startWorkflow = startWorkflow;
window.executeCustomWorkflow = executeCustomWorkflow;
window.sendCommand = sendCommand;
window.sendTemplate = sendTemplate;
window.gitAction = gitAction;
window.saveFile = saveFile;