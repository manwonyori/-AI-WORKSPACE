#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 CAFE24 콘텐츠 관리 - 시작점
이 파일 하나만 실행하면 모든 작업을 할 수 있습니다.

사용법:
python START_HERE.py
"""
import sys
import os
from pathlib import Path

# Windows UTF-8 인코딩 설정
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def show_menu():
    """메인 메뉴 표시"""
    print("=" * 60)
    print("🏪 CAFE24 콘텐츠 관리 시스템")
    print("=" * 60)
    print()
    print("선택하세요:")
    print("1. 📊 현재 상태 확인")
    print("2. 🔄 브랜드별 재분류 (완전)")
    print("3. 🧹 빈 폴더 정리")
    print("4. 📈 대시보드 열기")
    print("5. ❓ 도움말")
    print("0. 종료")
    print()

def check_status():
    """현재 상태 확인"""
    html_path = Path("html")
    
    print("\n📊 현재 상태:")
    print("-" * 40)
    
    if not html_path.exists():
        print("❌ html 폴더가 없습니다!")
        return
    
    total_files = 0
    for folder in html_path.iterdir():
        if folder.is_dir() and folder.name not in ['temp_txt', 'nul']:
            html_files = list(folder.glob("*.html"))
            if html_files:
                print(f"  {folder.name}: {len(html_files)}개")
                total_files += len(html_files)
    
    txt_files = len(list((html_path / "temp_txt").glob("*.txt"))) if (html_path / "temp_txt").exists() else 0
    
    print(f"\n총계:")
    print(f"  HTML 파일: {total_files}개")
    print(f"  TXT 원본: {txt_files}개")

def run_reclassification():
    """브랜드별 재분류 실행"""
    print("\n🔄 브랜드별 재분류를 시작합니다...")
    
    try:
        # scripts 폴더의 완전 재분류 스크립트 실행
        import subprocess
        import os
        
        # Windows에서 UTF-8 인코딩 설정
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run([sys.executable, "scripts/complete_reclassification.py"], 
                              capture_output=True, text=True, encoding='utf-8', 
                              errors='ignore', env=env)
        
        if result.returncode == 0:
            print("✅ 재분류 완료!")
        else:
            print("❌ 재분류 중 오류 발생")
            if result.stderr:
                print(result.stderr)
            
    except Exception as e:
        print(f"❌ 실행 오류: {e}")
        print("\n수동 실행:")
        print("python scripts/complete_reclassification.py")

def clean_folders():
    """빈 폴더 정리"""
    print("\n🧹 빈 폴더를 정리합니다...")
    
    try:
        import subprocess
        import os
        
        # Windows에서 UTF-8 인코딩 설정
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run([sys.executable, "scripts/clean_and_consolidate_folders.py"], 
                              capture_output=True, text=True, encoding='utf-8',
                              errors='ignore', env=env)
        
        if result.returncode == 0:
            print("✅ 폴더 정리 완료!")
        else:
            print("❌ 정리 중 오류 발생")
            if result.stderr:
                print(result.stderr)
            
    except Exception as e:
        print(f"❌ 실행 오류: {e}")

def open_dashboard():
    """대시보드 열기"""
    import webbrowser
    import os
    
    dashboard_path = Path("test/dashboard.html")
    if dashboard_path.exists():
        full_path = os.path.abspath(dashboard_path)
        webbrowser.open(f'file://{full_path}')
        print("📈 대시보드를 웹브라우저에서 열었습니다.")
    else:
        print("❌ dashboard.html 파일을 찾을 수 없습니다.")

def show_help():
    """도움말 표시"""
    print("\n❓ 도움말")
    print("-" * 40)
    print("🔍 주요 파일 위치:")
    print("  • scripts/complete_reclassification.py - 완전한 재분류")
    print("  • html/temp_txt/ - 원본 TXT 파일들 (239개)")
    print("  • html/[브랜드명]/ - 브랜드별 HTML 파일들")
    print("  • test/dashboard.html - 상태 대시보드")
    print()
    print("🚨 중요:")
    print("  • temp_txt 폴더는 절대 건드리지 마세요!")
    print("  • CSV 파일: download/manwonyori_20250901_301_e68d.csv")
    print()
    print("💡 문제 발생 시:")
    print("  1. python scripts/complete_verification.py (상태 확인)")
    print("  2. python scripts/complete_reclassification.py (재분류)")

def main():
    """메인 함수"""
    # 현재 디렉토리를 complete_content로 변경
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)
    
    while True:
        show_menu()
        
        try:
            choice = input("선택 (0-5): ").strip()
            
            if choice == '0':
                print("👋 종료합니다.")
                break
            elif choice == '1':
                check_status()
            elif choice == '2':
                run_reclassification()
            elif choice == '3':
                clean_folders()
            elif choice == '4':
                open_dashboard()
            elif choice == '5':
                show_help()
            else:
                print("❌ 잘못된 선택입니다. 0-5 사이의 숫자를 입력하세요.")
            
            input("\n계속하려면 Enter를 누르세요...")
            
        except KeyboardInterrupt:
            print("\n👋 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류: {e}")
            input("\n계속하려면 Enter를 누르세요...")

if __name__ == "__main__":
    main()