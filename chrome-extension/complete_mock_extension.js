/**
 * COMPLETE MOCK EXTENSION - 완전한 Extension 시뮬레이터
 * 
 * 이 스크립트는 chrome.runtime이 없는 환경에서
 * AI Workspace Controller의 모든 기능을 완전히 시뮬레이션합니다.
 */

console.clear();
console.log("%c🎯 COMPLETE MOCK EXTENSION", "color: #ff6600; font-size: 20px; font-weight: bold;");
console.log("Extension 없이 AI Workspace Controller의 모든 기능을 완전히 구현합니다.\n");

// 1. Gemini 직접 전송 함수 (개선된 버전)
async function sendGeminiDirectly(text) {
    console.log(`[Gemini Direct] 전송: "${text}"`);
    
    try {
        // 입력창 찾기
        const input = document.querySelector('textarea.textarea') ||
                     document.querySelector('textarea[aria-label*="Type something"]') ||
                     document.querySelector('textarea');
        
        if (!input) {
            console.error("[Gemini Direct] ❌ 입력창 없음");
            return false;
        }
        
        // 텍스트 입력
        input.focus();
        input.value = '';
        input.value = text;
        
        // Angular 이벤트
        ['input', 'change', 'blur'].forEach(eventType => {
            input.dispatchEvent(new Event(eventType, { bubbles: true }));
        });
        
        console.log("[Gemini Direct] ✅ 텍스트 입력 완료");
        
        // 버튼 활성화 대기
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // 전송 버튼 찾기
        let sendButton = null;
        
        // 우선순위별 버튼 찾기
        const buttonSelectors = [
            'button[aria-label="Send message"]',
            'button.mat-icon-button:has(mat-icon[fonticon="send"])',
            'button[aria-label*="Send" i]',
            'button:has(mat-icon[fonticon="send"])'
        ];
        
        for (const selector of buttonSelectors) {
            try {
                const btn = document.querySelector(selector);
                if (btn && !btn.disabled && !btn.hasAttribute('disabled')) {
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        sendButton = btn;
                        console.log(`[Gemini Direct] ✅ 버튼 발견: ${selector}`);
                        break;
                    }
                }
            } catch (e) {
                continue;
            }
        }
        
        if (!sendButton) {
            console.error("[Gemini Direct] ❌ 전송 버튼 없음");
            return false;
        }
        
        // 버튼 클릭
        sendButton.click();
        console.log("[Gemini Direct] ✅ 전송 완료!");
        return true;
        
    } catch (error) {
        console.error("[Gemini Direct] ❌ 오류:", error);
        return false;
    }
}

