"""
CUA Agent 통합 워크플로우
모든 기존 시스템을 CUA Agent로 완전 통합
"""

from typing import Dict, List, Any
import json
import sys
from pathlib import Path
from datetime import datetime

# 기존 시스템 경로 추가
sys.path.insert(0, r'C:\Users\8899y')
sys.path.insert(0, r'C:\Users\8899y\ai-council')
sys.path.insert(0, r'C:\Users\8899y\business-automation')

class UnifiedWorkflows:
    """모든 비즈니스 프로세스를 CUA 워크플로우로 통합"""
    
    def __init__(self):
        self.workflows = self._define_all_workflows()
        
    def _define_all_workflows(self) -> Dict[str, List[Dict]]:
        """모든 워크플로우 정의"""
        return {
            # ========== 송장 처리 워크플로우 ==========
            "invoice_morning": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/business-automation/invoice/invoice_master.py vendor"}, "description": "업체별 파일 생성"},
                {"type": "wait", "parameters": {"seconds": 2}, "description": "처리 대기"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/business-automation/invoice/invoice_master.py upload"}, "description": "업로드 CSV 생성"},
                {"type": "screenshot", "parameters": {}, "description": "결과 캡처"}
            ],
            
            "invoice_afternoon": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/business-automation/invoice/invoice_master.py check"}, "description": "처리 현황 확인"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/business-automation/invoice/invoice_master.py validate"}, "description": "송장 검증"},
                {"type": "screenshot", "parameters": {}, "description": "검증 결과 캡처"}
            ],
            
            # ========== AI Council 워크플로우 ==========
            "ai_council_meeting": [
                {"type": "execute", "parameters": {"command": "echo AI Council 회의 모드 - Claude Code Bridge 사용"}, "description": "AI Council 시작"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/core/claude_code_bridge.py"}, "description": "Claude Bridge 활성화"},
                {"type": "wait", "parameters": {"seconds": 3}, "description": "초기화 대기"},
                {"type": "screenshot", "parameters": {}, "description": "회의 상태 캡처"}
            ],
            
            "ai_tikitaka": [
                {"type": "execute", "parameters": {"command": "echo AI 티키타카 대화 - Claude Bridge 활용"}, "description": "티키타카 시작"},
                {"type": "wait", "parameters": {"seconds": 5}, "description": "대화 준비"},
                {"type": "read", "parameters": {}, "description": "대화 내용 확인"}
            ],
            
            "nano_banana_image": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/nano_banana/image_generation_system.py"}, "description": "나노바나나 이미지 시스템 시작"},
                {"type": "wait", "parameters": {"seconds": 2}, "description": "초기화 대기"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/ai_research/perplexity_integration.py"}, "description": "AI 연구 시스템 활성화"},
                {"type": "screenshot", "parameters": {}, "description": "생성 결과 캡처"}
            ],
            
            # ========== Cafe24 상품 관리 워크플로우 ==========
            "cafe24_product_update": [
                {"type": "execute", "parameters": {"command": "start chrome https://eclogin.cafe24.com/Shop/"}, "description": "Cafe24 관리자 열기"},
                {"type": "wait", "parameters": {"seconds": 3}, "description": "페이지 로딩 대기"},
                {"type": "find", "parameters": {"query": "상품관리"}, "description": "상품관리 메뉴 찾기"},
                {"type": "click", "parameters": {}, "description": "상품관리 클릭"}
            ],
            
            "cafe24_price_optimization": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/ecommerce/modules/price-optimizer/price_analyzer.py"}, "description": "가격 분석"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/ecommerce/modules/price-optimizer/margin_editor.py"}, "description": "마진 수정"},
                {"type": "screenshot", "parameters": {}, "description": "수정 결과 캡처"}
            ],
            
            "cafe24_keyword_processing": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/ecommerce/modules/keyword-processor/scripts/process_ai_batch.py"}, "description": "AI 키워드 처리"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/ecommerce/modules/keyword-processor/scripts/process_final.py"}, "description": "최종 키워드 생성"},
                {"type": "screenshot", "parameters": {}, "description": "키워드 결과 캡처"}
            ],
            
            # ========== 이메일 모니터링 워크플로우 ==========
            "email_monitoring": [
                {"type": "execute", "parameters": {"command": "echo 이메일 모니터링 시작"}, "description": "이메일 시스템 시작"},
                {"type": "wait", "parameters": {"seconds": 2}, "description": "초기화 대기"},
                {"type": "screenshot", "parameters": {}, "description": "상태 캡처"}
            ],
            
            "email_30min_monitor": [
                {"type": "execute", "parameters": {"command": "echo 30분 모니터링 모드"}, "description": "모니터링 시작"},
                {"type": "wait", "parameters": {"seconds": 5}, "description": "샘플 대기"},
                {"type": "read", "parameters": {}, "description": "결과 확인"}
            ],
            
            # ========== 주문/발주 관리 워크플로우 ==========
            "mart_order_create": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/orders/mart-orders/create_optimized_orders.py"}, "description": "최적화 주문서 생성"},
                {"type": "wait", "parameters": {"seconds": 2}, "description": "생성 대기"},
                {"type": "screenshot", "parameters": {}, "description": "주문서 캡처"}
            ],
            
            "ccw_order_process": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/orders/mart-orders/ccw_order_processor.py"}, "description": "CCW 주문 처리"},
                {"type": "wait", "parameters": {"seconds": 3}, "description": "처리 대기"},
                {"type": "read", "parameters": {}, "description": "처리 결과 읽기"}
            ],
            
            # ========== 시스템 관리 워크플로우 ==========
            "system_cleanup": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/cleanup_and_integrate_cua_fixed.py"}, "description": "시스템 정리"},
                {"type": "wait", "parameters": {"seconds": 2}, "description": "정리 대기"},
                {"type": "screenshot", "parameters": {}, "description": "정리 결과 캡처"}
            ],
            
            "system_status_check": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/check_cua_agent.py"}, "description": "CUA Agent 상태 확인"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/ai-council/QUICK_TEST.py"}, "description": "AI Council 테스트"},
                {"type": "screenshot", "parameters": {}, "description": "전체 상태 캡처"}
            ],
            
            # ========== 일일 자동화 워크플로우 ==========
            "daily_morning_routine": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/check_cua_agent.py"}, "description": "시스템 체크"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/business-automation/invoice/invoice_master.py vendor"}, "description": "송장 처리"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/PROJECT_STATUS_EMAIL_SYSTEM.py"}, "description": "이메일 확인"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/ai-council/ai_council.py morning"}, "description": "AI 아침 회의"},
                {"type": "screenshot", "parameters": {}, "description": "아침 루틴 완료"}
            ],
            
            "daily_evening_routine": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/business-automation/invoice/invoice_master.py check"}, "description": "송장 확인"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/ai-council/ai_council.py evening"}, "description": "AI 저녁 보고"},
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/cleanup_and_integrate_cua_fixed.py"}, "description": "시스템 정리"},
                {"type": "screenshot", "parameters": {}, "description": "저녁 루틴 완료"}
            ],
            
            # ========== 상세페이지 이미지 생성 워크플로우 ==========
            "detail_page_image_create": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/CUA-MASTER/modules/nano_banana/detail_page_image_generator.py"}, "description": "상세페이지 이미지 생성"},
                {"type": "wait", "parameters": {"seconds": 5}, "description": "생성 대기"},
                {"type": "find", "parameters": {"query": "생성된 이미지"}, "description": "이미지 확인"},
                {"type": "screenshot", "parameters": {}, "description": "생성 결과 캡처"}
            ],
            
            # ========== 마스터 통합 워크플로우 ==========
            "master_integration": [
                {"type": "execute", "parameters": {"command": "python C:/Users/8899y/RUN_CUA_INTEGRATED.py"}, "description": "통합 시스템 시작"},
                {"type": "wait", "parameters": {"seconds": 2}, "description": "초기화 대기"},
                {"type": "read", "parameters": {}, "description": "메뉴 읽기"},
                {"type": "type", "parameters": {"text": "1"}, "description": "송장 처리 선택"},
                {"type": "key", "parameters": {"key": "Enter"}, "description": "실행"},
                {"type": "screenshot", "parameters": {}, "description": "결과 캡처"}
            ]
        }
    
    def get_workflow(self, name: str) -> List[Dict]:
        """워크플로우 가져오기"""
        return self.workflows.get(name, [])
    
    def list_workflows(self) -> List[str]:
        """사용 가능한 워크플로우 목록"""
        return list(self.workflows.keys())
    
    def get_workflow_info(self) -> Dict[str, Dict]:
        """워크플로우 정보"""
        info = {}
        categories = {
            "invoice": "송장 처리",
            "ai": "AI Council",
            "cafe24": "Cafe24 관리",
            "email": "이메일 모니터링",
            "mart": "주문/발주",
            "ccw": "CCW 주문",
            "system": "시스템 관리",
            "daily": "일일 루틴",
            "detail": "상세페이지",
            "master": "마스터 통합"
        }
        
        for name, actions in self.workflows.items():
            category = None
            for key, cat_name in categories.items():
                if name.startswith(key):
                    category = cat_name
                    break
            
            info[name] = {
                "category": category or "기타",
                "description": actions[0]["description"] if actions else "",
                "steps": len(actions)
            }
        
        return info
    
    def save_workflow_report(self):
        """워크플로우 리포트 저장"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_workflows": len(self.workflows),
            "workflows": self.get_workflow_info(),
            "categories": {
                "송장 처리": 2,
                "AI Council": 3,
                "Cafe24 관리": 3,
                "이메일 모니터링": 2,
                "주문/발주": 2,
                "시스템 관리": 2,
                "일일 루틴": 2,
                "상세페이지": 1,
                "마스터 통합": 1
            }
        }
        
        report_path = Path(f"C:/Users/8899y/CUA-MASTER/data/workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report_path


# 기존 agent_enhanced.py와 통합
def integrate_with_agent():
    """Enhanced Agent에 통합 워크플로우 추가"""
    from .agent_enhanced import EnhancedComputerUseAgent
    
    # 워크플로우 로드
    unified = UnifiedWorkflows()
    
    # Agent의 execute_workflow 메서드 확장
    original_execute = EnhancedComputerUseAgent.execute_workflow
    
    def enhanced_execute_workflow(self, workflow_name: str, params: Dict = None):
        """확장된 워크플로우 실행"""
        # 통합 워크플로우 확인
        workflow = unified.get_workflow(workflow_name)
        if workflow:
            results = []
            for action_data in workflow:
                from .base import Action, ActionType
                action = Action(
                    type=ActionType[action_data['type'].upper()],
                    parameters=action_data.get('parameters', {}),
                    description=action_data.get('description')
                )
                result = self.execute_action(action)
                results.append(result)
                
                if not result.success:
                    break
            return results
        
        # 기존 워크플로우로 폴백
        return original_execute(self, workflow_name, params)
    
    # 메서드 교체
    EnhancedComputerUseAgent.execute_workflow = enhanced_execute_workflow
    
    return unified


if __name__ == "__main__":
    # 워크플로우 테스트
    workflows = UnifiedWorkflows()
    
    print("=" * 60)
    print("CUA Agent 통합 워크플로우")
    print("=" * 60)
    
    # 카테고리별 출력
    info = workflows.get_workflow_info()
    categories = {}
    
    for name, details in info.items():
        cat = details['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, details))
    
    for category, items in sorted(categories.items()):
        print(f"\n[{category}]")
        for name, details in items:
            print(f"  {name}: {details['description']} ({details['steps']}단계)")
    
    # 리포트 저장
    report_path = workflows.save_workflow_report()
    print(f"\n워크플로우 리포트 저장: {report_path}")