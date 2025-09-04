"""
Nano-Banana (Gemini 2.5 Flash Image) 통합 모듈
CUA 시스템과 연동하여 상품 이미지 자동 생성
"""
import os
import json
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import pandas as pd

class NanoBananaImageGenerator:
    def __init__(self):
        self.base_path = r"C:\Users\8899y\CUA-MASTER\modules"
        self.cafe24_path = os.path.join(self.base_path, "cafe24")
        self.ai_path = os.path.join(self.base_path, "ai_image_generation")
        
        # API 키 설정 (환경 변수에서 로드)
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        # 모델 설정
        self.model_name = "gemini-2.5-flash-image-preview"
        
        # 업체별 스타일 정의
        self.supplier_styles = {
            '인생': {
                'base_prompt': "프리미엄 한국 전통 음식, 정성스러운 손맛, 따뜻한 색감",
                'style': "Korean traditional premium food, warm lighting, homemade style",
                'mood': "authentic, warm, premium quality"
            },
            '인생만두': {
                'base_prompt': "김이 모락모락 나는 수제 만두, 정성가득, 집밥 느낌",
                'style': "Steaming hot handmade dumplings, Korean style, appetizing presentation",
                'mood': "cozy, appetizing, traditional"
            },
            '취영루': {
                'base_prompt': "고급 중화요리, 정통 중국 스타일, 화려하고 품격있는",
                'style': "Authentic Chinese cuisine, elegant presentation, red and gold accents",
                'mood': "luxurious, authentic Chinese, vibrant"
            },
            '최시남매': {
                'base_prompt': "젊고 트렌디한 음식, 인스타그램 감성, 밝고 화사한",
                'style': "Trendy modern food, Instagram-worthy, bright and colorful",
                'mood': "youthful, trendy, social media friendly"
            },
            '기타': {
                'base_prompt': "맛있어 보이는 음식, 깔끔한 프레젠테이션",
                'style': "Appetizing food, clean presentation, professional photography",
                'mood': "clean, professional, appetizing"
            }
        }
        
        # 생성된 이미지 저장 경로
        self.output_path = os.path.join(self.ai_path, "generated_images")
        os.makedirs(self.output_path, exist_ok=True)
        
        # 프롬프트 템플릿 저장 경로
        self.prompt_path = os.path.join(self.ai_path, "prompt_templates")
        os.makedirs(self.prompt_path, exist_ok=True)
        
    def load_product_data(self):
        """CSV에서 상품 데이터 로드"""
        download_folder = os.path.join(self.cafe24_path, "download")
        csv_files = [f for f in os.listdir(download_folder) if f.endswith('.csv')]
        
        if not csv_files:
            return None
            
        latest_csv = max(csv_files, key=lambda f: os.path.getctime(os.path.join(download_folder, f)))
        csv_path = os.path.join(download_folder, latest_csv)
        
        try:
            df = pd.read_csv(csv_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(csv_path, encoding='cp949')
            
        return df
    
    def classify_supplier(self, product_name):
        """상품명에서 업체 분류"""
        if "[인생]" in product_name and "만두" not in product_name:
            return "인생"
        elif "[인생만두]" in product_name:
            return "인생만두"
        elif "[취영루]" in product_name:
            return "취영루"
        elif "[최시남매]" in product_name:
            return "최시남매"
        else:
            return "기타"
    
    def create_enhanced_prompt(self, product_info):
        """상품 정보를 바탕으로 향상된 프롬프트 생성"""
        product_name = product_info['name']
        supplier = self.classify_supplier(product_name)
        
        # 기본 스타일 가져오기
        style_info = self.supplier_styles.get(supplier, self.supplier_styles['기타'])
        
        # 상품명에서 주요 키워드 추출
        keywords = []
        if "만두" in product_name:
            keywords.append("dumplings")
        if "김치" in product_name:
            keywords.append("kimchi")
        if "고기" in product_name or "육" in product_name:
            keywords.append("meat")
        if "해물" in product_name or "해산물" in product_name:
            keywords.append("seafood")
        if "야채" in product_name or "채소" in product_name:
            keywords.append("vegetables")
        
        # 최종 프롬프트 구성
        prompt = f"""
        Create a high-quality food product image:
        Product: {product_name}
        Style: {style_info['style']}
        Mood: {style_info['mood']}
        Keywords: {', '.join(keywords) if keywords else 'Korean food'}
        
        Requirements:
        - Professional food photography
        - Appetizing presentation
        - Clean white or natural background
        - Natural lighting
        - Show the actual food clearly
        - Make it look delicious and fresh
        """
        
        return prompt.strip()
    
    def generate_image(self, product_info):
        """Nano-Banana를 사용한 이미지 생성"""
        if not self.api_key:
            print("[ERROR] GEMINI_API_KEY not set")
            return None
            
        try:
            # 프롬프트 생성
            prompt = self.create_enhanced_prompt(product_info)
            
            # 모델 초기화
            model = genai.GenerativeModel(self.model_name)
            
            # 이미지 생성
            response = model.generate_content(prompt)
            
            # 이미지 저장
            if response and hasattr(response, 'images') and response.images:
                image = response.images[0]
                
                # 업체별 폴더 생성
                supplier = self.classify_supplier(product_info['name'])
                supplier_folder = os.path.join(self.output_path, supplier)
                os.makedirs(supplier_folder, exist_ok=True)
                
                # 이미지 파일 저장
                image_path = os.path.join(
                    supplier_folder, 
                    f"{product_info['no']}_generated.png"
                )
                image.save(image_path)
                
                # 메타데이터 저장
                metadata = {
                    'product_no': product_info['no'],
                    'product_name': product_info['name'],
                    'supplier': supplier,
                    'prompt': prompt,
                    'generated_at': datetime.now().isoformat(),
                    'model': self.model_name,
                    'image_path': image_path
                }
                
                metadata_path = image_path.replace('.png', '_metadata.json')
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                print(f"[SUCCESS] Image generated for {product_info['no']}: {product_info['name'][:30]}...")
                return image_path
                
        except Exception as e:
            print(f"[ERROR] Failed to generate image: {e}")
            return None
    
    def batch_generate(self, limit=10):
        """배치 이미지 생성"""
        # 상품 데이터 로드
        df = self.load_product_data()
        if df is None:
            print("[ERROR] No product data found")
            return
        
        # 이미 생성된 이미지 체크
        generated = set()
        for root, dirs, files in os.walk(self.output_path):
            for file in files:
                if file.endswith('_generated.png'):
                    product_no = file.replace('_generated.png', '')
                    generated.add(product_no)
        
        print(f"[INFO] Already generated: {len(generated)} images")
        
        # 생성할 상품 선택
        to_generate = []
        for _, row in df.iterrows():
            product_no = str(row.get('상품번호', ''))
            if product_no not in generated and len(to_generate) < limit:
                to_generate.append({
                    'no': product_no,
                    'name': str(row.get('상품명', ''))
                })
        
        print(f"[INFO] Generating {len(to_generate)} new images...")
        
        # 이미지 생성
        success_count = 0
        for product in to_generate:
            result = self.generate_image(product)
            if result:
                success_count += 1
            # API 제한 방지
            time.sleep(2)
        
        print(f"[COMPLETE] Generated {success_count}/{len(to_generate)} images")
        
        # 리포트 생성
        self.generate_report()
    
    def generate_report(self):
        """생성 결과 리포트"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'statistics': {},
            'images': []
        }
        
        # 통계 수집
        for root, dirs, files in os.walk(self.output_path):
            for file in files:
                if file.endswith('_metadata.json'):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        report['images'].append(metadata)
                        
                        supplier = metadata['supplier']
                        if supplier not in report['statistics']:
                            report['statistics'][supplier] = 0
                        report['statistics'][supplier] += 1
        
        # 리포트 저장
        report_path = os.path.join(
            self.ai_path, 
            f"nano_banana_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[REPORT] Generated: {report_path}")
        
        # HTML 리포트 생성
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Nano-Banana Image Generation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
                .stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .gallery {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .image-card {{ border: 1px solid #ddd; border-radius: 10px; overflow: hidden; }}
                .image-card img {{ width: 100%; height: 200px; object-fit: cover; }}
                .image-info {{ padding: 15px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🍌 Nano-Banana Image Generation Report</h1>
                <p>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Using Gemini 2.5 Flash Image (Preview)</p>
            </div>
            
            <div class="stats">
                {''.join([f'<div class="stat-card"><h3>{k}</h3><p style="font-size: 24px; font-weight: bold;">{v}</p></div>' for k, v in report['statistics'].items()])}
            </div>
            
            <h2>Generated Images</h2>
            <div class="gallery">
                {''.join([f'''
                <div class="image-card">
                    <img src="{img['image_path']}" alt="{img['product_name']}">
                    <div class="image-info">
                        <h4>{img['product_name'][:30]}...</h4>
                        <p>Supplier: {img['supplier']}</p>
                        <p>Product No: {img['product_no']}</p>
                    </div>
                </div>
                ''' for img in report['images'][:20]])}
            </div>
        </body>
        </html>
        """
        
        html_path = report_path.replace('.json', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        return html_path

if __name__ == "__main__":
    # API 키 설정 필요
    # os.environ['GEMINI_API_KEY'] = 'your-api-key-here'
    
    generator = NanoBananaImageGenerator()
    # generator.batch_generate(limit=5)  # 테스트로 5개만 생성