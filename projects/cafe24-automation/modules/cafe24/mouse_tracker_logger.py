"""
마우스 동작 로거 - 시각화 대신 로그로 추적
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import json

class MouseTracker:
    """마우스 동작 추적 및 로깅"""
    
    def __init__(self, driver):
        self.driver = driver
        self.log = []
        self.start_time = datetime.now()
        
    def log_action(self, action_type, details):
        """동작 로그 기록"""
        entry = {
            "time": (datetime.now() - self.start_time).total_seconds(),
            "action": action_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.log.append(entry)
        
        # 콘솔에 실시간 출력
        print(f"[{entry['time']:.1f}s] {action_type}: {details}")
        
    def move_to(self, element, description=""):
        """요소로 이동"""
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        
        location = element.location
        self.log_action("MOVE", {
            "x": location['x'],
            "y": location['y'],
            "element": description or element.tag_name
        })
        
    def click(self, element, description=""):
        """요소 클릭"""
        element.click()
        
        location = element.location
        self.log_action("CLICK", {
            "x": location['x'],
            "y": location['y'],
            "element": description or element.tag_name
        })
        
    def scroll_to(self, element, description=""):
        """요소로 스크롤"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        
        self.log_action("SCROLL", {
            "element": description or element.tag_name
        })
        
    def type_text(self, element, text, description=""):
        """텍스트 입력"""
        element.clear()
        element.send_keys(text)
        
        self.log_action("TYPE", {
            "text": text[:50] + "..." if len(text) > 50 else text,
            "element": description or element.tag_name
        })
        
    def save_log(self, filename=None):
        """로그 저장"""
        if not filename:
            filename = f"mouse_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "start_time": self.start_time.isoformat(),
                "duration": (datetime.now() - self.start_time).total_seconds(),
                "actions": self.log
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[로그 저장] {filename}")
        return filename
    
    def print_summary(self):
        """요약 출력"""
        print("\n" + "="*60)
        print("마우스 동작 요약")
        print("="*60)
        
        action_counts = {}
        for entry in self.log:
            action = entry['action']
            action_counts[action] = action_counts.get(action, 0) + 1
        
        for action, count in action_counts.items():
            print(f"  {action}: {count}회")
        
        print(f"\n총 동작: {len(self.log)}개")
        print(f"소요 시간: {(datetime.now() - self.start_time).total_seconds():.1f}초")

def demo_with_tracking():
    """추적 데모"""
    
    print("마우스 동작 추적 데모 시작...\n")
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    driver = webdriver.Chrome(options=options)
    tracker = MouseTracker(driver)
    
    try:
        # Google 검색 테스트
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # 검색창 찾기
        search_box = driver.find_element("name", "q")
        
        # 마우스 동작 추적
        tracker.move_to(search_box, "검색창")
        time.sleep(0.5)
        
        tracker.click(search_box, "검색창")
        time.sleep(0.5)
        
        tracker.type_text(search_box, "카페24", "검색창")
        time.sleep(1)
        
        # 요약 출력
        tracker.print_summary()
        
        # 로그 저장
        log_file = tracker.save_log("C:/Users/8899y/CUA-MASTER/modules/cafe24/learning/demo_mouse_log.json")
        
        print(f"\n마우스 동작이 로그 파일에 기록되었습니다.")
        print(f"시각화 대신 이 로그를 사용하여 동작을 추적할 수 있습니다.")
        
    except Exception as e:
        print(f"[ERROR] {e}")
    
    finally:
        input("\n엔터를 눌러 종료...")
        driver.quit()

if __name__ == "__main__":
    demo_with_tracking()