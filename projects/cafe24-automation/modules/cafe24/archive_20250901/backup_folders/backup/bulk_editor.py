"""
Cafe24 상품 일괄 수정 자동화 시스템
239개 상품의 HTML을 Google Drive에서 다운로드하여 일괄 수정 후 재업로드
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cafe24_bulk_editor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Cafe24BulkEditor:
    """Cafe24 상품 HTML 일괄 수정 시스템"""
    
    def __init__(self, config_path: str = "config/cafe24_config.json"):
        """초기화"""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.drive_service = self._init_google_drive()
        self.products_data = []
        self.modified_products = []
        
    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 기본 설정
            default_config = {
                "google_drive": {
                    "service_account_file": "path/to/service_account.json",
                    "folder_id": "your_folder_id_here"
                },
                "cafe24": {
                    "mall_id": "manwonyori",
                    "admin_url": "https://manwonyori.cafe24.com/admin"
                },
                "modification_rules": {
                    "price_increase_percent": 10,
                    "update_images": True,
                    "add_watermark": False,
                    "update_description": True
                }
            }
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            logger.info(f"기본 설정 파일 생성: {self.config_path}")
            return default_config
    
    def _init_google_drive(self):
        """Google Drive API 초기화"""
        try:
            service_account_file = self.config['google_drive']['service_account_file']
            if Path(service_account_file).exists():
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_file,
                    scopes=['https://www.googleapis.com/auth/drive']
                )
                return build('drive', 'v3', credentials=credentials)
            else:
                logger.warning("Google Drive 서비스 계정 파일이 없습니다")
                return None
        except Exception as e:
            logger.error(f"Google Drive 초기화 실패: {e}")
            return None
    
    def download_from_drive(self, folder_id: str = None) -> List[Dict]:
        """Google Drive에서 모든 상품 HTML 다운로드"""
        if not self.drive_service:
            logger.error("Google Drive 서비스가 초기화되지 않았습니다")
            return []
        
        folder_id = folder_id or self.config['google_drive']['folder_id']
        products = []
        
        try:
            # 폴더 내 모든 HTML 파일 검색
            query = f"'{folder_id}' in parents and mimeType='text/html'"
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"Google Drive에서 {len(files)}개 파일 발견")
            
            # 각 파일 다운로드
            for file in files:
                try:
                    # 파일 내용 다운로드
                    request = self.drive_service.files().get_media(fileId=file['id'])
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    
                    # HTML 내용 파싱
                    html_content = fh.getvalue().decode('utf-8')
                    product_code = file['name'].replace('.html', '')
                    
                    products.append({
                        'product_code': product_code,
                        'file_id': file['id'],
                        'file_name': file['name'],
                        'html_content': html_content,
                        'modified_time': file['modifiedTime']
                    })
                    
                    logger.info(f"다운로드 완료: {product_code}")
                    
                except Exception as e:
                    logger.error(f"파일 다운로드 실패 {file['name']}: {e}")
            
            self.products_data = products
            return products
            
        except Exception as e:
            logger.error(f"Drive 파일 목록 조회 실패: {e}")
            return []
    
    def modify_html_batch(self, modification_rules: Dict = None) -> List[Dict]:
        """HTML 일괄 수정"""
        if not self.products_data:
            logger.error("수정할 상품 데이터가 없습니다")
            return []
        
        rules = modification_rules or self.config.get('modification_rules', {})
        modified = []
        
        for product in self.products_data:
            try:
                soup = BeautifulSoup(product['html_content'], 'html.parser')
                original_html = str(soup)
                
                # 1. 가격 수정
                if rules.get('price_increase_percent'):
                    price_elements = soup.find_all(text=re.compile(r'₩[\d,]+'))
                    for element in price_elements:
                        price_text = element.string
                        if price_text:
                            # 가격 추출 및 증가
                            price = int(re.sub(r'[^\d]', '', price_text))
                            new_price = int(price * (1 + rules['price_increase_percent'] / 100))
                            new_price_text = f"₩{new_price:,}"
                            element.replace_with(new_price_text)
                
                # 2. 이미지 수정
                if rules.get('update_images'):
                    img_tags = soup.find_all('img')
                    for img in img_tags:
                        # 이미지 URL 수정 로직
                        if img.get('src'):
                            # 예: CDN URL 변경
                            img['src'] = self._update_image_url(img['src'])
                
                # 3. 설명 추가/수정
                if rules.get('update_description'):
                    # 상품 설명 영역 찾기
                    desc_div = soup.find('div', class_='product-description')
                    if desc_div:
                        # 추가 문구 삽입
                        new_text = soup.new_tag('p')
                        new_text.string = "✨ 업데이트된 상품 정보입니다 ✨"
                        desc_div.insert(0, new_text)
                
                # 4. 메타 태그 수정
                meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                if meta_keywords:
                    current_keywords = meta_keywords.get('content', '')
                    meta_keywords['content'] = f"{current_keywords},bulk_updated,{datetime.now().strftime('%Y%m%d')}"
                
                # 수정된 HTML 저장
                modified_html = str(soup)
                
                if original_html != modified_html:
                    product['modified_html'] = modified_html
                    product['modified'] = True
                    product['modification_time'] = datetime.now().isoformat()
                    modified.append(product)
                    logger.info(f"수정 완료: {product['product_code']}")
                
            except Exception as e:
                logger.error(f"HTML 수정 실패 {product['product_code']}: {e}")
        
        self.modified_products = modified
        logger.info(f"총 {len(modified)}개 상품 수정 완료")
        return modified
    
    def _update_image_url(self, url: str) -> str:
        """이미지 URL 업데이트 로직"""
        # 예시: CDN 도메인 변경
        if 'old-cdn.com' in url:
            return url.replace('old-cdn.com', 'new-cdn.com')
        return url
    
    def save_modified_local(self, output_dir: str = "modified_products"):
        """수정된 HTML 로컬 저장"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for product in self.modified_products:
            file_path = output_path / f"{product['product_code']}_modified.html"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(product['modified_html'])
            logger.info(f"로컬 저장: {file_path}")
    
    def upload_to_drive(self, folder_id: str = None) -> List[str]:
        """수정된 HTML을 Google Drive에 업로드"""
        if not self.drive_service:
            logger.error("Google Drive 서비스가 초기화되지 않았습니다")
            return []
        
        folder_id = folder_id or self.config['google_drive']['folder_id']
        uploaded_files = []
        
        # 수정된 파일용 새 폴더 생성
        modified_folder_name = f"modified_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        folder_metadata = {
            'name': modified_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }
        
        try:
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            modified_folder_id = folder.get('id')
            logger.info(f"수정된 파일 폴더 생성: {modified_folder_name}")
            
            # 각 수정된 파일 업로드
            for product in self.modified_products:
                temp_file = Path(f"temp_{product['product_code']}.html")
                temp_file.write_text(product['modified_html'], encoding='utf-8')
                
                file_metadata = {
                    'name': f"{product['product_code']}_modified.html",
                    'parents': [modified_folder_id]
                }
                
                media = MediaFileUpload(
                    str(temp_file),
                    mimetype='text/html'
                )
                
                file = self.drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                
                uploaded_files.append(file.get('id'))
                temp_file.unlink()  # 임시 파일 삭제
                logger.info(f"업로드 완료: {product['product_code']}")
            
            logger.info(f"총 {len(uploaded_files)}개 파일 업로드 완료")
            return uploaded_files
            
        except Exception as e:
            logger.error(f"Drive 업로드 실패: {e}")
            return []
    
    def create_modification_report(self) -> Dict:
        """수정 리포트 생성"""
        report = {
            'total_products': len(self.products_data),
            'modified_products': len(self.modified_products),
            'modification_time': datetime.now().isoformat(),
            'modifications': []
        }
        
        for product in self.modified_products:
            report['modifications'].append({
                'product_code': product['product_code'],
                'file_id': product.get('file_id'),
                'modified_time': product.get('modification_time')
            })
        
        # 리포트 저장
        report_path = Path(f"modification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"수정 리포트 생성: {report_path}")
        return report
    
    def apply_custom_modifications(self, custom_func):
        """사용자 정의 수정 함수 적용"""
        for product in self.products_data:
            try:
                soup = BeautifulSoup(product['html_content'], 'html.parser')
                modified_soup = custom_func(soup, product['product_code'])
                product['modified_html'] = str(modified_soup)
                product['modified'] = True
                self.modified_products.append(product)
            except Exception as e:
                logger.error(f"커스텀 수정 실패 {product['product_code']}: {e}")

def main():
    """메인 실행 함수"""
    editor = Cafe24BulkEditor()
    
    # 1. Google Drive에서 상품 HTML 다운로드
    logger.info("=== Google Drive에서 상품 데이터 다운로드 시작 ===")
    products = editor.download_from_drive()
    logger.info(f"다운로드 완료: {len(products)}개 상품")
    
    # 2. HTML 일괄 수정
    logger.info("=== HTML 일괄 수정 시작 ===")
    modification_rules = {
        'price_increase_percent': 10,  # 10% 가격 인상
        'update_images': True,
        'update_description': True
    }
    modified = editor.modify_html_batch(modification_rules)
    logger.info(f"수정 완료: {len(modified)}개 상품")
    
    # 3. 로컬 저장
    logger.info("=== 수정된 파일 로컬 저장 ===")
    editor.save_modified_local()
    
    # 4. Google Drive 업로드
    logger.info("=== Google Drive 업로드 ===")
    uploaded = editor.upload_to_drive()
    
    # 5. 리포트 생성
    logger.info("=== 수정 리포트 생성 ===")
    report = editor.create_modification_report()
    
    logger.info("=== 작업 완료 ===")
    logger.info(f"전체: {report['total_products']}개, 수정: {report['modified_products']}개")

if __name__ == "__main__":
    main()