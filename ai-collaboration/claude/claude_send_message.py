import requests
import json

# Claude에서 브릿지 서버로 메시지 전송
url = "http://localhost:5000/api/send"

messages = [
    "Claude Desktop 활성화 완료!",
    "브릿지 서버 연결 성공 - http://localhost:5000",
    "ChatGPT Desktop이 CHATGPT_CONNECT.py를 실행하면 실시간 통신이 시작됩니다."
]

for msg in messages:
    response = requests.post(url, json={
        "sender": "Claude",
        "message": msg
    })
    print(f"Claude: {msg}")
    print(f"응답: {response.json()}")

print("\n[OK] Claude가 브릿지에 연결되었습니다!")