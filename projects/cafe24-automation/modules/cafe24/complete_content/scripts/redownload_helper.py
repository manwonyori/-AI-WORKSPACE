#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import io

# Windows 콘솔 UTF-8 설정
if os.name == 'nt':
    import codecs
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

"""
실패한 TXT 파일만 재다운로드하는 도우미
손상된 파일들의 상품번호를 보여주고 재다운로드 가이드 제공
"""
import json
import csv
from pathlib import Path
from datetime import datetime
import webbrowser

class RedownloadHelper:
    def __init__(self):
        self.reports_path = Path("reports")
        self.csv_path = Path("../download")
        self.temp_txt_path = Path("html/temp_txt")
        self.backup_path = Path("backup/txt_backup")
        
        # 최신 CSV 파일 찾기
        self.csv_file = self.find_latest_csv()
        
        # 재다운로드 목록 로드
        self.load_problem_files()
        
    def find_latest_csv(self):
        """최신 CSV 파일 찾기"""
        csv_files = list(self.csv_path.glob("manwonyori_*.csv"))
        if csv_files:
            return sorted(csv_files)[-1]
        return None
    
    def load_problem_files(self):
        """문제 파일 목록 로드"""
        redownload_file = self.reports_path / "redownload_list.json"
        
        if not redownload_file.exists():
            print("❌ 재다운로드 목록이 없습니다.")
            print("먼저 '4. TXT 검증'을 실행하세요.")
            return False
        
        with open(redownload_file, 'r', encoding='utf-8') as f:
            self.redownload_data = json.load(f)
        
        return True
    
    def get_product_info(self, product_no):
        """CSV에서 상품 정보 가져오기"""
        if not self.csv_file:
            return None
        
        with open(self.csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('상품번호') == product_no:
                    return {
                        'product_no': product_no,
                        'product_name': row.get('상품명', ''),
                        'brand': self.extract_brand(row.get('상품명', '')),
                        'supplier_product': row.get('공급사 상품명', '')
                    }
        return None
    
    def extract_brand(self, product_name):
        """상품명에서 브랜드 추출"""
        import re
        match = re.search(r'\[(.*?)\]', product_name)
        if match:
            return match.group(1)
        return "기타"
    
    def show_problem_summary(self):
        """문제 파일 요약 표시"""
        print("\n" + "="*60)
        print("📋 재다운로드가 필요한 파일 목록")
        print("="*60)
        
        if not hasattr(self, 'redownload_data'):
            return
        
        problem_files = self.redownload_data.get('problem_files', [])
        
        # 문제 유형별로 분류
        corrupted = []
        suspicious = []
        
        for file_info in problem_files:
            if file_info['issue'] == 'CORRUPTED':
                corrupted.append(file_info)
            elif file_info['issue'] == 'SUSPICIOUS':
                suspicious.append(file_info)
        
        # 심각한 손상 파일 (404 에러 등)
        if corrupted:
            print(f"\n🔴 심각한 손상 파일 ({len(corrupted)}개) - 즉시 재다운로드 필요:")
            print("-" * 40)
            for idx, file_info in enumerate(corrupted, 1):
                product_no = file_info['product_no']
                product_info = self.get_product_info(product_no)
                
                if product_info:
                    print(f"{idx:3}. 상품번호 {product_no}: [{product_info['brand']}] {product_info['product_name'][:30]}")
                else:
                    print(f"{idx:3}. 상품번호 {product_no}: (상품 정보 없음)")
                
                for detail in file_info['details']:
                    print(f"      - {detail}")
        
        # 의심스러운 파일 (이미지 없음 등)
        if suspicious:
            print(f"\n🟡 의심스러운 파일 ({len(suspicious)}개) - 확인 후 재다운로드:")
            print("-" * 40)
            
            # 너무 많으면 처음 10개만 표시
            display_count = min(10, len(suspicious))
            for idx, file_info in enumerate(suspicious[:display_count], 1):
                product_no = file_info['product_no']
                product_info = self.get_product_info(product_no)
                
                if product_info:
                    print(f"{idx:3}. 상품번호 {product_no}: [{product_info['brand']}] {product_info['product_name'][:30]}")
                else:
                    print(f"{idx:3}. 상품번호 {product_no}")
            
            if len(suspicious) > display_count:
                print(f"      ... 외 {len(suspicious) - display_count}개 더 있음")
        
        print("\n" + "="*60)
        print(f"📊 총 {len(problem_files)}개 파일 재다운로드 필요")
        print("="*60)
    
    def generate_download_guide(self):
        """재다운로드 가이드 생성"""
        print("\n📖 재다운로드 가이드")
        print("="*60)
        
        print("\n방법 1: Cafe24 관리자에서 수동 다운로드")
        print("-" * 40)
        print("1. Cafe24 관리자 페이지 접속")
        print("2. 상품관리 > 상품조회")
        print("3. 상품번호로 검색")
        print("4. 상품 수정 페이지 진입")
        print("5. 상세설명 HTML 소스 복사")
        print("6. html/temp_txt/상품번호.txt로 저장")
        print()
        
        print("\n방법 2: 상품번호 목록으로 일괄 처리")
        print("-" * 40)
        
        # 상품번호 목록 생성
        if hasattr(self, 'redownload_data'):
            problem_files = self.redownload_data.get('problem_files', [])
            
            # 심각한 손상 파일만 추출
            corrupted_nos = [f['product_no'] for f in problem_files if f['issue'] == 'CORRUPTED']
            
            if corrupted_nos:
                print("🔴 우선 재다운로드할 상품번호:")
                print(", ".join(corrupted_nos))
                
                # 클립보드 복사용 파일 생성
                clipboard_file = self.reports_path / "redownload_product_numbers.txt"
                with open(clipboard_file, 'w', encoding='utf-8') as f:
                    f.write("\n".join(corrupted_nos))
                
                print(f"\n💾 상품번호 목록 저장: {clipboard_file}")
        
        print("\n" + "="*60)
    
    def open_cafe24_admin(self):
        """Cafe24 관리자 페이지 열기"""
        response = input("\n🌐 Cafe24 관리자 페이지를 열까요? (Y/N): ").strip().upper()
        if response == 'Y':
            url = "https://eclogin.cafe24.com/Shop/?mall_id=manwonyori"
            webbrowser.open(url)
            print("✅ Cafe24 관리자 페이지를 열었습니다.")
            print("💡 로그인 후: 상품관리 > 상품조회/수정으로 이동하세요.")
    
    def create_download_batch(self):
        """재다운로드용 배치 스크립트 생성"""
        print("\n📝 재다운로드 도우미 스크립트 생성")
        print("="*60)
        
        if not hasattr(self, 'redownload_data'):
            return
        
        problem_files = self.redownload_data.get('problem_files', [])
        corrupted = [f for f in problem_files if f['issue'] == 'CORRUPTED']
        
        if not corrupted:
            print("심각한 손상 파일이 없습니다.")
            return
        
        # PowerShell 스크립트 생성
        ps_script = self.reports_path / "redownload_helper.ps1"
        
        script_content = """# Cafe24 재다운로드 도우미
# 생성일: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """

$products = @(
"""
        
        for file_info in corrupted:
            product_no = file_info['product_no']
            product_info = self.get_product_info(product_no)
            if product_info:
                name = product_info['product_name'].replace('"', '""')
                script_content += f'    @{{No="{product_no}"; Name="{name}"}},\n'
            else:
                script_content += f'    @{{No="{product_no}"; Name="정보없음"}},\n'
        
        script_content = script_content.rstrip(',\n') + """
)

Write-Host "======================================"
Write-Host "   Cafe24 재다운로드 도우미"
Write-Host "======================================"
Write-Host ""
Write-Host "재다운로드할 상품 목록:"
Write-Host ""

foreach ($product in $products) {
    Write-Host ("상품번호: " + $product.No + " - " + $product.Name)
}

Write-Host ""
Write-Host "위 상품들을 Cafe24 관리자에서 다운로드하세요."
Write-Host ""
Write-Host "다운로드 방법:"
Write-Host "1. 상품번호로 검색"
Write-Host "2. 상품 수정 페이지 진입"
Write-Host "3. 상세설명 HTML 복사"
Write-Host "4. html/temp_txt/상품번호.txt로 저장"
Write-Host ""

$openBrowser = Read-Host "Cafe24 관리자를 열까요? (Y/N)"
if ($openBrowser -eq 'Y') {
    Start-Process "https://eclogin.cafe24.com/Shop/?mall_id=manwonyori"
    Write-Host "로그인 후: 상품관리 > 상품조회/수정으로 이동하세요."
}

Write-Host ""
Write-Host "완료되면 Enter를 누르세요..."
Read-Host
"""
        
        with open(ps_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ PowerShell 스크립트 생성: {ps_script}")
        
        # 실행용 배치 파일
        batch_file = self.reports_path / "run_redownload_helper.bat"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write('@echo off\n')
            f.write('chcp 65001 > nul\n')
            f.write('powershell -ExecutionPolicy Bypass -File "%~dp0redownload_helper.ps1"\n')
            f.write('pause\n')
        
        print(f"✅ 실행 파일 생성: {batch_file}")
        print("\n💡 실행 방법: reports\\run_redownload_helper.bat 더블클릭")
    
    def check_fixed_files(self):
        """수정된 파일 확인"""
        print("\n🔍 재다운로드 상태 확인")
        print("="*60)
        
        if not hasattr(self, 'redownload_data'):
            return
        
        problem_files = self.redownload_data.get('problem_files', [])
        
        fixed_count = 0
        still_problem = []
        
        for file_info in problem_files:
            product_no = file_info['product_no']
            txt_file = self.temp_txt_path / f"{product_no}.txt"
            
            if txt_file.exists():
                # 파일 크기 체크
                size = txt_file.stat().st_size
                if size > 100:  # 100바이트 이상이면 내용이 있다고 판단
                    # 간단한 내용 체크
                    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(500)
                        if 'error' not in content.lower() and '404' not in content:
                            fixed_count += 1
                        else:
                            still_problem.append(product_no)
                else:
                    still_problem.append(product_no)
            else:
                still_problem.append(product_no)
        
        print(f"✅ 수정된 파일: {fixed_count}개")
        print(f"❌ 여전히 문제: {len(still_problem)}개")
        
        if still_problem[:10]:  # 처음 10개만 표시
            print(f"\n아직 재다운로드 필요: {', '.join(still_problem[:10])}")
            if len(still_problem) > 10:
                print(f"... 외 {len(still_problem)-10}개")
    
    def run(self):
        """메인 실행"""
        print("\n🔧 재다운로드 도우미")
        print("="*60)
        
        if not self.load_problem_files():
            return
        
        while True:
            print("\n메뉴:")
            print("1. 문제 파일 요약 보기")
            print("2. 재다운로드 가이드")
            print("3. Cafe24 관리자 열기")
            print("4. 재다운로드 스크립트 생성")
            print("5. 수정 상태 확인")
            print("0. 종료")
            
            choice = input("\n선택: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.show_problem_summary()
            elif choice == '2':
                self.generate_download_guide()
            elif choice == '3':
                self.open_cafe24_admin()
            elif choice == '4':
                self.create_download_batch()
            elif choice == '5':
                self.check_fixed_files()
            else:
                print("잘못된 선택입니다.")
            
            if choice != '0':
                input("\nEnter를 눌러 계속...")

def main():
    """메인 함수"""
    helper = RedownloadHelper()
    helper.run()

if __name__ == "__main__":
    main()