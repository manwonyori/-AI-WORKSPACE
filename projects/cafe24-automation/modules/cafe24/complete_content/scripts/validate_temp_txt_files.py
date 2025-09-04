#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import io

# Windows 콘솔 UTF-8 설정
if os.name == 'nt':  # Windows
    import codecs
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

"""
temp_txt 파일 무결성 검증 및 재다운로드 시스템
손상되거나 잘못된 HTML TXT 파일들을 자동으로 감지하고 복구
"""
import re
import csv
from pathlib import Path
from datetime import datetime
import json
from collections import defaultdict

class TxtFileValidator:
    def __init__(self):
        self.temp_txt_path = Path("html/temp_txt")
        self.csv_path = None
        self.validation_results = {
            'valid_files': [],
            'corrupted_files': [],
            'empty_files': [],
            'missing_files': [],
            'suspicious_files': [],
            'total_files': 0,
            'validation_time': datetime.now().isoformat()
        }
        
        # 유효한 HTML 콘텐츠 패턴들
        self.valid_patterns = [
            r'<img\s+src=',  # 이미지 태그
            r'<center>',      # center 태그
            r'<br>',          # br 태그
            r'cafe24img\.com', # cafe24 이미지 도메인
            r'\.(jpg|jpeg|png|gif)', # 이미지 확장자
        ]
        
        # 손상 의심 패턴들
        self.corruption_patterns = [
            r'^$',  # 완전히 빈 파일
            r'^\s*$',  # 공백만 있는 파일
            r'404|not found|error', # 에러 메시지
            r'<html><head><title>.*error.*</title>', # HTML 에러 페이지
            r'access denied|forbidden', # 접근 거부
        ]
    
    def find_csv_file(self):
        """최신 CSV 파일 찾기"""
        download_path = Path("../download")
        if not download_path.exists():
            print(f"❌ 다운로드 폴더가 없습니다: {download_path}")
            return None
        
        csv_files = list(download_path.glob("manwonyori_*.csv"))
        if not csv_files:
            print(f"❌ CSV 파일을 찾을 수 없습니다: {download_path}")
            return None
        
        # 가장 최신 파일 선택
        latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
        self.csv_path = latest_csv
        print(f"📄 사용할 CSV: {latest_csv.name}")
        return latest_csv
    
    def get_product_list_from_csv(self):
        """CSV에서 상품번호 목록 추출"""
        if not self.csv_path:
            return []
        
        products = []
        try:
            with open(self.csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product_no = row.get('상품번호', '')
                    product_name = row.get('상품명', '')
                    if product_no:
                        products.append({
                            'no': product_no,
                            'name': product_name[:50]  # 이름 길이 제한
                        })
        except Exception as e:
            print(f"❌ CSV 읽기 실패: {e}")
            return []
        
        return products
    
    def validate_single_file(self, txt_file):
        """개별 TXT 파일 검증"""
        try:
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_size = txt_file.stat().st_size
            product_no = txt_file.stem
            
            # 기본 정보
            validation_info = {
                'product_no': product_no,
                'file_size': file_size,
                'content_length': len(content),
                'issues': [],
                'status': 'valid'
            }
            
            # 1. 파일 크기 체크 (너무 작으면 의심)
            if file_size < 50:  # 50바이트 미만
                validation_info['issues'].append('파일 크기가 너무 작음')
                validation_info['status'] = 'suspicious'
            
            # 2. 빈 파일 체크
            if not content.strip():
                validation_info['issues'].append('빈 파일')
                validation_info['status'] = 'empty'
                return validation_info
            
            # 3. 손상 패턴 체크
            for pattern in self.corruption_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    validation_info['issues'].append(f'손상 패턴 발견: {pattern}')
                    validation_info['status'] = 'corrupted'
                    break
            
            # 4. 유효한 HTML 콘텐츠 패턴 체크
            valid_pattern_count = 0
            for pattern in self.valid_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    valid_pattern_count += 1
            
            if valid_pattern_count == 0:
                validation_info['issues'].append('유효한 HTML 패턴이 없음')
                validation_info['status'] = 'suspicious'
            elif valid_pattern_count < 2:
                validation_info['issues'].append('HTML 패턴이 부족함')
                if validation_info['status'] == 'valid':
                    validation_info['status'] = 'suspicious'
            
            # 5. 이미지 링크 체크
            img_links = re.findall(r'src="([^"]*\.(jpg|jpeg|png|gif)[^"]*)"', content, re.IGNORECASE)
            validation_info['image_count'] = len(img_links)
            
            if len(img_links) == 0:
                validation_info['issues'].append('이미지 링크가 없음')
                if validation_info['status'] == 'valid':
                    validation_info['status'] = 'suspicious'
            
            # 6. 중복 내용 체크 (같은 내용이 반복되는 경우)
            lines = content.split('\n')
            unique_lines = set(line.strip() for line in lines if line.strip())
            if len(lines) > 5 and len(unique_lines) < 3:
                validation_info['issues'].append('중복 내용 의심')
                validation_info['status'] = 'suspicious'
            
            return validation_info
            
        except Exception as e:
            return {
                'product_no': txt_file.stem,
                'file_size': 0,
                'content_length': 0,
                'issues': [f'파일 읽기 실패: {e}'],
                'status': 'corrupted'
            }
    
    def validate_all_files(self):
        """모든 TXT 파일 검증"""
        print("🔍 temp_txt 파일 무결성 검증 시작")
        print("=" * 60)
        
        if not self.temp_txt_path.exists():
            print(f"❌ temp_txt 폴더가 없습니다: {self.temp_txt_path}")
            return
        
        # CSV에서 예상 파일 목록 가져오기
        csv_file = self.find_csv_file()
        if csv_file:
            expected_products = self.get_product_list_from_csv()
            expected_files = {p['no'] for p in expected_products}
            print(f"📋 CSV 기준 예상 파일: {len(expected_files)}개")
        else:
            expected_files = set()
        
        # 실제 파일 목록
        actual_files = list(self.temp_txt_path.glob("*.txt"))
        actual_product_nos = {f.stem for f in actual_files}
        
        print(f"📁 실제 TXT 파일: {len(actual_files)}개")
        print("-" * 40)
        
        self.validation_results['total_files'] = len(actual_files)
        
        # 누락된 파일 체크
        if expected_files:
            missing_files = expected_files - actual_product_nos
            if missing_files:
                self.validation_results['missing_files'] = list(missing_files)
                print(f"❌ 누락된 파일: {len(missing_files)}개")
                for missing in sorted(missing_files)[:5]:  # 처음 5개만 표시
                    print(f"   {missing}.txt")
                if len(missing_files) > 5:
                    print(f"   ... 및 {len(missing_files)-5}개 더")
        
        # 각 파일 검증
        validation_count = {'valid': 0, 'corrupted': 0, 'empty': 0, 'suspicious': 0}
        
        for txt_file in sorted(actual_files):
            validation_info = self.validate_single_file(txt_file)
            status = validation_info['status']
            validation_count[status] += 1
            
            # 결과별로 분류
            if status == 'valid':
                self.validation_results['valid_files'].append(validation_info)
            elif status == 'corrupted':
                self.validation_results['corrupted_files'].append(validation_info)
                print(f"❌ 손상: {validation_info['product_no']}.txt - {', '.join(validation_info['issues'])}")
            elif status == 'empty':
                self.validation_results['empty_files'].append(validation_info)
                print(f"⚠️  빈 파일: {validation_info['product_no']}.txt")
            elif status == 'suspicious':
                self.validation_results['suspicious_files'].append(validation_info)
                print(f"⚠️  의심: {validation_info['product_no']}.txt - {', '.join(validation_info['issues'])}")
        
        # 검증 결과 요약
        print("\n" + "=" * 60)
        print("📊 검증 결과")
        print("=" * 60)
        print(f"✅ 정상 파일: {validation_count['valid']}개")
        print(f"❌ 손상 파일: {validation_count['corrupted']}개")
        print(f"⚪ 빈 파일: {validation_count['empty']}개")
        print(f"⚠️  의심 파일: {validation_count['suspicious']}개")
        
        problem_count = validation_count['corrupted'] + validation_count['empty'] + validation_count['suspicious']
        if expected_files:
            print(f"📋 누락 파일: {len(self.validation_results['missing_files'])}개")
            problem_count += len(self.validation_results['missing_files'])
        
        if problem_count == 0:
            print("\n🎉 모든 파일이 정상입니다!")
        else:
            print(f"\n⚠️  총 {problem_count}개 파일에 문제가 있습니다.")
            print("재다운로드를 권장합니다.")
        
        return problem_count
    
    def generate_problem_file_list(self):
        """문제가 있는 파일 목록 생성"""
        problem_files = []
        
        # 손상된 파일들
        for file_info in self.validation_results['corrupted_files']:
            problem_files.append({
                'product_no': file_info['product_no'],
                'issue': 'CORRUPTED',
                'details': file_info['issues']
            })
        
        # 빈 파일들
        for file_info in self.validation_results['empty_files']:
            problem_files.append({
                'product_no': file_info['product_no'],
                'issue': 'EMPTY',
                'details': file_info['issues']
            })
        
        # 의심 파일들
        for file_info in self.validation_results['suspicious_files']:
            problem_files.append({
                'product_no': file_info['product_no'],
                'issue': 'SUSPICIOUS',
                'details': file_info['issues']
            })
        
        # 누락된 파일들
        for product_no in self.validation_results['missing_files']:
            problem_files.append({
                'product_no': product_no,
                'issue': 'MISSING',
                'details': ['파일이 존재하지 않음']
            })
        
        return problem_files
    
    def create_redownload_script(self, problem_files):
        """재다운로드 스크립트 생성"""
        if not problem_files:
            print("재다운로드할 파일이 없습니다.")
            return
        
        # 재다운로드 대상 파일 목록 저장
        redownload_list_path = Path("reports/redownload_list.json")
        redownload_list_path.parent.mkdir(exist_ok=True)
        
        redownload_data = {
            'generated_time': datetime.now().isoformat(),
            'total_files': len(problem_files),
            'problem_files': problem_files,
            'csv_file': str(self.csv_path) if self.csv_path else None
        }
        
        with open(redownload_list_path, 'w', encoding='utf-8') as f:
            json.dump(redownload_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 재다운로드 목록 저장: {redownload_list_path}")
        
        # 재다운로드 가이드 스크립트 생성
        guide_script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자동 생성된 재다운로드 가이드
문제가 있는 {len(problem_files)}개 파일의 재다운로드 방법
"""

problem_files = {problem_files}

print("🔄 재다운로드 대상 파일들:")
print("=" * 50)

for i, file_info in enumerate(problem_files, 1):
    product_no = file_info['product_no']
    issue = file_info['issue']
    details = ', '.join(file_info['details'])
    
    print(f"{{i:3d}}. {{product_no}}.txt - {{issue}}")
    print(f"     문제: {{details}}")

print("\\n💡 재다운로드 방법:")
print("1. Cafe24 관리자 페이지 로그인")
print("2. 상품관리 > 상품조회")
print("3. 위 상품번호들의 상세설명 HTML 복사")
print("4. html/temp_txt/ 폴더에 XXX.txt로 저장")
print("5. scripts/apply_txt_to_html.py 실행")
'''
        
        guide_path = Path("scripts/redownload_guide.py")
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_script)
        
        print(f"📝 재다운로드 가이드: {guide_path}")
    
    def generate_validation_report(self):
        """검증 리포트 생성"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = Path(f"reports/txt_validation_report_{timestamp}.json")
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)
        
        # 텍스트 리포트도 생성
        txt_report_path = report_path.with_suffix('.txt')
        with open(txt_report_path, 'w', encoding='utf-8') as f:
            f.write("temp_txt 파일 무결성 검증 리포트\\n")
            f.write("=" * 50 + "\\n\\n")
            f.write(f"검증 시간: {self.validation_results['validation_time']}\\n")
            f.write(f"총 파일 수: {self.validation_results['total_files']}\\n\\n")
            
            f.write(f"✅ 정상 파일: {len(self.validation_results['valid_files'])}개\\n")
            f.write(f"❌ 손상 파일: {len(self.validation_results['corrupted_files'])}개\\n")
            f.write(f"⚪ 빈 파일: {len(self.validation_results['empty_files'])}개\\n")
            f.write(f"⚠️  의심 파일: {len(self.validation_results['suspicious_files'])}개\\n")
            f.write(f"📋 누락 파일: {len(self.validation_results['missing_files'])}개\\n\\n")
            
            if self.validation_results['corrupted_files']:
                f.write("손상된 파일 상세:\\n")
                for file_info in self.validation_results['corrupted_files']:
                    f.write(f"  {file_info['product_no']}.txt - {', '.join(file_info['issues'])}\\n")
                f.write("\\n")
            
            if self.validation_results['missing_files']:
                f.write("누락된 파일:\\n")
                for product_no in sorted(self.validation_results['missing_files']):
                    f.write(f"  {product_no}.txt\\n")
        
        print(f"📋 상세 리포트: {report_path}")
        print(f"📋 텍스트 리포트: {txt_report_path}")
        
        return report_path

def main():
    """메인 실행 함수"""
    validator = TxtFileValidator()
    
    # 검증 실행
    problem_count = validator.validate_all_files()
    
    # 리포트 생성
    validator.generate_validation_report()
    
    if problem_count > 0:
        # 문제 파일 목록 생성
        problem_files = validator.generate_problem_file_list()
        
        # 재다운로드 스크립트 생성
        validator.create_redownload_script(problem_files)
        
        print("\\n💡 다음 단계:")
        print("1. scripts/redownload_guide.py 확인")
        print("2. 문제 파일들 수동 재다운로드")
        print("3. 재검증 실행")
    
    return problem_count == 0

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎉 모든 temp_txt 파일이 정상입니다!")
    else:
        print("\\n⚠️  일부 파일에 문제가 있습니다. 재다운로드를 진행하세요.")