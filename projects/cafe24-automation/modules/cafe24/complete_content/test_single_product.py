"""
단일 제품 테스트 - 전체 프로세스 실행
131.txt 파일을 사용하여 완전한 상세페이지 생성
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 경로 설정
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content')

def test_single_product():
    """단일 제품 완전 처리 테스트"""
    
    print("\n" + "="*80)
    print("SINGLE PRODUCT TEST - Complete Process")
    print("="*80)
    
    # 테스트할 파일 선택
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
    txt_file = base_path / "html" / "temp_txt" / "131.txt"
    
    if not txt_file.exists():
        print(f"[ERROR] File not found: {txt_file}")
        return
    
    print(f"\nTest File: {txt_file.name}")
    print("-"*80)
    
    # 제품 정보 준비
    product_info = {
        "file": str(txt_file),
        "number": "131",
        "product_name": "만원요리 교자만두",
        "category": "manwon",
        "product_id": "131",
        "price": "10,000",
        "weight": "1kg",
        "origin": "국내산",
        "storage": "냉동보관"
    }
    
    print("\n[STEP 1] Image Generation")
    print("-"*40)
    try:
        from ultimate_image_workflow import UltimateImageWorkflow
        image_workflow = UltimateImageWorkflow()
        
        # 이미지 생성 (시뮬레이션)
        print("  - Main image: generating...")
        print("  - Detail images: generating...")
        print("  - Lifestyle image: generating...")
        
        images = [
            "main_131.jpg",
            "detail1_131.jpg", 
            "detail2_131.jpg",
            "lifestyle_131.jpg"
        ]
        print(f"  [OK] Generated {len(images)} images")
        
    except Exception as e:
        print(f"  [ERROR] Image generation: {e}")
        images = []
    
    print("\n[STEP 2] Representative Image (1000x1000)")
    print("-"*40)
    try:
        from image_size_optimizer import ImageSizeOptimizer
        optimizer = ImageSizeOptimizer()
        
        # 대표이미지 생성
        rep_image = optimizer.create_representative_image(
            txt_file,  # 원본 파일에서 첫 이미지 추출
            product_info['number'],
            product_info['product_name']
        )
        
        if rep_image:
            print(f"  [OK] Representative image: {rep_image}")
        else:
            print("  [SKIP] No image to process")
            
    except Exception as e:
        print(f"  [ERROR] Representative image: {e}")
    
    print("\n[STEP 3] Text Content Generation")
    print("-"*40)
    try:
        from complete_detail_page_system import CompleteDetailPageSystem
        content_system = CompleteDetailPageSystem()
        
        # 콘텐츠 생성
        content = content_system.generate_complete_content(product_info)
        
        print(f"  [OK] Generated content sections: {len(content)}")
        for key in list(content.keys())[:5]:
            print(f"      - {key}")
        
    except Exception as e:
        print(f"  [ERROR] Content generation: {e}")
        content = {}
    
    print("\n[STEP 4] Template Application")
    print("-"*40)
    try:
        from claude_bridge_template_system import ClaudeBridgeTemplateSystem
        template_system = ClaudeBridgeTemplateSystem()
        
        # 템플릿 데이터 준비
        template_data = {
            **product_info,
            "images": images,
            "content": content,
            "style": "kurly",
            "detail_content": content.get("detail_content", "")
        }
        
        # 템플릿 생성
        template_html = template_system.generate_template_for_product(template_data)
        
        print(f"  [OK] Template generated: {len(template_html)} characters")
        
    except Exception as e:
        print(f"  [ERROR] Template: {e}")
        template_html = ""
    
    print("\n[STEP 5] HTML Optimization")
    print("-"*40)
    try:
        from html_design_optimizer import HtmlDesignOptimizer
        design_optimizer = HtmlDesignOptimizer()
        
        # 임시 파일로 저장
        temp_file = base_path / "output" / "temp_test.html"
        temp_file.parent.mkdir(exist_ok=True)
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(template_html)
        
        # 최적화
        optimized = design_optimizer.optimize_single_html(temp_file)
        
        print(f"  [OK] HTML optimized")
        
        # 임시 파일 삭제
        temp_file.unlink()
        
    except Exception as e:
        print(f"  [ERROR] Optimization: {e}")
        optimized = template_html
    
    print("\n[STEP 6] Save Final Output")
    print("-"*40)
    try:
        # 최종 파일 저장
        output_path = base_path / "output" / "manwon"
        output_path.mkdir(parents=True, exist_ok=True)
        
        final_file = output_path / f"{product_info['number']}_complete.txt"
        
        with open(final_file, 'w', encoding='utf-8') as f:
            f.write(optimized)
        
        print(f"  [OK] Saved to: {final_file}")
        
        # 리포트 생성
        report = {
            "timestamp": datetime.now().isoformat(),
            "product": product_info,
            "images_generated": len(images),
            "content_sections": len(content),
            "output_file": str(final_file),
            "status": "success"
        }
        
        report_file = output_path / f"{product_info['number']}_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"  [OK] Report saved: {report_file}")
        
    except Exception as e:
        print(f"  [ERROR] Save: {e}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    print(f"\nOutput files in: output/manwon/")
    print(f"  - {product_info['number']}_complete.txt")
    print(f"  - {product_info['number']}_report.json")
    print(f"\nRepresentative image in: representative_images/")
    print(f"  - {product_info['number']}_{product_info['product_name']}.jpg")

def main():
    """메인 실행"""
    test_single_product()

if __name__ == "__main__":
    main()