# -*- coding: utf-8 -*-
"""
Direct URL CUA Agent - 사용자 지정 URL 경로로 직접 진입
정확한 Cafe24 Excel 다운로드 URL 경로 사용
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
import glob
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

class DirectURLCUAAgent:
    """사용자 지정 URL 경로로 직접 진입하는 CUA Agent"""
    
    def __init__(self, download_folder="C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\download"):
        """초기화"""
        self.driver = None
        self.download_folder = download_folder
        self.config_file = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\config\\cafe24_config.json"
        self.config = {}
        
        # 사용자 지정 URL 경로들
        self.excel_base_url = "https://manwonyori.cafe24.com/admin/php/shop1/Excel/ExcelCreateRequest.php"
        self.excel_product_url = "https://manwonyori.cafe24.com/admin/php/shop1/Excel/ExcelCreateRequest.php?request=product"
        self.excel_none_url = "https://manwonyori.cafe24.com/admin/php/shop1/Excel/ExcelCreateRequest.php#none"
        self.target_url = "https://manwonyori.cafe24.com/admin/php/shop1/Excel/ExcelCreateRequest.php#none"  # 사용자 지정 URL
        self.excel_download_url = "https://manwonyori.cafe24.com/admin/php/shop1/Excel/ExcelCreateDownload.php?request=product#DirectDownload"
        
        # 다운로드 폴더 생성
        os.makedirs(download_folder, exist_ok=True)
        
        print("[DIRECT-URL-CUA] 사용자 지정 URL 경로로 직접 진입하는 CUA Agent")
        print(f"[DOWNLOAD-PATH] {download_folder}")
        print(f"[TARGET-URL] {self.excel_product_url}")
        
        # 설정 로드
        self.load_config()
        
    def load_config(self):
        """설정 파일 로드"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"   [CONFIG] 설정 로드 완료")
        except Exception as e:
            # 기본 설정 사용
            self.config = {
                'cafe24': {
                    'admin_url': 'https://manwonyori.cafe24.com/admin',
                    'mall_id': 'manwonyori',
                    'username': 'manwonyori',
                    'password': 'happy8263!'
                }
            }
            print(f"   [CONFIG] 기본 설정 사용")
    
    def setup_chrome_driver(self):
        """Chrome 드라이버 설정"""
        print("\n[STEP-1] Chrome 드라이버 설정...")
        
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 다운로드 경로 지정
        prefs = {
            "download.default_directory": self.download_folder,
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("   [OK] Chrome 드라이버 설정 완료")
            return True
        except Exception as e:
            print(f"   [ERROR] 드라이버 설정 실패: {e}")
            return False
    
    def step2_login_to_admin(self):
        """STEP-2: 관리자 로그인"""
        print("\n[STEP-2] 관리자 로그인...")
        
        try:
            # 2-1: 관리자 URL 접근
            admin_url = self.config['cafe24']['admin_url']
            self.driver.get(admin_url)
            time.sleep(3)
            print("   [2-1] 관리자 페이지 접근 완료")
            
            # 2-2: 보안 알림 처리
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text[:50]
                print(f"   [2-2] 보안 알림 처리: {alert_text}...")
                alert.accept()
                time.sleep(1)
            except:
                print("   [2-2] 보안 알림 없음")
            
            # 2-3: 로그인 폼 입력
            username_input = self.driver.find_element(By.XPATH, "//input[@type='text' and not(@placeholder='')]")
            username_input.clear()
            username_input.send_keys(self.config['cafe24']['username'])
            
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_input.clear()
            password_input.send_keys(self.config['cafe24']['password'])
            
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
            login_button.click()
            time.sleep(3)
            print("   [2-3] 로그인 완료")
            
            # 2-4: 로그인 후 알림 처리
            alert_count = 0
            while alert_count < 5:
                try:
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    alert_count += 1
                    time.sleep(1)
                except:
                    break
            
            print("   [SUCCESS] 관리자 로그인 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 로그인 실패: {e}")
            return False
    
    def step3_direct_excel_access(self):
        """STEP-3: 사용자 지정 Excel 다운로드 URL로 직접 접근"""
        print("\n[STEP-3] Excel 다운로드 페이지 직접 접근...")
        
        try:
            # 3-1: ExcelCreateRequest.php로 직접 접근
            print(f"   [3-1] 기본 Excel 페이지 접근: {self.excel_base_url}")
            self.driver.get(self.excel_base_url)
            time.sleep(3)
            print("   [3-1] 기본 Excel 페이지 접근 완료")
            
            # 3-2: request=product 파라미터로 상품 다운로드 페이지 접근
            print(f"   [3-2] 상품 Excel 다운로드 페이지 접근: {self.excel_product_url}")
            self.driver.get(self.excel_product_url)
            time.sleep(5)
            print("   [3-2] 상품 Excel 다운로드 페이지 접근 완료")
            
            # 3-3: 페이지 로딩 확인
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("   [3-3] 페이지 로딩 완료")
            
            # 3-4: 현재 URL 확인
            current_url = self.driver.current_url
            print(f"   [3-4] 현재 URL: {current_url}")
            
            print("   [SUCCESS] Excel 다운로드 페이지 직접 접근 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] Excel 페이지 접근 실패: {e}")
            return False
    
    def step4_set_period_6months(self):
        """STEP-4: 기간을 6개월로 설정 - 사용자 지정 순서"""
        print("\n[STEP-4] 기간 6개월 설정...")
        print("   [INFO] 기간 옵션: 오늘, 3일, 7일, 1개월, 3개월, 6개월")
        
        try:
            # 4-1: 먼저 6개월 텍스트를 직접 클릭 시도
            print("   [4-1] '6개월' 텍스트 직접 클릭 시도...")
            
            # 6개월 텍스트를 포함하는 모든 요소 찾기
            six_month_texts = [
                "//label[text()='6개월']",
                "//span[text()='6개월']",
                "//td[text()='6개월']",
                "//label[contains(text(), '6개월')]",
                "//span[contains(text(), '6개월')]",
                "//*[text()='6개월' and not(self::input)]"
            ]
            
            for selector in six_month_texts:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            print(f"   [4-1] '6개월' 텍스트 발견: {selector}")
                            element.click()
                            time.sleep(2)
                            print("   [4-1] '6개월' 텍스트 클릭 완료")
                            print("   [SUCCESS] 기간 6개월 설정 완료")
                            return True
                except:
                    continue
            
            # 4-2: 라디오 버튼 직접 찾기
            print("   [4-2] 6개월 라디오 버튼 검색...")
            
            # 라디오 버튼 선택자들
            period_selectors = [
                "//input[@value='6' and @type='radio']",
                "//input[@value='6months' and @type='radio']", 
                "//input[@value='180' and @type='radio']",  # 180일
                "//input[@value='183' and @type='radio']",  # 6개월 (약 183일)
                "//label[contains(text(), '6개월')]//input[@type='radio']",
                "//label[contains(text(), '6개월')]/..//input[@type='radio']",
                "//label[text()='6개월']//input[@type='radio']",
                "//label[text()='6개월']/..//input[@type='radio']",
                "//*[contains(text(), '6개월')]/input[@type='radio']",
                "//*[text()='6개월']/input[@type='radio']",
                "//input[@name='search_date' and @value='180']",
                "//input[@name='search_period' and @value='6']"
            ]
            
            period_option = None
            found_selector = None
            
            for selector in period_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            period_option = element
                            found_selector = selector
                            print(f"   [4-1] 6개월 옵션 발견: {selector}")
                            break
                    if period_option:
                        break
                except:
                    continue
            
            if period_option:
                # 4-2: 6개월 옵션 클릭
                print("   [4-2] 6개월 옵션 클릭 중...")
                period_option.click()
                time.sleep(2)
                print("   [4-2] 6개월 옵션 클릭 완료")
                
                print("   [SUCCESS] 기간 6개월 설정 완료")
                return True
            else:
                # 4-3: 6개월 옵션을 찾지 못한 경우 - 모든 라디오 버튼 상세 출력
                print("   [4-3] 6개월 옵션을 찾지 못함 - 모든 라디오 버튼 상세 확인")
                all_radios = self.driver.find_elements(By.XPATH, "//input[@type='radio']")
                print(f"   [4-3] 페이지 내 전체 라디오 버튼: {len(all_radios)}개")
                
                # 모든 라디오 버튼 정보 출력 (디버그용)
                print("   [4-3] 모든 라디오 버튼 정보:")
                for i, radio in enumerate(all_radios):
                    try:
                        value = radio.get_attribute('value') or ''
                        name = radio.get_attribute('name') or ''
                        id_attr = radio.get_attribute('id') or ''
                        checked = radio.get_attribute('checked') or ''
                        
                        # 부모 요소의 텍스트 가져오기
                        parent_text = ''
                        try:
                            parent = radio.find_element(By.XPATH, "./..")
                            parent_text = parent.text.replace('\n', ' ')[:50]
                        except:
                            pass
                        
                        # 라벨 텍스트 가져오기
                        label_text = ''
                        if id_attr:
                            try:
                                label = self.driver.find_element(By.XPATH, f"//label[@for='{id_attr}']")
                                label_text = label.text
                            except:
                                pass
                        
                        print(f"      [{i+1}] name='{name}' value='{value}' id='{id_attr}' checked='{checked}'")
                        if parent_text:
                            print(f"          parent: '{parent_text}'")
                        if label_text:
                            print(f"          label: '{label_text}'")
                        
                        # 기간 관련 라디오 버튼인지 확인
                        if any(keyword in f"{parent_text} {label_text} {name}" for keyword in ['기간', '개월', 'month', '날짜', 'date', 'period', 'search']):
                            print(f"          >>> [기간 관련 옵션]")
                            
                            # 6개월 관련 키워드로 재시도
                            if any(keyword in f"{value} {parent_text} {label_text}" for keyword in ['6', '6개월', '180', '183']):
                                print(f"          >>> [6개월 후보 발견!] 클릭 시도...")
                                try:
                                    radio.click()
                                    time.sleep(2)
                                    print("   [4-3] 6개월 라디오 버튼 클릭 성공!")
                                    print("   [SUCCESS] 기간 6개월 설정 완료")
                                    return True
                                except Exception as e:
                                    print(f"          클릭 실패: {e}")
                    except Exception as e:
                        print(f"      [{i+1}] 정보 읽기 실패: {e}")
                
                print("   [WARNING] 6개월 옵션을 찾을 수 없음 - 기본값으로 진행")
                return True
            
            
        except Exception as e:
            print(f"   [INFO] 기간 설정 생략: {e}")
            return True  # 실패해도 계속 진행
    
    def step5_select_template(self):
        """STEP-5: 카페24상품다운로드양식전체 선택"""
        print("\n[STEP-5] 다운로드 양식 선택...")
        
        try:
            # 5-1: aManagesList 선택자 찾기
            print("   [5-1] 양식 선택 드롭다운 검색...")
            select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "aManagesList"))
            )
            print("   [5-1] 양식 선택 드롭다운 발견")
            
            # 5-2: Select 객체 생성 및 옵션 확인
            select = Select(select_element)
            options = select.options
            print(f"   [5-2] 사용 가능한 옵션: {len(options)}개")
            
            for option in options:
                option_text = option.text
                option_value = option.get_attribute('value')
                selected = option.is_selected()
                print(f"       - {option_text} (value: {option_value}) {'[SELECTED]' if selected else ''}")
            
            # 5-3: 카페24상품다운로드양식전체 선택
            try:
                select.select_by_visible_text("카페24상품다운로드양식전체")
                print("   [5-3] '카페24상품다운로드양식전체' 선택 완료")
            except:
                try:
                    select.select_by_value("52")
                    print("   [5-3] value='52'로 선택 완료")
                except:
                    print("   [5-3] 이미 선택된 상태 또는 선택 불가")
            
            # 5-4: 선택 상태 확인
            selected_option = select.first_selected_option
            selected_text = selected_option.text
            print(f"   [5-4] 현재 선택된 양식: {selected_text}")
            
            print("   [SUCCESS] 다운로드 양식 선택 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 양식 선택 실패: {e}")
            return False
    
    def step6_request_excel_file(self):
        """STEP-6: 엑셀파일요청 버튼 클릭"""
        print("\n[STEP-6] 엑셀파일 생성 요청...")
        
        try:
            # 6-1: 다양한 방법으로 엑셀파일요청 버튼 찾기
            print("   [6-1] '엑셀파일요청' 버튼 검색...")
            
            button_selectors = [
                "//input[@value='엑셀파일 생성 요청']",
                "//input[@value='엑셀파일생성요청']",
                "//input[@value='엑셀파일요청']",
                "//input[@value='엑셀 파일 요청']", 
                "//input[contains(@value, '엑셀파일')]",
                "//input[contains(@value, '엑셀 파일')]",
                "//input[contains(@value, '생성 요청')]",
                "//button[contains(text(), '엑셀파일 생성 요청')]",
                "//button[contains(text(), '엑셀파일생성요청')]",
                "//button[contains(text(), '엑셀 파일')]",
                "//input[@type='submit' and contains(@onclick, '엑셀')]",
                "//input[@type='button' and contains(@onclick, '엑셀')]",
                "//*[contains(text(), '엑셀파일 생성 요청')]",
                "//*[contains(text(), '엑셀파일생성요청')]"
            ]
            
            request_button = None
            for selector in button_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            request_button = element
                            print(f"   [6-1] 버튼 발견: {selector}")
                            break
                    if request_button:
                        break
                except:
                    continue
            
            if not request_button:
                # 페이지 소스에서 엑셀 관련 요소 찾기
                page_source = self.driver.page_source
                print("   [6-1] 페이지에서 '엑셀' 관련 요소 검색...")
                
                if '엑셀파일요청' in page_source:
                    print("   [6-1] 페이지에 '엑셀파일요청' 텍스트 존재")
                elif '엑셀' in page_source:
                    print("   [6-1] 페이지에 '엑셀' 관련 텍스트 존재")
                else:
                    print("   [6-1] 페이지에 엑셀 관련 요소 없음")
                
                # 모든 input과 button 요소 출력
                all_inputs = self.driver.find_elements(By.XPATH, "//input[@type='submit' or @type='button']")
                all_buttons = self.driver.find_elements(By.XPATH, "//button")
                
                print(f"   [6-1] 페이지 내 submit/button 요소: {len(all_inputs + all_buttons)}개")
                print("   [6-1] 모든 버튼 정보 출력:")
                for i, elem in enumerate(all_inputs + all_buttons):
                    try:
                        value = elem.get_attribute('value') or ''
                        text = elem.text or ''
                        onclick = elem.get_attribute('onclick') or ''
                        tag_name = elem.tag_name
                        
                        if value or text or onclick:
                            display_info = f"{tag_name}: value='{value}' text='{text}' onclick='{onclick[:30]}'"
                            print(f"      - {i+1}: {display_info}")
                            
                            # 엑셀 관련 요소 특별 표시
                            if ('엑셀' in value or 'excel' in value.lower() or 
                                '엑셀' in text or 'excel' in text.lower() or
                                '엑셀' in onclick or 'excel' in onclick.lower()):
                                print(f"         >>> [EXCEL-RELATED] <<<")
                    except:
                        pass
                
                raise Exception("엑셀파일요청 버튼을 찾을 수 없음")
            
            # 6-2: 버튼 클릭
            request_button.click()
            print("   [6-2] '엑셀파일요청' 버튼 클릭 완료")
            
            # 6-3: 확인 팝업 처리
            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert_text = alert.text[:50]
                print(f"   [6-3] 확인 팝업: {alert_text}...")
                alert.accept()
                print("   [6-3] 확인 팝업 처리 완료")
            except:
                print("   [6-3] 확인 팝업 없음")
            
            print("   [SUCCESS] 엑셀파일 생성 요청 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 엑셀파일 요청 실패: {e}")
            return False
    
    def step7_wait_and_download(self):
        """STEP-7: 파일 생성 대기 및 다운로드"""
        print("\n[STEP-7] 파일 생성 대기 및 다운로드...")
        
        try:
            # 7-1: 파일 생성 대기
            print("   [7-1] 엑셀 파일 생성 대기 (30초)...")
            time.sleep(30)
            
            # 7-2: DirectDownload URL로 이동 시도
            print(f"   [7-2] DirectDownload URL 접근: {self.excel_download_url}")
            try:
                self.driver.get(self.excel_download_url)
                time.sleep(3)
                print("   [7-2] DirectDownload 페이지 접근 완료")
            except:
                print("   [7-2] DirectDownload 페이지 접근 생략")
            
            # 7-3: 다운로드 링크 찾기
            print("   [7-3] 다운로드 링크 검색...")
            download_selectors = [
                "//span[text()='다운로드']",
                "//a[contains(text(), '다운로드')]", 
                "//input[@value='다운로드']",
                "//*[contains(@onclick, 'download')]",
                "//span[contains(text(), '다운로드')]"
            ]
            
            download_link = None
            for selector in download_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            download_link = element
                            print(f"   [7-3] 다운로드 링크 발견: {selector}")
                            break
                    if download_link:
                        break
                except:
                    continue
            
            if download_link:
                # 7-4: 다운로드 실행
                download_link.click()
                print("   [7-4] 다운로드 시작!")
                time.sleep(15)  # 다운로드 완료 대기
            else:
                print("   [7-4] 다운로드 링크를 찾을 수 없음")
                # 페이지 새로고침 후 재시도
                self.driver.refresh()
                time.sleep(5)
                
                download_link = None
                for selector in download_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                download_link = element
                                print(f"   [7-4] 새로고침 후 다운로드 링크 발견: {selector}")
                                break
                        if download_link:
                            break
                    except:
                        continue
                
                if download_link:
                    download_link.click()
                    print("   [7-4] 다운로드 시작!")
                    time.sleep(15)
                else:
                    print("   [7-4] 다운로드 링크를 찾을 수 없습니다")
                    return False
            
            print("   [SUCCESS] 다운로드 프로세스 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 다운로드 실패: {e}")
            return False
    
    def step8_verify_result(self):
        """STEP-8: 다운로드 결과 확인"""
        print("\n[STEP-8] 다운로드 결과 확인...")
        
        try:
            # 최근 파일 확인 (5분 내)
            excel_files = glob.glob(os.path.join(self.download_folder, "*.csv"))
            excel_files.extend(glob.glob(os.path.join(self.download_folder, "*.xlsx")))
            excel_files.extend(glob.glob(os.path.join(self.download_folder, "*.xls")))
            
            recent_files = []
            current_time = time.time()
            
            for file_path in excel_files:
                file_mtime = os.path.getmtime(file_path)
                if current_time - file_mtime < 300:  # 5분 내
                    recent_files.append({
                        'path': file_path,
                        'name': os.path.basename(file_path),
                        'size': os.path.getsize(file_path),
                        'time': datetime.fromtimestamp(file_mtime)
                    })
            
            if recent_files:
                print(f"   [SUCCESS] 새 다운로드 파일: {len(recent_files)}개")
                for file_info in recent_files:
                    print(f"   [FILE] {file_info['name']}")
                    print(f"   [SIZE] {file_info['size']:,} bytes ({file_info['size']/1024/1024:.1f} MB)")
                    print(f"   [TIME] {file_info['time'].strftime('%H:%M:%S')}")
                return True, recent_files
            else:
                print("   [INFO] 5분 내 새 파일 없음")
                return False, []
                
        except Exception as e:
            print(f"   [ERROR] 결과 확인 실패: {e}")
            return False, []
    
    def run_direct_url_workflow(self):
        """사용자 지정 URL 경로로 직접 워크플로우 실행"""
        print("\n" + "="*80)
        print("[DIRECT-URL-WORKFLOW] 사용자 지정 URL 경로로 직접 진입")
        print("ExcelCreateRequest.php → request=product → 양식선택 → 다운로드")
        print("="*80)
        
        try:
            # 각 단계 실행
            if not self.setup_chrome_driver():
                return False
            
            if not self.step2_login_to_admin():
                return False
            
            if not self.step3_direct_excel_access():
                return False
            
            if not self.step4_set_period_6months():
                return False
            
            if not self.step5_select_template():
                return False
            
            if not self.step6_request_excel_file():
                return False
            
            if not self.step7_wait_and_download():
                return False
            
            success, files = self.step8_verify_result()
            
            if success:
                print("\n" + "="*80)
                print("[DIRECT-URL-SUCCESS] URL 직접 진입 방식 성공!")
                print("사용자 지정 경로로 완벽 실행")
                print("="*80)
            else:
                print("\n[DIRECT-URL-INFO] 워크플로우 완료 - 파일 확인 필요")
            
            return success
            
        except Exception as e:
            print(f"\n[DIRECT-URL-ERROR] 실행 중 오류: {e}")
            return False
        
        finally:
            print("\n[WAIT] 결과 확인을 위해 15초 대기...")
            time.sleep(15)
            
            if self.driver:
                self.driver.quit()
                print("[CLEANUP] Direct URL 실행 완료")

def main():
    """메인 실행"""
    print("="*80)
    print("DIRECT URL CUA AGENT")
    print("사용자 지정 URL 경로로 직접 진입하여 Excel 다운로드")
    print("="*80)
    
    # Direct URL CUA Agent 실행
    direct_agent = DirectURLCUAAgent()
    success = direct_agent.run_direct_url_workflow()
    
    if success:
        print("\n[RESULT] Direct URL 방식 성공!")
        print("사용자 지정 경로로 완벽 실행")
    else:
        print("\n[RESULT] Direct URL 방식 완료")
        print("각 단계별 로그를 확인하세요")

if __name__ == "__main__":
    main()