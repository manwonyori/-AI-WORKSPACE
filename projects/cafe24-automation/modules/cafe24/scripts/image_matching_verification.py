#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일들과 다운로드된 이미지들 간의 매칭 검증 시스템

이 스크립트는:
1. HTML 파일들에서 참조된 이미지 URL을 분석
2. FTP 다운로드된 실제 이미지 파일들을 스캔
3. 매칭 상태를 검증하고 통계 생성
"""

import os
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict
import datetime

class ImageMatchingVerifier:
    def __init__(self):
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24")
        self.html_path = self.base_path / "complete_content" / "html"
        self.ftp_download_path = self.base_path / "ftp_mirror" / "download" / "web" / "product"
        self.image_analysis_file = self.base_path / "image_analysis_report.json"
        
        # 매칭 결과 저장
        self.matching_results = {
            'total_html_images': 0,
            'matched_images': 0,
            'unmatched_images': 0,
            'suppliers': {},
            'missing_files': [],
            'available_files': [],
            'url_patterns': {},
            'detailed_matches': {}
        }
    
    def load_image_analysis_report(self):
        """image_analysis_report.json 파일 로드"""
        try:
            with open(self.image_analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"이미지 분석 보고서 로드 실패: {e}")
            return None
    
    def extract_image_path_from_url(self, url):
        """URL에서 파일 경로 추출"""
        if not url.startswith('https://ecimg.cafe24img.com'):
            return None
            
        # URL 구조: https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/...
        parsed = urlparse(url)
        path_parts = parsed.path.split('/')
        
        if len(path_parts) >= 6 and path_parts[3] == 'web' and path_parts[4] == 'product':
            # /pg.../manwonyori/web/product/... -> product/ 이후 부분만 추출
            relative_path = '/'.join(path_parts[5:])
            return relative_path
        
        return None
    
    def scan_ftp_downloaded_files(self):
        """FTP 다운로드된 파일들 스캔"""
        downloaded_files = {}
        
        if not self.ftp_download_path.exists():
            print(f"FTP 다운로드 경로를 찾을 수 없습니다: {self.ftp_download_path}")
            return downloaded_files
        
        for root, dirs, files in os.walk(self.ftp_download_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    full_path = Path(root) / file
                    relative_path = full_path.relative_to(self.ftp_download_path)
                    
                    # 파일 경로를 키로 저장 (forward slash 사용)
                    path_key = str(relative_path).replace('\\', '/')
                    downloaded_files[path_key] = str(full_path)
        
        return downloaded_files
    
    def categorize_by_supplier(self, file_path):
        """파일 경로에서 공급업체 분류"""
        path_parts = file_path.lower().split('/')
        
        # 공급업체별 패턴 분석
        if len(path_parts) > 0:
            first_part = path_parts[0]
            
            # 알려진 공급업체 폴더들
            if first_part in ['life', 'ccw', 'taekong', 'bs', 'chi', 'choi', 'haesun']:
                return first_part
            elif first_part in ['25_06_02', '25_06_10']:
                return '기타_날짜폴더'
            elif first_part in ['big', 'medium', 'small', 'tiny', 'extra']:
                return '기타_크기폴더'
            else:
                return '기타'
        
        return '분류불가'
    
    def verify_image_matching(self):
        """이미지 매칭 검증 수행"""
        print("이미지 매칭 검증을 시작합니다...")
        
        # 1. 이미지 분석 보고서 로드
        image_report = self.load_image_analysis_report()
        if not image_report:
            return None
        
        # 2. FTP 다운로드된 파일들 스캔
        print("FTP 다운로드된 파일들을 스캔합니다...")
        downloaded_files = self.scan_ftp_downloaded_files()
        print(f"다운로드된 이미지 파일 수: {len(downloaded_files)}")
        
        # 3. HTML에서 추출된 이미지 URL 분석
        print("HTML 이미지 URL을 분석합니다...")
        
        for file_key, file_data in image_report.get('file_details', {}).items():
            images = file_data.get('images', [])
            self.matching_results['total_html_images'] += len(images)
            
            supplier = file_key.split('/')[0] if '/' in file_key else '분류불가'
            if supplier not in self.matching_results['suppliers']:
                self.matching_results['suppliers'][supplier] = {
                    'total_images': 0,
                    'matched': 0,
                    'unmatched': 0,
                    'missing_files': []
                }
            
            self.matching_results['suppliers'][supplier]['total_images'] += len(images)
            
            file_matches = []
            
            for image_url in images:
                relative_path = self.extract_image_path_from_url(image_url)
                
                if relative_path:
                    # URL 패턴 분석
                    pattern_key = self.categorize_by_supplier(relative_path)
                    if pattern_key not in self.matching_results['url_patterns']:
                        self.matching_results['url_patterns'][pattern_key] = 0
                    self.matching_results['url_patterns'][pattern_key] += 1
                    
                    # 파일 존재 여부 확인
                    if relative_path in downloaded_files:
                        self.matching_results['matched_images'] += 1
                        self.matching_results['suppliers'][supplier]['matched'] += 1
                        self.matching_results['available_files'].append({
                            'html_file': file_key,
                            'image_url': image_url,
                            'relative_path': relative_path,
                            'local_path': downloaded_files[relative_path]
                        })
                        file_matches.append({
                            'url': image_url,
                            'path': relative_path,
                            'status': 'matched',
                            'local_file': downloaded_files[relative_path]
                        })
                    else:
                        self.matching_results['unmatched_images'] += 1
                        self.matching_results['suppliers'][supplier]['unmatched'] += 1
                        missing_info = {
                            'html_file': file_key,
                            'image_url': image_url,
                            'expected_path': relative_path
                        }
                        self.matching_results['missing_files'].append(missing_info)
                        self.matching_results['suppliers'][supplier]['missing_files'].append(missing_info)
                        file_matches.append({
                            'url': image_url,
                            'path': relative_path,
                            'status': 'missing'
                        })
                else:
                    # cafe24 이미지가 아닌 경우
                    file_matches.append({
                        'url': image_url,
                        'status': 'external'
                    })
            
            self.matching_results['detailed_matches'][file_key] = file_matches
        
        return self.matching_results
    
    def generate_report(self):
        """검증 결과 보고서 생성"""
        results = self.verify_image_matching()
        if not results:
            print("검증 결과를 생성할 수 없습니다.")
            return None
        
        # 보고서 생성
        report = {
            'verification_date': datetime.datetime.now().isoformat(),
            'summary': {
                'total_html_images': results['total_html_images'],
                'matched_images': results['matched_images'],
                'unmatched_images': results['unmatched_images'],
                'match_rate': f"{(results['matched_images'] / results['total_html_images'] * 100):.2f}%" if results['total_html_images'] > 0 else "0%"
            },
            'supplier_analysis': results['suppliers'],
            'url_patterns': results['url_patterns'],
            'missing_files_sample': results['missing_files'][:20],  # 처음 20개만 샘플로
            'total_missing_files': len(results['missing_files']),
            'detailed_matches': results['detailed_matches']
        }
        
        # JSON 파일로 저장
        report_file = self.base_path / f"image_matching_verification_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n=== 이미지 매칭 검증 결과 ===")
        print(f"검증 완료 시간: {report['verification_date']}")
        print(f"전체 HTML 이미지 수: {report['summary']['total_html_images']}")
        print(f"매칭된 이미지 수: {report['summary']['matched_images']}")
        print(f"누락된 이미지 수: {report['summary']['unmatched_images']}")
        print(f"매칭률: {report['summary']['match_rate']}")
        
        print(f"\n=== 공급업체별 매칭 현황 ===")
        for supplier, data in report['supplier_analysis'].items():
            print(f"{supplier}: {data['matched']}/{data['total_images']} 매칭 ({(data['matched']/data['total_images']*100):.1f}%)")
        
        print(f"\n=== URL 패턴 분석 ===")
        for pattern, count in report['url_patterns'].items():
            print(f"{pattern}: {count}개 이미지")
        
        if report['total_missing_files'] > 0:
            print(f"\n=== 누락된 파일 샘플 (처음 10개) ===")
            for i, missing in enumerate(report['missing_files_sample'][:10]):
                print(f"{i+1}. {missing['html_file']} - {missing['expected_path']}")
        
        print(f"\n보고서가 저장되었습니다: {report_file}")
        return report_file

def main():
    """메인 실행 함수"""
    verifier = ImageMatchingVerifier()
    report_file = verifier.generate_report()
    
    if report_file:
        print(f"\n검증 완료! 상세한 결과는 {report_file}에서 확인하세요.")
    else:
        print("검증 실패!")

if __name__ == "__main__":
    main()