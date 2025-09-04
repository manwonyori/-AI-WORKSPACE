#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
송장 마스터 시스템 - 모든 기능 통합
단 하나의 파일로 모든 송장 처리
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import re
import sys

class InvoiceMaster:
    """송장 처리 올인원 시스템"""
    
    def __init__(self):
        self.base_path = Path("D:/주문취합/주문_배송")
        self.all_items = {}  # 전체 데이터
        self.processed_items = set()  # 처리 완료
        
        # 카페24 배송업체 번호
        self.DELIVERY_MAPPING = {
            '우체국택배': 3, '우체국': 3,
            '자체배송': 2,
            'CJ대한통운': 4, 'CJ': 4,
            '한진택배': 5, '한진': 5,
            '로젠택배': 7, '로젠': 7,
            '롯데택배': 33, '롯데': 33
        }
    
    def run(self, command, date=None):
        """명령 실행"""
        if not date:
            date = datetime.now().strftime("%Y%m%d")
        
        commands = {
            'vendor': self.generate_vendor_files,  # 업체별 파일 생성
            'upload': self.generate_upload_csv,    # 업로드 CSV 생성
            'check': self.check_yesterday,         # 어제 확인
            'validate': self.validate_invoices,    # 송장 검증
        }
        
        if command in commands:
            return commands[command](date)
        else:
            print(f"사용법: vendor|upload|check|validate [날짜]")
    
    def extract_vendor(self, product_name):
        """업체 추출"""
        if pd.isna(product_name):
            return '기타'
        
        match = re.search(r'\[([^\]]+)\]', str(product_name))
        if match:
            vendor = match.group(1)
            if '최씨남매' in vendor:
                return '최씨남매제조' if '제조' in vendor else '최씨남매'
            elif '모비딕' in vendor:
                return '모비딕'
            elif '인생' in vendor:
                return '인생'
            elif '반찬단지' in vendor:
                return '반찬단지'
            elif '취영루' in vendor:
                return '취영루'
            elif 'BS' in vendor.upper():
                return 'BS'
            elif '피자코리아' in vendor:
                return '피자코리아'
            return vendor
        return '기타'
    
    def generate_vendor_files(self, target_date):
        """업체별 파일 생성 (중복 제거)"""
        print(f"=== {target_date} 업체별 파일 생성 ===")
        
        # 1. 한달간 데이터 로드
        current_date = datetime.strptime(target_date, "%Y%m%d")
        for i in range(30):
            check_date = current_date - timedelta(days=i)
            date_str = check_date.strftime("%Y%m%d")
            date_folder = self.base_path / date_str
            
            if not date_folder.exists():
                continue
            
            csv_files = list(date_folder.glob("manwonyori_*.csv"))
            if csv_files:
                try:
                    df = pd.read_csv(csv_files[0], encoding='utf-8-sig')
                    for _, row in df.iterrows():
                        item_no = row.get('품목별 주문번호', '')
                        if item_no:
                            self.all_items[item_no] = {
                                'date': date_str,
                                'data': row,
                                'vendor': self.extract_vendor(row.get('주문상품명', ''))
                            }
                    print(f"  {date_str}: {len(df)}건")
                except:
                    pass
        
        # 2. 이미 처리된 것 제외
        for i in range(30):
            check_date = current_date - timedelta(days=i)
            date_str = check_date.strftime("%Y%m%d")
            invoice_folder = self.base_path / date_str / "송장"
            
            if invoice_folder.exists():
                for invoice_file in invoice_folder.glob("*.xlsx"):
                    if "upload_" not in invoice_file.name:
                        try:
                            df = pd.read_excel(invoice_file)
                            for col in ['품목별 주문번호', '개별 주문번호']:
                                if col in df.columns:
                                    for item in df[col].dropna():
                                        self.processed_items.add(str(item).strip())
                                    break
                        except:
                            pass
        
        # 3. 미처리 업체별 분류
        pending_items = {}
        for item_no, item_data in self.all_items.items():
            if item_no not in self.processed_items:
                vendor = item_data['vendor']
                if vendor not in pending_items:
                    pending_items[vendor] = []
                pending_items[vendor].append(item_data['data'])
        
        # 4. 파일 생성
        date_folder = self.base_path / target_date
        for vendor, items in pending_items.items():
            if vendor == '기타' or not items:
                continue
            
            df_vendor = pd.DataFrame(items)
            
            if vendor == '인생':
                # 인생 특별 처리
                df_insaeng = pd.DataFrame()
                df_insaeng['쇼핑몰명'] = df_vendor['쇼핑몰']
                df_insaeng['쇼핑몰아이디'] = df_vendor['쇼핑몰번호']
                df_insaeng['주문번호'] = df_vendor['주문번호']
                df_insaeng['품목별 주문번호'] = df_vendor['품목별 주문번호']
                df_insaeng['송장번호'] = ''
                df_insaeng['택배사'] = ''
                df_insaeng['받는분성함'] = df_vendor['수령인']
                df_insaeng['받는분주소(전체, 상세)'] = df_vendor['수령인 주소'] + ' ' + df_vendor['수령인 상세 주소']
                df_insaeng['받는분전화번호'] = df_vendor['수령인 휴대전화']
                df_insaeng['품목명'] = df_vendor['주문상품명(옵션포함)'].fillna(df_vendor['주문상품명'])
                df_insaeng['상품명'] = ''
                df_insaeng['상품수량'] = df_vendor['수량']
                df_insaeng['배송메시지1'] = df_vendor['배송메시지']
                df_insaeng['보내는분성함'] = '만원요리'
                df_insaeng['보내는분주소(전체, 상세)'] = ''
                df_insaeng['보내는분전화번호'] = ''
                
                filename = f"[인생]_만원요리_인생_{target_date}_미처리.xlsx"
                df_insaeng.to_excel(date_folder / filename, index=False)
            else:
                filename = f"만원요리_{vendor}_{target_date}_미처리.xlsx"
                df_vendor.to_excel(date_folder / filename, index=False)
            
            print(f"생성: {filename} ({len(items)}건)")
        
        total = sum(len(items) for items in pending_items.values())
        print(f"총 미처리: {total}건")
    
    def generate_upload_csv(self, target_date):
        """업로드 CSV 생성"""
        print(f"=== {target_date} 업로드 CSV 생성 ===")
        
        invoice_folder = self.base_path / target_date / "송장"
        if not invoice_folder.exists():
            print("송장 폴더 없음")
            return
        
        upload_data = []
        
        for excel_file in invoice_folder.glob("*.xls*"):
            if any(skip in excel_file.name for skip in ["upload_", "템플릿", "test_"]):
                continue
            
            try:
                df = pd.read_excel(excel_file)
                
                # 운송장번호 컬럼 찾기
                tracking_col = None
                for col in ['운송장번호', '송장번호', '송장', '택배번호']:
                    if col in df.columns:
                        tracking_col = col
                        break
                
                if not tracking_col:
                    continue
                
                # 택배사 컬럼 찾기
                courier_col = None
                for col in ['택배사', '배송사', '운송사']:
                    if col in df.columns:
                        courier_col = col
                        break
                
                for _, row in df.iterrows():
                    tracking = row.get(tracking_col)
                    if pd.isna(tracking):
                        continue
                    
                    # 운송장번호 정규화
                    if isinstance(tracking, (int, float)):
                        tracking_str = f"{int(tracking):d}"
                    else:
                        tracking_str = str(tracking).strip()
                    
                    # 택배사 → 배송업체번호
                    courier = row.get(courier_col, '') if courier_col else ''
                    delivery_code = 3  # 기본값
                    for key, code in self.DELIVERY_MAPPING.items():
                        if key in str(courier):
                            delivery_code = code
                            break
                    
                    # 쇼핑몰번호/아이디 처리
                    mall_number = 1
                    if '쇼핑몰번호' in row:
                        mall_number = int(row.get('쇼핑몰번호', 1))
                    elif '쇼핑몰아이디' in row:
                        mall_number = int(row.get('쇼핑몰아이디', 1))
                    
                    upload_data.append({
                        '쇼핑몰': row.get('쇼핑몰', row.get('쇼핑몰명', '만원요리 최씨남매')),
                        '쇼핑몰번호': mall_number,
                        '주문번호': row.get('주문번호', ''),
                        '품목별 주문번호': row.get('품목별 주문번호', ''),
                        '운송장번호': tracking_str,
                        '배송 업체 번호': delivery_code,
                        '수량': ''
                    })
                
                print(f"  처리: {excel_file.name} ({len(df)}건)")
                
            except Exception as e:
                print(f"  오류: {excel_file.name} - {e}")
        
        if upload_data:
            upload_df = pd.DataFrame(upload_data)
            csv_file = invoice_folder / f"upload_{target_date}.csv"
            upload_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"생성: upload_{target_date}.csv ({len(upload_data)}건)")
        else:
            print("처리할 데이터 없음")
    
    def check_yesterday(self, target_date=None):
        """어제 처리 현황"""
        if not target_date:
            yesterday = datetime.now() - timedelta(days=1)
            target_date = yesterday.strftime("%Y%m%d")
        
        print(f"=== {target_date} 처리 현황 ===")
        
        date_folder = self.base_path / target_date
        if not date_folder.exists():
            print("폴더 없음")
            return
        
        # 원본 CSV
        csv_files = list(date_folder.glob("manwonyori_*.csv"))
        if csv_files:
            df = pd.read_csv(csv_files[0], encoding='utf-8-sig')
            print(f"원본: {len(df)}건")
        
        # 업체별 파일
        vendor_files = list(date_folder.glob("만원요리_*.xlsx")) + list(date_folder.glob("[인생]_*.xlsx"))
        if vendor_files:
            print(f"업체파일: {len(vendor_files)}개")
        
        # 송장
        invoice_folder = date_folder / "송장"
        if invoice_folder.exists():
            invoices = [f for f in invoice_folder.glob("*.xlsx") if "upload_" not in f.name]
            print(f"송장: {len(invoices)}개")
            
            upload_files = list(invoice_folder.glob("upload_*.csv"))
            if upload_files:
                print(f"업로드: 준비완료")
    
    def validate_invoices(self, target_date):
        """송장 검증"""
        print(f"=== {target_date} 송장 검증 ===")
        
        # 원본 데이터 로드
        valid_items = set()
        for i in range(30):
            check_date = datetime.strptime(target_date, "%Y%m%d") - timedelta(days=i)
            date_str = check_date.strftime("%Y%m%d")
            csv_files = list((self.base_path / date_str).glob("manwonyori_*.csv"))
            
            if csv_files:
                try:
                    df = pd.read_csv(csv_files[0], encoding='utf-8-sig')
                    for item in df['품목별 주문번호'].dropna():
                        valid_items.add(str(item))
                except:
                    pass
        
        print(f"유효 품목: {len(valid_items)}개")
        
        # 송장 검증
        invoice_folder = self.base_path / target_date / "송장"
        if invoice_folder.exists():
            for invoice_file in invoice_folder.glob("*.xlsx"):
                if "upload_" not in invoice_file.name:
                    try:
                        df = pd.read_excel(invoice_file)
                        invalid = []
                        for _, row in df.iterrows():
                            item_no = str(row.get('품목별 주문번호', '')).strip()
                            if item_no and item_no not in valid_items:
                                invalid.append(item_no)
                        
                        if invalid:
                            print(f"  {invoice_file.name}: {len(invalid)}개 오류")
                        else:
                            print(f"  {invoice_file.name}: OK")
                    except:
                        pass

def main():
    """메인 실행"""
    master = InvoiceMaster()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        date = sys.argv[2] if len(sys.argv) > 2 else None
        master.run(command, date)
    else:
        print("""
송장 마스터 시스템
사용법: python invoice_master.py [명령] [날짜]

명령어:
  vendor   - 업체별 파일 생성 (중복제거)
  upload   - 업로드 CSV 생성
  check    - 처리 현황 확인
  validate - 송장 검증

예시:
  python invoice_master.py vendor 20250829
  python invoice_master.py upload 20250829
  python invoice_master.py check
""")

if __name__ == "__main__":
    main()