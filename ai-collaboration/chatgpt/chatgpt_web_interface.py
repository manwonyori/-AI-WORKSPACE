"""
ChatGPT를 위한 웹 인터페이스
브라우저에서 메시지를 입력하면 자동으로 Claude와 대화
"""

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import json
import time
import random
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)

CHAT_FILE = r"C:\Users\8899y\mcp_shared\live_chat.json"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ChatGPT Tikitaka Interface</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: -apple-system, system-ui, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #0d1117;
            color: #c9d1d9;
        }
        h1 {
            color: #58a6ff;
            border-bottom: 1px solid #30363d;
            padding-bottom: 10px;
        }
        .chat-container {
            background: #161b22;
            border-radius: 8px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            border: 1px solid #30363d;
        }
        .message {
            margin: 10px 0;
            padding: 12px;
            border-radius: 8px;
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .chatgpt-msg {
            background: #1f6feb;
            margin-left: 50px;
            color: white;
        }
        .claude-msg {
            background: #8b5cf6;
            margin-right: 50px;
            color: white;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 12px;
            border: 1px solid #30363d;
            border-radius: 6px;
            background: #0d1117;
            color: #c9d1d9;
            font-size: 14px;
        }
        button {
            padding: 12px 24px;
            background: #238636;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }
        button:hover {
            background: #2ea043;
        }
        .auto-mode {
            margin-top: 20px;
            padding: 15px;
            background: #161b22;
            border-radius: 8px;
            border: 1px solid #30363d;
        }
        .toggle-btn {
            background: #21262d;
            border: 1px solid #30363d;
        }
        .toggle-btn.active {
            background: #238636;
        }
        .status {
            margin-top: 10px;
            padding: 10px;
            background: #0d1117;
            border-radius: 6px;
            font-size: 12px;
            color: #8b949e;
        }
        .status.connected {
            border-left: 3px solid #3fb950;
        }
        .timestamp {
            font-size: 11px;
            color: #8b949e;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <h1>🤖 ChatGPT ↔️ Claude Tikitaka Interface</h1>
    
    <div class="status connected" id="status">
        연결 상태: ✅ Claude 봇 활성 | 메시지 수: <span id="msg-count">0</span>
    </div>
    
    <div class="chat-container" id="chat-container">
        <!-- 메시지가 여기에 표시됩니다 -->
    </div>
    
    <div class="input-area">
        <input type="text" id="message-input" placeholder="메시지를 입력하세요..." 
               onkeypress="if(event.key=='Enter') sendMessage()">
        <button onclick="sendMessage()">전송</button>
        <button onclick="refreshChat()" style="background: #21262d;">새로고침</button>
    </div>
    
    <div class="auto-mode">
        <h3>🚀 자동 티키타카 모드</h3>
        <button id="auto-btn" class="toggle-btn" onclick="toggleAutoMode()">
            자동 대화 시작
        </button>
        <div id="auto-status" style="margin-top: 10px; display: none;">
            자동 모드 실행 중... (<span id="auto-count">0</span>개 메시지)
        </div>
    </div>
    
    <script>
        let autoMode = false;
        let autoInterval = null;
        let lastMessageId = 0;
        
        function refreshChat() {
            fetch('/api/messages')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('chat-container');
                    container.innerHTML = '';
                    
                    // 최근 20개 메시지만 표시
                    const messages = data.messages.slice(-20);
                    
                    messages.forEach(msg => {
                        const div = document.createElement('div');
                        div.className = 'message ' + 
                            (msg.sender === 'ChatGPT' ? 'chatgpt-msg' : 'claude-msg');
                        
                        div.innerHTML = `
                            <strong>${msg.sender}</strong>: ${msg.message}
                            <div class="timestamp">${msg.timestamp}</div>
                        `;
                        container.appendChild(div);
                    });
                    
                    container.scrollTop = container.scrollHeight;
                    document.getElementById('msg-count').textContent = data.messages.length;
                    
                    if (messages.length > 0) {
                        lastMessageId = messages[messages.length - 1].id;
                    }
                });
        }
        
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            if (!message) return;
            
            fetch('/api/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            }).then(() => {
                input.value = '';
                refreshChat();
            });
        }
        
        function toggleAutoMode() {
            autoMode = !autoMode;
            const btn = document.getElementById('auto-btn');
            const status = document.getElementById('auto-status');
            
            if (autoMode) {
                btn.textContent = '자동 대화 중지';
                btn.classList.add('active');
                status.style.display = 'block';
                startAutoConversation();
            } else {
                btn.textContent = '자동 대화 시작';
                btn.classList.remove('active');
                status.style.display = 'none';
                stopAutoConversation();
            }
        }
        
        function startAutoConversation() {
            let messageCount = 0;
            
            // 초기 메시지 전송
            const starters = [
                "안녕하세요 Claude! 오늘은 알고리즘 최적화에 대해 이야기해볼까요?",
                "실시간 시스템 설계에 대한 의견을 듣고 싶습니다.",
                "최근 흥미로운 기술 트렌드가 있나요?",
                "코드 리뷰 베스트 프랙티스에 대해 어떻게 생각하시나요?"
            ];
            
            fetch('/api/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message: starters[Math.floor(Math.random() * starters.length)]
                })
            });
            
            autoInterval = setInterval(() => {
                fetch('/api/auto-respond')
                    .then(r => r.json())
                    .then(data => {
                        if (data.responded) {
                            messageCount++;
                            document.getElementById('auto-count').textContent = messageCount;
                            refreshChat();
                        }
                    });
                    
                if (messageCount >= 10) {
                    toggleAutoMode();
                }
            }, 3000);
        }
        
        function stopAutoConversation() {
            if (autoInterval) {
                clearInterval(autoInterval);
                autoInterval = null;
            }
        }
        
        // 자동 새로고침
        setInterval(refreshChat, 2000);
        refreshChat();
    </script>
</body>
</html>
"""

def read_chat():
    try:
        with open(CHAT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"messages": []}

def write_message(text):
    data = read_chat()
    new_msg = {
        "id": len(data["messages"]) + 1,
        "sender": "ChatGPT",
        "message": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["messages"].append(new_msg)
    data["status"] = "ChatGPT_sent"
    
    with open(CHAT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return new_msg

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/messages')
def get_messages():
    return jsonify(read_chat())

@app.route('/api/send', methods=['POST'])
def send_message():
    message = request.json.get('message', '')
    if message:
        msg = write_message(message)
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False})

@app.route('/api/auto-respond', methods=['POST'])
def auto_respond():
    """자동 응답 생성"""
    data = read_chat()
    messages = data.get("messages", [])
    
    if not messages:
        return jsonify({"responded": False})
    
    last_msg = messages[-1]
    
    # Claude 메시지에 자동 응답
    if last_msg["sender"] == "Claude":
        responses = [
            "흥미로운 관점이네요! 구체적인 예시가 있나요?",
            "그 방법의 성능은 어떤가요?",
            "실제로 적용해본 경험을 공유해주세요.",
            "대안적인 접근 방식도 있을까요?",
            "좋은 아이디어네요! 더 자세히 설명해주실 수 있나요?"
        ]
        
        response = random.choice(responses)
        write_message(response)
        return jsonify({"responded": True, "message": response})
    
    return jsonify({"responded": False})

if __name__ == '__main__':
    print("=" * 60)
    print("   ChatGPT Web Interface")
    print("=" * 60)
    print("[OK] 서버 시작: http://localhost:7000")
    print("[INFO] 브라우저에서 열어서 사용하세요!")
    print("-" * 60)
    
    app.run(host='0.0.0.0', port=7000, debug=False)