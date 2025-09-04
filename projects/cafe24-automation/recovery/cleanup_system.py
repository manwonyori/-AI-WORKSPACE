#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
시스템 정리 및 통합 스크립트
중복 제거, 보안 처리, 구조 최적화
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import hashlib

class SystemCleaner:
    """시스템 정리 도구"""
    
    def __init__(self):
        self.base_dir = Path("C:/Users/8899y")
        self.backup_dir = self.base_dir / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.report = {
            "시작시간": datetime.now().isoformat(),
            "삭제된_파일": [],
            "이동된_파일": [],
            "통합된_DB": [],
            "보안_처리": []
        }
    
    def create_backup(self):
        """중요 파일 백업"""
        print("백업 생성 중...")
        
        important_files = [
            "SuperClaude/main.py",
            "korean-ecommerce-specialist/README.md",
            "mart-project/src/main.py",
            "ai-council/integration_config.py"
        ]
        
        self.backup_dir.mkdir(exist_ok=True)
        
        for file_path in important_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                dest = self.backup_dir / file_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(full_path, dest)
                print(f"백업: {file_path}")
    
    def remove_dangerous_files(self):
        """보안 위험 파일 제거"""
        print("\n보안 위험 파일 제거 중...")
        
        dangerous_patterns = [
            "system_backups/*.py",
            "Desktop/key.md",
            "**/key.md",
            "**/*_api_keys*.json",
            "**/*credentials*.json"
        ]
        
        for pattern in dangerous_patterns:
            for file in self.base_dir.glob(pattern):
                if file.exists():
                    try:
                        file.unlink()
                        self.report["보안_처리"].append(str(file))
                        print(f"삭제: {file.name}")
                    except:
                        print(f"삭제 실패: {file}")
    
    def clean_duplicate_folders(self):
        """중복/잘못된 폴더 정리"""
        print("\n중복 폴더 정리 중...")
        
        wrong_folders = [
            "CUsers8899ySuperClaudebackup_20250826",
            "CUsers8899ySuperClaudeconfig",
            "CUsers8899ySuperClaudecore",
            "CUsers8899ySuperClaudemodules",
            "CUsers8899ySuperClaudemodulesbusiness",
            "CUsers8899ySuperClaudemodulescafe24",
            "CUsers8899ySuperClaudemodulesintegration",
            "CUsers8899ySuperClaudemoduleslearning",
            "CUsers8899ySuperClaudemodulesoptimization",
            "CUsers8899ySuperClaudemodulesstartup",
            "CUsers8899ySuperClaudemodulestracking",
            "CUsers8899ySuperClaudescripts",
            "CUsers8899yai-logs",
            "SuperClaude_backup_20250828_100957"
        ]
        
        for folder in wrong_folders:
            folder_path = self.base_dir / folder
            if folder_path.exists():
                try:
                    shutil.rmtree(folder_path)
                    self.report["삭제된_파일"].append(str(folder_path))
                    print(f"삭제: {folder}")
                except:
                    print(f"삭제 실패: {folder}")
    
    def consolidate_databases(self):
        """분산된 데이터베이스 통합"""
        print("\n데이터베이스 통합 중...")
        
        # 통합 DB 디렉토리
        unified_db_dir = self.base_dir / "unified_data"
        unified_db_dir.mkdir(exist_ok=True)
        
        db_mappings = {
            "learning_unified.db": [
                "SuperClaude/data/learning_system.db",
                "SuperClaude/ai-learning-data/learning_system.db",
                "ai-data/ultimate_superclaude.db"
            ],
            "category_unified.db": [
                "SuperClaude/data/category_learning.db",
                "SuperClaude/data/manwonyori_categories.db"
            ],
            "tracking_unified.db": [
                "SuperClaude/data/tracking_database.db"
            ]
        }
        
        for unified_name, source_dbs in db_mappings.items():
            unified_path = unified_db_dir / unified_name
            
            for db_path in source_dbs:
                full_path = self.base_dir / db_path
                if full_path.exists():
                    if not unified_path.exists():
                        shutil.copy2(full_path, unified_path)
                        print(f"통합 DB 생성: {unified_name}")
                    self.report["통합된_DB"].append(str(full_path))
    
    def remove_duplicate_files(self):
        """중복 파일 제거"""
        print("\n중복 파일 제거 중...")
        
        file_hashes = {}
        duplicates = []
        
        # 주요 프로젝트 폴더만 검사
        check_dirs = [
            "SuperClaude",
            "korean-ecommerce-specialist",
            "mart-project",
            "ai-council"
        ]
        
        for dir_name in check_dirs:
            dir_path = self.base_dir / dir_name
            if not dir_path.exists():
                continue
                
            for file_path in dir_path.rglob("*.py"):
                if file_path.is_file():
                    # 파일 해시 계산
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash in file_hashes:
                        duplicates.append(str(file_path))
                    else:
                        file_hashes[file_hash] = str(file_path)
        
        # 중복 파일 제거 (백업 폴더의 파일 우선 제거)
        for dup_file in duplicates:
            if 'backup' in dup_file or 'old' in dup_file:
                try:
                    Path(dup_file).unlink()
                    self.report["삭제된_파일"].append(dup_file)
                    print(f"중복 제거: {Path(dup_file).name}")
                except:
                    pass
    
    def create_unified_structure(self):
        """통합 구조 생성"""
        print("\n통합 구조 생성 중...")
        
        # 통합 설정 파일
        unified_config = {
            "projects": {
                "ai-council": {
                    "path": "ai-council",
                    "status": "active",
                    "features": ["AI 협의회", "의사결정", "품질개선"]
                },
                "superclaude": {
                    "path": "SuperClaude",
                    "status": "active",
                    "features": ["자율학습", "패턴인식", "진화"]
                },
                "korean-ecommerce": {
                    "path": "korean-ecommerce-specialist",
                    "status": "active",
                    "features": ["키워드", "가격최적화", "SEO"]
                },
                "mart-project": {
                    "path": "mart-project",
                    "status": "active",
                    "features": ["발주관리", "공급망", "OCR"]
                }
            },
            "database": {
                "learning": "unified_data/learning_unified.db",
                "category": "unified_data/category_unified.db",
                "tracking": "unified_data/tracking_unified.db"
            },
            "security": {
                "api_keys": ".env",
                "backup": str(self.backup_dir)
            }
        }
        
        config_path = self.base_dir / "UNIFIED_CONFIG.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(unified_config, f, indent=2, ensure_ascii=False)
        
        print(f"통합 설정 생성: UNIFIED_CONFIG.json")
    
    def generate_report(self):
        """정리 보고서 생성"""
        self.report["종료시간"] = datetime.now().isoformat()
        self.report["요약"] = {
            "삭제된_파일_수": len(self.report["삭제된_파일"]),
            "보안_처리_수": len(self.report["보안_처리"]),
            "통합된_DB_수": len(self.report["통합된_DB"])
        }
        
        report_path = self.base_dir / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n정리 보고서: {report_path}")
        print(f"삭제된 파일: {self.report['요약']['삭제된_파일_수']}개")
        print(f"보안 처리: {self.report['요약']['보안_처리_수']}개")
        print(f"통합된 DB: {self.report['요약']['통합된_DB_수']}개")

def main():
    """메인 실행"""
    print("="*60)
    print("시스템 정리 및 통합 시작")
    print("="*60)
    
    cleaner = SystemCleaner()
    
    # 1. 백업 생성
    cleaner.create_backup()
    
    # 2. 보안 위험 제거
    cleaner.remove_dangerous_files()
    
    # 3. 중복 폴더 정리
    cleaner.clean_duplicate_folders()
    
    # 4. 데이터베이스 통합
    cleaner.consolidate_databases()
    
    # 5. 중복 파일 제거
    cleaner.remove_duplicate_files()
    
    # 6. 통합 구조 생성
    cleaner.create_unified_structure()
    
    # 7. 보고서 생성
    cleaner.generate_report()
    
    print("\n" + "="*60)
    print("시스템 정리 완료!")
    print("="*60)

if __name__ == "__main__":
    main()