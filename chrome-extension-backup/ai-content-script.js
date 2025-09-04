/**
 * AI Platform Content Script
 * 각 AI 플랫폼 페이지에 주입되어 실제 상호작용을 처리
 */

(function() {
    const platform = detectPlatform();
    
    function detectPlatform() {
        const hostname = window.location.hostname;
        if (hostname.includes('chatgpt.com')) return 'chatgpt';
        if (hostname.includes('claude.ai')) return 'claude';
        if (hostname.includes('perplexity.ai')) return 'perplexity';
        return null;
    }
    
    // 플랫폼별 선택자
    const selectors = {
        chatgpt: {
            input: 'textarea[data-id="root"]',
            sendButton: 'button[data-testid="send-button"]',
            messages: '.group.w-full',
            lastMessage: '.group.w-full:last-child .markdown'
        },
        claude: {
            input: 'div.ProseMirror',
            sendButton: 'button[aria-label="Send Message"]',
            messages: 'div[data-test-render-count]',
            lastMessage: 'div[data-test-render-count]:last-child'
        },
        perplexity: {
            input: 'textarea.grow',
            sendButton: 'button[aria-label="Submit"]',
            messages: '.prose',
            lastMessage: '.prose:last-child'
        }
    };
    
    /**
     * 메시지 입력
     */
    function inputMessage(text) {
        const selector = selectors[platform]?.input;
        if (!selector) return false;
        
        const inputElement = document.querySelector(selector);
        if (!inputElement) return false;
        
        if (platform === 'claude') {
            // Claude는 contenteditable div 사용
            inputElement.innerHTML = text;
            inputElement.dispatchEvent(new Event('input', {bubbles: true}));
        } else {
            // ChatGPT와 Perplexity는 textarea 사용
            inputElement.value = text;
            inputElement.dispatchEvent(new Event('input', {bubbles: true}));
        }
        
        return true;
    }
    
    /**
     * 메시지 전송
     */
    function sendMessage() {
        const selector = selectors[platform]?.sendButton;
        if (!selector) return false;
        
        const button = document.querySelector(selector);
        if (button && !button.disabled) {
            button.click();
            return true;
        }
        
        // 대체 방법: Enter 키 시뮬레이션
        const inputSelector = selectors[platform]?.input;
        const input = document.querySelector(inputSelector);
        if (input) {
            const enterEvent = new KeyboardEvent('keydown', {
                key: 'Enter',
                code: 'Enter',
                keyCode: 13,
                which: 13,
                bubbles: true
            });
            input.dispatchEvent(enterEvent);
            return true;
        }
        
        return false;
    }
    
    /**
     * 응답 대기 및 읽기
     */
    async function waitForResponse(timeout = 30000) {
        const startTime = Date.now();
        let lastMessageCount = document.querySelectorAll(selectors[platform]?.messages).length;
        
        while (Date.now() - startTime < timeout) {
            await new Promise(resolve => setTimeout(resolve, 500));
            
            const currentMessageCount = document.querySelectorAll(selectors[platform]?.messages).length;
            
            if (currentMessageCount > lastMessageCount) {
                // 새 메시지 감지
                await new Promise(resolve => setTimeout(resolve, 2000)); // 응답 완료 대기
                
                const lastMessage = document.querySelector(selectors[platform]?.lastMessage);
                if (lastMessage) {
                    return lastMessage.innerText || lastMessage.textContent;
                }
            }
        }
        
        throw new Error('Response timeout');
    }
    
    /**
     * 명령 실행
     */
    async function executeCommand(command, context) {
        console.log(`[${platform}] Executing command:`, command);
        
        // 컨텍스트 포함 메시지 구성
        let fullMessage = command;
        if (context && Object.keys(context).length > 0) {
            fullMessage = `${command}\n\nContext:\n${JSON.stringify(context, null, 2)}`;
        }
        
        // 메시지 입력
        if (!inputMessage(fullMessage)) {
            throw new Error('Failed to input message');
        }
        
        // 잠시 대기
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 메시지 전송
        if (!sendMessage()) {
            throw new Error('Failed to send message');
        }
        
        // 응답 대기
        try {
            const response = await waitForResponse();
            return {
                platform,
                command,
                response,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                platform,
                command,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }
    
    /**
     * 코드 블록 추출
     */
    function extractCodeBlocks() {
        const codeBlocks = [];
        const codeElements = document.querySelectorAll('pre code, .code-block');
        
        codeElements.forEach(element => {
            const language = element.className.match(/language-(\w+)/)?.[1] || 'text';
            const code = element.textContent;
            
            codeBlocks.push({
                language,
                code,
                timestamp: new Date().toISOString()
            });
        });
        
        return codeBlocks;
    }
    
    /**
     * 대화 내역 추출
     */
    function extractConversation() {
        const messages = [];
        const messageElements = document.querySelectorAll(selectors[platform]?.messages);
        
        messageElements.forEach((element, index) => {
            const isUser = index % 2 === 0; // 간단한 추정
            messages.push({
                role: isUser ? 'user' : 'assistant',
                content: element.innerText || element.textContent,
                timestamp: new Date().toISOString()
            });
        });
        
        return messages;
    }
    
    /**
     * 메시지 리스너
     */
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        console.log(`[${platform}] Received message:`, request);
        
        if (request.type === 'AI_COMMAND') {
            executeCommand(request.command, request.context)
                .then(result => sendResponse(result))
                .catch(error => sendResponse({error: error.message}));
            return true; // 비동기 응답
        }
        
        if (request.type === 'EXTRACT_CODE') {
            sendResponse(extractCodeBlocks());
            return true;
        }
        
        if (request.type === 'EXTRACT_CONVERSATION') {
            sendResponse(extractConversation());
            return true;
        }
        
        if (request.type === 'GET_STATUS') {
            sendResponse({
                platform,
                ready: !!document.querySelector(selectors[platform]?.input),
                url: window.location.href
            });
            return true;
        }
    });
    
    /**
     * 자동 명령 실행 (URL 파라미터 기반)
     */
    function checkAutoCommand() {
        const params = new URLSearchParams(window.location.search);
        const autoCommand = params.get('mcp_command');
        const context = params.get('mcp_context');
        
        if (autoCommand) {
            setTimeout(() => {
                executeCommand(autoCommand, context ? JSON.parse(context) : {})
                    .then(result => {
                        // 결과를 extension으로 전송
                        chrome.runtime.sendMessage({
                            type: 'AUTO_COMMAND_RESULT',
                            result
                        });
                    });
            }, 3000); // 페이지 로드 대기
        }
    }
    
    /**
     * MCP 통합 UI 추가
     */
    function addMCPInterface() {
        const mcpButton = document.createElement('div');
        mcpButton.innerHTML = `
            <div style="
                position: fixed;
                bottom: 80px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 20px;
                border-radius: 25px;
                cursor: pointer;
                z-index: 10000;
                font-family: system-ui;
                font-size: 14px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s;
            " 
            onmouseover="this.style.transform='scale(1.05)'"
            onmouseout="this.style.transform='scale(1)'"
            id="mcp-integration-button">
                <span>🤖</span>
                <span>MCP Active</span>
            </div>
        `;
        
        document.body.appendChild(mcpButton);
        
        mcpButton.addEventListener('click', () => {
            chrome.runtime.sendMessage({
                type: 'OPEN_MCP_PANEL',
                platform
            });
        });
    }
    
    /**
     * 초기화
     */
    function initialize() {
        if (!platform) return;
        
        console.log(`[MCP Integration] Initialized for ${platform}`);
        
        // 자동 명령 확인
        checkAutoCommand();
        
        // MCP UI 추가
        setTimeout(addMCPInterface, 2000);
        
        // 상태 보고
        chrome.runtime.sendMessage({
            type: 'PLATFORM_READY',
            platform,
            url: window.location.href
        });
    }
    
    // 페이지 로드 완료 후 초기화
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }
})();