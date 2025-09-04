"""
ChatGPT-Claude 실시간 통신 모니터
MCP 서버를 통한 양방향 통신 지원
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
import asyncio
import aiohttp

class ChatGPTClaudeBridge:
    def __init__(self):
        self.base_path = Path(r"C:\Users\8899y\mcp_shared")
        self.bridge_file = self.base_path / "chatgpt_claude_bridge.json"
        self.mcp_server = "http://localhost:3006"
        
    def read_bridge_status(self):
        """브릿지 상태 읽기"""
        if self.bridge_file.exists():
            with open(self.bridge_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def write_message(self, sender, content, msg_type="text"):
        """메시지 작성"""
        bridge_data = self.read_bridge_status()
        if not bridge_data:
            bridge_data = {
                "bridge_info": {
                    "status": "active"
                },
                "messages": [],
                "shared_tasks": []
            }
        
        message = {
            "id": len(bridge_data["messages"]) + 1,
            "sender": sender,
            "type": msg_type,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        bridge_data["messages"].append(message)
        
        with open(self.bridge_file, 'w', encoding='utf-8') as f:
            json.dump(bridge_data, f, indent=2, ensure_ascii=False)
        
        return message
    
    def monitor_folder(self, folder_name):
        """폴더 모니터링"""
        folder_path = self.base_path / folder_name
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
            
        files = list(folder_path.glob("*"))
        return [str(f.relative_to(self.base_path)) for f in files]
    
    async def check_mcp_connection(self):
        """MCP 서버 연결 확인"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.mcp_server}/sse", timeout=2) as resp:
                    return resp.status == 200
        except:
            return False
    
    def create_task(self, title, description, assigned_to="both"):
        """공유 작업 생성"""
        bridge_data = self.read_bridge_status()
        
        task = {
            "id": len(bridge_data.get("shared_tasks", [])) + 1,
            "title": title,
            "description": description,
            "assigned_to": assigned_to,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        bridge_data["shared_tasks"].append(task)
        
        with open(self.bridge_file, 'w', encoding='utf-8') as f:
            json.dump(bridge_data, f, indent=2, ensure_ascii=False)
        
        return task

def main():
    """메인 실행 함수"""
    bridge = ChatGPTClaudeBridge()
    
    # 초기 메시지 작성
    bridge.write_message("Claude", "브릿지 시스템 활성화됨")
    
    # ChatGPT를 위한 작업 생성
    bridge.create_task(
        "ChatGPT 연결 테스트",
        "from_chatgpt 폴더에 응답 파일을 생성해주세요",
        "ChatGPT"
    )
    
    # 상태 출력
    status = bridge.read_bridge_status()
    print("=== ChatGPT-Claude Bridge Status ===")
    print(f"Messages: {len(status['messages'])}")
    print(f"Tasks: {len(status['shared_tasks'])}")
    print(f"Claude files: {bridge.monitor_folder('from_claude')}")
    print(f"ChatGPT files: {bridge.monitor_folder('from_chatgpt')}")
    
    # MCP 서버 상태
    loop = asyncio.new_event_loop()
    mcp_status = loop.run_until_complete(bridge.check_mcp_connection())
    print(f"MCP Server: {'✅ Connected' if mcp_status else '❌ Disconnected'}")

if __name__ == "__main__":
    main()