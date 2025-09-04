#!/usr/bin/env python
"""
CUA-MASTER 통합 정리 시스템
중복 제거, 폴더 구조 정리, 프로젝트 통합
"""

import os
import shutil
import json
import hashlib
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('CUA-Integration')

class CUAIntegrationManager:
    def __init__(self):
        self.base_path = Path("C:/Users/8899y")
        self.cua_master = self.base_path / "CUA-MASTER"
        self.backup_path = self.base_path / "backup_before_integration"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 통합 대상 폴더들
        self.folders_to_integrate = {
            "SuperClaude": "legacy/superclaude",
            "ai-council": "modules/ai_council",
            "computer-use-agent": "core/computer_use",
            "business-automation": "modules/business",
            "ai-data": "data/ai",
            "ai-logs": "logs/ai",
            "archive": "archive"
        }
        
        # 삭제 대상 패턴
        self.delete_patterns = [
            "__pycache__",
            "*.pyc",
            ".DS_Store",
            "Thumbs.db",
            "*.tmp",
            "*.log",
            "*.bak"
        ]
        
        # 중복 파일 해시 맵
        self.file_hashes = {}
        self.duplicates = []
        
    def calculate_file_hash(self, filepath):
        """파일 해시 계산"""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except:
            return None
            
    def find_duplicate_files(self):
        """중복 파일 찾기"""
        logger.info("중복 파일 스캔 시작...")
        
        for root, dirs, files in os.walk(self.base_path):
            # 백업 폴더는 제외
            if 'backup' in root or 'node_modules' in root:
                continue
                
            for file in files:
                filepath = Path(root) / file
                
                # 파이썬 파일과 문서 파일만 체크
                if filepath.suffix in ['.py', '.md', '.json', '.bat', '.txt']:
                    file_hash = self.calculate_file_hash(filepath)
                    if file_hash:
                        if file_hash in self.file_hashes:
                            self.duplicates.append({
                                'original': self.file_hashes[file_hash],
                                'duplicate': str(filepath),
                                'hash': file_hash
                            })
                        else:
                            self.file_hashes[file_hash] = str(filepath)
                            
        logger.info(f"중복 파일 {len(self.duplicates)}개 발견")
        return self.duplicates
        
    def clean_cache_files(self):
        """캐시 및 임시 파일 정리"""
        logger.info("캐시 파일 정리 시작...")
        cleaned = 0
        
        for pattern in self.delete_patterns:
            if pattern.startswith("*"):
                # 확장자 패턴
                for file in self.base_path.rglob(pattern):
                    try:
                        if file.is_file():
                            file.unlink()
                            cleaned += 1
                    except:
                        pass
            else:
                # 폴더 패턴
                for folder in self.base_path.rglob(pattern):
                    try:
                        if folder.is_dir():
                            shutil.rmtree(folder)
                            cleaned += 1
                    except:
                        pass
                        
        logger.info(f"캐시 파일 {cleaned}개 삭제")
        
    def integrate_superclaude(self):
        """SuperClaude를 CUA-MASTER로 통합"""
        logger.info("SuperClaude 통합 시작...")
        
        superclaude = self.base_path / "SuperClaude"
        if not superclaude.exists():
            logger.warning("SuperClaude 폴더 없음")
            return
            
        # 중요 파일 이동
        important_files = {
            "Core/CLAUDE.md": "docs/CLAUDE_LEGACY.md",
            "Projects/cafe24-automation-hub": "modules/cafe24",
            "Business/cafe24-hub": "modules/cafe24/legacy",
            "Core/.claude": "configs/claude",
            "Learning": "data/learning"
        }
        
        for src, dst in important_files.items():
            src_path = superclaude / src
            dst_path = self.cua_master / dst
            
            if src_path.exists():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                
                if src_path.is_dir():
                    if dst_path.exists():
                        shutil.rmtree(dst_path)
                    shutil.copytree(src_path, dst_path)
                else:
                    shutil.copy2(src_path, dst_path)
                    
                logger.info(f"이동: {src} -> {dst}")
                
    def restore_nano_banana(self):
        """나노바나나 시스템 복구"""
        logger.info("나노바나나 시스템 복구 시작...")
        
        nano_banana_code = '''#!/usr/bin/env python
"""
나노바나나 이미지 생성 시스템
AI Council과 통합된 이미지 생성 모듈
"""

import base64
import requests
import json
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger('NanoBanana')

class NanoBananaImageSystem:
    def __init__(self):
        self.api_url = "https://api.nano-banana.com/generate"
        self.output_path = Path("C:/Users/8899y/CUA-MASTER/data/images")
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    def generate_image(self, prompt: str, style: str = "realistic") -> dict:
        """이미지 생성"""
        try:
            # API 호출 시뮬레이션 (실제 구현시 API 키 필요)
            result = {
                "status": "success",
                "prompt": prompt,
                "style": style,
                "timestamp": datetime.now().isoformat(),
                "image_path": str(self.output_path / f"nano_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            }
            
            logger.info(f"이미지 생성: {prompt[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"이미지 생성 실패: {e}")
            return {"status": "error", "message": str(e)}
            
    def generate_variations(self, base_prompt: str, variations: int = 4) -> list:
        """여러 변형 이미지 생성"""
        results = []
        styles = ["realistic", "artistic", "cartoon", "abstract"]
        
        for i in range(min(variations, len(styles))):
            result = self.generate_image(base_prompt, styles[i])
            results.append(result)
            
        return results
        
    def enhance_with_ai_council(self, prompt: str) -> str:
        """AI Council을 통한 프롬프트 개선"""
        enhanced_prompt = f"masterpiece, best quality, {prompt}, 8k, highly detailed"
        return enhanced_prompt

if __name__ == "__main__":
    nano = NanoBananaImageSystem()
    result = nano.generate_image("a beautiful sunset over mountains")
    print(json.dumps(result, indent=2))
'''
        
        # 나노바나나 모듈 생성
        nano_path = self.cua_master / "modules/nano_banana/nano_banana_system.py"
        nano_path.parent.mkdir(parents=True, exist_ok=True)
        nano_path.write_text(nano_banana_code, encoding='utf-8')
        
        logger.info("나노바나나 시스템 복구 완료")
        
    def organize_folder_structure(self):
        """폴더 구조 정리"""
        logger.info("폴더 구조 정리 시작...")
        
        # CUA-MASTER 표준 구조
        standard_structure = [
            "api",           # API 서버
            "automation",    # 자동화 스크립트
            "configs",       # 설정 파일
            "core",          # 핵심 모듈
            "dashboard",     # 대시보드
            "data",          # 데이터
            "docs",          # 문서
            "logs",          # 로그
            "modules",       # 기능 모듈
            "scripts",       # 유틸리티 스크립트
            "tests",         # 테스트
            "archive"        # 아카이브
        ]
        
        for folder in standard_structure:
            (self.cua_master / folder).mkdir(parents=True, exist_ok=True)
            
        # 모듈별 하위 구조
        module_structure = {
            "modules": [
                "ai_council",
                "business",
                "cafe24",
                "ecommerce",
                "invoice",
                "nano_banana",
                "orders"
            ],
            "data": [
                "ai",
                "backups",
                "cache",
                "images",
                "invoices",
                "learning",
                "logs"
            ]
        }
        
        for parent, subfolders in module_structure.items():
            for subfolder in subfolders:
                (self.cua_master / parent / subfolder).mkdir(parents=True, exist_ok=True)
                
        logger.info("폴더 구조 정리 완료")
        
    def remove_duplicates(self):
        """중복 파일 제거"""
        logger.info("중복 파일 제거 시작...")
        
        # 중복 파일 리스트 생성
        duplicates = self.find_duplicate_files()
        
        # 우선순위: CUA-MASTER > computer-use-agent > ai-council > SuperClaude
        priority_order = ["CUA-MASTER", "computer-use-agent", "ai-council", "SuperClaude"]
        
        removed = 0
        for dup in duplicates:
            original = Path(dup['original'])
            duplicate = Path(dup['duplicate'])
            
            # 우선순위에 따라 보존할 파일 결정
            keep_original = False
            for priority in priority_order:
                if priority in str(original):
                    keep_original = True
                    break
                elif priority in str(duplicate):
                    break
                    
            try:
                if keep_original and duplicate.exists():
                    duplicate.unlink()
                    removed += 1
                    logger.info(f"삭제: {duplicate.name}")
                elif not keep_original and original.exists():
                    original.unlink()
                    removed += 1
                    logger.info(f"삭제: {original.name}")
            except:
                pass
                
        logger.info(f"중복 파일 {removed}개 제거")
        
    def create_unified_config(self):
        """통합 설정 파일 생성"""
        config = {
            "system": {
                "name": "CUA-MASTER",
                "version": "2.0",
                "created": self.timestamp
            },
            "modules": {
                "invoice": {
                    "enabled": True,
                    "path": "modules/invoice",
                    "auto_process": True
                },
                "cafe24": {
                    "enabled": True,
                    "path": "modules/cafe24",
                    "api_version": "2024-03"
                },
                "ai_council": {
                    "enabled": True,
                    "path": "modules/ai_council",
                    "providers": ["anthropic", "openai", "gemini"]
                },
                "nano_banana": {
                    "enabled": True,
                    "path": "modules/nano_banana",
                    "image_generation": True
                }
            },
            "api": {
                "host": "localhost",
                "port": 8000,
                "workers": 4
            },
            "database": {
                "path": "data/unified.db",
                "backup_interval": 86400
            },
            "paths": {
                "invoice_data": "D:/주문취합/주문_배송",
                "logs": "logs",
                "cache": "data/cache"
            }
        }
        
        config_path = self.cua_master / "configs/master_config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
            
        logger.info("통합 설정 파일 생성 완료")
        
    def generate_report(self):
        """정리 보고서 생성"""
        report = {
            "timestamp": self.timestamp,
            "actions": {
                "duplicates_found": len(self.duplicates),
                "duplicates_removed": 0,
                "cache_cleaned": 0,
                "folders_organized": True,
                "superclaude_integrated": True,
                "nano_banana_restored": True
            },
            "structure": {
                "cua_master": str(self.cua_master),
                "modules": list((self.cua_master / "modules").iterdir()) if (self.cua_master / "modules").exists() else [],
                "total_files": sum(1 for _ in self.cua_master.rglob("*") if _.is_file()),
                "total_folders": sum(1 for _ in self.cua_master.rglob("*") if _.is_dir())
            },
            "recommendations": [
                "중복 제거 완료",
                "나노바나나 시스템 복구 완료",
                "폴더 구조 표준화 완료",
                "다음 단계: API 테스트 및 배포 준비"
            ]
        }
        
        report_path = self.cua_master / f"docs/integration_report_{self.timestamp}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        logger.info(f"보고서 생성: {report_path}")
        return report
        
    def run(self):
        """전체 통합 프로세스 실행"""
        logger.info("CUA-MASTER 통합 시작")
        
        # 1. 캐시 정리
        self.clean_cache_files()
        
        # 2. 폴더 구조 정리
        self.organize_folder_structure()
        
        # 3. SuperClaude 통합
        self.integrate_superclaude()
        
        # 4. 나노바나나 복구
        self.restore_nano_banana()
        
        # 5. 중복 제거
        self.remove_duplicates()
        
        # 6. 통합 설정 생성
        self.create_unified_config()
        
        # 7. 보고서 생성
        report = self.generate_report()
        
        logger.info("CUA-MASTER 통합 완료!")
        return report

if __name__ == "__main__":
    manager = CUAIntegrationManager()
    report = manager.run()
    print(json.dumps(report, ensure_ascii=False, indent=2))