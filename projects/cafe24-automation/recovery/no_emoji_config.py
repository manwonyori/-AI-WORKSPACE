#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이모지 제거 및 시스템 설정 스크립트
전체 시스템에서 이모지를 생성하지 않도록 설정
"""

import os
import json
import re
from pathlib import Path

def remove_emojis_from_settings():
    """Claude 설정에서 이모지 제거"""
    settings_file = Path.home() / ".claude" / "settings.json"
    
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # hooks에서 이모지 제거
        if 'hooks' in settings:
            for hook_type, hooks in settings['hooks'].items():
                for hook_group in hooks:
                    if 'hooks' in hook_group:
                        for hook in hook_group['hooks']:
                            if 'command' in hook:
                                # 이모지 패턴 제거
                                hook['command'] = re.sub(r'[]', '', hook['command'])
                                # ULTIMATE 기반 제거
                                hook['command'] = hook['command'].replace('ULTIMATE 기반, ', '')
                                hook['command'] = hook['command'].replace(', ULTIMATE 기반', '')
        
        # 설정 저장
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        print("Claude 설정에서 이모지 및 ULTIMATE 제거 완료")

def remove_emojis_from_python_files():
    """Python 파일들에서 이모지 제거"""
    current_dir = Path.cwd()
    
    # Python 파일 찾기
    python_files = list(current_dir.glob('**/*.py'))
    
    emoji_pattern = r'[]'
    
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 이모지가 있는지 확인
            if re.search(emoji_pattern, content):
                # 이모지 제거
                new_content = re.sub(emoji_pattern + r'\s*', '', content)
                
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"이모지 제거: {py_file}")
        
        except Exception as e:
            print(f"처리 실패 {py_file}: {e}")

def set_no_emoji_environment():
    """환경 변수 설정"""
    os.environ['NO_EMOJI'] = 'true'
    os.environ['CLAUDE_NO_EMOJI'] = 'true'
    print("환경 변수 설정 완료")

if __name__ == "__main__":
    print("=== 이모지 제거 및 설정 시작 ===")
    
    # 1. Claude 설정 수정
    remove_emojis_from_settings()
    
    # 2. Python 파일 수정
    remove_emojis_from_python_files()
    
    # 3. 환경 변수 설정
    set_no_emoji_environment()
    
    print("=== 완료 ===")
    print("다음 Claude 세션부터 이모지가 생성되지 않습니다.")