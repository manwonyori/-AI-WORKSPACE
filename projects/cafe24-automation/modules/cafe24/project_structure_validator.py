#!/usr/bin/env python3
"""
Cafe24 Project Structure Validator
정리된 프로젝트 구조가 올바른지 검증하는 스크립트

작성일: 2025-09-01
목적: 아카이빙 후 프로젝트 구조 검증
"""

import os
from pathlib import Path
import json
import datetime

def validate_project_structure():
    """프로젝트 구조 검증"""
    base_path = Path(__file__).parent
    
    print("=== Cafe24 프로젝트 구조 검증 ===")
    print(f"검증일: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"기준 경로: {base_path}")
    print()
    
    # 검증할 핵심 요소들
    validation_results = {
        'core_scripts': [],
        'config_files': [],
        'folder_structure': [],
        'archive_status': [],
        'missing_items': []
    }
    
    # 1. 핵심 스크립트 확인
    core_scripts = [
        'scripts/sftp_downloader.py',
        'scripts/image_matching_verification.py',
        'scripts/extract_image_links.py',
        'scripts/quick_status.py',
        'scripts/verified_downloader.py'
    ]
    
    print("1. 핵심 스크립트 확인:")
    for script in core_scripts:
        script_path = base_path / script
        if script_path.exists():
            print(f"   [OK] {script}")
            validation_results['core_scripts'].append(script)
        else:
            print(f"   [MISSING] {script}")
            validation_results['missing_items'].append(script)
    
    # 2. 설정 파일 확인
    config_files = [
        'FTP_CONFIG.json',
        'ftp_mirror/download_mapping.json',
        'requirements.txt'
    ]
    
    print("\n2. 설정 파일 확인:")
    for config in config_files:
        config_path = base_path / config
        if config_path.exists():
            print(f"   [OK] {config}")
            validation_results['config_files'].append(config)
        else:
            print(f"   [MISSING] {config}")
            validation_results['missing_items'].append(config)
    
    # 3. 폴더 구조 확인
    required_folders = [
        'scripts',
        'config', 
        'ftp_mirror',
        'complete_content',
        'utils',
        f'archive_{datetime.datetime.now().strftime("%Y%m%d")}'
    ]
    
    print("\n3. 폴더 구조 확인:")
    for folder in required_folders:
        folder_path = base_path / folder
        if folder_path.exists() and folder_path.is_dir():
            print(f"   [OK] {folder}/")
            validation_results['folder_structure'].append(folder)
        else:
            print(f"   [MISSING] {folder}/")
            validation_results['missing_items'].append(f"{folder}/")
    
    # 4. 아카이브 상태 확인
    archive_folder = base_path / f'archive_{datetime.datetime.now().strftime("%Y%m%d")}'
    
    print("\n4. 아카이브 상태 확인:")
    if archive_folder.exists():
        archive_items = ['test_files', 'temp_files', 'backup_folders', 'archive_report.html']
        for item in archive_items:
            item_path = archive_folder / item
            if item_path.exists():
                print(f"   [OK] archive/{item}")
                validation_results['archive_status'].append(item)
            else:
                print(f"   [MISSING] archive/{item}")
                validation_results['missing_items'].append(f"archive/{item}")
    else:
        print(f"   [MISSING] 아카이브 폴더 없음")
        validation_results['missing_items'].append("archive_folder")
    
    # 5. 문서 파일 확인
    docs = ['README.md', 'FINAL_STATUS_REPORT.md', 'SUCCESSFUL_FORMULA_20250831.md']
    
    print("\n5. 문서 파일 확인:")
    for doc in docs:
        doc_path = base_path / doc
        if doc_path.exists():
            print(f"   [OK] {doc}")
        else:
            print(f"   [MISSING] {doc}")
            validation_results['missing_items'].append(doc)
    
    # 6. 검증 결과 요약
    print("\n" + "="*50)
    print("검증 결과 요약:")
    print(f"[OK] 핵심 스크립트: {len(validation_results['core_scripts'])}/5개")
    print(f"[OK] 설정 파일: {len(validation_results['config_files'])}/3개")  
    print(f"[OK] 폴더 구조: {len(validation_results['folder_structure'])}/6개")
    print(f"[OK] 아카이브 상태: {len(validation_results['archive_status'])}/4개")
    
    if validation_results['missing_items']:
        print(f"\n[MISSING] 누락된 항목들:")
        for item in validation_results['missing_items']:
            print(f"   - {item}")
    else:
        print(f"\n[SUCCESS] 모든 검증 항목 통과!")
    
    # 검증 결과 JSON 저장
    validation_results['timestamp'] = datetime.datetime.now().isoformat()
    validation_results['base_path'] = str(base_path)
    validation_results['total_missing'] = len(validation_results['missing_items'])
    validation_results['validation_passed'] = len(validation_results['missing_items']) == 0
    
    with open(base_path / 'structure_validation_report.json', 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[REPORT] 상세 검증 보고서: structure_validation_report.json")
    
    return validation_results['validation_passed']

def check_file_counts():
    """파일 개수 통계"""
    base_path = Path(__file__).parent
    
    print("\n" + "="*50)
    print("파일 통계:")
    
    stats = {}
    
    # scripts 폴더
    scripts_path = base_path / 'scripts'
    if scripts_path.exists():
        scripts_count = len(list(scripts_path.glob('*.py')))
        stats['scripts'] = scripts_count
        print(f"Scripts 폴더: {scripts_count}개 Python 파일")
    
    # complete_content 폴더
    content_path = base_path / 'complete_content' / 'html'
    if content_path.exists():
        html_count = len(list(content_path.rglob('*.html')))
        stats['html_files'] = html_count
        print(f"HTML 파일: {html_count}개")
    
    # images 폴더
    images_path = base_path / 'complete_content' / 'images'  
    if images_path.exists():
        image_count = len(list(images_path.rglob('*.jpg'))) + len(list(images_path.rglob('*.png')))
        stats['image_files'] = image_count
        print(f"이미지 파일: {image_count}개")
    
    # 아카이브 폴더
    archive_path = base_path / f'archive_{datetime.datetime.now().strftime("%Y%m%d")}'
    if archive_path.exists():
        archive_count = len(list(archive_path.rglob('*')))
        stats['archived_items'] = archive_count
        print(f"아카이브된 항목: {archive_count}개")
    
    return stats

if __name__ == "__main__":
    # 구조 검증
    validation_passed = validate_project_structure()
    
    # 파일 통계
    file_stats = check_file_counts()
    
    # 최종 결과
    print("\n" + "="*50)
    if validation_passed:
        print("[SUCCESS] 프로젝트 구조 검증 완료!")
        print("[OK] 모든 핵심 파일과 폴더가 올바르게 정리되었습니다.")
    else:
        print("[WARNING] 일부 항목이 누락되었습니다.")
        print("[INFO] structure_validation_report.json 파일을 확인하세요.")
    
    print(f"\n[INFO] 검증 완료: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")