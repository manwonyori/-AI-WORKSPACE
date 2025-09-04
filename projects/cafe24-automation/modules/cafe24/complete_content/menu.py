#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def clear_screen():
    """화면 지우기"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """메뉴 표시"""
    clear_screen()
    print("="*50)
    print("       CAFE24 콘텐츠 관리 시스템")
    print("="*50)
    print()
    print("1. 📊 현재 상태 확인")
    print("2. 📥 CSV 데이터 다운로드")
    print("3. 🌐 HTML 콘텐츠 다운로드")
    print("4. 🔍 TXT 파일 무결성 검증")
    print("5. 🔴 실패 파일 자동 재다운로드")
    print("6. 🔧 TXT 파일 자동 수정")
    print("7. 🔄 브랜드별 재분류")
    print("8. 🧹 빈 폴더 정리")
    print("9. 📈 대시보드 열기")
    print("F. 📁 HTML 폴더 열기")
    print("0. ❌ 종료")
    print()
    print("="*50)
    print()

def run_status():
    """상태 확인"""
    print("\n📊 현재 상태 확인 중...")
    if Path("START_HERE.py").exists():
        subprocess.run([sys.executable, "START_HERE.py"])
    else:
        print("❌ START_HERE.py 파일을 찾을 수 없습니다.")

def run_csv_download():
    """CSV 다운로드 안내"""
    print("\n📥 CSV 데이터 다운로드")
    print("\n⚠️  Cafe24 관리자 페이지에서 수동으로 다운로드해주세요.")
    print("\n📍 다운로드 경로:")
    print("   C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\download\\")
    print("\n📋 CSV 파일명 형식: manwonyori_YYYYMMDD_XXX_XXXX.csv")
    print()
    
    response = input("Cafe24 관리자 페이지를 열까요? (Y/N): ").strip().upper()
    if response == 'Y':
        os.system("start https://eclogin.cafe24.com/Shop/?mall_id=manwonyori")
        print("\n💡 로그인 후: 상품관리 > 전체상품관리 > 상품 엑셀 다운로드")

def run_html_download():
    """HTML 다운로드"""
    print("\n🌐 HTML 콘텐츠 다운로드")
    script_path = Path("scripts/html_downloader.py")
    
    if script_path.exists():
        print("✅ HTML 다운로더 스크립트 발견")
        subprocess.run([sys.executable, str(script_path)])
    else:
        print("❌ HTML 다운로더 스크립트가 없습니다.")
        print("\n📝 수동 다운로드 가이드:")
        print("   1. Cafe24 관리자 > 상품관리 > 상품조회")
        print("   2. 각 상품의 상세설명 HTML 복사")
        print("   3. html/temp_txt/ 폴더에 XXX.txt로 저장")
        print("   4. scripts\\apply_txt_to_html.py 실행")

def run_validate_txt():
    """TXT 파일 검증"""
    print("\n🔍 TXT 파일 무결성 검증")
    script_path = Path("scripts/validate_temp_txt_files.py")
    
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)])
        print("\n📝 검증 완료! reports 폴더에서 결과를 확인하세요.")
    else:
        print("❌ 검증 스크립트를 찾을 수 없습니다.")

def run_auto_fix():
    """TXT 자동 수정"""
    print("\n🔧 TXT 파일 자동 수정")
    script_path = Path("scripts/auto_fix_txt_files.py")
    
    if script_path.exists():
        print("✅ 자동 수정 스크립트 발견")
        # Y를 자동으로 입력
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdin=subprocess.PIPE,
            text=True
        )
        process.communicate(input="Y\n")
        print("\n✅ 자동 수정 완료! 재검증을 실행하세요.")
    else:
        print("❌ 자동 수정 스크립트를 찾을 수 없습니다.")

def run_reclassify():
    """브랜드별 재분류"""
    print("\n🔄 브랜드별 재분류")
    script_path = Path("scripts/complete_reclassification.py")
    
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)])
        print("\n✅ 재분류 완료!")
    else:
        print("❌ 재분류 스크립트를 찾을 수 없습니다.")

def run_clean():
    """빈 폴더 정리"""
    print("\n🧹 빈 폴더 정리")
    script_path = Path("scripts/clean_and_consolidate_folders.py")
    
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)])
        print("\n✅ 정리 완료!")
    else:
        print("❌ 정리 스크립트를 찾을 수 없습니다.")

def open_dashboard():
    """대시보드 열기"""
    print("\n📈 대시보드 열기")
    dashboard_path = Path("test/dashboard.html")
    
    if dashboard_path.exists():
        os.system(f"start {dashboard_path}")
        print("✅ 대시보드가 브라우저에서 열렸습니다.")
    else:
        print("❌ 대시보드 파일을 찾을 수 없습니다.")

def open_folder():
    """HTML 폴더 열기"""
    print("\n📁 HTML 폴더 열기")
    html_path = Path("html")
    
    if html_path.exists():
        os.system(f"explorer {html_path.absolute()}")
        print("✅ 폴더가 열렸습니다.")
    else:
        print("❌ HTML 폴더를 찾을 수 없습니다.")

def run_auto_redownload():
    """실패 파일 자동 재다운로드"""
    print("\n🔴 실패 파일 자동 재다운로드")
    
    # 재다운로드 목록 확인
    redownload_list = Path("reports/redownload_list.json")
    if not redownload_list.exists():
        print("\n⚠️  재다운로드 목록이 없습니다.")
        print("먼저 '4. TXT 파일 무결성 검증'을 실행하세요.")
        return
    
    # 자동 재다운로드 스크립트 실행
    script_path = Path("scripts/auto_redownload.py")
    if script_path.exists():
        print("\n자동 재다운로드를 시작합니다...")
        subprocess.run([sys.executable, str(script_path)])
        
        print("\n💡 재다운로드 완료!")
        print("'4. TXT 파일 무결성 검증'으로 결과를 확인하세요.")
    else:
        # 대체: 수동 가이드
        print("\n자동 재다운로드 스크립트가 없습니다.")
        guide_path = Path("scripts/redownload_helper.py")
        if guide_path.exists():
            print("수동 재다운로드 가이드를 실행합니다...")
            subprocess.run([sys.executable, str(guide_path)])
        else:
            print("❌ 재다운로드 스크립트를 찾을 수 없습니다.")

def main():
    """메인 루프"""
    while True:
        show_menu()
        
        try:
            choice = input("선택 (0-9, F): ").strip().upper()
            
            if choice == '0':
                print("\n👋 CAFE24 콘텐츠 관리 시스템을 종료합니다.")
                break
            elif choice == '1':
                run_status()
            elif choice == '2':
                run_csv_download()
            elif choice == '3':
                run_html_download()
            elif choice == '4':
                run_validate_txt()
            elif choice == '5':
                run_auto_redownload()
            elif choice == '6':
                run_auto_fix()
            elif choice == '7':
                run_reclassify()
            elif choice == '8':
                run_clean()
            elif choice == '9':
                open_dashboard()
            elif choice == 'F':
                open_folder()
            else:
                print("\n❌ 잘못된 선택입니다.")
            
            if choice != '0':
                input("\n계속하려면 Enter를 누르세요...")
                
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            input("\n계속하려면 Enter를 누르세요...")

if __name__ == "__main__":
    main()