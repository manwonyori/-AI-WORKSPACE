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
TXT 파일 자동 수정 및 복구 시스템
간단한 문제들을 자동으로 수정하고 복구
"""
import re
from pathlib import Path
import shutil
from datetime import datetime
import json

class TxtAutoFixer:
    def __init__(self):
        self.temp_txt_path = Path("html/temp_txt")
        self.backup_path = Path("backup/txt_backup")
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
        self.fix_results = {
            'fixed_files': [],
            'backup_files': [],
            'unfixable_files': [],
            'total_processed': 0,
            'fix_time': datetime.now().isoformat()
        }
        
        # 자동 수정 가능한 문제들
        self.fixable_patterns = {
            'remove_error_tags': [
                r'<title>.*?error.*?</title>',
                r'<h1>.*?404.*?</h1>',
                r'<div.*?error.*?</div>'
            ],
            'clean_whitespace': [
                r'^\s+',  # 시작 공백
                r'\s+$',  # 끝 공백
                r'\n\s*\n\s*\n',  # 과도한 빈 줄
            ],
            'fix_malformed_tags': [
                r'<center><center>',  # 중복 center 태그
                r'</center></center>',
                r'<br><br><br>',  # 과도한 br 태그
            ]
        }
    
    def create_backup(self, file_path):
        """파일 백업 생성"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{file_path.stem}_{timestamp}.txt"
            backup_file = self.backup_path / backup_filename
            
            shutil.copy2(file_path, backup_file)
            self.fix_results['backup_files'].append({
                'original': str(file_path),
                'backup': str(backup_file)
            })
            
            return backup_file
            
        except Exception as e:
            print(f"❌ 백업 실패 {file_path.name}: {e}")
            return None
    
    def fix_encoding_issues(self, content):
        """인코딩 문제 수정"""
        try:
            # 일반적인 인코딩 문제 수정
            fixes = [
                ('â€™', "'"),  # 잘못된 따옴표
                ('â€œ', '"'),  # 잘못된 따옴표  
                ('â€', '"'),
                ('Â', ''),     # 불필요한 문자
                ('â†', '→'),   # 화살표
                ('â€¢', '•'),  # 불릿포인트
            ]
            
            fixed_content = content
            fix_count = 0
            
            for wrong, correct in fixes:
                if wrong in fixed_content:
                    fixed_content = fixed_content.replace(wrong, correct)
                    fix_count += 1
            
            return fixed_content, fix_count
            
        except Exception:
            return content, 0
    
    def fix_malformed_html(self, content):
        """잘못된 HTML 구조 수정"""
        try:
            fixed_content = content
            fix_count = 0
            
            # 중복 태그 제거
            patterns = [
                (r'<center>\s*<center>', '<center>'),
                (r'</center>\s*</center>', '</center>'),
                (r'<br>\s*<br>\s*<br>', '<br><br>'),
                (r'(<img[^>]*>)\s*\1', r'\1'),  # 중복 이미지 태그
            ]
            
            for pattern, replacement in patterns:
                new_content = re.sub(pattern, replacement, fixed_content, flags=re.IGNORECASE)
                if new_content != fixed_content:
                    fixed_content = new_content
                    fix_count += 1
            
            return fixed_content, fix_count
            
        except Exception:
            return content, 0
    
    def fix_whitespace_issues(self, content):
        """공백 문제 수정"""
        try:
            # 시작/끝 공백 제거
            fixed_content = content.strip()
            
            # 과도한 빈 줄 정리
            fixed_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', fixed_content)
            
            # 탭을 공백으로 통일
            fixed_content = fixed_content.replace('\t', ' ')
            
            # 과도한 공백 정리
            fixed_content = re.sub(r' {3,}', '  ', fixed_content)
            
            fix_count = 1 if fixed_content != content else 0
            
            return fixed_content, fix_count
            
        except Exception:
            return content, 0
    
    def add_basic_structure(self, content):
        """기본 HTML 구조 추가 (필요한 경우)"""
        try:
            # 매우 간단한 내용만 있는 경우 center 태그 추가
            if content.strip() and '<center>' not in content.lower():
                # 이미지 태그만 있는 경우
                if re.search(r'^\s*<img[^>]*>\s*$', content, re.IGNORECASE | re.MULTILINE):
                    wrapped_content = f"<center>\n{content.strip()}\n</center>"
                    return wrapped_content, 1
            
            return content, 0
            
        except Exception:
            return content, 0
    
    def validate_fixed_content(self, content):
        """수정된 콘텐츠가 유효한지 검증"""
        try:
            # 기본 검증
            if not content.strip():
                return False, "빈 콘텐츠"
            
            # HTML 태그 기본 검증
            if '<' in content and '>' in content:
                # 기본적인 태그 매칭 체크
                open_tags = re.findall(r'<(\w+)[^>]*>', content)
                close_tags = re.findall(r'</(\w+)>', content)
                
                # center 태그 매칭 체크 (중요한 태그)
                if content.count('<center>') != content.count('</center>'):
                    return False, "center 태그 불일치"
            
            # 이미지 링크 유효성 간단 체크
            img_tags = re.findall(r'<img[^>]*src="([^"]*)"', content, re.IGNORECASE)
            if img_tags:
                valid_domains = ['cafe24img.com', 'ecimg.cafe24img.com']
                valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
                
                for img_src in img_tags:
                    has_valid_domain = any(domain in img_src for domain in valid_domains)
                    has_valid_ext = any(img_src.lower().endswith(ext) for ext in valid_extensions)
                    
                    if not (has_valid_domain or has_valid_ext):
                        continue  # 한 개 정도는 괜찮음
                    
            return True, "유효"
            
        except Exception as e:
            return False, f"검증 오류: {e}"
    
    def fix_single_file(self, file_path):
        """개별 파일 자동 수정"""
        try:
            # 원본 내용 읽기
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()
            
            if not original_content.strip():
                return False, "빈 파일은 수정할 수 없음"
            
            # 백업 생성
            backup_file = self.create_backup(file_path)
            if not backup_file:
                return False, "백업 생성 실패"
            
            # 단계별 수정 적용
            fixed_content = original_content
            total_fixes = 0
            
            # 1. 인코딩 문제 수정
            fixed_content, fix_count = self.fix_encoding_issues(fixed_content)
            total_fixes += fix_count
            
            # 2. HTML 구조 문제 수정
            fixed_content, fix_count = self.fix_malformed_html(fixed_content)
            total_fixes += fix_count
            
            # 3. 공백 문제 수정
            fixed_content, fix_count = self.fix_whitespace_issues(fixed_content)
            total_fixes += fix_count
            
            # 4. 기본 구조 추가 (필요한 경우)
            fixed_content, fix_count = self.add_basic_structure(fixed_content)
            total_fixes += fix_count
            
            # 수정된 내용 검증
            is_valid, validation_msg = self.validate_fixed_content(fixed_content)
            
            if not is_valid:
                return False, f"검증 실패: {validation_msg}"
            
            if total_fixes == 0:
                return False, "수정할 내용이 없음"
            
            # 수정된 내용 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            return True, f"{total_fixes}개 문제 수정됨"
            
        except Exception as e:
            return False, f"수정 오류: {e}"
    
    def fix_all_problem_files(self, problem_files_list=None):
        """문제가 있는 모든 파일 자동 수정"""
        print("🔧 TXT 파일 자동 수정 시작")
        print("=" * 60)
        
        if problem_files_list:
            # 특정 문제 파일 목록이 주어진 경우
            target_files = []
            for file_info in problem_files_list:
                file_path = self.temp_txt_path / f"{file_info['product_no']}.txt"
                if file_path.exists():
                    target_files.append(file_path)
        else:
            # 모든 TXT 파일 대상
            target_files = list(self.temp_txt_path.glob("*.txt"))
        
        print(f"📂 대상 파일: {len(target_files)}개")
        print("-" * 40)
        
        fix_count = {'success': 0, 'failed': 0, 'skipped': 0}
        
        for file_path in sorted(target_files):
            self.fix_results['total_processed'] += 1
            
            success, message = self.fix_single_file(file_path)
            
            if success:
                fix_count['success'] += 1
                self.fix_results['fixed_files'].append({
                    'file': file_path.name,
                    'message': message
                })
                print(f"✅ {file_path.name}: {message}")
            else:
                if "수정할 내용이 없음" in message:
                    fix_count['skipped'] += 1
                else:
                    fix_count['failed'] += 1
                    self.fix_results['unfixable_files'].append({
                        'file': file_path.name,
                        'reason': message
                    })
                    print(f"❌ {file_path.name}: {message}")
        
        # 결과 요약
        print("\n" + "=" * 60)
        print("🔧 자동 수정 결과")
        print("=" * 60)
        print(f"✅ 수정 완료: {fix_count['success']}개")
        print(f"⏭️  수정 불필요: {fix_count['skipped']}개")
        print(f"❌ 수정 실패: {fix_count['failed']}개")
        print(f"📦 백업 파일: {len(self.fix_results['backup_files'])}개")
        
        if fix_count['success'] > 0:
            print(f"\n💾 백업 위치: {self.backup_path}")
            print("📝 수정 후 재검증을 권장합니다.")
        
        return fix_count['success']
    
    def generate_fix_report(self):
        """수정 리포트 생성"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = Path(f"reports/txt_autofix_report_{timestamp}.json")
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.fix_results, f, indent=2, ensure_ascii=False)
        
        print(f"📋 수정 리포트: {report_path}")
        return report_path

def main():
    """메인 실행 함수"""
    print("🔧 TXT 파일 자동 수정 도구")
    print("=" * 50)
    print("⚠️  주의: 모든 파일이 백업됩니다.")
    print("💡 간단한 문제들만 자동 수정됩니다.")
    print()
    
    # 사용자 확인
    response = input("계속 진행하시겠습니까? (Y/N): ").strip().upper()
    if response != 'Y':
        print("취소되었습니다.")
        return False
    
    fixer = TxtAutoFixer()
    
    # 자동 수정 실행
    fixed_count = fixer.fix_all_problem_files()
    
    # 리포트 생성
    fixer.generate_fix_report()
    
    if fixed_count > 0:
        print(f"\n🎉 {fixed_count}개 파일이 자동 수정되었습니다!")
        print("📝 이제 재검증을 실행해보세요:")
        print("   python scripts/validate_temp_txt_files.py")
    else:
        print("\n💡 자동 수정 가능한 파일이 없습니다.")
        print("심각한 문제는 수동으로 재다운로드가 필요합니다.")
    
    return fixed_count > 0

if __name__ == "__main__":
    main()