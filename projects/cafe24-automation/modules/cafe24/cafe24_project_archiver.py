#!/usr/bin/env python3
"""
Cafe24 Project Archiver
체계적으로 프로젝트 파일들을 정리하고 아카이빙하는 스크립트

작성일: 2025-08-31
목적: Cafe24 프로젝트의 모든 파일을 정리하고 성공적인 워크플로우만 유지
"""

import os
import shutil
import json
import datetime
from pathlib import Path
import logging

class Cafe24ProjectArchiver:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.archive_date = datetime.datetime.now().strftime("%Y%m%d")
        self.archive_folder = self.base_path / f"archive_{self.archive_date}"
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_path / f'archiver_{self.archive_date}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 핵심 유지 파일들 정의
        self.core_files = {
            'scripts': [
                'sftp_downloader.py',
                'image_matching_verification.py', 
                'extract_image_links.py',
                'verified_downloader.py',
                'quick_status.py',
                'restart_download.py',
                'run_cua.py'
            ],
            'config': [
                'FTP_CONFIG.json',
                'requirements.txt'
            ],
            'data': [
                'download_mapping.json'
            ],
            'docs': [
                'FINAL_STATUS_REPORT.md',
                'SUCCESSFUL_FORMULA_20250831.md',
                'README.md',
                'FTP_DOWNLOAD_GUIDE.md'
            ]
        }
        
        # 아카이브 대상 파일/폴더 패턴
        self.archive_patterns = {
            'temp_files': [
                'retry_list.json',
                '*.log',
                'autonomous_workflow.log',
                'nul'
            ],
            'test_files': [
                'test_*.py',
                'quick_test.py',
                '*_test.py'
            ],
            'old_versions': [
                '*_v2.py',
                '*_old.py',
                'enhanced_*.py'
            ],
            'backup_folders': [
                'backup',
                'test_output',
                'bulk_processing_output',
                'advanced_editing_output'
            ]
        }

    def create_archive_structure(self):
        """아카이브 폴더 구조 생성"""
        self.logger.info(f"아카이브 폴더 생성: {self.archive_folder}")
        
        archive_subdirs = [
            'completed_scripts',
            'temp_files', 
            'old_versions',
            'test_files',
            'backup_folders',
            'reports'
        ]
        
        for subdir in archive_subdirs:
            (self.archive_folder / subdir).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"생성됨: {subdir}")

    def analyze_current_structure(self):
        """현재 프로젝트 구조 분석"""
        self.logger.info("현재 프로젝트 구조 분석 중...")
        
        analysis = {
            'total_files': 0,
            'directories': [],
            'file_sizes': {},
            'file_types': {},
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        for root, dirs, files in os.walk(self.base_path):
            rel_path = os.path.relpath(root, self.base_path)
            if not rel_path.startswith('archive_'):  # 기존 아카이브 폴더 제외
                analysis['directories'].append(rel_path)
                
                for file in files:
                    file_path = Path(root) / file
                    if file_path.exists():
                        analysis['total_files'] += 1
                        size = file_path.stat().st_size
                        analysis['file_sizes'][str(file_path.relative_to(self.base_path))] = size
                        
                        ext = file_path.suffix.lower()
                        analysis['file_types'][ext] = analysis['file_types'].get(ext, 0) + 1
        
        # 분석 결과 저장
        with open(self.archive_folder / 'structure_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"총 {analysis['total_files']}개 파일 분석 완료")
        return analysis

    def move_temp_files(self):
        """임시 파일들 아카이브로 이동"""
        self.logger.info("임시 파일들 아카이브 중...")
        moved_count = 0
        
        # 현재 실행 중인 로그 파일 제외
        current_log = f"archiver_{self.archive_date}.log"
        
        for pattern in self.archive_patterns['temp_files']:
            files = list(self.base_path.glob(pattern))
            for file_path in files:
                if file_path.is_file() and file_path.name != current_log:
                    try:
                        dest = self.archive_folder / 'temp_files' / file_path.name
                        shutil.move(str(file_path), str(dest))
                        self.logger.info(f"이동됨: {file_path.name}")
                        moved_count += 1
                    except PermissionError:
                        self.logger.warning(f"이동 불가 (사용 중): {file_path.name}")
                    except Exception as e:
                        self.logger.error(f"이동 실패 {file_path.name}: {e}")
        
        return moved_count

    def move_test_files(self):
        """테스트 파일들 아카이브로 이동"""
        self.logger.info("테스트 파일들 아카이브 중...")
        moved_count = 0
        
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if any(file.startswith(prefix) for prefix in ['test_', 'quick_test']):
                    file_path = Path(root) / file
                    if not str(file_path).startswith(str(self.archive_folder)):
                        try:
                            dest = self.archive_folder / 'test_files' / file
                            shutil.move(str(file_path), str(dest))
                            self.logger.info(f"이동됨: {file}")
                            moved_count += 1
                        except PermissionError:
                            self.logger.warning(f"이동 불가 (사용 중): {file}")
                        except Exception as e:
                            self.logger.error(f"이동 실패 {file}: {e}")
        
        return moved_count

    def move_backup_folders(self):
        """백업 폴더들 아카이브로 이동"""
        self.logger.info("백업 폴더들 아카이브 중...")
        moved_count = 0
        
        for folder_name in self.archive_patterns['backup_folders']:
            folder_path = self.base_path / folder_name
            if folder_path.exists() and folder_path.is_dir():
                try:
                    dest = self.archive_folder / 'backup_folders' / folder_name
                    shutil.move(str(folder_path), str(dest))
                    self.logger.info(f"폴더 이동됨: {folder_name}")
                    moved_count += 1
                except PermissionError:
                    self.logger.warning(f"폴더 이동 불가 (사용 중): {folder_name}")
                except Exception as e:
                    self.logger.error(f"폴더 이동 실패 {folder_name}: {e}")
        
        return moved_count

    def organize_core_structure(self):
        """핵심 폴더 구조 정리"""
        self.logger.info("핵심 폴더 구조 정리 중...")
        
        # 새로운 폴더 구조 생성
        core_structure = {
            'scripts': self.base_path / 'scripts',
            'config': self.base_path / 'config', 
            'docs': self.base_path / 'docs',
            'html': self.base_path / 'html',
            'ftp_mirror': self.base_path / 'ftp_mirror',
            'utils': self.base_path / 'utils'
        }
        
        for folder_name, folder_path in core_structure.items():
            folder_path.mkdir(exist_ok=True)
            self.logger.info(f"핵심 폴더 확인/생성: {folder_name}")
        
        # 핵심 스크립트들을 scripts 폴더로 이동 (이미 있지 않다면)
        for script in self.core_files['scripts']:
            src = self.base_path / script
            if src.exists():
                dest = core_structure['scripts'] / script
                if not dest.exists():
                    shutil.move(str(src), str(dest))
                    self.logger.info(f"스크립트 이동: {script}")

    def update_documentation(self):
        """문서 업데이트"""
        self.logger.info("문서 업데이트 중...")
        
        # README.md 업데이트
        readme_content = f"""# Cafe24 자동화 프로젝트

## 프로젝트 개요
Cafe24 쇼핑몰의 상품 정보 수집 및 관리를 위한 자동화 시스템

## 프로젝트 정리일: {self.archive_date}

## 폴더 구조
```
cafe24/
├── scripts/           # 핵심 실행 스크립트
├── config/            # 설정 파일들
├── docs/              # 문서 파일들
├── html/              # HTML 파일들
├── ftp_mirror/        # FTP 다운로드 데이터
├── utils/             # 유틸리티 스크립트들
└── archive_{self.archive_date}/  # 아카이브된 파일들
```

## 핵심 스크립트
- **sftp_downloader.py**: SFTP를 통한 파일 다운로드 (메인 스크립트)
- **image_matching_verification.py**: 이미지 매칭 검증
- **extract_image_links.py**: HTML에서 이미지 링크 추출
- **verified_downloader.py**: 검증된 다운로더
- **quick_status.py**: 빠른 상태 확인

## 성공 워크플로우
1. FTP_CONFIG.json 설정 확인
2. sftp_downloader.py 실행으로 파일 다운로드
3. extract_image_links.py로 이미지 링크 추출
4. image_matching_verification.py로 검증
5. quick_status.py로 상태 확인

## 설정 파일
- **FTP_CONFIG.json**: FTP 접속 정보
- **download_mapping.json**: 다운로드 매핑 데이터
- **requirements.txt**: Python 패키지 의존성

## 사용법
```bash
python scripts/sftp_downloader.py
python scripts/quick_status.py
```

## 아카이브 정보
- 아카이브 날짜: {self.archive_date}
- 임시 파일, 테스트 파일, 백업 폴더들이 archive_{self.archive_date}/ 폴더로 이동됨
"""
        
        with open(self.base_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 최종 상태 보고서 업데이트
        status_report = f"""# Cafe24 프로젝트 최종 상태 보고서

## 업데이트 날짜: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 프로젝트 정리 완료
- 아카이브 폴더: archive_{self.archive_date}
- 핵심 파일들만 메인 폴더에 유지
- 불필요한 임시 파일들 정리 완료

## 성공적인 워크플로우 확정
1. SFTP 다운로드 시스템 완성
2. 이미지 매칭 검증 시스템 구축
3. 자동화된 상태 확인 시스템

## 핵심 성과
- 안정적인 FTP/SFTP 다운로드 시스템 구축
- 이미지 매칭 및 검증 시스템 완성
- HTML 콘텐츠 관리 시스템 구축
- 자동화된 모니터링 시스템

## 유지보수 가이드
- 정기적인 다운로드 상태 확인: quick_status.py 실행
- 설정 파일 백업 권장: config/ 폴더
- 로그 파일 정기 정리
"""
        
        with open(self.base_path / 'FINAL_STATUS_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(status_report)
        
        self.logger.info("문서 업데이트 완료")

    def generate_archive_report(self, stats):
        """아카이브 보고서 생성"""
        report = {
            'archive_date': self.archive_date,
            'archive_folder': str(self.archive_folder),
            'statistics': stats,
            'core_files_preserved': self.core_files,
            'archive_patterns_used': self.archive_patterns,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        with open(self.archive_folder / 'archive_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # HTML 보고서도 생성
        html_report = f"""<!DOCTYPE html>
<html>
<head>
    <title>Cafe24 Project Archive Report</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .section {{ margin: 20px 0; }}
        .stats {{ background: #f8f9fa; padding: 15px; border-radius: 5px; }}
        .file-list {{ background: #ffffff; border: 1px solid #dee2e6; padding: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Cafe24 프로젝트 아카이브 보고서</h1>
        <p>생성일: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>아카이브 통계</h2>
        <div class="stats">
            <p><strong>임시 파일 이동:</strong> {stats.get('temp_files', 0)}개</p>
            <p><strong>테스트 파일 이동:</strong> {stats.get('test_files', 0)}개</p>
            <p><strong>백업 폴더 이동:</strong> {stats.get('backup_folders', 0)}개</p>
        </div>
    </div>
    
    <div class="section">
        <h2>유지된 핵심 파일들</h2>
        <div class="file-list">
            <h3>스크립트</h3>
            <ul>{"".join(f"<li>{f}</li>" for f in self.core_files['scripts'])}</ul>
            
            <h3>설정 파일</h3>
            <ul>{"".join(f"<li>{f}</li>" for f in self.core_files['config'])}</ul>
            
            <h3>문서</h3>
            <ul>{"".join(f"<li>{f}</li>" for f in self.core_files['docs'])}</ul>
        </div>
    </div>
</body>
</html>"""
        
        with open(self.archive_folder / 'archive_report.html', 'w', encoding='utf-8') as f:
            f.write(html_report)

    def run_archival_process(self):
        """전체 아카이빙 프로세스 실행"""
        self.logger.info(f"Cafe24 프로젝트 아카이빙 시작 - {self.archive_date}")
        
        # 1. 아카이브 구조 생성
        self.create_archive_structure()
        
        # 2. 현재 구조 분석
        analysis = self.analyze_current_structure()
        
        # 3. 파일들 이동
        stats = {}
        stats['temp_files'] = self.move_temp_files()
        stats['test_files'] = self.move_test_files() 
        stats['backup_folders'] = self.move_backup_folders()
        
        # 4. 핵심 구조 정리
        self.organize_core_structure()
        
        # 5. 문서 업데이트
        self.update_documentation()
        
        # 6. 아카이브 보고서 생성
        self.generate_archive_report(stats)
        
        self.logger.info("아카이빙 프로세스 완료!")
        self.logger.info(f"아카이브 폴더: {self.archive_folder}")
        self.logger.info(f"통계: {stats}")
        
        return stats

def main():
    """메인 실행 함수"""
    # 현재 디렉토리에서 실행
    base_path = Path(__file__).parent
    
    print(f"Cafe24 프로젝트 아카이버 시작")
    print(f"대상 경로: {base_path}")
    print(f"아카이브 날짜: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    
    # 자동 실행 모드
    print("\n자동 아카이빙 모드로 진행합니다...")
    
    # 아카이버 실행
    archiver = Cafe24ProjectArchiver(base_path)
    stats = archiver.run_archival_process()
    
    print("\n=== 아카이빙 완료 ===")
    print(f"임시 파일 이동: {stats['temp_files']}개")
    print(f"테스트 파일 이동: {stats['test_files']}개") 
    print(f"백업 폴더 이동: {stats['backup_folders']}개")
    print(f"\n아카이브 폴더: archive_{datetime.datetime.now().strftime('%Y%m%d')}")
    print("README.md와 FINAL_STATUS_REPORT.md가 업데이트되었습니다.")

if __name__ == "__main__":
    main()