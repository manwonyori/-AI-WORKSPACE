"""
링크 기반 상품설명 강화 시스템
- 실제 이미지 링크를 활용한 풍부한 콘텐츠
- 제품별 스토리텔링 강화
- 다양한 이미지와 설명 조합
"""

import os
import re
from pathlib import Path

class ProductDescriptionEnhancer:
    def __init__(self):
        """상품설명 강화기 초기화"""
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.input_path = self.base_path / "html" / "temp_txt"
        self.output_path = self.base_path / "output" / "content_only"
        self.template_file = self.output_path / "131_content.html"
    
    def extract_all_images(self, file_path):
        """파일에서 모든 이미지 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # 모든 이미지 URL 추출
            img_matches = re.findall(r'<img[^>]*src=["\'](https://[^"\']+)["\']', content, re.IGNORECASE)
            
            # 중복 제거하고 유효한 이미지만
            unique_images = []
            for img in img_matches:
                if img not in unique_images and ('manwonyori' in img or 'ecimg.cafe24' in img):
                    unique_images.append(img)
            
            return unique_images[:6]  # 최대 6개 이미지
            
        except Exception as e:
            print(f"[ERROR] 이미지 추출 실패: {e}")
            return []
    
    def create_enhanced_description(self, product_number, images):
        """제품별 강화된 상품설명 생성"""
        
        # 제품별 상세 스토리
        product_stories = {
            '131': {
                'title': '만원요리 × 취영루 콜라보레이션',
                'subtitle': '70년 전통의 취영루와 만원요리가 만나 탄생한 프리미엄 교자만두',
                'story': [
                    '1950년부터 이어온 취영루의 전통 레시피',
                    '엄선된 국내산 돼지고기와 신선한 채소',
                    '얇고 쫄깃한 만두피와 육즙 가득한 속재료의 완벽한 조화',
                    '냉동 상태로 보관하여 언제든 간편하게 즐기는 프리미엄 만두'
                ],
                'features': [
                    '🏆 70년 전통 취영루의 정통 레시피',
                    '🥟 한입에 터지는 육즙과 풍미',
                    '❄️ 냉동 보관으로 신선함 그대로',
                    '⚡ 3분 만에 완성되는 간편 조리'
                ]
            },
            '132': {
                'title': '고기왕만두 - 푸짐함의 끝판왕',
                'subtitle': '일반 만두보다 2배 큰 사이즈! 한 개만 먹어도 든든한 왕만두',
                'story': [
                    '500g 대용량으로 온 가족이 함께 즐기기 좋은 사이즈',
                    '큼직하게 썬 돼지고기와 각종 채소가 듬뿍',
                    '찜기에서 푹 쪄낸 부드럽고 촉촉한 식감',
                    '한 끼 식사로도 충분한 든든함과 영양'
                ],
                'features': [
                    '👑 왕만두 사이즈로 만족감 극대화',
                    '🥩 푸짐한 고기와 채소 가득',
                    '🍽️ 한 개만으로도 든든한 한 끼',
                    '👨‍👩‍👧‍👦 온 가족이 함께 즐기는 행복한 식사'
                ]
            },
            '133': {
                'title': '김치만두 - 매콤달콤한 한국의 맛',
                'subtitle': '신김치의 깊은 맛과 고소한 고기가 만나 완성된 김치만두',
                'story': [
                    '잘 익은 포기김치를 적당히 다져 넣어 감칠맛 극대화',
                    '매콤한 김치와 고소한 돼지고기의 환상적인 조화',
                    '팬에 구워 바삭한 겉면과 촉촉한 속살의 대비',
                    '한국인이라면 누구나 좋아하는 익숙하고 친근한 맛'
                ],
                'features': [
                    '🌶️ 잘 익은 김치의 깊고 진한 맛',
                    '🔥 매콤달콤한 한국 전통 맛',
                    '🍳 바삭하게 구워 더욱 고소한 풍미',
                    '🇰🇷 한국인의 소울푸드, 김치만두'
                ]
            },
            '134': {
                'title': '물만두 - 깔끔하고 담백한 본연의 맛',
                'subtitle': '맑은 국물과 함께 즐기는 깔끔하고 건강한 물만두',
                'story': [
                    '담백한 돼지고기와 신선한 채소만으로 만든 심플한 맛',
                    '얇고 부드러운 만두피로 국물과의 조화 극대화',
                    '끓는 물에 삶아 국물까지 시원하게 즐기는 진짜 물만두',
                    '기름기 없이 깔끔해서 언제 먹어도 부담 없는 건강식'
                ],
                'features': [
                    '💧 맑고 시원한 국물과 함께',
                    '🌿 담백하고 깔끔한 맛의 정수',
                    '💪 기름기 없는 건강한 조리법',
                    '🍲 든든한 한 그릇 완성'
                ]
            },
            '135': {
                'title': '튀김만두 - 바삭바삭 겉바속촉',
                'subtitle': '바삭한 튀김옷과 촉촉한 속재료의 완벽한 하모니',
                'story': [
                    '고온에서 바삭하게 튀겨낸 골든 브라운 겉면',
                    '겉은 바삭, 속은 촉촉한 겉바속촉의 완벽한 식감',
                    '간식으로도, 안주로도 완벽한 만능 튀김만두',
                    '에어프라이어로 간편하게 바삭함 그대로 재현'
                ],
                'features': [
                    '✨ 바삭바삭 겉바속촉의 식감',
                    '🍤 고급 튀김옷의 완벽한 코팅',
                    '🍺 간식과 안주 겸용 만능템',
                    '🔥 에어프라이어로 더욱 간편하게'
                ]
            },
            '140': {
                'title': '새우만두 - 프리미엄 해산물의 맛',
                'subtitle': '탱글탱글한 새우와 부드러운 만두의 고급스러운 만남',
                'story': [
                    '신선한 새우를 듬뿍 넣어 만든 프리미엄 해산물 만두',
                    '탱글탱글한 새우의 식감과 달콤한 맛이 일품',
                    '고급 중식당에서나 맛볼 수 있는 퀄리티를 집에서',
                    '특별한 날, 특별한 사람과 함께 즐기는 고급 만두'
                ],
                'features': [
                    '🦐 신선한 새우가 듬뿍',
                    '🌟 프리미엄 해산물의 깊은 맛',
                    '🏮 중식당 퀄리티를 집에서',
                    '🎁 특별한 날을 위한 특별한 만두'
                ]
            }
        }
        
        story_data = product_stories.get(product_number, product_stories['131'])
        
        # 이미지 갤러리 HTML 생성
        image_gallery = ""
        if len(images) >= 2:
            image_gallery = f"""
    <!-- 상품 이미지 갤러리 -->
    <div class="image-gallery" style="margin: 30px 0;">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
        <img src="{images[0]}" alt="제품 이미지 1" class="product-image" style="margin: 0;">
        <img src="{images[1]}" alt="제품 이미지 2" class="product-image" style="margin: 0;">
      </div>
    </div>"""
        
        # 추가 이미지가 있다면
        additional_images = ""
        if len(images) > 2:
            additional_images = f"""
    <!-- 추가 상세 이미지 -->
    <div class="detail-images" style="margin: 25px 0;">"""
            for i, img in enumerate(images[2:], 3):
                additional_images += f'\n      <img src="{img}" alt="상세 이미지 {i}" class="product-image">'
            additional_images += "\n    </div>"
        
        # 강화된 상품설명 HTML
        enhanced_html = f"""
      <div class="product-story" style="background: linear-gradient(135deg, #fff5f5 0%, #fff 100%); padding: 25px; border-radius: 12px; margin: 20px 0; border: 1px solid #ffe0e0;">
        <h3 style="color: #ff6b6b; font-size: 20px; font-weight: 700; margin-bottom: 8px; text-align: center;">{story_data['title']}</h3>
        <p style="color: #666; text-align: center; margin-bottom: 20px; font-style: italic;">{story_data['subtitle']}</p>
        
        <!-- 제품 스토리 -->
        <div class="story-content" style="margin: 20px 0;">
          <h4 style="color: #333; font-size: 18px; margin-bottom: 15px; font-weight: 600;">✨ 제품 이야기</h4>
          <ul style="list-style: none; padding: 0;">"""
        
        for story_item in story_data['story']:
            enhanced_html += f'\n            <li style="padding: 8px 0; color: #555; font-size: 16px; line-height: 1.6; padding-left: 20px; position: relative;"><span style="position: absolute; left: 0; color: #ff6b6b;">•</span>{story_item}</li>'
        
        enhanced_html += f"""
          </ul>
        </div>
        
        <!-- 핵심 특징 -->
        <div class="key-features" style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #f0f0f0;">
          <h4 style="color: #333; font-size: 18px; margin-bottom: 15px; font-weight: 600; text-align: center;">🌟 핵심 포인트</h4>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">"""
        
        for feature in story_data['features']:
            enhanced_html += f'\n            <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; font-size: 15px; color: #333; text-align: center; border-left: 3px solid #ff6b6b;">{feature}</div>'
        
        enhanced_html += """
          </div>
        </div>
      </div>"""
        
        return enhanced_html, image_gallery, additional_images
    
    def enhance_product_samples(self, product_numbers=['131', '132', '133', '134', '135', '140']):
        """제품 샘플들의 상품설명 강화"""
        
        # 템플릿 로드
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        success_count = 0
        
        for product_number in product_numbers:
            try:
                print(f"\n[처리중] 제품 {product_number}")
                
                # 원본 파일에서 이미지 추출
                source_file = self.input_path / f"{product_number}.txt"
                images = []
                
                if source_file.exists():
                    images = self.extract_all_images(source_file)
                    print(f"  추출된 이미지: {len(images)}개")
                else:
                    print(f"  원본 파일 없음: {source_file}")
                
                # 기존 샘플 파일 읽기
                sample_file = self.output_path / f"{product_number}_final_sample.html"
                if not sample_file.exists():
                    print(f"  샘플 파일 없음: {sample_file}")
                    continue
                
                with open(sample_file, 'r', encoding='utf-8') as f:
                    sample_content = f.read()
                
                # 강화된 상품설명 생성
                enhanced_desc, image_gallery, additional_images = self.create_enhanced_description(product_number, images)
                
                # 기존 간단한 설명 부분을 강화된 버전으로 교체
                # 기존의 highlight-box와 간단한 설명을 찾아서 교체
                old_section = re.search(r'(<div class="highlight-box">.*?</div>\s*<p[^>]*>.*?</p>)', sample_content, re.DOTALL)
                
                if old_section:
                    sample_content = sample_content.replace(old_section.group(1), enhanced_desc)
                
                # 이미지 갤러리 추가 (조리방법 뒤에)
                cooking_method_end = sample_content.find('</div>\n    </div>\n    \n    <!-- 콘텐츠 이미지')
                if cooking_method_end != -1 and image_gallery:
                    sample_content = sample_content[:cooking_method_end] + "</div>" + image_gallery + "\n    </div>\n    \n    <!-- 콘텐츠 이미지" + sample_content[cooking_method_end + 25:]
                
                # 추가 이미지 삽입 (기존 콘텐츠 이미지 뒤에)
                if additional_images:
                    img_pattern = r'(<img src="[^"]*" alt="상품 상세 이미지" class="product-image">)'
                    sample_content = re.sub(img_pattern, r'\1' + additional_images, sample_content)
                
                # 강화된 버전으로 저장
                enhanced_file = self.output_path / f"{product_number}_enhanced.html"
                with open(enhanced_file, 'w', encoding='utf-8') as f:
                    f.write(sample_content)
                
                print(f"  [완료] {enhanced_file}")
                success_count += 1
                
            except Exception as e:
                print(f"  [ERROR] {product_number} 강화 실패: {e}")
        
        print(f"\n[최종] 총 {success_count}개 제품 설명 강화 완료!")
        return success_count

if __name__ == "__main__":
    enhancer = ProductDescriptionEnhancer()
    enhancer.enhance_product_samples()