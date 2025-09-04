#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
완전 통합 Type D 배치 처리 시스템
- 274개 txt 파일 일괄 처리
- 업체별 자동 분류 및 저장
- 메타데이터 및 인덱스 생성
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Tuple
import traceback

# 현재 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template_manager import TemplateManager
from typeD_organizer import TypeDOrganizer
from bs4 import BeautifulSoup

class TypeDBatchProcessor:
    """Type D 일괄 처리 시스템"""
    
    def __init__(self):
        self.cua_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt")
        self.output_base = Path("output/typeD_final")
        self.output_base.mkdir(parents=True, exist_ok=True)
        
        # 템플릿 매니저와 조직화 시스템 초기화
        self.template_manager = TemplateManager()
        self.organizer = TypeDOrganizer(str(self.output_base))
        
        # 처리 통계
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'vendors': {}
        }
    
    def extract_product_info(self, txt_file: Path) -> Dict:
        """txt 파일에서 제품 정보 추출"""
        try:
            # 파일 읽기 (인코딩 자동 감지)
            content = None
            for encoding in ['utf-8', 'cp949', 'euc-kr']:
                try:
                    with open(txt_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except:
                    continue
            
            if not content:
                return None
            
            # BeautifulSoup으로 파싱
            soup = BeautifulSoup(content, 'html.parser')
            
            # 제품명 추출
            product_name = "제품"
            title_tag = soup.find('title')
            if title_tag and title_tag.text:
                product_name = title_tag.text.strip()
            
            # 이미지 추출
            images = []
            for img in soup.find_all('img', src=True):
                img_url = img['src']
                if img_url and 'ecimg.cafe24img.com' in img_url:
                    images.append(img_url)
            
            # 텍스트 콘텐츠 추출
            text_content = []
            for tag in soup.find_all(['p', 'div', 'span']):
                text = tag.get_text(strip=True)
                if text and len(text) > 10:
                    text_content.append(text)
            
            # 파일 번호
            file_number = txt_file.stem
            
            return {
                'number': file_number,
                'name': product_name,
                'images': images[:5],  # 최대 5개 이미지
                'description': ' '.join(text_content[:3]) if text_content else '',
                'content_lines': text_content[:10]  # 콘텐츠 라인들
            }
            
        except Exception as e:
            print(f"  추출 실패 {txt_file.name}: {e}")
            return None
    
    def generate_typeD_content(self, product_info: Dict) -> Dict:
        """Type D 템플릿용 콘텐츠 생성"""
        
        # 기본값 설정
        name = product_info.get('name', '제품')
        description = product_info.get('description', '')
        images = product_info.get('images', [])
        content_lines = product_info.get('content_lines', [])
        
        # Type D 변수 매핑
        template_vars = {
            'main_headline': f"드디어 만나는 진짜 {name}",
            'sub_headline': "매일 먹어도 질리지 않는 특별한 맛",
            
            # WHY 섹션
            'why_title': f"왜 {name}를 선택해야 할까요?",
            'why_points': [
                "최고급 원재료만을 엄선하여 사용합니다",
                "전통 제조 방식을 고수하며 정성을 담았습니다",
                "합리적인 가격으로 프리미엄 품질을 제공합니다"
            ],
            
            # STORY 섹션
            'story_title': "우리의 이야기",
            'story_intro': description if description else f"{name}의 특별한 이야기를 들려드립니다",
            'story_content': content_lines[:3] if content_lines else [
                "오랜 시간 연구 개발을 통해 완성된 레시피입니다",
                "고객님의 건강한 식탁을 위해 최선을 다합니다",
                "신선하고 안전한 제품을 약속드립니다"
            ],
            
            # HOW 섹션
            'how_title': "이렇게 만들어집니다",
            'how_steps': [
                "신선한 재료를 매일 아침 공수합니다",
                "숙련된 전문가가 정성껏 조리합니다",
                "철저한 품질 검사를 거쳐 포장됩니다",
                "신속하고 안전하게 배송해드립니다"
            ],
            
            # TRUST 섹션
            'trust_title': "믿고 드실 수 있습니다",
            'trust_points': [
                "HACCP 인증 시설에서 제조",
                "100% 국내산 원재료 사용",
                "고객 만족도 98% 달성"
            ],
            
            # 이미지
            'product_images': images,
            'main_image': images[0] if images else '',
            
            # 기타 정보
            'product_name': name,
            'product_number': product_info.get('number', ''),
            'generated_date': datetime.now().strftime('%Y년 %m월 %d일')
        }
        
        return template_vars
    
    def process_single_file(self, txt_file: Path) -> Dict:
        """단일 파일 처리"""
        try:
            # 1. 제품 정보 추출
            product_info = self.extract_product_info(txt_file)
            if not product_info:
                return {'status': 'failed', 'file': str(txt_file), 'error': '정보 추출 실패'}
            
            # 2. Type D 콘텐츠 생성
            template_vars = self.generate_typeD_content(product_info)
            
            # 3. 템플릿 렌더링
            html_content = self.template_manager.render_template('typeD', template_vars)
            
            # 4. 업체별 분류 및 저장
            save_result = self.organizer.save_typeD_file(
                html_content, 
                str(txt_file),
                product_info
            )
            
            return {
                'status': 'success',
                'file': str(txt_file),
                'vendor': save_result['vendor'],
                'output': save_result['output_path'],
                'product': product_info['name']
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'file': str(txt_file),
                'error': str(e),
                'trace': traceback.format_exc()
            }
    
    def process_all_files(self, max_workers: int = 4):
        """모든 txt 파일 병렬 처리"""
        
        # txt 파일 목록 수집
        txt_files = list(self.cua_dir.glob("*.txt"))
        self.stats['total'] = len(txt_files)
        
        print(f"\n=== Type D 일괄 처리 시작 ===")
        print(f"소스 디렉토리: {self.cua_dir}")
        print(f"출력 디렉토리: {self.output_base}")
        print(f"총 {len(txt_files)}개 파일 발견\n")
        
        # 진행 상황 표시
        start_time = time.time()
        
        # 순차 처리 (병렬 처리시 인코딩 문제 방지)
        for i, txt_file in enumerate(txt_files, 1):
            print(f"[{i}/{len(txt_files)}] {txt_file.name} 처리 중...", end="")
            
            result = self.process_single_file(txt_file)
            
            if result['status'] == 'success':
                self.stats['success'] += 1
                vendor = result['vendor']
                self.stats['vendors'][vendor] = self.stats['vendors'].get(vendor, 0) + 1
                print(f" OK [{vendor}]")
            else:
                self.stats['failed'] += 1
                print(f" FAIL: {result.get('error', 'Unknown')}")
        
        # 처리 완료
        elapsed = time.time() - start_time
        
        print(f"\n=== 처리 완료 ===")
        print(f"소요 시간: {elapsed:.1f}초")
        print(f"성공: {self.stats['success']}개")
        print(f"실패: {self.stats['failed']}개")
        
        # 업체별 통계
        if self.stats['vendors']:
            print(f"\n=== 업체별 생성 현황 ===")
            for vendor, count in sorted(self.stats['vendors'].items()):
                print(f"  {vendor:15} : {count:3}개")
    
    def generate_final_reports(self):
        """최종 보고서 생성"""
        
        # 1. 메타데이터 생성
        print("\n메타데이터 생성 중...")
        metadata = self.organizer.create_metadata()
        
        # 2. 인덱스 HTML 생성
        print("인덱스 페이지 생성 중...")
        index_file = self.organizer.create_index_html()
        
        # 3. 처리 로그 저장
        log_file = self.output_base / f"processing_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                'processing_time': datetime.now().isoformat(),
                'stats': self.stats,
                'metadata': metadata
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n=== 최종 보고서 ===")
        print(f"메타데이터: {self.output_base}/metadata.json")
        print(f"인덱스 페이지: {index_file}")
        print(f"처리 로그: {log_file}")
        
        # 브라우저에서 인덱스 열기
        import webbrowser
        webbrowser.open(str(index_file))


def main():
    """메인 실행 함수"""
    
    processor = TypeDBatchProcessor()
    
    try:
        # 1. 모든 파일 처리
        processor.process_all_files(max_workers=4)
        
        # 2. 최종 보고서 생성
        processor.generate_final_reports()
        
        print("\n[COMPLETE] 모든 처리가 완료되었습니다!")
        print(f"[OUTPUT] 결과 확인: {processor.output_base}")
        
    except KeyboardInterrupt:
        print("\n\n[STOPPED] 사용자에 의해 중단됨")
    except Exception as e:
        print(f"\n\n[ERROR] 오류 발생: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()