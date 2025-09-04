"""
CUA-MASTER Cafe24 Module Main Runner
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.direct_url_cua_agent import DirectURLCUAAgent

def main():
    print("="*80)
    print("CUA-MASTER CAFE24 MODULE")
    print("최적화된 Cafe24 자동화 시스템")
    print("="*80)
    
    agent = DirectURLCUAAgent()
    success = agent.run_direct_url_workflow()
    
    if success:
        print("\n[SUCCESS] CUA Agent 실행 완료!")
    else:
        print("\n[INFO] CUA Agent 실행 종료")

if __name__ == "__main__":
    main()
