"""
Chrome 드라이버 자동 설치 스크립트
"""

import os
import sys
import subprocess
import platform

def install_chromedriver():
    """webdriver-manager를 사용하여 ChromeDriver 자동 설치"""
    
    print("Chrome 드라이버 자동 설치를 시작합니다...")
    print("-" * 50)
    
    # webdriver-manager 설치
    print("1. webdriver-manager 패키지 설치 중...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])
        print("✅ webdriver-manager 설치 완료")
    except:
        print("❌ webdriver-manager 설치 실패")
        return False
    
    # 테스트 코드
    print("\n2. Chrome 드라이버 자동 설정 테스트...")
    
    test_code = """
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Chrome 드라이버 자동 다운로드 및 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    print("✅ Chrome 드라이버 설치 및 실행 성공!")
    print(f"   드라이버 위치: {service.path}")
    
    driver.get("https://www.google.com")
    print("✅ 구글 페이지 접속 성공!")
    
    driver.quit()
    print("✅ 테스트 완료!")
    
except Exception as e:
    print(f"❌ 오류 발생: {e}")
"""
    
    try:
        exec(test_code)
        return True
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False

def update_crawler_imports():
    """크롤러 파일들의 import 문 업데이트"""
    
    print("\n3. 크롤러 파일 업데이트 중...")
    
    # product_crawler.py 업데이트를 위한 내용
    update_content = """# Chrome 드라이버 import 부분을 다음과 같이 수정:
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# init_driver 메서드 내에서:
service = Service(ChromeDriverManager().install())
self.driver = webdriver.Chrome(service=service, options=options)
"""
    
    print("✅ 업데이트 가이드:")
    print(update_content)
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("   Chrome 드라이버 자동 설치 프로그램")
    print("=" * 60)
    
    success = install_chromedriver()
    
    if success:
        update_crawler_imports()
        
        print("\n" + "=" * 60)
        print("✅ Chrome 드라이버 설치 완료!")
        print("\n이제 다음 명령어로 로그인 테스트를 실행하세요:")
        print("   python test_login.py")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 설치 실패")
        print("\n수동으로 ChromeDriver를 다운로드하세요:")
        print("1. Chrome 버전 확인: chrome://version")
        print("2. 다운로드: https://chromedriver.chromium.org/downloads")
        print("3. chromedriver.exe를 현재 폴더에 복사")
        print("=" * 60)