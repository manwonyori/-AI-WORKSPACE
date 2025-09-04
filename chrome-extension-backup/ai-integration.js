/**
 * AI Platform Integration Module
 * ChatGPT, Claude, Perplexity와 실시간 통합
 */

class AIIntegration {
    constructor() {
        this.platforms = {
            chatgpt: {
                name: 'ChatGPT',
                url: 'https://chatgpt.com',
                active: false,
                capabilities: ['code', 'analysis', 'mcp']
            },
            claude: {
                name: 'Claude',
                url: 'https://claude.ai',
                active: false,
                capabilities: ['code', 'analysis', 'mcp', 'vision']
            },
            perplexity: {
                name: 'Perplexity',
                url: 'https://perplexity.ai',
                active: false,
                capabilities: ['search', 'research', 'mcp']
            }
        };
        
        this.sharedMemory = new Map();
        this.taskQueue = [];
        this.workflows = [];
    }
    
    /**
     * AI 플랫폼에 명령 전송
     */
    async sendCommand(platform, command, context = {}) {
        const message = {
            type: 'AI_COMMAND',
            platform: platform,
            command: command,
            context: context,
            timestamp: Date.now()
        };
        
        // Content script로 메시지 전송
        chrome.tabs.query({url: this.platforms[platform].url + '/*'}, (tabs) => {
            if (tabs.length > 0) {
                chrome.tabs.sendMessage(tabs[0].id, message);
            } else {
                console.log(`${platform} tab not found. Opening...`);
                this.openPlatform(platform);
            }
        });
        
        return message;
    }
    
    /**
     * AI 플랫폼 열기
     */
    async openPlatform(platform) {
        const url = this.platforms[platform].url;
        chrome.tabs.create({url: url}, (tab) => {
            this.platforms[platform].tabId = tab.id;
            this.platforms[platform].active = true;
        });
    }
    
    /**
     * 크로스 플랫폼 워크플로우 실행
     */
    async executeWorkflow(workflow) {
        const results = [];
        
        for (const step of workflow.steps) {
            const result = await this.executeStep(step);
            results.push(result);
            
            // 다음 단계에 결과 전달
            if (step.passResultTo) {
                this.sharedMemory.set(step.passResultTo, result);
            }
        }
        
        return results;
    }
    
