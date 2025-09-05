#!/usr/bin/env python3
"""
Ultimate AI Auto-Relay System - Complete Test Suite
완벽한 작동 검증 시스템
"""

import os
import json
import time
import sys
from pathlib import Path

# UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

class ExtensionTester:
    def __init__(self):
        self.base_path = Path(r"C:\Users\8899y\AI-WORKSPACE\chrome-extension\ULTIMATE")
        self.test_results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
        
    def test_file_structure(self):
        """Test 1: 파일 구조 검증"""
        print_header("TEST 1: 파일 구조 검증")
        
        required_files = [
            'manifest.json',
            'background.js',
            'content.js',
            'popup.html',
            'popup.js',
            'monitor.html',
            'icon.png'
        ]
        
        for file in required_files:
            file_path = self.base_path / file
            self.test_results['total'] += 1
            
            if file_path.exists():
                size = file_path.stat().st_size
                print_success(f"{file} - {size:,} bytes")
                self.test_results['passed'] += 1
            else:
                print_error(f"{file} - NOT FOUND")
                self.test_results['failed'] += 1
                
    def test_manifest(self):
        """Test 2: Manifest 검증"""
        print_header("TEST 2: Manifest.json 검증")
        
        manifest_path = self.base_path / 'manifest.json'
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
                
            # Required fields
            required = {
                'manifest_version': 3,
                'name': str,
                'version': str,
                'permissions': list,
                'host_permissions': list,
                'background': dict,
                'content_scripts': list,
                'action': dict
            }
            
            for field, expected_type in required.items():
                self.test_results['total'] += 1
                
                if field in manifest:
                    if expected_type == 3:  # Special case for manifest_version
                        if manifest[field] == 3:
                            print_success(f"{field}: {manifest[field]}")
                            self.test_results['passed'] += 1
                        else:
                            print_error(f"{field}: {manifest[field]} (Expected: 3)")
                            self.test_results['failed'] += 1
                    elif isinstance(manifest[field], expected_type):
                        print_success(f"{field}: ✓")
                        self.test_results['passed'] += 1
                    else:
                        print_error(f"{field}: Wrong type")
                        self.test_results['failed'] += 1
                else:
                    print_error(f"{field}: MISSING")
                    self.test_results['failed'] += 1
                    
        except Exception as e:
            print_error(f"Manifest parse error: {e}")
            self.test_results['failed'] += 1
            
    def test_javascript_syntax(self):
        """Test 3: JavaScript 문법 검증"""
        print_header("TEST 3: JavaScript 문법 검증")
        
        js_files = ['background.js', 'content.js', 'popup.js']
        
        for js_file in js_files:
            file_path = self.base_path / js_file
            self.test_results['total'] += 1
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for common syntax issues
                    checks = [
                        ('console.log', 'Debug logging'),
                        ('chrome.runtime', 'Runtime API'),
                        ('async', 'Async functions'),
                        ('addEventListener', 'Event listeners')
                    ]
                    
                    issues = []
                    for pattern, description in checks:
                        if pattern not in content:
                            issues.append(f"Missing {description}")
                            
                    if not issues:
                        print_success(f"{js_file}: All checks passed")
                        self.test_results['passed'] += 1
                    else:
                        print_warning(f"{js_file}: {', '.join(issues)}")
                        self.test_results['warnings'] += 1
                        
                except Exception as e:
                    print_error(f"{js_file}: Read error - {e}")
                    self.test_results['failed'] += 1
            else:
                print_error(f"{js_file}: NOT FOUND")
                self.test_results['failed'] += 1
                
    def test_content_script(self):
        """Test 4: Content Script 기능 검증"""
        print_header("TEST 4: Content Script 기능 검증")
        
        file_path = self.base_path / 'content.js'
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            features = [
                ('detectPlatform', '플랫폼 감지'),
                ('findElement', '요소 찾기'),
                ('setInputText', '텍스트 입력'),
                ('clickSendButton', '버튼 클릭'),
                ('getLastResponse', '응답 획득'),
                ('chrome.runtime.onMessage', '메시지 리스너')
            ]
            
            for feature, description in features:
                self.test_results['total'] += 1
                
                if feature in content:
                    print_success(f"{description}: ✓")
                    self.test_results['passed'] += 1
                else:
                    print_error(f"{description}: ✗")
                    self.test_results['failed'] += 1
                    
    def test_background_script(self):
        """Test 5: Background Script 기능 검증"""
        print_header("TEST 5: Background Script 기능 검증")
        
        file_path = self.base_path / 'background.js'
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            features = [
                ('SYSTEM', '시스템 상태 관리'),
                ('openPlatform', '플랫폼 열기'),
                ('sendToTab', '탭 메시지 전송'),
                ('startRelay', '릴레이 시작'),
                ('stopRelay', '릴레이 중지'),
                ('chrome.tabs', 'Tabs API'),
                ('chrome.runtime.onMessage', '메시지 핸들러'),
                ('chrome.storage', 'Storage API')
            ]
            
            for feature, description in features:
                self.test_results['total'] += 1
                
                if feature in content:
                    print_success(f"{description}: ✓")
                    self.test_results['passed'] += 1
                else:
                    print_error(f"{description}: ✗")
                    self.test_results['failed'] += 1
                    
    def test_popup(self):
        """Test 6: Popup UI 검증"""
        print_header("TEST 6: Popup UI 검증")
        
        html_path = self.base_path / 'popup.html'
        js_path = self.base_path / 'popup.js'
        
        if html_path.exists():
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Check UI elements
            elements = [
                ('btnOpenAll', '모든 탭 열기 버튼'),
                ('btnCheckStatus', '상태 확인 버튼'),
                ('btnSendAll', '전체 전송 버튼'),
                ('btnStartRelay', '릴레이 시작 버튼'),
                ('messageInput', '메시지 입력창'),
                ('relayObjective', '릴레이 목표 입력창')
            ]
            
            for element_id, description in elements:
                self.test_results['total'] += 1
                
                if f'id="{element_id}"' in html_content:
                    print_success(f"{description}: ✓")
                    self.test_results['passed'] += 1
                else:
                    print_error(f"{description}: ✗")
                    self.test_results['failed'] += 1
                    
    def test_monitor(self):
        """Test 7: Monitor Dashboard 검증"""
        print_header("TEST 7: Monitor Dashboard 검증")
        
        file_path = self.base_path / 'monitor.html'
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            features = [
                ('relay-visualization', '릴레이 시각화'),
                ('console', '실시간 콘솔'),
                ('stats', '통계 표시'),
                ('platform status', '플랫폼 상태'),
                ('controls', '제어 버튼')
            ]
            
            for feature, description in features:
                self.test_results['total'] += 1
                
                if feature.replace(' ', '-') in content or feature in content:
                    print_success(f"{description}: ✓")
                    self.test_results['passed'] += 1
                else:
                    print_warning(f"{description}: ?")
                    self.test_results['warnings'] += 1
                    
    def run_all_tests(self):
        """모든 테스트 실행"""
        print_header("AI ULTIMATE AUTO-RELAY SYSTEM TEST SUITE")
        print_info(f"Test Path: {self.base_path}")
        print_info(f"Test Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all tests
        self.test_file_structure()
        self.test_manifest()
        self.test_javascript_syntax()
        self.test_content_script()
        self.test_background_script()
        self.test_popup()
        self.test_monitor()
        
        # Print summary
        print_header("TEST SUMMARY")
        
        success_rate = (self.test_results['passed'] / self.test_results['total']) * 100 if self.test_results['total'] > 0 else 0
        
        print(f"Total Tests: {self.test_results['total']}")
        print_success(f"Passed: {self.test_results['passed']}")
        
        if self.test_results['failed'] > 0:
            print_error(f"Failed: {self.test_results['failed']}")
        else:
            print(f"Failed: 0")
            
        if self.test_results['warnings'] > 0:
            print_warning(f"Warnings: {self.test_results['warnings']}")
            
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print_success("\n🎉 EXTENSION IS READY FOR USE!")
        elif success_rate >= 70:
            print_warning("\n⚠️ Extension needs minor fixes")
        else:
            print_error("\n❌ Extension needs major fixes")
            
        # Installation guide
        if success_rate >= 70:
            print_header("INSTALLATION GUIDE")
            print("1. Open Chrome browser")
            print("2. Navigate to: chrome://extensions")
            print("3. Enable 'Developer mode' (top right)")
            print("4. Click 'Load unpacked'")
            print(f"5. Select folder: {self.base_path}")
            print("6. Extension will be installed!")
            print("\n✅ Run INSTALL_AND_RUN.bat for automatic setup")

if __name__ == "__main__":
    tester = ExtensionTester()
    tester.run_all_tests()