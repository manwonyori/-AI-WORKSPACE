"""
완성된 HTML 템플릿을 활용한 최종 샘플 생성기
- 현재 131_content.html의 완벽한 모바일 반응형 구조 활용
- 다른 제품들의 정보로 샘플 생성
"""

import os
import re
from pathlib import Path

class FinalSampleGenerator:
    def __init__(self):
        """최종 샘플 생성기 초기화"""
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.input_path = self.base_path / "html" / "temp_txt"
        self.output_path = self.base_path / "output" / "content_only"
        self.template_file = self.output_path / "131_content.html"
    
    def load_template(self):
        """완성된 템플릿 로드"""
        with open(self.template_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_product_info(self, file_path):
        """제품 정보 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # 제품명 추출
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            product_name = title_match.group(1) if title_match else f"만원요리 제품 {file_path.stem}"
            
            # 이미지 추출
            img_matches = re.findall(r'<img[^>]*src=["\'](.*?)["\']', content, re.IGNORECASE)
            main_image = img_matches[0] if img_matches else "https://via.placeholder.com/800x600?text=상품이미지"
            detail_image = img_matches[1] if len(img_matches) > 1 else main_image
            
            # 간단한 설명 추출
            desc_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
            description = ""
            if desc_match:
                description = re.sub(r'<[^>]+>', '', desc_match.group(1))[:100]
            
            if not description:
                description = f"{product_name}의 프리미엄 간편식입니다."
            
            return {
                'product_name': product_name,
                'main_image': main_image,
                'detail_image': detail_image,
                'description': description
            }
        except Exception as e:
            print(f"[ERROR] 정보 추출 실패: {e}")
            return {
                'product_name': f"만원요리 제품 {file_path.stem}",
                'main_image': "https://via.placeholder.com/800x600?text=상품이미지",
                'detail_image': "https://via.placeholder.com/800x600?text=상세이미지", 
                'description': "프리미엄 간편식의 새로운 기준"
            }
    
    def generate_sample(self, template, product_info, product_number):
        """템플릿에 제품 정보 적용하여 샘플 생성"""
        
        # 제품별 특성 정의
        product_specs = {
            '132': {'weight': '500g', 'type': '왕만두', 'cooking': '찜기 10분'},
            '133': {'weight': '400g', 'type': '군만두', 'cooking': '팬 5분'},
            '134': {'weight': '600g', 'type': '물만두', 'cooking': '끓는물 8분'},
            '135': {'weight': '350g', 'type': '튀김만두', 'cooking': '기름 3분'},
            '140': {'weight': '450g', 'type': '새우만두', 'cooking': '전자레인지 4분'}
        }
        
        spec = product_specs.get(product_number, {'weight': '360g', 'type': '교자만두', 'cooking': '전자레인지 3-5분'})
        
        # 템플릿 치환
        sample = template
        
        # 기본 정보 치환
        sample = sample.replace('만원요리 최씨남매 X 취영루 오리지널 교자만두', product_info['product_name'])
        sample = sample.replace('만원요리 최씨남매 X 취영루 단독 공급', product_info['description'])
        
        # 이미지 치환
        sample = re.sub(
            r'src="https://ecimg\.cafe24img\.com/[^"]*"',
            f'src="{product_info["detail_image"]}"',
            sample
        )
        
        # 내용량 치환
        sample = sample.replace('<td>360g</td>', f'<td>{spec["weight"]}</td>')
        
        # 조리방법 개별화
        cooking_methods = {
            '132': ['냉동 상태에서 찜기에 10분', '전자레인지 5-7분', '에어프라이어 8분'],
            '133': ['팬에 기름 두르고 5분 굽기', '에어프라이어 6분', '전자레인지 4분'],
            '134': ['끓는 물에 8분간 삶기', '찜기 12분', '전자레인지 5분'],
            '135': ['기름에 3분간 튀기기', '에어프라이어 5분', '오븐 180도 10분'],
            '140': ['냉동 상태에서 바로 조리', '전자레인지 4분', '찜기 8분']
        }
        
        methods = cooking_methods.get(product_number, ['냉동 상태에서 바로 조리 가능', '전자레인지 3-5분', '에어프라이어 5-7분'])
        
        # 조리방법 리스트 치환
        old_cooking = '''<ol>
          <li>냉동 상태에서 바로 조리 가능</li>
          <li>전자레인지 3-5분</li>
          <li>에어프라이어 5-7분</li>
        </ol>'''
        
        new_cooking = f'''<ol>
          <li>{methods[0]}</li>
          <li>{methods[1]}</li>
          <li>{methods[2]}</li>
        </ol>'''
        
        sample = sample.replace(old_cooking, new_cooking)
        
        # 제품 특징 개별화
        features = {
            '132': ['육즙 가득한 왕만두', '큼직한 크기로 한 끼 식사 완성', '풍부한 속재료로 만족감 극대화'],
            '133': ['바삭한 겉면의 군만두', '고소한 맛이 일품인 구이식', '간편하게 팬에서 바로 조리'],
            '134': ['국물과 함께 즐기는 물만두', '부드러운 식감의 만두피', '깔끔한 국물 맛의 완성'],
            '135': ['바삭함이 살아있는 튀김만두', '겉바속촉의 완벽한 식감', '스낵처럼 간편하게'],
            '140': ['프리미엄 새우가 들어간 만두', '신선한 새우의 탱글한 식감', '고급스러운 맛의 완성']
        }
        
        feature_list = features.get(product_number, ['엄선된 재료로 만든 프리미엄 제품', '간편한 조리로 완벽한 한 끼 식사', '합리적인 가격의 고품질 간편식'])
        
        # 특징 리스트 치환
        old_features = '''<ul>
          <li>엄선된 재료로 만든 프리미엄 제품</li>
          <li>간편한 조리로 완벽한 한 끼 식사</li>
          <li>합리적인 가격의 고품질 간편식</li>
        </ul>'''
        
        new_features = f'''<ul>
          <li>{feature_list[0]}</li>
          <li>{feature_list[1]}</li>
          <li>{feature_list[2]}</li>
        </ul>'''
        
        sample = sample.replace(old_features, new_features)
        
        # 오타 수정 (㈜r값진한끼 -> ㈜값진한끼)
        sample = sample.replace('㈜r값진한끼', '㈜값진한끼')
        
        return sample
    
    def create_samples(self, product_numbers=['132', '133', '134', '135', '140']):
        """여러 제품 샘플 생성"""
        
        # 템플릿 로드
        template = self.load_template()
        print(f"[로드] 템플릿 로드 완료: {self.template_file}")
        
        success_count = 0
        
        for product_number in product_numbers:
            try:
                # 원본 파일에서 정보 추출
                source_file = self.input_path / f"{product_number}.txt"
                
                if source_file.exists():
                    product_info = self.extract_product_info(source_file)
                    print(f"[추출] {product_number}: {product_info['product_name'][:30]}...")
                else:
                    # 파일이 없으면 기본값 사용
                    product_info = {
                        'product_name': f"만원요리 프리미엄 제품 {product_number}",
                        'main_image': "https://via.placeholder.com/800x600?text=상품이미지",
                        'detail_image': "https://via.placeholder.com/800x600?text=상세이미지",
                        'description': "프리미엄 간편식의 새로운 기준"
                    }
                    print(f"[기본값] {product_number}: 원본 파일 없음, 기본값 사용")
                
                # 샘플 생성
                sample_html = self.generate_sample(template, product_info, product_number)
                
                # 파일 저장
                output_file = self.output_path / f"{product_number}_final_sample.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(sample_html)
                
                print(f"[완료] {output_file}")
                success_count += 1
                
            except Exception as e:
                print(f"[ERROR] {product_number} 생성 실패: {e}")
        
        print(f"\n[최종] 총 {success_count}개 샘플 생성 완료!")
        print(f"저장 위치: {self.output_path}")
        
        return success_count

if __name__ == "__main__":
    generator = FinalSampleGenerator()
    generator.create_samples()