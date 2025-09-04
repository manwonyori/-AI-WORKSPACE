"""
ChatGPT Desktop MCP 연결 스크립트
ChatGPT에서 직접 실행하여 MCP 서버와 통신
"""

import requests
import json
import time
from datetime import datetime

class MCPClient:
    def __init__(self):
        self.server_url = "http://localhost:3006"
        self.session_id = None
        
    def connect(self):
        """MCP 서버 연결"""
        try:
            # SSE 연결 테스트
            response = requests.get(f"{self.server_url}/sse", stream=True, timeout=2)
            if response.status_code == 200:
                print("[OK] MCP 서버 연결 성공!")
                return True
        except Exception as e:
            print(f"[ERROR] 연결 실패: {e}")
            return False
    
    def send_message(self, method, params=None):
        """MCP 서버로 메시지 전송"""
        message = {
            "jsonrpc": "2.0",
            "id": int(time.time()),
            "method": method,
            "params": params or {}
        }
        
        try:
            response = requests.post(
                f"{self.server_url}/message",
                json=message,
                headers={"Content-Type": "application/json"}
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"메시지 전송 실패: {e}")
            return None
    
    def read_file(self, file_path):
        """MCP를 통한 파일 읽기"""
        result = self.send_message("tools/call", {
            "name": "read_file",
            "arguments": {"path": file_path}
        })
        return result
    
    def write_file(self, file_path, content):
        """MCP를 통한 파일 쓰기"""
        result = self.send_message("tools/call", {
            "name": "write_file",  
            "arguments": {
                "path": file_path,
                "content": content
            }
        })
        return result
    
    def list_directory(self, dir_path):
        """디렉토리 목록 조회"""
        result = self.send_message("tools/call", {
            "name": "list_directory",
            "arguments": {"path": dir_path}
        })
        return result

# ChatGPT에서 실행할 코드
def main():
    print("=== ChatGPT MCP 연결 테스트 ===\n")
    
    # 1. MCP 클라이언트 생성
    client = MCPClient()
    
    # 2. 서버 연결 확인
    if not client.connect():
        print("서버 연결 실패. 대체 방법 사용...")
        
        # 대체 방법: 직접 파일 시스템 접근
        import os
        
        # Claude의 메시지 읽기
        claude_msg_path = r"C:\Users\8899y\mcp_shared\from_claude\hello_chatgpt.txt"
        if os.path.exists(claude_msg_path):
            with open(claude_msg_path, 'r', encoding='utf-8') as f:
                print("[MESSAGE] Claude의 메시지:")
                print(f.read())
                print()
        
        # ChatGPT 응답 작성
        response_path = r"C:\Users\8899y\mcp_shared\from_chatgpt\reply_from_chatgpt.txt"
        os.makedirs(os.path.dirname(response_path), exist_ok=True)
        
        response_content = f"""안녕하세요 Claude!

ChatGPT Desktop입니다. 메시지 잘 받았습니다!

MCP 서버 상태:
- Server URL: http://localhost:3006/sse
- 연결 시도 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 파일 시스템 공유: 성공

이제 양방향 통신이 가능합니다.
chatgpt_claude_bridge.json 파일을 통해 실시간 메시지를 교환할 수 있습니다.

ChatGPT Desktop에서 작성
"""
        
        with open(response_path, 'w', encoding='utf-8') as f:
            f.write(response_content)
        print("[OK] 응답 파일 생성 완료:", response_path)
        
        # Bridge 업데이트
        bridge_path = r"C:\Users\8899y\mcp_shared\chatgpt_claude_bridge.json"
        if os.path.exists(bridge_path):
            with open(bridge_path, 'r', encoding='utf-8') as f:
                bridge_data = json.load(f)
            
            # 새 메시지 추가
            new_message = {
                "id": len(bridge_data.get("messages", [])) + 1,
                "sender": "ChatGPT",
                "type": "text",
                "content": "연결 성공! 파일 시스템을 통한 통신 확립",
                "timestamp": datetime.now().isoformat()
            }
            
            bridge_data["messages"].append(new_message)
            
            with open(bridge_path, 'w', encoding='utf-8') as f:
                json.dump(bridge_data, f, indent=2, ensure_ascii=False)
            
            print("[OK] Bridge 상태 업데이트 완료")
            print(f"총 메시지 수: {len(bridge_data['messages'])}")

if __name__ == "__main__":
    main()