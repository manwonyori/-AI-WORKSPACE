"""
Claude Bridge 통합 상세페이지 시스템
- 품질 중심의 자동화 시스템
- 이미지 생성 및 최적화 통합
- 카페24 업로드 준비
"""

import os
import json
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class ClaudeBridgeUnifiedSystem:
    def __init__(self):
        """Claude Bridge 통합 시스템 초기화"""
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.bridge_path = Path(r"C:\Users\8899y\claude_bridge")
        self.input_path = self.base_path / "html" / "temp_txt"
        self.output_base = self.base_path / "output"
        
        # 출력 디렉토리 구조
        self.output_dirs = {
            'unified': self.output_base / 'unified',
            'images': self.output_base / 'images',
            'ready_to_upload': self.output_base / 'ready_to_upload',
            'reports': self.output_base / 'reports',
            'cafe24_format': self.output_base / 'cafe24_format'
        }
        
        # 디렉토리 생성
        for dir_path in self.output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 브랜드 디자인 시스템
        self.design_system = {
            'brand': {
                'name': '만원요리',
                'tagline': '프리미엄 간편식의 새로운 기준',
                'primary_color': '#E4A853',
                'secondary_color': '#C53030',
                'accent_color': '#5f0080'
            },
            'layout': {
                'max_width': '1200px',
                'mobile_breakpoint': '768px',
                'desktop_image_size': '500px',
                'mobile_image_size': '100%'
            },
            'typography': {
                'font_family': 'Noto Sans KR',
                'title_size': '28px',
                'subtitle_size': '16px',
                'body_size': '14px'
            }
        }
        
        # Claude Bridge 통신 설정
        self.bridge_config = {
            'request_dir': self.bridge_path / 'requests',
            'response_dir': self.bridge_path / 'responses',
            'status_file': self.bridge_path / 'status.json'
        }
        
        self._ensure_bridge_dirs()
    
    def _ensure_bridge_dirs(self):
        """Bridge 디렉토리 확인 및 생성"""
        for dir_path in [self.bridge_config['request_dir'], self.bridge_config['response_dir']]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def analyze_product_content(self, file_path: Path) -> Dict:
        """제품 콘텐츠 심층 분석"""
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            analysis = {
                'product_number': file_path.stem,
                'has_images': bool(re.findall(r'<img[^>]*src=["\'](.*?)["\']', content)),
                'has_price': bool(re.search(r'\d{1,3}(?:,\d{3})*\s*원', content)),
                'has_description': bool(re.search(r'<p[^>]*>.*?</p>', content, re.DOTALL)),
                'structure_type': self._detect_structure_type(content),
                'quality_score': self._calculate_quality_score(content)
            }
            
            # 제품 정보 추출
            product_info = self._extract_detailed_info(content)
            analysis['product_info'] = product_info
            
            # 개선 필요 사항
            analysis['improvements_needed'] = self._identify_improvements(content, product_info)
            
            return analysis
            
        except Exception as e:
            print(f"[ERROR] 콘텐츠 분석 실패: {e}")
            return {}
    
    def _detect_structure_type(self, content: str) -> str:
        """HTML 구조 타입 감지"""
        if 'kurly' in content.lower() or '--kurly-' in content:
            return 'kurly_style'
        elif 'strategic-header' in content:
            return 'strategic_style'
        elif '<table' in content and 'ingredient' in content.lower():
            return 'table_based'
        else:
            return 'basic'
    
    def _calculate_quality_score(self, content: str) -> int:
        """콘텐츠 품질 점수 계산 (0-100)"""
        score = 0
        
        # 기본 요소 체크
        if '<title>' in content: score += 10
        if re.search(r'<meta.*viewport', content): score += 10
        if re.search(r'<meta.*charset', content): score += 10
        
        # 이미지 품질
        images = re.findall(r'<img[^>]*>', content)
        if images:
            score += min(len(images) * 5, 20)
            if any('alt=' in img for img in images): score += 5
        
        # 스타일 품질
        if '<style>' in content or 'style=' in content: score += 10
        if 'responsive' in content.lower() or '@media' in content: score += 15
        
        # 콘텐츠 풍부도
        if len(content) > 5000: score += 10
        if re.search(r'<h[1-6]>', content): score += 5
        if '<table>' in content: score += 5
        
        return min(score, 100)
    
    def _extract_detailed_info(self, content: str) -> Dict:
        """상세 제품 정보 추출"""
        info = {
            'title': '',
            'price': '',
            'discount': '',
            'images': [],
            'description': '',
            'specifications': {}
        }
        
        # 제목 추출
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            info['title'] = title_match.group(1).strip()
        
        # 가격 정보
        price_matches = re.findall(r'(\d{1,3}(?:,\d{3})*)\s*원', content)
        if price_matches:
            info['price'] = price_matches[0]
        
        # 할인율
        discount_match = re.search(r'(\d+)\s*%', content)
        if discount_match:
            info['discount'] = discount_match.group(1)
        
        # 이미지 URL
        img_matches = re.findall(r'<img[^>]*src=["\'](.*?)["\']', content, re.IGNORECASE)
        info['images'] = img_matches[:10]
        
        # 설명 추출
        desc_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        if desc_match:
            info['description'] = re.sub(r'<[^>]+>', '', desc_match.group(1))[:500]
        
        return info
    
    def _identify_improvements(self, content: str, product_info: Dict) -> List[str]:
        """개선 필요 사항 식별"""
        improvements = []
        
        if not product_info['images']:
            improvements.append("이미지 추가 필요")
        elif len(product_info['images']) < 3:
            improvements.append("추가 이미지 필요 (최소 3개 권장)")
        
        if not product_info['description']:
            improvements.append("상품 설명 추가 필요")
        
        if '@media' not in content:
            improvements.append("반응형 디자인 적용 필요")
        
        if 'nutrition' not in content.lower() and 'ingredient' not in content.lower():
            improvements.append("영양 정보 또는 원재료 정보 추가 권장")
        
        return improvements
    
    def generate_optimized_page(self, product_number: str, optimization_level: str = 'full') -> Dict:
        """최적화된 페이지 생성"""
        file_path = self.input_path / f"{product_number}.txt"
        
        if not file_path.exists():
            return {'error': f"파일을 찾을 수 없습니다: {file_path}"}
        
        # 콘텐츠 분석
        analysis = self.analyze_product_content(file_path)
        
        # 최적화 레벨에 따른 처리
        if optimization_level == 'full':
            result = self._full_optimization(analysis)
        elif optimization_level == 'minimal':
            result = self._minimal_optimization(analysis)
        else:
            result = self._standard_optimization(analysis)
        
        # 결과 저장
        self._save_optimized_content(result, product_number, optimization_level)
        
        # Claude Bridge로 전송
        self._send_to_bridge(result, product_number)
        
        return result
    
    def _full_optimization(self, analysis: Dict) -> Dict:
        """완전 최적화 - 이미지 생성 포함"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'optimization_level': 'full',
            'analysis': analysis,
            'generated_content': {}
        }
        
        # 새로운 이미지 생성 요청
        if analysis['quality_score'] < 70 or not analysis['product_info']['images']:
            result['image_generation_request'] = {
                'product_name': analysis['product_info']['title'],
                'style': 'professional_product',
                'count': 5,
                'sizes': ['1000x1000', '500x500', '800x600']
            }
        
        # HTML 재구성
        result['generated_content']['html'] = self._create_premium_html(analysis)
        result['generated_content']['css'] = self._create_premium_css()
        result['generated_content']['javascript'] = self._create_interactive_js()
        
        return result
    
    def _standard_optimization(self, analysis: Dict) -> Dict:
        """표준 최적화 - 기존 리소스 활용"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'optimization_level': 'standard',
            'analysis': analysis,
            'generated_content': {}
        }
        
        # 기존 이미지 최적화
        if analysis['product_info']['images']:
            result['optimized_images'] = self._optimize_existing_images(analysis['product_info']['images'])
        
        # HTML 개선
        result['generated_content']['html'] = self._improve_existing_html(analysis)
        
        return result
    
    def _minimal_optimization(self, analysis: Dict) -> Dict:
        """최소 최적화 - 필수 요소만"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'optimization_level': 'minimal',
            'analysis': analysis,
            'generated_content': {}
        }
        
        # 반응형 CSS만 추가
        result['generated_content']['responsive_css'] = self._create_responsive_css()
        
        return result
    
    def _create_premium_html(self, analysis: Dict) -> str:
        """프리미엄 HTML 생성"""
        info = analysis['product_info']
        
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{info['title']} - 만원요리</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
</head>
<body>
    <div class="premium-container">
        <!-- 프리미엄 헤더 -->
        <header class="product-header">
            <div class="brand-section">
                <span class="brand-logo">만원요리</span>
                <span class="brand-tagline">프리미엄 간편식의 새로운 기준</span>
            </div>
        </header>
        
        <!-- 메인 콘텐츠 -->
        <main class="product-main">
            <section class="product-showcase">
                <div class="image-gallery">
                    <div class="main-image-wrapper">
                        <img src="{info['images'][0] if info['images'] else 'placeholder.jpg'}" 
                             alt="{info['title']}" class="main-image">
                        {f'<span class="discount-badge">{info["discount"]}% OFF</span>' if info['discount'] else ''}
                    </div>
                </div>
                
                <div class="product-details">
                    <h1 class="product-title">{info['title']}</h1>
                    <div class="price-section">
                        <span class="final-price">{info['price']}원</span>
                    </div>
                    <div class="action-buttons">
                        <button class="btn-primary">구매하기</button>
                        <button class="btn-secondary">장바구니</button>
                    </div>
                </div>
            </section>
        </main>
    </div>
</body>
</html>"""
        
        return html
    
    def _create_premium_css(self) -> str:
        """프리미엄 CSS 생성"""
        return """
        :root {
            --brand-gold: #E4A853;
            --brand-red: #C53030;
            --brand-dark: #1F2937;
            --max-width: 1200px;
        }
        
        .premium-container {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 20px;
        }
        
        @media (max-width: 768px) {
            .product-showcase {
                flex-direction: column;
            }
        }
        """
    
    def _create_responsive_css(self) -> str:
        """반응형 CSS만 생성"""
        return """
        @media (max-width: 768px) {
            img { max-width: 100%; height: auto; }
            .container { padding: 10px; }
        }
        """
    
    def _create_interactive_js(self) -> str:
        """인터랙티브 JavaScript 생성"""
        return """
        function initializeProduct() {
            // 이미지 갤러리
            document.querySelectorAll('.thumbnail').forEach(thumb => {
                thumb.addEventListener('click', function() {
                    document.querySelector('.main-image').src = this.src;
                });
            });
        }
        document.addEventListener('DOMContentLoaded', initializeProduct);
        """
    
    def _optimize_existing_images(self, images: List[str]) -> List[Dict]:
        """기존 이미지 최적화"""
        optimized = []
        for img in images:
            optimized.append({
                'original': img,
                'optimized': img,  # 실제로는 리사이징/압축 처리
                'sizes': {
                    'desktop': '500px',
                    'mobile': '100%'
                }
            })
        return optimized
    
    def _improve_existing_html(self, analysis: Dict) -> str:
        """기존 HTML 개선"""
        # 실제 구현시 기존 HTML을 파싱하여 개선
        return "<!-- Improved HTML -->"
    
    def _save_optimized_content(self, result: Dict, product_number: str, level: str):
        """최적화된 콘텐츠 저장"""
        # HTML 저장
        if 'generated_content' in result and 'html' in result['generated_content']:
            html_file = self.output_dirs['unified'] / f"{product_number}_{level}_optimized.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(result['generated_content']['html'])
            print(f"  [SAVED] HTML: {html_file}")
        
        # 리포트 저장
        report_file = self.output_dirs['reports'] / f"{product_number}_{level}_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"  [SAVED] Report: {report_file}")
    
    def _send_to_bridge(self, result: Dict, product_number: str):
        """Claude Bridge로 전송"""
        request = {
            'timestamp': datetime.now().isoformat(),
            'type': 'product_optimization',
            'product_number': product_number,
            'data': result
        }
        
        request_file = self.bridge_config['request_dir'] / f"request_{product_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(request_file, 'w', encoding='utf-8') as f:
            json.dump(request, f, ensure_ascii=False, indent=2)
        
        print(f"  [BRIDGE] Request sent: {request_file}")
    
    def process_batch(self, product_numbers: List[str], optimization_level: str = 'standard'):
        """배치 처리"""
        results = []
        total = len(product_numbers)
        
        print(f"\n[배치 처리 시작] 총 {total}개 제품")
        print(f"최적화 레벨: {optimization_level}")
        print("-" * 50)
        
        for i, product_number in enumerate(product_numbers, 1):
            print(f"\n[{i}/{total}] 제품 {product_number} 처리중...")
            result = self.generate_optimized_page(product_number, optimization_level)
            results.append(result)
            
            if 'error' not in result:
                print(f"  [OK] 품질 점수: {result['analysis']['quality_score']}/100")
        
        # 배치 리포트 생성
        batch_report = {
            'timestamp': datetime.now().isoformat(),
            'total_products': total,
            'optimization_level': optimization_level,
            'average_quality': sum(r['analysis']['quality_score'] for r in results if 'error' not in r) / len(results),
            'results': results
        }
        
        report_file = self.output_dirs['reports'] / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(batch_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n[배치 완료] 리포트: {report_file}")
        return batch_report

def main():
    """메인 실행"""
    system = ClaudeBridgeUnifiedSystem()
    
    # 단일 제품 테스트
    print("\n=== Claude Bridge 통합 시스템 ===")
    print("품질 중심 최적화 시작...")
    
    # 131번 제품 완전 최적화
    result = system.generate_optimized_page("131", "full")
    
    if 'error' not in result:
        print(f"\n[성공] 제품 131 최적화 완료")
        print(f"  품질 점수: {result['analysis']['quality_score']}/100")
        print(f"  개선 사항: {', '.join(result['analysis']['improvements_needed'])}")
    
    # 배치 처리 예제 (주석 처리)
    # products = ["131", "132", "133"]
    # batch_result = system.process_batch(products, "standard")

if __name__ == "__main__":
    main()