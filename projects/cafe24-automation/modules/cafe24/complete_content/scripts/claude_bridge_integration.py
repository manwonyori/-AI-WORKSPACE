import os
import json
import pandas as pd
from typing import Dict, List
from pathlib import Path

class ClaudeBridgeIntegration:
    def __init__(self):
        self.base_path = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content")
        self.html_path = self.base_path / "html"
        self.csv_path = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/download/manwonyori_20250901_301_e68d.csv")
        self.template_path = self.base_path / "output" / "content_only" / "132_research_applied.html"
        
        # 브랜드별 폴더 경로
        self.brand_folders = {
            "취영루": self.html_path / "취영루",
            "인생": self.html_path / "인생", 
            "씨씨더블유": self.html_path / "씨씨더블유",
            "태공식품": self.html_path / "태공식품",
            "반찬단지": self.html_path / "반찬단지",
            "최씨남매": self.html_path / "최씨남매",
            "모비딕": self.html_path / "모비딕",
            "비에스": self.html_path / "비에스",
            "단지식품유통": self.html_path / "단지식품유통",
            "피자코리아": self.html_path / "피자코리아"
        }
        
        self.csv_data = None
        self.load_csv_data()
    
    def load_csv_data(self):
        """CSV 데이터 로드"""
        try:
            self.csv_data = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            print(f"[로드] CSV 데이터 로드 완료: {len(self.csv_data)}개 제품")
        except Exception as e:
            print(f"[오류] CSV 로드 실패: {e}")
    
    def analyze_existing_structure(self):
        """기존 브랜드 폴더 구조 분석"""
        print("\n=== 기존 브랜드 폴더 분석 ===")
        
        analysis_result = {}
        
        for brand_name, folder_path in self.brand_folders.items():
            if folder_path.exists():
                html_files = list(folder_path.glob("*.html"))
                product_numbers = [int(f.stem) for f in html_files if f.stem.isdigit()]
                
                analysis_result[brand_name] = {
                    "folder_exists": True,
                    "html_count": len(html_files),
                    "product_numbers": sorted(product_numbers),
                    "sample_files": [f.name for f in html_files[:3]]
                }
                
                print(f"{brand_name}: {len(html_files)}개 HTML 파일")
                if product_numbers:
                    print(f"  제품번호 범위: {min(product_numbers)}-{max(product_numbers)}")
            else:
                analysis_result[brand_name] = {
                    "folder_exists": False,
                    "html_count": 0,
                    "product_numbers": [],
                    "sample_files": []
                }
                print(f"{brand_name}: 폴더 없음")
        
        return analysis_result
    
    def map_csv_to_folders(self):
        """CSV 데이터와 폴더 구조 매핑"""
        print("\n=== CSV-폴더 매핑 분석 ===")
        
        mapping_result = {
            "matched": {},
            "missing_in_csv": {},
            "missing_in_folders": {}
        }
        
        # CSV에서 브랜드별 제품번호 추출
        csv_brands = {}
        for _, row in self.csv_data.iterrows():
            product_name = row['상품명']
            product_number = row['상품번호']
            
            # 브랜드 추출
            import re
            brand_match = re.search(r'\[([^\]]+)\]', product_name)
            if brand_match:
                brand = brand_match.group(1)
                if brand not in csv_brands:
                    csv_brands[brand] = []
                csv_brands[brand].append({
                    'number': product_number,
                    'name': product_name,
                    'code': row['상품코드']
                })
        
        # 매핑 분석
        for brand_name, folder_path in self.brand_folders.items():
            if folder_path.exists():
                html_files = list(folder_path.glob("*.html"))
                folder_numbers = {int(f.stem) for f in html_files if f.stem.isdigit()}
                
                if brand_name in csv_brands:
                    csv_numbers = {item['number'] for item in csv_brands[brand_name]}
                    
                    matched = folder_numbers & csv_numbers
                    missing_in_csv = folder_numbers - csv_numbers
                    missing_in_folders = csv_numbers - folder_numbers
                    
                    mapping_result["matched"][brand_name] = sorted(list(matched))
                    if missing_in_csv:
                        mapping_result["missing_in_csv"][brand_name] = sorted(list(missing_in_csv))
                    if missing_in_folders:
                        mapping_result["missing_in_folders"][brand_name] = sorted(list(missing_in_folders))
                    
                    print(f"{brand_name}: 매치 {len(matched)}개, 폴더만 {len(missing_in_csv)}개, CSV만 {len(missing_in_folders)}개")
                else:
                    mapping_result["missing_in_csv"][brand_name] = sorted(list(folder_numbers))
                    print(f"{brand_name}: CSV에 브랜드 없음, HTML만 {len(folder_numbers)}개")
        
        return mapping_result
    
    def generate_claude_bridge_plan(self):
        """Claude Bridge 처리 계획 생성"""
        print("\n=== Claude Bridge 처리 계획 ===")
        
        structure_analysis = self.analyze_existing_structure()
        mapping_analysis = self.map_csv_to_folders()
        
        processing_plan = {
            "phase_1_verified": [],  # 이미 검증된 브랜드 (취영루 등)
            "phase_2_complete": [],  # HTML 완성된 브랜드
            "phase_3_missing": [],   # 누락된 제품들
            "phase_4_quality": []    # 품질 개선 대상
        }
        
        # Phase 1: 검증된 브랜드 (취영루)
        if "취영루" in structure_analysis and structure_analysis["취영루"]["html_count"] >= 10:
            processing_plan["phase_1_verified"].append({
                "brand": "취영루",
                "count": structure_analysis["취영루"]["html_count"],
                "template_available": True,
                "priority": 1
            })
        
        # Phase 2: 완성도 높은 브랜드들
        for brand, data in structure_analysis.items():
            if brand != "취영루" and data["html_count"] >= 20:  # 20개 이상
                processing_plan["phase_2_complete"].append({
                    "brand": brand,
                    "count": data["html_count"],
                    "priority": 2
                })
        
        # Phase 3: 누락된 제품들
        for brand, missing_list in mapping_analysis["missing_in_folders"].items():
            if missing_list:
                processing_plan["phase_3_missing"].append({
                    "brand": brand,
                    "missing_products": missing_list,
                    "count": len(missing_list),
                    "priority": 3
                })
        
        # 결과 출력
        print("Phase 1 (검증된 브랜드):", len(processing_plan["phase_1_verified"]))
        print("Phase 2 (완성된 브랜드):", len(processing_plan["phase_2_complete"]))  
        print("Phase 3 (누락 제품):", sum(item["count"] for item in processing_plan["phase_3_missing"]))
        
        return processing_plan
    
    def execute_claude_bridge_phase(self, phase: str, brand: str = None):
        """Claude Bridge 단계별 실행"""
        print(f"\n=== Claude Bridge Phase {phase} 실행 ===")
        
        if phase == "1" and brand == "취영루":
            return self.process_chuyoungru_brand()
        elif phase == "2":
            return self.process_complete_brands()
        elif phase == "3":
            return self.process_missing_products()
        else:
            print("지원하지 않는 단계입니다.")
            return False
    
    def process_chuyoungru_brand(self):
        """취영루 브랜드 Claude Bridge 처리"""
        print("[처리] 취영루 브랜드 개선 작업...")
        
        chuyoungru_path = self.brand_folders["취영루"]
        if not chuyoungru_path.exists():
            print("[오류] 취영루 폴더가 존재하지 않습니다.")
            return False
        
        # 132_research_applied.html 템플릿 기반으로 처리
        template_content = ""
        if self.template_path.exists():
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            print("[템플릿] 132번 연구 적용 템플릿 로드 완료")
        
        # 취영루 HTML 파일들 개선
        html_files = list(chuyoungru_path.glob("*.html"))
        print(f"[작업] {len(html_files)}개 HTML 파일 개선 시작...")
        
        for html_file in html_files:
            try:
                # 기존 HTML 읽기
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    original_content = f.read()
                
                # Claude Bridge 처리 (여기서는 시뮬레이션)
                improved_content = self.apply_claude_bridge_improvements(
                    original_content, template_content, html_file.stem
                )
                
                # 개선된 내용 저장
                backup_file = html_file.with_suffix('.backup.html')
                html_file.rename(backup_file)  # 백업 생성
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(improved_content)
                
                print(f"[완료] {html_file.name} 개선 완료")
                
            except Exception as e:
                print(f"[오류] {html_file.name} 처리 실패: {e}")
        
        return True
    
    def apply_claude_bridge_improvements(self, original: str, template: str, product_id: str):
        """Claude Bridge 개선 적용 (실제로는 더 복잡한 AI 처리)"""
        # 여기서는 간단한 구조 개선만 시뮬레이션
        # 실제로는 Claude API를 통해 제품별 맞춤 개선
        
        improved = original
        
        # 브랜드 스토리 추가 (최상단)
        if "브랜드 스토리" not in improved:
            brand_story_section = '''
        <!-- 브랜드 스토리 (최상단) -->
        <div class="content-section">
            <h2 class="section-title">📖 브랜드 스토리</h2>
            <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; margin: 20px 0;">
                <p style="color: #666; line-height: 1.8; font-size: 15px; text-align: center;">
                    <strong style="color: #2c2c2c;">취영루</strong>는 1945년부터 3대에 걸쳐 만두 하나에 집중해온 대한민국 대표 만두 전문기업입니다. 
                    70년간 변하지 않는 정통 제조법과 엄선된 재료로 깊은 맛을 자랑합니다.
                </p>
            </div>
        </div>
'''
            # body 태그 직후에 삽입
            improved = improved.replace('<body>', f'<body>{brand_story_section}')
        
        return improved
    
    def process_complete_brands(self):
        """완성된 브랜드들 처리"""
        print("[처리] 완성된 브랜드들 품질 개선...")
        return True
    
    def process_missing_products(self):
        """누락된 제품들 처리"""
        print("[처리] 누락된 제품들 생성...")
        return True

def main():
    """메인 실행 함수"""
    bridge = ClaudeBridgeIntegration()
    
    print("=== CUA-MASTER Claude Bridge 통합 시스템 ===")
    
    # 1. 기존 구조 분석
    structure = bridge.analyze_existing_structure()
    
    # 2. CSV 매핑 분석  
    mapping = bridge.map_csv_to_folders()
    
    # 3. 처리 계획 생성
    plan = bridge.generate_claude_bridge_plan()
    
    # 4. 처리 계획 저장
    plan_file = bridge.base_path / "scripts" / "claude_bridge_plan.json"
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump({
            "structure_analysis": structure,
            "mapping_analysis": mapping, 
            "processing_plan": plan
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장] 처리 계획 저장: {plan_file}")
    
    return bridge

if __name__ == "__main__":
    main()