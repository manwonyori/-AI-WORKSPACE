import re
from pathlib import Path

def check_accuracy():
    temp_txt_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt")
    template_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
    
    products = ['131', '132', '133', '134', '135', '140']
    
    print("=" * 60)
    print("제품 정보 정확성 검수")
    print("=" * 60)
    
    for product in products:
        print(f"\n[제품 {product}]")
        
        # 원본 정보 읽기
        txt_file = temp_txt_path / f"{product}.txt"
        if txt_file.exists():
            with open(txt_file, 'r', encoding='utf-8') as f:
                original = f.read()
            
            # 제품명 추출
            title_match = re.search(r'<title>(.*?)</title>', original)
            original_title = title_match.group(1) if title_match else "제품명 없음"
            
            # 메인 카피 추출
            main_copy_match = re.search(r'<h1[^>]*class="header-main-copy"[^>]*>(.*?)</h1>', original, re.DOTALL)
            if main_copy_match:
                main_copy = re.sub(r'<[^>]+>', ' ', main_copy_match.group(1)).strip()
                main_copy = ' '.join(main_copy.split())
            else:
                main_copy = "메인 카피 없음"
                
            print(f"원본 제품명: {original_title}")
            print(f"원본 메인 카피: {main_copy[:80]}...")
            
        # 현재 템플릿 정보 읽기
        template_file = template_path / f"{product}_final_clean.html"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # 템플릿 특징 추출
            features = re.findall(r'<li[^>]*>✓\s*(.*?)</li>', template)
            print(f"현재 템플릿 특징:")
            for i, feature in enumerate(features[:3], 1):
                print(f"  {i}. {feature}")
                
        print("-" * 40)

if __name__ == "__main__":
    check_accuracy()