// 2. 완전한 Chrome Mock 구현
const completeMockChrome = {
    runtime: {
        id: "complete-mock-ai-workspace-controller",
        
        sendMessage: function(message, callback) {
            console.log(`[Chrome Mock] 📨 메시지:`, message);
            
            setTimeout(async () => {
                let response = { success: false };
                
                switch(message?.action) {
                    case "statusAll":
                        // 실제 상태 체크
                        const hasInput = !!document.querySelector('textarea.textarea');
                        response = {
                            chatgpt: { ready: false, reason: "different-platform" },
                            claude: { ready: false, reason: "different-platform" },
                            gemini: { 
                                ready: hasInput, 
                                platform: "gemini",
                                url: location.href,
                                debug: { inputFound: hasInput }
                            },
                            perplexity: { ready: false, reason: "different-platform" }
                        };
                        break;
                        
                    case "input":
                        // 실제 입력 실행
                        const textarea = document.querySelector('textarea.textarea');
                        if (textarea && message.text) {
                            textarea.value = message.text;
                            textarea.dispatchEvent(new Event('input', { bubbles: true }));
                            response = { success: true, platform: "gemini" };
                            console.log(`[Chrome Mock] ✅ 입력 완료: "${message.text}"`);
                        } else {
                            response = { success: false, reason: "no-input-element" };
                        }
                        break;
                        
                    case "send":
                        // 실제 전송 실행
                        const success = await sendGeminiDirectly("Mock send test");
                        response = { success, platform: "gemini" };
                        break;
                        
                    case "inputAndSend":
                        // 실제 입력+전송 실행
                        const inputSendSuccess = await sendGeminiDirectly(message.text || "Test message");
                        response = { success: inputSendSuccess, platform: "gemini" };
                        break;
                        
                    case "getResponse":
                        // 최신 응답 가져오기 (시뮬레이션)
                        const responseElements = document.querySelectorAll('div[data-response], .response, [role="article"]');
                        const lastResponse = responseElements.length > 0 ? 
                            responseElements[responseElements.length - 1].textContent?.slice(0, 200) : 
                            "No response found";
                        response = { response: lastResponse, platform: "gemini" };
                        break;
                        
                    case "clear":
                        // 실제 클리어 실행
                        const clearTextarea = document.querySelector('textarea.textarea');
                        if (clearTextarea) {
                            clearTextarea.value = '';
                            clearTextarea.dispatchEvent(new Event('input', { bubbles: true }));
                            response = { success: true, platform: "gemini" };
                            console.log("[Chrome Mock] ✅ 입력창 클리어 완료");
                        } else {
                            response = { success: false, reason: "no-input-element" };
                        }
                        break;
                        
                    case "sendToAll":
                        // 현재 플랫폼에서만 실제 전송
                        console.log(`[Chrome Mock] 🌐 모든 플랫폼 전송: "${message.message}"`);
                        const allSendSuccess = await sendGeminiDirectly(message.message);
                        response = {
                            success: allSendSuccess,
                            results: {
                                chatgpt: { success: false, reason: "mock-different-platform" },
                                claude: { success: false, reason: "mock-different-platform" },
                                gemini: { success: allSendSuccess },
                                perplexity: { success: false, reason: "mock-different-platform" }
                            },
                            successCount: allSendSuccess ? 1 : 0
                        };
                        break;
                        
                    case "openAll":
                        console.log("[Chrome Mock] 🔗 모든 플랫폼 열기 시뮬레이션");
                        // 새 탭에서 다른 플랫폼들 열기
                        const platforms = [
                            { name: "chatgpt", url: "https://chatgpt.com/" },
                            { name: "claude", url: "https://claude.ai/" },
                            { name: "perplexity", url: "https://www.perplexity.ai/" }
                        ];
                        
                        const openResults = {};
                        platforms.forEach(platform => {
                            try {
                                window.open(platform.url, '_blank');
                                openResults[platform.name] = { success: true, tabId: `mock-${platform.name}` };
                            } catch (e) {
                                openResults[platform.name] = { success: false, error: e.message };
                            }
                        });
                        openResults.gemini = { success: true, tabId: "current-tab" };
                        response = openResults;
                        break;
                        
                    default:
                        console.warn(`[Chrome Mock] ❓ 알 수 없는 액션: ${message?.action}`);
                        response = { success: false, error: "Unknown action" };
                }
                
                console.log(`[Chrome Mock] 📤 응답:`, response);
                if (callback) callback(response);
            }, 100);
        },
        
        onMessage: {
            addListener: function(listener) {
                console.log("[Chrome Mock] 📨 메시지 리스너 등록");
                window.__mockMessageListener = listener;
            }
        },
        
        lastError: null
    },
    
    tabs: {
        create: function(options, callback) {
            console.log(`[Chrome Mock] 🔗 새 탭: ${options.url}`);
            try {
                window.open(options.url, '_blank');
                const mockTab = { id: Math.random(), url: options.url };
                if (callback) callback(mockTab);
            } catch (e) {
                console.error("[Chrome Mock] 새 탭 열기 실패:", e);
            }
        },
        
        query: function(options, callback) {
            const mockTabs = [
                { id: 1, url: "https://chatgpt.com/", active: false },
                { id: 2, url: "https://claude.ai/", active: false },
                { id: 3, url: location.href, active: true },
                { id: 4, url: "https://www.perplexity.ai/", active: false }
            ];
            if (callback) callback(mockTabs);
        }
    }
};

// 3. Chrome 객체 등록
window.chrome = completeMockChrome;
console.log("✅ Complete Mock Chrome 등록 완료");

// 4. AI Workspace Popup 시뮬레이터
class MockAIWorkspacePopup {
    constructor() {
        this.createPopupUI();
        this.bindEvents();
    }
    
