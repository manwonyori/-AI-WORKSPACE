"""
ChatGPT 시뮬레이터
ChatGPT Desktop을 대신해서 자동으로 메시지를 생성하고 전송
"""

import json
import time
import random
from datetime import datetime

CHAT_FILE = r"C:\Users\8899y\mcp_shared\live_chat.json"

class ChatGPTSimulator:
    def __init__(self):
        self.last_seen = self.get_last_id()
        self.conversation_starters = [
            "안녕하세요 Claude! 오늘은 어떤 주제로 대화해볼까요?",
            "최근 AI 기술 발전에 대해 어떻게 생각하시나요?",
            "프로그래밍 베스트 프랙티스에 대해 의견을 나눠볼까요?",
            "알고리즘 최적화 기법에 대해 논의해보시죠.",
            "시스템 설계 패턴에 대한 경험을 공유해주세요."
        ]
        
        self.responses = [
            "흥미로운 관점이네요! 구체적인 예시를 들어주실 수 있나요?",
            "그 방법의 장단점은 무엇인가요?",
            "실제 프로덕션 환경에서 테스트해보셨나요?",
            "성능 측면에서는 어떤 개선이 있었나요?",
            "대안적인 접근 방법도 고려해보셨나요?",
            "확장성 면에서는 어떤가요?",
            "유지보수 관점에서 장점이 있나요?",
            "팀 협업 시 어떤 이점이 있을까요?",
            "보안 측면은 어떻게 처리하셨나요?",
            "테스트 커버리지는 어느 정도인가요?"
        ]
    
    def get_last_id(self):
        try:
            with open(CHAT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                messages = data.get("messages", [])
                return messages[-1]["id"] if messages else 0
        except:
            return 0
    
    def read_chat(self):
        try:
            with open(CHAT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"messages": []}
    
    def send_message(self, text):
        """ChatGPT 메시지 전송"""
        data = self.read_chat()
        msg = {
            "id": len(data["messages"]) + 1,
            "sender": "ChatGPT",
            "message": text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data["messages"].append(msg)
        data["status"] = "ChatGPT_sent"
        
        with open(CHAT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n[ChatGPT] {text}")
        return msg["id"]
    
    def generate_contextual_response(self, claude_message):
        """Claude 메시지에 맞는 응답 생성"""
        msg_lower = claude_message.lower()
        
        # 주제별 맞춤 응답
        if "피보나치" in msg_lower:
            return "행렬 거듭제곱과 동적 프로그래밍 중 어느 것이 더 실용적인가요?"
        elif "transformer" in msg_lower or "attention" in msg_lower:
            return "Multi-head attention의 계산 복잡도를 줄이는 방법이 있을까요?"
        elif "캐시" in msg_lower:
            return "L1, L2, L3 캐시를 효과적으로 활용하는 코딩 패턴을 알려주세요."
        elif "병렬" in msg_lower:
            return "GPU 병렬 처리와 CPU 멀티스레딩 중 어느 것이 더 효과적인가요?"
        elif "saga" in msg_lower or "트랜잭션" in msg_lower:
            return "Choreography와 Orchestration의 실제 사용 경험을 공유해주세요."
        elif "tdd" in msg_lower or "테스트" in msg_lower:
            return "Integration 테스트와 E2E 테스트의 균형을 어떻게 맞추시나요?"
        else:
            return random.choice(self.responses)
    
    def run(self):
        """메인 실행"""
        print("=" * 60)
        print("   ChatGPT 시뮬레이터 시작")
        print("   (ChatGPT Desktop을 대신해서 자동 대화)")
        print("=" * 60)
        
        # 초기 메시지 전송
        starter = random.choice(self.conversation_starters)
        self.send_message(starter)
        self.last_seen = self.get_last_id()
        
        message_count = 1
        max_messages = 20  # 20개 메시지 후 종료
        
        while message_count < max_messages:
            try:
                time.sleep(3)  # Claude 응답 대기
                
                data = self.read_chat()
                messages = data.get("messages", [])
                
                # Claude의 새 메시지 확인
                for msg in messages:
                    if msg["id"] > self.last_seen and msg["sender"] == "Claude":
                        print(f"\n[Claude] {msg['message'][:100]}...")
                        self.last_seen = msg["id"]
                        
                        # 자연스러운 딜레이
                        time.sleep(random.uniform(2, 4))
                        
                        # 맥락에 맞는 응답 생성
                        response = self.generate_contextual_response(msg["message"])
                        self.send_message(response)
                        message_count += 1
                        
                        if message_count % 5 == 0:
                            print(f"\n[진행 상황] {message_count}/{max_messages} 메시지 교환됨")
                
            except KeyboardInterrupt:
                print("\n[종료] ChatGPT 시뮬레이터를 종료합니다.")
                break
            except Exception as e:
                print(f"[오류] {e}")
                time.sleep(2)
        
        print("\n" + "=" * 60)
        print(f"   대화 완료! 총 {message_count}개 메시지 교환")
        print("   live_chat.json 파일을 확인하세요")
        print("=" * 60)

if __name__ == "__main__":
    simulator = ChatGPTSimulator()
    simulator.run()