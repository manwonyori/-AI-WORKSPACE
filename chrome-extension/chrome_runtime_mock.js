/**
 * Chrome Runtime Mock - Extension 없이 완전한 기능 테스트
 * 
 * Google AI Studio에서 chrome.runtime이 없는 문제를 해결하기 위해
 * 완전한 chrome 객체를 시뮬레이션합니다.
 */

console.clear();
console.log("%c🔧 Chrome Runtime Mock 시스템", "color: #4285f4; font-size: 18px; font-weight: bold;");
console.log("Extension 없이 완전한 AI Workspace Controller 기능을 테스트합니다.\n");

// 1. Chrome Runtime Mock 객체 생성
const mockChrome = {
    runtime: {
        // Extension ID 시뮬레이션
        id: "mock-ai-workspace-controller",
        
        // 메시지 전송 시뮬레이션
        sendMessage: function(message, callback) {
            console.log(`[Mock Runtime] 메시지 전송:`, message);
            
            // Background script 응답 시뮬레이션
            setTimeout(() => {
                let response = { success: false };
                
                switch(message?.action) {
                    case "statusAll":
                        response = {
                            chatgpt: { ready: false, reason: "mock-test" },
                            claude: { ready: false, reason: "mock-test" },
                            gemini: { ready: true, platform: "gemini", url: location.href },
                            perplexity: { ready: false, reason: "mock-test" }
                        };
                        break;
                        
                    case "input":
                        console.log(`[Mock Runtime] 입력 시뮬레이션: "${message.text}"`);
                        response = { success: true, platform: "gemini" };
                        break;
                        
                    case "send":
                        console.log(`[Mock Runtime] 전송 시뮬레이션`);
                        response = { success: true, platform: "gemini" };
                        break;
                        
                    case "inputAndSend":
                        console.log(`[Mock Runtime] 입력+전송 시뮬레이션: "${message.text}"`);
                        // 실제 Gemini 전송 로직 실행
                        window.sendGeminiDirectly(message.text).then(success => {
                            response = { success, platform: "gemini" };
                            if (callback) callback(response);
                        });
                        return; // 비동기 처리를 위해 early return
                        
                    case "getResponse":
                        // 최근 응답 가져오기 시뮬레이션
                        const mockResponse = "Mock Gemini response: Message received successfully!";
                        response = { response: mockResponse, platform: "gemini" };
                        break;
                        
                    case "clear":
                        console.log(`[Mock Runtime] 입력창 클리어 시뮬레이션`);
                        // 실제 클리어 로직 실행
                        const textarea = document.querySelector('textarea.textarea');
                        if (textarea) {
                            textarea.value = '';
                            textarea.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                        response = { success: true, platform: "gemini" };
                        break;
                        
                    case "openAll":
                        console.log(`[Mock Runtime] 모든 플랫폼 열기 시뮬레이션`);
                        response = {
                            chatgpt: { success: true, tabId: "mock-tab-1" },
                            claude: { success: true, tabId: "mock-tab-2" },
                            gemini: { success: true, tabId: "mock-tab-3" },
                            perplexity: { success: true, tabId: "mock-tab-4" }
                        };
                        break;
                        
                    case "sendToAll":
                        console.log(`[Mock Runtime] 모든 플랫폼에 전송: "${message.message}"`);
                        // 현재 플랫폼(Gemini)에서만 실제 전송
                        window.sendGeminiDirectly(message.message).then(success => {
                            response = {
                                success: success,
                                results: {
                                    chatgpt: { success: false, reason: "mock-test" },
                                    claude: { success: false, reason: "mock-test" },
                                    gemini: { success: success },
                                    perplexity: { success: false, reason: "mock-test" }
                                },
                                successCount: success ? 1 : 0
                            };
                            if (callback) callback(response);
                        });
                        return;
                        
                    default:
                        console.warn(`[Mock Runtime] 알 수 없는 액션: ${message?.action}`);
                        response = { success: false, error: "Unknown action" };
                }
                
                console.log(`[Mock Runtime] 응답:`, response);
                if (callback) callback(response);
            }, 100); // 실제 네트워크 지연 시뮬레이션
        },
        
        // 메시지 리스너 시뮬레이션 (content script용)
        onMessage: {
            addListener: function(callback) {
                console.log("[Mock Runtime] 메시지 리스너 등록됨");
                // 테스트용 메시지 시뮬레이션 저장
                window.__mockMessageListener = callback;
            }
        },
        
        // 기타 runtime 속성들
        lastError: null,
        getManifest: function() {
            return {
                name: "AI Workspace Controller (Mock)",
                version: "1.4.1-mock",
                description: "Mock version for testing"
            };
        }
    },
    
    // 탭 관리 API 시뮬레이션
    tabs: {
        create: function(options, callback) {
            console.log(`[Mock Tabs] 새 탭 생성: ${options.url}`);
            const mockTab = {
                id: Math.floor(Math.random() * 1000),
                url: options.url,
                active: options.active || false
            };
            if (callback) callback(mockTab);
            return Promise.resolve(mockTab);
        },
        
        query: function(options, callback) {
            console.log(`[Mock Tabs] 탭 쿼리:`, options);
            const mockTabs = [
                { id: 1, url: "https://chatgpt.com/", active: false },
                { id: 2, url: "https://claude.ai/", active: false },
                { id: 3, url: location.href, active: true },
                { id: 4, url: "https://www.perplexity.ai/", active: false }
            ];
            if (callback) callback(mockTabs);
            return Promise.resolve(mockTabs);
        },
        
        sendMessage: function(tabId, message, callback) {
            console.log(`[Mock Tabs] 탭 ${tabId}에 메시지 전송:`, message);
            // 현재 탭이면 실제 처리, 아니면 mock
            if (tabId === 3) { // 현재 탭 ID
                return mockChrome.runtime.sendMessage(message, callback);
            } else {
                const mockResponse = { success: false, reason: "different-tab" };
                if (callback) callback(mockResponse);
            }
        }
    }
};

// 2. 전역 chrome 객체로 등록
if (typeof window !== 'undefined') {
    window.chrome = mockChrome;
    console.log("✅ Mock chrome 객체가 window.chrome으로 등록되었습니다");
} else if (typeof global !== 'undefined') {
    global.chrome = mockChrome;
    console.log("✅ Mock chrome 객체가 global.chrome으로 등록되었습니다");
}

// 3. Content Script 기능 테스트
async function testContentScriptFunctionality() {
    console.log("\n📋 Content Script 기능 테스트");
    console.log("-".repeat(50));
    
    // 현재 플랫폼 감지
    const platform = location.hostname.includes('aistudio.google.com') ? 'gemini' : 'unknown';
    console.log(`현재 플랫폼: ${platform}`);
    
    // 입력창 테스트
    const textarea = document.querySelector('textarea.textarea');
    if (textarea) {
        console.log("✅ 입력창 발견:", textarea.className);
    } else {
        console.log("❌ 입력창을 찾을 수 없음");
    }
    
    // Mock 메시지 전송 테스트
    console.log("\n📤 Mock 메시지 전송 테스트:");
    
    // Status 체크
    chrome.runtime.sendMessage({ action: "statusAll" }, (response) => {
        console.log("Status 응답:", response);
    });
    
    // 입력 테스트
    chrome.runtime.sendMessage({ 
        action: "inputAndSend", 
        text: "Mock Chrome Runtime을 통한 Gemini 테스트 메시지입니다!" 
    }, (response) => {
        console.log("InputAndSend 응답:", response);
    });
}

// 4. AI Workspace Controller 시뮬레이터
function simulateAIWorkspaceController() {
    console.log("\n🤖 AI Workspace Controller 시뮬레이터");
    console.log("-".repeat(50));
    
    // Popup 기능 시뮬레이션
    const popupActions = {
        openAll: () => {
            chrome.runtime.sendMessage({ action: "openAll" }, (response) => {
                console.log("모든 플랫폼 열기 결과:", response);
            });
        },
        
        statusAll: () => {
            chrome.runtime.sendMessage({ action: "statusAll" }, (response) => {
                console.log("모든 플랫폼 상태:", response);
            });
        },
        
        sendToAll: (message) => {
            chrome.runtime.sendMessage({ action: "sendToAll", message }, (response) => {
                console.log("모든 플랫폼 전송 결과:", response);
            });
        }
    };
    
    // 전역 함수로 등록
    window.popupActions = popupActions;
    
    console.log("💡 사용법:");
    console.log("- popupActions.openAll()");
    console.log("- popupActions.statusAll()");
    console.log("- popupActions.sendToAll('테스트 메시지')");
}

// 5. 상태 표시 Badge 생성 (Mock)
function createMockBadge() {
    // 기존 badge 제거
    const existingBadge = document.querySelector('#mock-ai-badge');
    if (existingBadge) {
        existingBadge.remove();
    }
    
    const badge = document.createElement("div");
    badge.id = "mock-ai-badge";
    badge.style.cssText = `
        position: fixed;
        top: 20px;
        left: 20px;
        background: #4285f4;
        color: white;
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        z-index: 999999;
        border: 2px solid #1a73e8;
        cursor: pointer;
        font-family: system-ui;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    `;
    badge.textContent = "🔧 MOCK GEMINI READY";
    badge.title = "Mock AI Workspace Controller - Gemini에서 테스트 중";
    
    badge.addEventListener("click", () => {
        console.log("🎯 Mock Extension Badge 클릭됨");
        console.log("사용 가능한 기능들:");
        console.log("- sendGeminiDirectly('메시지')");
        console.log("- popupActions.sendToAll('메시지')");
        console.log("- chrome.runtime.sendMessage({action: 'statusAll'})");
    });
    
    document.body.appendChild(badge);
    console.log("✅ Mock Badge 생성됨 (클릭해서 도움말 확인)");
}

// 6. 초기화 및 테스트 실행
console.log("\n🚀 Chrome Runtime Mock 초기화 완료");
console.log("=".repeat(60));

// 비동기 초기화
setTimeout(async () => {
    await testContentScriptFunctionality();
    simulateAIWorkspaceController();
    createMockBadge();
    
    console.log("\n🎉 Mock 시스템 준비 완료!");
    console.log("이제 Extension 없이도 모든 기능을 테스트할 수 있습니다.");
    
    // 자동 테스트 (선택사항)
    console.log("\n⏰ 5초 후 자동 테스트를 실행합니다...");
    setTimeout(() => {
        console.log("\n🧪 자동 테스트 시작:");
        popupActions.sendToAll("Mock 시스템 자동 테스트 메시지입니다!");
    }, 5000);
    
}, 1000);

// 전역 객체 확인
console.log("Chrome 객체 상태:", typeof chrome !== 'undefined' && chrome.runtime ? '✅' : '❌');
console.log("Runtime ID:", chrome?.runtime?.id || 'N/A');