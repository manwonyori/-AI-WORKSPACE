"""
Cafe24 상품 관리 전체 워크플로우 실행 스크립트
239개 상품 크롤링 → Google Drive 저장 → 일괄 수정 → 재업로드 자동화
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Optional

# 모듈 import
from product_crawler import Cafe24ProductCrawler
from bulk_editor import Cafe24BulkEditor
from auto_updater import SmartUpdater

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'cafe24_workflow_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Cafe24WorkflowManager:
    """Cafe24 상품 관리 워크플로우 매니저"""
    
    def __init__(self, config_file: str = "config/cafe24_config.json"):
        """초기화"""
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.crawler = None
        self.editor = None
        self.updater = None
        self.workflow_results = {}
        
    def _load_config(self) -> Dict:
        """설정 파일 로드 또는 생성"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 기본 설정 생성
            default_config = {
                "cafe24": {
                    "mall_id": "manwonyori",
                    "admin_url": "https://manwonyori.cafe24.com/admin",
                    "username": "your_username",
                    "password": "your_password"
                },
                "google_drive": {
                    "service_account_file": "path/to/service_account.json",
                    "folder_id": "your_folder_id"
                },
                "workflow": {
                    "crawl_products": True,
                    "save_to_drive": True,
                    "bulk_modify": True,
                    "auto_update": True,
                    "headless_mode": False
                },
                "modification_rules": {
                    "price_increase_percent": 10,
                    "update_images": True,
                    "update_description": True
                }
            }
            
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"기본 설정 파일 생성: {self.config_file}")
            logger.info("cafe24_config.json 파일을 수정하여 실제 정보를 입력하세요")
            return default_config
    
    def step1_crawl_products(self) -> List[Dict]:
        """Step 1: Cafe24에서 상품 크롤링"""
        logger.info("=" * 50)
        logger.info("STEP 1: 상품 크롤링 시작")
        logger.info("=" * 50)
        
        self.crawler = Cafe24ProductCrawler(str(self.config_file))
        self.crawler.init_driver(headless=self.config['workflow']['headless_mode'])
        
        # 로그인
        if not self.crawler.login_cafe24():
            logger.error("Cafe24 로그인 실패")
            return []
        
        # 상품 목록 가져오기
        products = self.crawler.get_product_list()
        logger.info(f"총 {len(products)}개 상품 발견")
        
        # 각 상품의 상세 HTML 크롤링
        for product in products:
            detail = self.crawler.crawl_product_detail(product)
            if detail:
                # 로컬 저장
                file_path = self.crawler.save_product_local(
                    detail['product_code'],
                    detail['detail_html']
                )
                logger.info(f"크롤링 완료: {detail['product_code']}")
        
        self.crawler.cleanup()
        
        self.workflow_results['crawled_products'] = len(products)
        return products
    
    def step2_upload_to_drive(self) -> bool:
        """Step 2: Google Drive에 업로드"""
        logger.info("=" * 50)
        logger.info("STEP 2: Google Drive 업로드")
        logger.info("=" * 50)
        
        # crawler에서 Google Drive 업로드 기능 사용
        self.crawler = Cafe24ProductCrawler(str(self.config_file))
        
        # 크롤링된 파일들 업로드
        crawled_dir = Path("crawled_products")
        if not crawled_dir.exists():
            logger.error("크롤링된 상품 디렉토리가 없습니다")
            return False
        
        uploaded_count = 0
        for html_file in crawled_dir.glob("*.html"):
            file_id = self.crawler.upload_to_drive(html_file)
            if file_id:
                uploaded_count += 1
                logger.info(f"업로드 성공: {html_file.name}")
        
        self.workflow_results['uploaded_files'] = uploaded_count
        logger.info(f"총 {uploaded_count}개 파일 업로드 완료")
        return uploaded_count > 0
    
    def step3_bulk_modify(self) -> List[Dict]:
        """Step 3: HTML 일괄 수정"""
        logger.info("=" * 50)
        logger.info("STEP 3: HTML 일괄 수정")
        logger.info("=" * 50)
        
        self.editor = Cafe24BulkEditor(str(self.config_file))
        
        # Google Drive에서 다운로드
        products = self.editor.download_from_drive()
        logger.info(f"{len(products)}개 상품 다운로드 완료")
        
        # 일괄 수정 수행
        modified = self.editor.modify_html_batch(
            self.config.get('modification_rules')
        )
        
        # 수정된 파일 로컬 저장
        self.editor.save_modified_local()
        
        # Google Drive에 수정된 파일 업로드
        if self.config['workflow']['save_to_drive']:
            self.editor.upload_to_drive()
        
        self.workflow_results['modified_products'] = len(modified)
        logger.info(f"총 {len(modified)}개 상품 수정 완료")
        return modified
    
    def step4_auto_update(self) -> Dict:
        """Step 4: Cafe24에 자동 업데이트"""
        logger.info("=" * 50)
        logger.info("STEP 4: Cafe24 자동 업데이트")
        logger.info("=" * 50)
        
        self.updater = SmartUpdater(str(self.config_file))
        self.updater.init_driver(headless=self.config['workflow']['headless_mode'])
        
        # 로그인
        if not self.updater.login_cafe24():
            logger.error("Cafe24 로그인 실패")
            return {}
        
        # 수정된 파일들 업데이트
        results = self.updater.update_from_directory("modified_products")
        
        # 리포트 생성
        report = self.updater.create_update_report()
        
        self.updater.cleanup()
        
        self.workflow_results['updated_products'] = report['success_count']
        self.workflow_results['failed_updates'] = report['fail_count']
        
        return report
    
    def run_full_workflow(self):
        """전체 워크플로우 실행"""
        logger.info("=" * 60)
        logger.info("Cafe24 상품 관리 전체 워크플로우 시작")
        logger.info(f"시작 시간: {datetime.now()}")
        logger.info("=" * 60)
        
        workflow_config = self.config.get('workflow', {})
        
        try:
            # Step 1: 크롤링
            if workflow_config.get('crawl_products', True):
                products = self.step1_crawl_products()
                if not products:
                    logger.error("크롤링 실패, 워크플로우 중단")
                    return
            
            # Step 2: Google Drive 업로드
            if workflow_config.get('save_to_drive', True):
                if not self.step2_upload_to_drive():
                    logger.warning("Google Drive 업로드 실패, 계속 진행")
            
            # Step 3: 일괄 수정
            if workflow_config.get('bulk_modify', True):
                modified = self.step3_bulk_modify()
                if not modified:
                    logger.error("수정할 상품이 없음")
                    return
            
            # Step 4: 자동 업데이트
            if workflow_config.get('auto_update', True):
                report = self.step4_auto_update()
            
            # 최종 리포트
            self._create_final_report()
            
        except Exception as e:
            logger.error(f"워크플로우 실행 중 오류: {e}")
            raise
        
        finally:
            logger.info("=" * 60)
            logger.info(f"워크플로우 종료: {datetime.now()}")
            logger.info("=" * 60)
    
    def _create_final_report(self):
        """최종 워크플로우 리포트 생성"""
        report = {
            'workflow_date': datetime.now().isoformat(),
            'config_file': str(self.config_file),
            'results': self.workflow_results,
            'summary': {
                'total_crawled': self.workflow_results.get('crawled_products', 0),
                'total_uploaded': self.workflow_results.get('uploaded_files', 0),
                'total_modified': self.workflow_results.get('modified_products', 0),
                'total_updated': self.workflow_results.get('updated_products', 0),
                'total_failed': self.workflow_results.get('failed_updates', 0)
            }
        }
        
        report_file = Path(f"workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"최종 리포트 생성: {report_file}")
        logger.info("=" * 50)
        logger.info("워크플로우 실행 결과:")
        logger.info(f"- 크롤링: {report['summary']['total_crawled']}개")
        logger.info(f"- Drive 업로드: {report['summary']['total_uploaded']}개")
        logger.info(f"- 수정: {report['summary']['total_modified']}개")
        logger.info(f"- Cafe24 업데이트: {report['summary']['total_updated']}개")
        logger.info(f"- 실패: {report['summary']['total_failed']}개")
        logger.info("=" * 50)

def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cafe24 상품 관리 워크플로우')
    parser.add_argument('--config', default='config/cafe24_config.json',
                       help='설정 파일 경로')
    parser.add_argument('--step', choices=['crawl', 'upload', 'modify', 'update', 'all'],
                       default='all', help='실행할 단계 선택')
    
    args = parser.parse_args()
    
    manager = Cafe24WorkflowManager(args.config)
    
    if args.step == 'all':
        manager.run_full_workflow()
    elif args.step == 'crawl':
        manager.step1_crawl_products()
    elif args.step == 'upload':
        manager.step2_upload_to_drive()
    elif args.step == 'modify':
        manager.step3_bulk_modify()
    elif args.step == 'update':
        manager.step4_auto_update()
    
    logger.info("프로그램 종료")

if __name__ == "__main__":
    main()