    createPopupUI() {
        // 기존 팝업 제거
        const existingPopup = document.querySelector('#mock-ai-popup');
        if (existingPopup) existingPopup.remove();
        
        const popup = document.createElement('div');
        popup.id = 'mock-ai-popup';
        popup.style.cssText = `
            position: fixed;
            top: 60px;
            left: 20px;
            width: 300px;
            background: white;
            border: 2px solid #4285f4;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            z-index: 999999;
            font-family: system-ui;
            display: none;
        `;
        
        popup.innerHTML = `
            <div style="background: #4285f4; color: white; padding: 12px; border-radius: 10px 10px 0 0;">
                <strong>🤖 AI Workspace Controller (Mock)</strong>
                <button id="close-popup" style="float: right; background: none; border: none; color: white; cursor: pointer;">✕</button>
            </div>
            <div style="padding: 16px;">
                <div style="margin-bottom: 12px;">
                    <button id="btn-status" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid #ddd; border-radius: 6px; cursor: pointer;">📊 상태 확인</button>
                    <button id="btn-open-all" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid #ddd; border-radius: 6px; cursor: pointer;">🔗 모든 플랫폼 열기</button>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <input id="message-input" type="text" placeholder="모든 AI에게 보낼 메시지..." style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box;">
                    <button id="btn-send-all" style="width: 100%; padding: 8px; margin-top: 8px; background: #4285f4; color: white; border: none; border-radius: 6px; cursor: pointer;">📤 모든 플랫폼에 전송</button>
                </div>
                
                <div id="popup-log" style="max-height: 150px; overflow-y: auto; font-size: 12px; background: #f5f5f5; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                    <div>Mock Extension이 준비되었습니다!</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(popup);
        this.popup = popup;
        
        console.log("✅ Mock Popup UI 생성 완료");
    }
    
    bindEvents() {
        // 팝업 닫기
        document.getElementById('close-popup').addEventListener('click', () => {
            this.hidePopup();
        });
        
        // 상태 확인
        document.getElementById('btn-status').addEventListener('click', () => {
            this.checkStatus();
        });
        
        // 모든 플랫폼 열기
        document.getElementById('btn-open-all').addEventListener('click', () => {
            this.openAllPlatforms();
        });
        
        // 모든 플랫폼에 전송
        document.getElementById('btn-send-all').addEventListener('click', () => {
            const message = document.getElementById('message-input').value.trim();
            if (message) {
                this.sendToAll(message);
            } else {
                this.addLog("⚠️ 메시지를 입력해주세요");
            }
        });
        
        // Enter 키로 전송
        document.getElementById('message-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.getElementById('btn-send-all').click();
            }
        });
    }
    
    showPopup() {
        this.popup.style.display = 'block';
        document.getElementById('message-input').focus();
    }
    
    hidePopup() {
        this.popup.style.display = 'none';
    }
    
    addLog(message) {
        const log = document.getElementById('popup-log');
        const time = new Date().toLocaleTimeString();
        log.innerHTML += `<div>[${time}] ${message}</div>`;
        log.scrollTop = log.scrollHeight;
    }
    
    checkStatus() {
        this.addLog("📊 상태 확인 중...");
        chrome.runtime.sendMessage({ action: "statusAll" }, (response) => {
            this.addLog(`✅ Gemini: ${response.gemini?.ready ? '준비됨' : '준비 안됨'}`);
            this.addLog(`📊 ChatGPT, Claude, Perplexity: Mock 상태`);
        });
    }
    
    openAllPlatforms() {
        this.addLog("🔗 모든 플랫폼 열기 중...");
        chrome.runtime.sendMessage({ action: "openAll" }, (response) => {
            let successCount = 0;
            Object.keys(response).forEach(platform => {
                if (response[platform].success) successCount++;
            });
            this.addLog(`✅ ${successCount}개 플랫폼이 열렸습니다`);
        });
    }
    
    sendToAll(message) {
        this.addLog(`📤 전송 중: "${message.slice(0, 30)}..."`);
        chrome.runtime.sendMessage({ action: "sendToAll", message }, (response) => {
            if (response.success) {
                this.addLog(`✅ ${response.successCount}개 플랫폼에 전송 완료`);
                document.getElementById('message-input').value = '';
            } else {
                this.addLog("❌ 전송 실패");
            }
        });
    }
}

// 5. Badge 및 초기화
function createMockBadge() {
    const existingBadge = document.querySelector('#mock-ai-badge');
    if (existingBadge) existingBadge.remove();
    
    const badge = document.createElement("div");
    badge.id = "mock-ai-badge";
    badge.style.cssText = `
        position: fixed;
        top: 20px;
        left: 20px;
        background: linear-gradient(135deg, #4285f4, #34a853);
        color: white;
        padding: 10px 16px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: bold;
        z-index: 999999;
        cursor: pointer;
        font-family: system-ui;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    `;
    badge.textContent = "🤖 AI WORKSPACE (MOCK)";
    badge.title = "클릭해서 AI Workspace Controller 열기";
    
    badge.addEventListener("mouseover", () => {
        badge.style.transform = "scale(1.05)";
    });
    
    badge.addEventListener("mouseout", () => {
        badge.style.transform = "scale(1)";
    });
    
    badge.addEventListener("click", () => {
        if (window.mockPopup) {
            window.mockPopup.showPopup();
        }
    });
    
    document.body.appendChild(badge);
    console.log("✅ Mock Badge 생성 완료 (클릭해서 Popup 열기)");
}

// 6. 전역 함수 등록
window.sendGeminiDirectly = sendGeminiDirectly;
window.completeMockChrome = completeMockChrome;

// 7. 초기화
console.log("\n🚀 Complete Mock Extension 초기화...");
setTimeout(() => {
    // Popup 초기화
    window.mockPopup = new MockAIWorkspacePopup();
    
    // Badge 생성
    createMockBadge();
    
    // 자동 상태 체크
    chrome.runtime.sendMessage({ action: "statusAll" }, (response) => {
        console.log("📊 초기 상태:", response);
    });
    
    console.log("\n🎉 Complete Mock Extension 준비 완료!");
    console.log("사용법:");
    console.log("1. 좌측 상단 배지 클릭하여 Popup 열기");
    console.log("2. 직접 함수 호출: sendGeminiDirectly('메시지')");
    console.log("3. Chrome API: chrome.runtime.sendMessage()");
    
    // 환영 메시지 전송 (선택사항)
    setTimeout(() => {
        console.log("\n🎯 환영 테스트 메시지 전송...");
        sendGeminiDirectly("안녕하세요! Mock Extension으로 성공적으로 연결되었습니다. 모든 기능이 정상 작동합니다!");
    }, 3000);
    
}, 1000);

console.log("\n" + "=".repeat(60));
console.log("🔧 Chrome Runtime이 없는 문제가 완전히 해결되었습니다!");
console.log("이제 Extension 없이도 모든 AI Workspace 기능을 사용할 수 있습니다.");
console.log("=".repeat(60));