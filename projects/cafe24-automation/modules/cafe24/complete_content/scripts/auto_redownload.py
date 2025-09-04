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
실패한 파일 자동 재다운로드
기존 html_downloader.py와 연동하여 실패한 파일만 다운로드
"""
import json
import csv
import time
import requests
from pathlib import Path
from datetime import datetime
import subprocess

class AutoRedownloader:
    def __init__(self):
        self.reports_path = Path("reports")
        self.temp_txt_path = Path("html/temp_txt")
        self.csv_path = Path("../download")
        self.failed_products = []
        
        # 재다운로드 목록 로드
        self.load_failed_list()
        
    def load_failed_list(self):
        """실패 파일 목록 로드"""
        redownload_file = self.reports_path / "redownload_list.json"
        
        if not redownload_file.exists():
            print("❌ 재다운로드 목록이 없습니다.")
            print("먼저 TXT 검증을 실행하세요.")
            return False
        
        with open(redownload_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 심각한 손상 파일만 추출 (404 에러 등)
        problem_files = data.get('problem_files', [])
        self.failed_products = [
            f['product_no'] for f in problem_files 
            if f['issue'] == 'CORRUPTED'
        ]
        
        print(f"📋 재다운로드 대상: {len(self.failed_products)}개 파일")
        print(f"   상품번호: {', '.join(self.failed_products)}")
        
        return True
    
    def find_latest_csv(self):
        """최신 CSV 파일 찾기"""
        csv_files = list(self.csv_path.glob("manwonyori_*.csv"))
        if csv_files:
            return sorted(csv_files)[-1]
        return None
    
    def get_product_info(self, product_no):
        """CSV에서 상품 정보 가져오기"""
        csv_file = self.find_latest_csv()
        if not csv_file:
            return None
        
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('상품번호') == product_no:
                    return row
        return None
    
    def download_with_api(self, product_no):
        """Cafe24 API로 다운로드 시도"""
        print(f"  API 다운로드 시도: 상품번호 {product_no}")
        
        # OAuth 토큰 파일 확인
        token_file = Path("../SuperClaude/Core/cafe24_tokens.json")
        if not token_file.exists():
            return False
        
        try:
            with open(token_file, 'r', encoding='utf-8') as f:
                tokens = json.load(f)
            
            access_token = tokens.get('access_token')
            if not access_token:
                return False
            
            # API 호출
            mall_id = "manwonyori"
            url = f"https://{mall_id}.cafe24api.com/api/v2/products/{product_no}"
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'X-Cafe24-Api-Version': '2024-06-01'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                product = data.get('product', {})
                
                # 상세설명 추출
                description = product.get('description', '')
                
                if description:
                    # TXT 파일로 저장
                    txt_file = self.temp_txt_path / f"{product_no}.txt"
                    with open(txt_file, 'w', encoding='utf-8') as f:
                        f.write(description)
                    
                    print(f"    ✅ API 다운로드 성공: {txt_file.name}")
                    return True
            
        except Exception as e:
            print(f"    ❌ API 오류: {e}")
        
        return False
    
    def download_with_selenium(self, product_no):
        """Selenium으로 다운로드 (html_downloader.py 활용)"""
        print(f"  Selenium 다운로드 시도: 상품번호 {product_no}")
        
        # 임시 다운로드 목록 생성
        temp_list = self.reports_path / "temp_download_list.json"
        with open(temp_list, 'w', encoding='utf-8') as f:
            json.dump({'products': [product_no]}, f)
        
        # html_downloader.py 실행 (있다면)
        downloader_script = Path("scripts/html_downloader.py")
        if downloader_script.exists():
            try:
                # 수정된 html_downloader 호출
                result = subprocess.run(
                    [sys.executable, str(downloader_script), '--product-list', str(temp_list)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    print(f"    ✅ Selenium 다운로드 성공")
                    return True
                else:
                    print(f"    ❌ Selenium 다운로드 실패")
                    
            except subprocess.TimeoutExpired:
                print(f"    ⏱️ 다운로드 시간 초과")
            except Exception as e:
                print(f"    ❌ 실행 오류: {e}")
        
        return False
    
    def manual_download_guide(self, product_no):
        """수동 다운로드 가이드"""
        product_info = self.get_product_info(product_no)
        
        if product_info:
            product_name = product_info.get('상품명', '')
            print(f"\n📝 수동 다운로드 가이드:")
            print(f"   상품번호: {product_no}")
            print(f"   상품명: {product_name}")
        else:
            print(f"\n📝 수동 다운로드 가이드:")
            print(f"   상품번호: {product_no}")
        
        print(f"\n   1. Cafe24 관리자 접속")
        print(f"   2. 상품관리 > 상품조회")
        print(f"   3. 상품번호 {product_no} 검색")
        print(f"   4. 상세설명 HTML 복사")
        print(f"   5. html/temp_txt/{product_no}.txt로 저장")
    
    def check_download_result(self, product_no):
        """다운로드 결과 확인"""
        txt_file = self.temp_txt_path / f"{product_no}.txt"
        
        if not txt_file.exists():
            return False
        
        # 파일 크기 확인
        if txt_file.stat().st_size < 100:
            return False
        
        # 내용 확인
        with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(500)
            
            # 에러 패턴 체크
            if any(error in content.lower() for error in ['404', 'error', 'not found']):
                return False
            
            # HTML 패턴 체크
            if '<' in content and '>' in content:
                return True
        
        return False
    
    def run(self):
        """메인 실행"""
        if not self.load_failed_list():
            return
        
        if not self.failed_products:
            print("✅ 재다운로드할 파일이 없습니다.")
            return
        
        print("\n🔄 자동 재다운로드 시작")
        print("="*60)
        
        success_count = 0
        failed_list = []
        
        for idx, product_no in enumerate(self.failed_products, 1):
            print(f"\n[{idx}/{len(self.failed_products)}] 상품번호 {product_no}")
            
            # 1. API 시도
            if self.download_with_api(product_no):
                success_count += 1
                continue
            
            # 2. Selenium 시도 (html_downloader.py가 있다면)
            if Path("scripts/html_downloader.py").exists():
                if self.download_with_selenium(product_no):
                    success_count += 1
                    continue
            
            # 3. 실패한 경우
            failed_list.append(product_no)
            print(f"    ⚠️ 자동 다운로드 실패 - 수동 다운로드 필요")
            
            # 잠시 대기
            time.sleep(1)
        
        # 결과 요약
        print("\n" + "="*60)
        print("📊 재다운로드 결과")
        print("="*60)
        print(f"✅ 성공: {success_count}개")
        print(f"❌ 실패: {len(failed_list)}개")
        
        if failed_list:
            print(f"\n수동 다운로드 필요: {', '.join(failed_list)}")
            
            # 수동 다운로드 가이드 제공
            response = input("\n수동 다운로드 가이드를 보시겠습니까? (Y/N): ").strip().upper()
            if response == 'Y':
                for product_no in failed_list:
                    self.manual_download_guide(product_no)
                    print("-"*40)
            
            # Cafe24 관리자 열기
            response = input("\nCafe24 관리자를 열까요? (Y/N): ").strip().upper()
            if response == 'Y':
                import webbrowser
                webbrowser.open("https://eclogin.cafe24.com/Shop/?mall_id=manwonyori")
        
        # 재검증 권장
        if success_count > 0:
            print("\n💡 다운로드 완료 후 TXT 검증을 다시 실행하세요.")

def main():
    """메인 함수"""
    downloader = AutoRedownloader()
    downloader.run()

if __name__ == "__main__":
    main()