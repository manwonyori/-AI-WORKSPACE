import os
import json
import shutil
from pathlib import Path
from datetime import datetime

class ChuyoungruRealImprovement:
    """실제 데이터 기반 취영루 품질 개선"""
    
    def __init__(self):
        self.base_path = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content")
        self.original_path = self.base_path / "html" / "취영루"
        self.improved_path = self.base_path / "output" / "chuyoungru_real"
        self.backup_path = self.original_path / "backup"
        self.template_path = self.base_path / "output" / "content_only" / "132_research_applied.html"
        self.real_data_path = self.base_path / "research" / "real_product_data.json"
        
        # 디렉토리 생성
        self.improved_path.mkdir(parents=True, exist_ok=True)
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
        # 실제 데이터 로드
        self.load_real_data()
        
        # 템플릿 로드
        self.load_template()
    
    def load_real_data(self):
        """실제 추출된 데이터 로드"""
        if not self.real_data_path.exists():
            print("[오류] real_product_data.json 없음. real_data_extractor.py 먼저 실행")
            self.real_data = {}
            return
        
        with open(self.real_data_path, 'r', encoding='utf-8') as f:
            self.real_data = json.load(f)
        
        print(f"[로드] {len(self.real_data)}개 제품 실제 데이터 로드")
    
    def load_template(self):
        """기준 템플릿 로드"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                self.template = f.read()
            print("[템플릿] 132번 기준 템플릿 로드 완료")
        except:
            print("[경고] 템플릿 없음, 기본 구조 사용")
            self.template = self.get_default_template()
    
    def get_default_template(self):
        """기본 템플릿 구조"""
        return """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Pretendard', sans-serif; margin: 0; padding: 20px; }}
        .product-content-wrapper {{ max-width: 860px; margin: 0 auto; }}
        .content-section {{ margin-bottom: 40px; }}
        .section-title {{ font-size: 24px; font-weight: 600; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #e8e8e8; }}
        .highlight-box {{ background: #fafafa; padding: 25px; margin: 25px 0; border-left: 2px solid #2c2c2c; }}
        .detail-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .detail-table th, .detail-table td {{ padding: 15px 12px; text-align: left; border-bottom: 1px solid #e0e0e0; }}
        .detail-table th {{ width: 140px; background: #fafafa; font-weight: 500; }}
    </style>
</head>
<body>
    <div class="product-content-wrapper">
        <!-- 브랜드 스토리 -->
        <div class="content-section">
            <h2 class="section-title">브랜드 스토리</h2>
            <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; margin: 20px 0;">
                <p style="color: #666; line-height: 1.8; font-size: 15px; text-align: center;">
                    <strong style="color: #2c2c2c;">취영루</strong>는 1945년부터 3대에 걸쳐 만두 하나에 집중해온 대한민국 대표 만두 전문기업입니다.
                </p>
            </div>
        </div>
        
        <!-- 상품설명 -->
        <div class="content-section">
            <h2 class="section-title">상품설명</h2>
            <div class="highlight-box">
                <ul>{features}</ul>
            </div>
            <p style="margin: 20px 0; color: #666; font-size: 16px; line-height: 1.7;">
                {description}
            </p>
        </div>
        
        <!-- 제품 이미지 -->
        <div class="image-gallery" style="margin: 30px 0;">
            <h3 style="color: #333; font-size: 18px; font-weight: 600; margin-bottom: 20px; text-align: center;">제품 상세 이미지</h3>
            {images}
        </div>
    </div>
</body>
</html>"""
    
    def create_backup(self, product_id):
        """백업 생성"""
        original_file = self.original_path / f"{product_id}.html"
        if original_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_path / f"{product_id}_{timestamp}.backup.html"
            shutil.copy2(original_file, backup_file)
            return True
        return False
    
    def improve_single_product(self, product_id):
        """개별 제품 개선 - 실제 데이터 사용"""
        
        product_data = self.real_data.get(str(product_id))
        if not product_data:
            print(f"[경고] {product_id}번 실제 데이터 없음")
            return False
        
        print(f"\n[개선] {product_id}: {product_data.get('title', 'Unknown')}")
        
        # 백업
        self.create_backup(product_id)
        
        # HTML 생성
        if self.template:
            html = self.template
        else:
            html = self.get_default_template()
        
        # 1. 제목 교체
        title = product_data.get('title', f'취영루 제품 {product_id}')
        html = html.replace('[취영루] 고기왕만두 420g', title)
        html = html.replace('만원요리 최씨남매 X 취영루 고기왕만두 420g', title)
        html = html.replace('<title>만원요리 최씨남매 X 취영루 고기왕만두 420g</title>', 
                           f'<title>{title}</title>')
        
        # 2. 특징 리스트 생성 (실제 데이터에서)
        features = product_data.get('features', [])
        if features:
            features_html = ""
            for feature in features:
                feature_title = feature.get('title', '')
                feature_desc = feature.get('desc', '')
                # 제목과 설명을 하나의 문장으로
                combined = f"{feature_title}: {feature_desc}" if feature_desc else feature_title
                features_html += f'            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ {combined}</li>\n'
        else:
            # 기본 특징 (실제 데이터가 없을 때)
            features_html = self.get_default_features(product_id)
        
        # 기존 특징 리스트 교체
        old_features = """            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 70년 전통 취영루의 정통 제조법</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 국산 돼지고기 25.9% 함유로 풍부한 육즙</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 왕만두 사이즈 (1개 84g)로 든든한 포만감</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ HACCP 인증 시설에서 안전하게 제조</li>"""
        
        if old_features in html:
            html = html.replace(old_features, features_html.rstrip())
        
        # 3. 이미지 교체 (실제 이미지 URL)
        images = product_data.get('images', [])
        if images:
            # 이미지 URL 교체
            for img in images:
                src = img.get('src', '')
                alt = img.get('alt', '')
                
                # 특정 이미지 패턴 교체
                if 'kyoja' in src and product_id == 131:
                    html = html.replace(
                        'https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g.jpg',
                        src
                    )
                    html = html.replace(
                        'https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g-d.jpg',
                        src.replace('.jpg', '-d.jpg') if '-d' not in src else src
                    )
                elif 'kimchi' in src and product_id == 133:
                    html = html.replace(
                        'https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g.jpg',
                        src
                    )
                elif 'gunmandu' in src and product_id == 134:
                    html = html.replace(
                        'https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g.jpg',
                        src
                    )
                elif 'water' in src and product_id in [135, 145]:
                    html = html.replace(
                        'https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g.jpg',
                        src
                    )
        
        # 4. 설명 교체
        description = product_data.get('description', '')
        if description:
            html = html.replace(
                '신선한 국산 돼지고기와 채소를 아낌없이 넣어 한 입 베어물면 육즙이 터져 나오는 깊은 맛을 경험하실 수 있습니다.',
                description[:200] + '...' if len(description) > 200 else description
            )
        
        # 5. 제품별 고유 텍스트 교체
        product_specific = self.get_product_specific_text(product_id, product_data)
        for old_text, new_text in product_specific.items():
            html = html.replace(old_text, new_text)
        
        # 저장
        improved_file = self.improved_path / f"{product_id}_real.html"
        with open(improved_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[완료] {improved_file.name} 저장")
        return True
    
    def get_default_features(self, product_id):
        """기본 특징 (실제 데이터 없을 때)"""
        features_map = {
            131: """            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 정통 교자만두 스타일</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 팬에 구워 바삭하게</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 아담한 사이즈 35g</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 국산 돼지고기 18.5%</li>""",
            133: """            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 잘 익은 김치의 깊은 맛</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 매콤달콤한 한국의 맛</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 왕만두 사이즈 84g</li>
            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ 김치 15.8% 함유</li>"""
        }
        return features_map.get(product_id, "")
    
    def get_product_specific_text(self, product_id, data):
        """제품별 고유 텍스트 맵핑"""
        title = data.get('title', '')
        
        replacements = {}
        
        # 제품명에 따른 텍스트 교체
        if '교자' in title:
            replacements['고기왕만두'] = '교자만두'
            replacements['왕만두 사이즈'] = '교자 사이즈'
            replacements['84g'] = '35g'
        elif '김치' in title:
            replacements['고기왕만두'] = '김치왕만두'
            replacements['풍부한 육즙'] = '김치의 시원한 맛'
        elif '물만두' in title:
            replacements['고기왕만두'] = '물만두'
            replacements['왕만두 사이즈'] = '물만두 사이즈'
            replacements['84g'] = '50g'
        elif '군만두' in title:
            replacements['고기왕만두'] = '군만두'
            replacements['왕만두 사이즈'] = '군만두 사이즈'
            replacements['찜기 조리'] = '기름 튀김'
        
        return replacements
    
    def improve_all_products(self):
        """전체 제품 개선"""
        
        print("\n" + "=" * 60)
        print("   실제 데이터 기반 취영루 품질 개선")
        print("=" * 60)
        
        success = 0
        total = len(self.real_data)
        
        for product_id in self.real_data.keys():
            if self.improve_single_product(int(product_id)):
                success += 1
        
        print(f"\n=== 완료 ===")
        print(f"성공: {success}/{total}")
        print(f"저장: {self.improved_path}")
        
        return success == total

def main():
    """메인 실행"""
    improver = ChuyoungruRealImprovement()
    improver.improve_all_products()

if __name__ == "__main__":
    main()