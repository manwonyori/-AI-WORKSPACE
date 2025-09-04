#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
개선된 HTML 파일과 다운로드 이미지 매칭 검증 시스템

이 스크립트는:
1. 파일명 기반의 스마트 매칭 수행
2. 공급업체 폴더간 교차 참조 지원
3. 상세한 매칭 통계 및 누락 파일 분석 제공
"""

import os
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict
import datetime
import difflib

class EnhancedImageMatchingVerifier:
    def __init__(self):
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24")
        self.html_path = self.base_path / "complete_content" / "html"
        self.ftp_download_path = self.base_path / "ftp_mirror" / "download" / "web" / "product"
        self.image_analysis_file = self.base_path / "image_analysis_report.json"
        
        # 매칭 결과 저장
        self.matching_results = {
            'total_html_images': 0,
            'exact_matched': 0,
            'filename_matched': 0,
            'unmatched': 0,
            'suppliers': {},
            'missing_files': [],
            'available_files': [],
            'cross_reference_matches': [],
            'detailed_analysis': {}
        }
        
        # 파일명 기반 인덱스
        self.filename_index = {}
        
    def load_image_analysis_report(self):
        """image_analysis_report.json 파일 로드"""
        try:
            with open(self.image_analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"이미지 분석 보고서 로드 실패: {e}")
            return None
    
    def extract_filename_from_url(self, url):
        """URL에서 파일명만 추출"""
        parsed = urlparse(url)
        return os.path.basename(parsed.path)
    
    def extract_image_path_from_url(self, url):
        """URL에서 상대 경로 추출"""
        if not url.startswith('https://ecimg.cafe24img.com'):
            return None
            
        parsed = urlparse(url)
        path_parts = parsed.path.split('/')
        
        if len(path_parts) >= 6 and path_parts[3] == 'web' and path_parts[4] == 'product':
            relative_path = '/'.join(path_parts[5:])
            return relative_path
        
        return None
    
    def build_filename_index(self, downloaded_files):
        """파일명 기반 인덱스 구축"""
        filename_index = defaultdict(list)
        
        for full_path, local_path in downloaded_files.items():
            filename = os.path.basename(full_path)
            filename_index[filename].append({
                'full_path': full_path,
                'local_path': local_path,
                'supplier': self.categorize_by_supplier(full_path)
            })
        
        return filename_index
    
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
                    
                    path_key = str(relative_path).replace('\\', '/')
                    downloaded_files[path_key] = str(full_path)
        
        return downloaded_files
    
    def categorize_by_supplier(self, file_path):
        """파일 경로에서 공급업체 분류"""
        path_parts = file_path.lower().split('/')
        
        if len(path_parts) > 0:
            first_part = path_parts[0]
            
            supplier_mapping = {
                'life': '인생',
                'ccw': '씨씨더블유', 
                'taekong': '태콩',
                'bs': 'BS',
                'chi': '치킨',
                'choi': '최가네',
                'haesun': '해순'
            }
            
            return supplier_mapping.get(first_part, '기타')
        
        return '분류불가'
    
    def find_best_filename_match(self, target_filename, filename_index):
        """파일명 기반 최적 매칭 찾기"""
        # 1. 정확한 매칭
        if target_filename in filename_index:
            return filename_index[target_filename], 'exact'
        
        # 2. 유사한 파일명 찾기
        all_filenames = list(filename_index.keys())
        close_matches = difflib.get_close_matches(target_filename, all_filenames, n=3, cutoff=0.8)
        
        if close_matches:
            return filename_index[close_matches[0]], 'similar'
        
        # 3. 확장자 제거 후 매칭
        base_name = os.path.splitext(target_filename)[0]
        for filename in all_filenames:
            if os.path.splitext(filename)[0] == base_name:
                return filename_index[filename], 'base_match'
        
        return None, 'not_found'
    
    def verify_enhanced_matching(self):
        """향상된 이미지 매칭 검증 수행"""
        print("향상된 이미지 매칭 검증을 시작합니다...")
        
        # 1. 이미지 분석 보고서 로드
        image_report = self.load_image_analysis_report()
        if not image_report:
            return None
        
        # 2. FTP 다운로드된 파일들 스캔
        print("FTP 다운로드된 파일들을 스캔합니다...")
        downloaded_files = self.scan_ftp_downloaded_files()
        print(f"다운로드된 이미지 파일 수: {len(downloaded_files)}")
        
        # 3. 파일명 인덱스 구축
        print("파일명 인덱스를 구축합니다...")
        filename_index = self.build_filename_index(downloaded_files)
        
        # 4. HTML 이미지 URL 분석 및 매칭
        print("HTML 이미지 URL 분석 및 매칭을 수행합니다...")
        
        for file_key, file_data in image_report.get('file_details', {}).items():
            images = file_data.get('images', [])
            self.matching_results['total_html_images'] += len(images)
            
            supplier = file_key.split('/')[0] if '/' in file_key else '분류불가'
            if supplier not in self.matching_results['suppliers']:
                self.matching_results['suppliers'][supplier] = {
                    'total_images': 0,
                    'exact_matched': 0,
                    'filename_matched': 0,
                    'unmatched': 0,
                    'cross_references': []
                }
            
            self.matching_results['suppliers'][supplier]['total_images'] += len(images)
            
            file_matches = []
            
            for image_url in images:
                relative_path = self.extract_image_path_from_url(image_url)
                filename = self.extract_filename_from_url(image_url)
                
                match_info = {
                    'url': image_url,
                    'expected_path': relative_path,
                    'filename': filename,
                    'status': 'unmatched',
                    'match_type': None,
                    'actual_path': None,
                    'supplier_mismatch': False
                }
                
                if relative_path:
                    # 1. 정확한 경로 매칭 시도
                    if relative_path in downloaded_files:
                        match_info.update({
                            'status': 'matched',
                            'match_type': 'exact_path',
                            'actual_path': relative_path
                        })
                        self.matching_results['exact_matched'] += 1
                        self.matching_results['suppliers'][supplier]['exact_matched'] += 1
                    
                    # 2. 파일명 기반 매칭 시도
                    elif filename:
                        matches, match_type = self.find_best_filename_match(filename, filename_index)
                        
                        if matches:
                            best_match = matches[0]  # 첫 번째 매칭 사용
                            match_info.update({
                                'status': 'matched',
                                'match_type': f'filename_{match_type}',
                                'actual_path': best_match['full_path'],
                                'supplier_mismatch': best_match['supplier'] != supplier
                            })
                            
                            self.matching_results['filename_matched'] += 1
                            self.matching_results['suppliers'][supplier]['filename_matched'] += 1
                            
                            if match_info['supplier_mismatch']:
                                self.matching_results['cross_reference_matches'].append({
                                    'html_file': file_key,
                                    'expected_supplier': supplier,
                                    'actual_supplier': best_match['supplier'],
                                    'filename': filename,
                                    'actual_path': best_match['full_path']
                                })
                        else:
                            match_info['status'] = 'unmatched'
                            self.matching_results['unmatched'] += 1
                            self.matching_results['suppliers'][supplier]['unmatched'] += 1
                            self.matching_results['missing_files'].append({
                                'html_file': file_key,
                                'image_url': image_url,
                                'expected_path': relative_path,
                                'filename': filename
                            })
                
                file_matches.append(match_info)
            
            self.matching_results['detailed_analysis'][file_key] = file_matches
        
        return self.matching_results
    
    def generate_enhanced_report(self):
        """향상된 검증 결과 보고서 생성"""
        results = self.verify_enhanced_matching()
        if not results:
            print("검증 결과를 생성할 수 없습니다.")
            return None
        
        total_matched = results['exact_matched'] + results['filename_matched']
        match_rate = (total_matched / results['total_html_images'] * 100) if results['total_html_images'] > 0 else 0
        
        # 보고서 생성
        report = {
            'verification_date': datetime.datetime.now().isoformat(),
            'enhanced_summary': {
                'total_html_images': results['total_html_images'],
                'exact_path_matches': results['exact_matched'],
                'filename_matches': results['filename_matched'],
                'total_matches': total_matched,
                'unmatched_images': results['unmatched'],
                'overall_match_rate': f"{match_rate:.2f}%",
                'exact_match_rate': f"{(results['exact_matched'] / results['total_html_images'] * 100):.2f}%",
                'filename_match_rate': f"{(results['filename_matched'] / results['total_html_images'] * 100):.2f}%"
            },
            'supplier_detailed_analysis': results['suppliers'],
            'cross_reference_matches': results['cross_reference_matches'],
            'missing_files': results['missing_files'],
            'detailed_file_analysis': results['detailed_analysis']
        }
        
        # JSON 파일로 저장
        report_file = self.base_path / f"enhanced_image_matching_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 콘솔 출력
        print(f"\n=== 향상된 이미지 매칭 검증 결과 ===")
        print(f"검증 완료 시간: {report['verification_date']}")
        print(f"전체 HTML 이미지 수: {report['enhanced_summary']['total_html_images']}")
        print(f"정확한 경로 매칭: {report['enhanced_summary']['exact_path_matches']}")
        print(f"파일명 기반 매칭: {report['enhanced_summary']['filename_matches']}")
        print(f"전체 매칭 수: {report['enhanced_summary']['total_matches']}")
        print(f"매칭되지 않은 수: {report['enhanced_summary']['unmatched_images']}")
        print(f"전체 매칭률: {report['enhanced_summary']['overall_match_rate']}")
        
        print(f"\n=== 공급업체별 상세 분석 ===")
        for supplier, data in report['supplier_detailed_analysis'].items():
            total = data['total_images']
            exact = data['exact_matched']
            filename = data['filename_matched']
            unmatched = data['unmatched']
            total_matched = exact + filename
            rate = (total_matched / total * 100) if total > 0 else 0
            print(f"{supplier}: {total_matched}/{total} 매칭 ({rate:.1f}%) [정확:{exact}, 파일명:{filename}, 미매칭:{unmatched}]")
        
        if results['cross_reference_matches']:
            print(f"\n=== 공급업체 교차 참조 매칭 ({len(results['cross_reference_matches'])}건) ===")
            for i, cross_ref in enumerate(results['cross_reference_matches'][:10]):  # 처음 10건만 표시
                print(f"{i+1}. {cross_ref['html_file']} - {cross_ref['filename']}")
                print(f"   예상: {cross_ref['expected_supplier']} → 실제: {cross_ref['actual_supplier']}")
        
        if results['missing_files']:
            print(f"\n=== 진짜 누락된 파일 ({len(results['missing_files'])}건) ===")
            for i, missing in enumerate(results['missing_files'][:5]):  # 처음 5건만 표시
                print(f"{i+1}. {missing['html_file']} - {missing['filename']}")
        
        print(f"\n상세 보고서가 저장되었습니다: {report_file}")
        return report_file

def main():
    """메인 실행 함수"""
    verifier = EnhancedImageMatchingVerifier()
    report_file = verifier.generate_enhanced_report()
    
    if report_file:
        print(f"\n검증 완료! 상세한 결과는 {report_file}에서 확인하세요.")
    else:
        print("검증 실패!")

if __name__ == "__main__":
    main()