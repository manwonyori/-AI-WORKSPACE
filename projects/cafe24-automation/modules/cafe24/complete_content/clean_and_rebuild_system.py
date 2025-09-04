"""
Cafe24 상세페이지 완전 재구축 시스템
폴더 정리 + 이미지 매핑 + 템플릿 생성 통합
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import re
import pandas as pd

class CleanAndRebuildSystem:
    def __init__(self):
        self.base_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.output_dir = self.base_dir / "output_clean"  # 새로운 깨끗한 출력 폴더
        self.csv_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\download\manwonyori_20250901_301_e68d.csv")
        
        # 취영루 제품별 정확한 이미지 매핑
        self.chuyoungru_images = {
            "131": {
                "name": "교자만두 360g",
                "code": "P00000IR",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/kyoja/kyoja-360g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/kyoja/kyoja-360g-d.jpg"
                }
            },
            "132": {
                "name": "고기왕만두 420g",
                "code": "P00000IS",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g-d.jpg"
                }
            },
            "133": {
                "name": "김치만두 420g",
                "code": "P00000IT",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/kimchi/kimchi-420g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/kimchi/kimchi-420g-d.jpg"
                }
            },
            "134": {
                "name": "물만두 420g",
                "code": "P00000IU",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/mul/mul-420g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/mul/mul-420g-d.jpg"
                }
            },
            "135": {
                "name": "튀김만두 300g",
                "code": "P00000IV",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/fried/fried-300g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/fried/fried-300g-d.jpg"
                }
            },
            "136": {
                "name": "갈비만두 420g",
                "code": "P00000IW",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/galbi/galbi-420g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/galbi/galbi-420g-d.jpg"
                }
            },
            "137": {
                "name": "새우만두 420g",
                "code": "P00000IX",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/shrimp/shrimp-420g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/shrimp/shrimp-420g-d.jpg"
                }
            },
            "138": {
                "name": "감자만두 420g",
                "code": "P00000IY",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/potato/potato-420g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/potato/potato-420g-d.jpg"
                }
            },
            "139": {
                "name": "야채만두 420g",
                "code": "P00000IZ",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/vege/vege-420g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/vege/vege-420g-d.jpg"
                }
            },
            "140": {
                "name": "새우만두 420g",
                "code": "P00000JA",
                "images": {
                    "common": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "product": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/shrimp/shrimp-420g.jpg",
                    "detail": "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/shrimp/shrimp-420g-d.jpg"
                }
            }
        }
    
    def step1_clean_folders(self):
        """Step 1: 폴더 구조 정리"""
        print("\n" + "="*60)
        print("STEP 1: 폴더 구조 정리")
        print("="*60)
        
        # 기존 output 폴더들 백업
        backup_dir = self.base_dir / f"backup_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        for folder in ["output", "output_clean"]:
            source = self.base_dir / folder
            if source.exists():
                dest = backup_dir / folder
                shutil.move(str(source), str(dest))
                print(f"[백업] {folder} → {dest}")
        
        # 새로운 깨끗한 폴더 구조 생성
        folders = [
            self.output_dir,
            self.output_dir / "chuyoungru",
            self.output_dir / "insaeng",
            self.output_dir / "ccw",
            self.output_dir / "templates",
            self.output_dir / "reports"
        ]
        
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"[생성] {folder}")
        
        return True
    
    def step2_create_template(self, product_id: str):
        """Step 2: 제품별 정확한 템플릿 생성"""
        
        if product_id not in self.chuyoungru_images:
            print(f"[오류] {product_id} 제품 정보가 없습니다.")
            return None
        
        product_info = self.chuyoungru_images[product_id]
        images = product_info['images']
        
        html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>만원요리 최씨남매 X 취영루 {product_info['name']}</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }}
        
        .product-wrapper {{
            max-width: 860px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 600;
            margin: 30px 0 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e8e8e8;
            color: #2c2c2c;
        }}
        
        .product-images {{
            margin: 30px 0;
        }}
        
        .product-images img {{
            width: 100%;
            margin-bottom: 20px;
            border-radius: 8px;
        }}
        
        @media (max-width: 768px) {{
            .product-wrapper {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="product-wrapper">
        <!-- 제품명 -->
        <h1 class="section-title">만원요리 최씨남매 X 취영루 {product_info['name']}</h1>
        
        <!-- 제품 이미지 섹션 -->
        <div class="product-images">
            <!-- 취영루 공통 이미지 -->
            <img src="{images['common']}" alt="취영루 HACCP 인증 정보">
            
            <!-- {product_id}번 제품 전용 이미지 -->
            <img src="{images['product']}" alt="취영루 {product_info['name']} 제품 이미지">
            
            <!-- {product_id}번 제품 상세 정보 -->
            <img src="{images['detail']}" alt="취영루 {product_info['name']} 상세 정보">
        </div>
        
        <!-- 제품 코드 정보 (숨김) -->
        <div style="display:none;">
            제품번호: {product_id}
            제품코드: {product_info['code']}
            브랜드: 취영루
        </div>
    </div>
</body>
</html>"""
        
        return html_template
    
    def step3_generate_all_templates(self):
        """Step 3: 모든 취영루 제품 템플릿 생성"""
        print("\n" + "="*60)
        print("STEP 3: 취영루 제품 템플릿 생성")
        print("="*60)
        
        success_count = 0
        
        for product_id in self.chuyoungru_images.keys():
            product_info = self.chuyoungru_images[product_id]
            print(f"\n[생성 중] {product_id} - {product_info['name']}")
            
            # 템플릿 생성
            html_content = self.step2_create_template(product_id)
            
            if html_content:
                # 파일 저장
                output_file = self.output_dir / "chuyoungru" / f"{product_id}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"  [OK] 저장: {output_file.name}")
                print(f"  [OK] 이미지: {product_info['images']['product'].split('/')[-2]}")
                success_count += 1
            else:
                print(f"  [X] 실패")
        
        print(f"\n완료: {success_count}/{len(self.chuyoungru_images)} 템플릿 생성")
        return success_count
    
    def step4_verify_images(self):
        """Step 4: 생성된 템플릿 이미지 검증"""
        print("\n" + "="*60)
        print("STEP 4: 이미지 링크 검증")
        print("="*60)
        
        verification_results = []
        
        for html_file in (self.output_dir / "chuyoungru").glob("*.html"):
            product_id = html_file.stem
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 이미지 링크 추출
            img_pattern = r'<img\s+src="([^"]+)"'
            images = re.findall(img_pattern, content)
            
            # 검증
            is_valid = True
            issues = []
            
            if len(images) != 3:
                is_valid = False
                issues.append(f"이미지 개수 오류: {len(images)}개 (3개여야 함)")
            
            # 제품별 고유 이미지 확인
            if product_id in self.chuyoungru_images:
                expected = self.chuyoungru_images[product_id]['images']['product']
                if expected not in images:
                    is_valid = False
                    issues.append(f"제품 이미지 누락")
                else:
                    # 중복 체크
                    for other_id in self.chuyoungru_images:
                        if other_id != product_id:
                            other_img = self.chuyoungru_images[other_id]['images']['product']
                            if other_img in images:
                                is_valid = False
                                issues.append(f"다른 제품({other_id}) 이미지 포함")
            
            result = {
                "product_id": product_id,
                "valid": is_valid,
                "images_count": len(images),
                "issues": issues
            }
            
            verification_results.append(result)
            
            if is_valid:
                print(f"[OK] {product_id}: 정상")
            else:
                print(f"[X] {product_id}: 문제 발견 - {', '.join(issues)}")
        
        # 검증 보고서 저장
        report_file = self.output_dir / "reports" / "verification_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total": len(verification_results),
                "valid": sum(1 for r in verification_results if r['valid']),
                "invalid": sum(1 for r in verification_results if not r['valid']),
                "details": verification_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n검증 보고서: {report_file}")
        return verification_results
    
    def run_complete_rebuild(self):
        """전체 재구축 프로세스 실행"""
        print("\n" + "="*70)
        print("Cafe24 상세페이지 완전 재구축 시작")
        print("="*70)
        
        # Step 1: 폴더 정리
        self.step1_clean_folders()
        
        # Step 2-3: 템플릿 생성
        template_count = self.step3_generate_all_templates()
        
        # Step 4: 검증
        verification = self.step4_verify_images()
        
        # 최종 보고
        print("\n" + "="*70)
        print("재구축 완료")
        print("="*70)
        print(f"[OK] 생성된 템플릿: {template_count}개")
        print(f"[OK] 검증 통과: {sum(1 for r in verification if r['valid'])}개")
        print(f"[OK] 출력 폴더: {self.output_dir}")
        
        # 샘플 파일 열기
        sample_file = self.output_dir / "chuyoungru" / "131.html"
        if sample_file.exists():
            os.system(f'start "" "{sample_file}"')
            print(f"\n샘플 파일 열기: 131.html (교자만두)")

def main():
    rebuilder = CleanAndRebuildSystem()
    rebuilder.run_complete_rebuild()

if __name__ == "__main__":
    main()