    /**
     * 워크플로우 단계 실행
     */
    async executeStep(step) {
        switch (step.type) {
            case 'ai_command':
                return await this.sendCommand(step.platform, step.command, step.context);
                
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
    
    /**
     * MCP 도구 호출
     */
    async callMCPTool(toolName, params) {
        return new Promise((resolve, reject) => {
            chrome.runtime.sendMessage({
                action: 'mcp_call',
                tool: toolName,
                params: params
            }, (response) => {
                if (response.error) {
                    reject(response.error);
                } else {
                    resolve(response.result);
                }
            });
        });
    }
    
    /**
     * 파일 작업 처리
     */
    async handleFileOperation(operation, params) {
        const operations = {
            read: 'filesystem.read_text_file',
            write: 'filesystem.write_file',
            list: 'filesystem.list_directory',
            search: 'filesystem.search_files'
        };
        
        return await this.callMCPTool(operations[operation], params);
    }
    
    /**
     * GitHub 작업 처리
     */
    async handleGitHubAction(action, params) {
        const actions = {
            commit: async (p) => {
                await this.callMCPTool('github.create_commit', p);
            },
            push: async (p) => {
                await this.callMCPTool('github.push_to_remote', p);
            },
            pull: async (p) => {
                await this.callMCPTool('github.pull_from_remote', p);
            },
            createPR: async (p) => {
                await this.callMCPTool('github.create_pull_request', p);
            }
        };
        
        return await actions[action](params);
    }
    
    /**
     * 실시간 협업 세션 시작
     */
    async startCollaborationSession(config) {
        const session = {
            id: Date.now().toString(),
            name: config.name,
            platforms: config.platforms || ['chatgpt', 'claude'],
            created: new Date().toISOString(),
            messages: [],
            tasks: []
        };
        
        // 각 플랫폼 활성화
        for (const platform of session.platforms) {
            await this.openPlatform(platform);
        }
        
        // 세션 저장
        this.saveSession(session);
        
        return session;
    }
    
    /**
     * 세션 저장
     */
    saveSession(session) {
        chrome.storage.local.get(['ai_sessions'], (data) => {
            const sessions = data.ai_sessions || [];
            sessions.push(session);
            chrome.storage.local.set({ai_sessions: sessions});
        });
    }
    
    /**
     * 작업 큐에 추가
     */
    addToQueue(task) {
        this.taskQueue.push({
            ...task,
            id: Date.now().toString(),
            status: 'pending',
            created: new Date().toISOString()
        });
        
        // 자동 실행
        if (task.autoExecute) {
            this.processQueue();
        }
    }
    
    /**
     * 작업 큐 처리
     */
    async processQueue() {
        while (this.taskQueue.length > 0) {
            const task = this.taskQueue.shift();
            
            if (task.status === 'pending') {
                task.status = 'processing';
                
                try {
                    const result = await this.executeTask(task);
                    task.status = 'completed';
                    task.result = result;
                } catch (error) {
                    task.status = 'failed';
                    task.error = error.message;
                }
                
                // 결과 저장
                this.saveTaskResult(task);
            }
        }
    }
    
    /**
     * 작업 실행
     */
    async executeTask(task) {
        switch (task.type) {
            case 'multi_ai_analysis':
                return await this.multiAIAnalysis(task);
                
            case 'code_generation':
                return await this.generateCode(task);
                
            case 'research':
                return await this.conductResearch(task);
                
            default:
                return await this.executeStep(task);
        }
    }
    
    /**
     * 다중 AI 분석
     */
    async multiAIAnalysis(task) {
        const results = {};
        
        // ChatGPT에 분석 요청
        results.chatgpt = await this.sendCommand('chatgpt', 
            `Analyze: ${task.query}`, 
            {context: task.context}
        );
        
        // Claude에 분석 요청
        results.claude = await this.sendCommand('claude', 
            `Provide detailed analysis: ${task.query}`,
            {context: task.context}
        );
        
        // Perplexity에 검색 요청
        results.perplexity = await this.sendCommand('perplexity',
            `Search and summarize: ${task.query}`,
            {context: task.context}
        );
        
        return results;
    }
    
    /**
     * 코드 생성
     */
    async generateCode(task) {
        // Claude에 코드 생성 요청
        const code = await this.sendCommand('claude',
            `Generate ${task.language} code: ${task.description}`,
            {requirements: task.requirements}
        );
        
        // ChatGPT에 검증 요청
        const validation = await this.sendCommand('chatgpt',
            `Review and improve this code: ${code}`,
            {language: task.language}
        );
        
        // 파일로 저장
        if (task.savePath) {
            await this.handleFileOperation('write', {
                path: task.savePath,
                content: validation.improvedCode || code
            });
        }
        
        return {code, validation};
    }
    
    /**
     * 연구 수행
     */
    async conductResearch(task) {
        // Perplexity로 초기 검색
        const search = await this.sendCommand('perplexity',
            `Research: ${task.topic}`,
            {depth: task.depth || 'comprehensive'}
        );
        
        // ChatGPT로 분석
        const analysis = await this.sendCommand('chatgpt',
            `Analyze research findings: ${JSON.stringify(search)}`,
            {focus: task.focus}
        );
        
        // Claude로 종합
        const synthesis = await this.sendCommand('claude',
            `Synthesize research: ${JSON.stringify({search, analysis})}`,
            {format: task.outputFormat || 'detailed_report'}
        );
        
        return {search, analysis, synthesis};
    }
    
    /**
     * 작업 결과 저장
     */
    saveTaskResult(task) {
        chrome.storage.local.get(['task_results'], (data) => {
            const results = data.task_results || [];
            results.push(task);
            chrome.storage.local.set({task_results: results});
        });
    }
}

// 전역 인스턴스 생성
window.aiIntegration = new AIIntegration();