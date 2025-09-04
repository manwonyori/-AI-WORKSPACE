"""
Cafe24 이미지 일괄 다운로드 및 관리 시스템
SFTP를 통한 이미지 백업 및 버전 관리
"""
import os
import json
import time
import paramiko
import requests
from datetime import datetime
from pathlib import Path
import hashlib
import shutil
from urllib.parse import urlparse
import re

class ImageBackupManager:
    """Cafe24 이미지 백업 및 관리"""
    
    def __init__(self):
        self.base_folder = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\image_backup"
        self.html_folder = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\product_html_management"
        self.sftp_config = {
            'host': 'ecimg-ftp-c01.cafe24img.com',
            'port': 8013,
            'username': 'manwonyori',
            'password': 'happy8263!'
        }
        
        # 폴더 생성
        os.makedirs(self.base_folder, exist_ok=True)
        os.makedirs(os.path.join(self.base_folder, 'originals'), exist_ok=True)
        os.makedirs(os.path.join(self.base_folder, 'organized'), exist_ok=True)
        os.makedirs(os.path.join(self.base_folder, 'mapping'), exist_ok=True)
        
        self.image_mapping = {}
        self.download_stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def connect_sftp(self):
        """SFTP 연결"""
        try:
            print("[SFTP] 연결 시도...")
            transport = paramiko.Transport((self.sftp_config['host'], self.sftp_config['port']))
            transport.connect(username=self.sftp_config['username'], password=self.sftp_config['password'])
            sftp = paramiko.SFTPClient.from_transport(transport)
            print("[SFTP] 연결 성공")
            return sftp, transport
        except Exception as e:
            print(f"[SFTP] 연결 실패: {e}")
            return None, None
    
    def collect_image_urls(self):
        """스크래핑된 HTML에서 모든 이미지 URL 수집"""
        all_images = {}
        
        # 각 업체 폴더 순회
        for supplier in os.listdir(self.html_folder):
            supplier_path = os.path.join(self.html_folder, supplier)
            if not os.path.isdir(supplier_path):
                continue
            
            all_images[supplier] = []
            
            # 각 상품 폴더 순회
            for product in os.listdir(supplier_path):
                product_path = os.path.join(supplier_path, product)
                if not os.path.isdir(product_path):
                    continue
                
                # images.json 파일 읽기
                images_file = os.path.join(product_path, 'images.json')
                if os.path.exists(images_file):
                    with open(images_file, 'r', encoding='utf-8') as f:
                        images_data = json.load(f)
                        
                        for img in images_data:
                            img['product_code'] = product.split('_')[0]
                            img['supplier'] = supplier
                            all_images[supplier].append(img)
        
        print(f"[수집] 이미지 URL 수집 완료")
        for supplier, images in all_images.items():
            print(f"  {supplier}: {len(images)}개 이미지")
        
        return all_images
    
    def download_via_http(self, url, save_path):
        """HTTP를 통한 이미지 다운로드"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            print(f"    [HTTP 실패] {e}")
        return False
    
    def download_via_sftp(self, sftp, remote_path, local_path):
        """SFTP를 통한 이미지 다운로드"""
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            sftp.get(remote_path, local_path)
            return True
        except Exception as e:
            print(f"    [SFTP 실패] {e}")
        return False
    
    def get_file_hash(self, filepath):
        """파일 해시값 계산 (중복 체크용)"""
        if not os.path.exists(filepath):
            return None
        
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def process_image_url(self, url):
        """Cafe24 이미지 URL 파싱"""
        parsed = urlparse(url)
        
        # Cafe24 이미지 경로 패턴 분석
        if 'cafe24.com' in parsed.netloc:
            # 예: /web/product/big/202408/xxx.jpg
            path_parts = parsed.path.split('/')
            
            # 카테고리 추출 (product, upload, etc)
            category = 'unknown'
            if 'product' in path_parts:
                category = 'product'
            elif 'upload' in path_parts:
                category = 'upload'
            
            # 파일명 추출
            filename = os.path.basename(parsed.path)
            
            return {
                'category': category,
                'filename': filename,
                'full_path': parsed.path,
                'is_cafe24': True
            }
        else:
            return {
                'category': 'external',
                'filename': os.path.basename(parsed.path),
                'full_path': parsed.path,
                'is_cafe24': False
            }
    
    def download_all_images(self, all_images):
        """모든 이미지 다운로드"""
        print("\n[다운로드] 이미지 다운로드 시작...")
        
        # SFTP 연결 시도
        sftp, transport = self.connect_sftp()
        
        for supplier, images in all_images.items():
            print(f"\n[{supplier}] 처리 중...")
            supplier_folder = os.path.join(self.base_folder, 'organized', supplier)
            os.makedirs(supplier_folder, exist_ok=True)
            
            for img_info in images:
                self.download_stats['total'] += 1
                url = img_info['original_url']
                
                # URL 파싱
                parsed_info = self.process_image_url(url)
                
                # 저장 경로 설정
                product_code = img_info['product_code']
                local_filename = f"{product_code}_{parsed_info['filename']}"
                local_path = os.path.join(supplier_folder, local_filename)
                
                # 이미 다운로드된 파일 확인
                if os.path.exists(local_path):
                    print(f"  [SKIP] {local_filename} - 이미 존재")
                    self.download_stats['skipped'] += 1
                    
                    # 매핑 정보 저장
                    self.image_mapping[url] = {
                        'local_path': local_path,
                        'supplier': supplier,
                        'product_code': product_code,
                        'original_url': url,
                        'hash': self.get_file_hash(local_path)
                    }
                    continue
                
                print(f"  [다운로드] {local_filename}")
                
                # HTTP 다운로드 시도
                if self.download_via_http(url, local_path):
                    print(f"    [OK] HTTP 다운로드 성공")
                    self.download_stats['success'] += 1
                    
                    # 매핑 정보 저장
                    self.image_mapping[url] = {
                        'local_path': local_path,
                        'supplier': supplier,
                        'product_code': product_code,
                        'original_url': url,
                        'hash': self.get_file_hash(local_path),
                        'download_method': 'http',
                        'downloaded_at': datetime.now().isoformat()
                    }
                    
                # SFTP 다운로드 시도
                elif sftp and parsed_info['is_cafe24']:
                    remote_path = parsed_info['full_path']
                    if self.download_via_sftp(sftp, remote_path, local_path):
                        print(f"    [OK] SFTP 다운로드 성공")
                        self.download_stats['success'] += 1
                        
                        self.image_mapping[url] = {
                            'local_path': local_path,
                            'supplier': supplier,
                            'product_code': product_code,
                            'original_url': url,
                            'hash': self.get_file_hash(local_path),
                            'download_method': 'sftp',
                            'downloaded_at': datetime.now().isoformat()
                        }
                    else:
                        self.download_stats['failed'] += 1
                else:
                    print(f"    [FAIL] 다운로드 실패")
                    self.download_stats['failed'] += 1
                
                time.sleep(0.5)  # 서버 부하 방지
        
        # SFTP 연결 종료
        if sftp:
            sftp.close()
        if transport:
            transport.close()
    
    def save_mapping(self):
        """이미지 매핑 정보 저장"""
        mapping_file = os.path.join(self.base_folder, 'mapping', f'image_mapping_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(self.image_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"[MAPPING] 매핑 정보 저장: {mapping_file}")
    
    def create_backup_report(self):
        """백업 리포트 생성"""
        report_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>이미지 백업 리포트</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .stats {{ background: #f0f0f0; padding: 15px; margin-bottom: 20px; }}
        .supplier-section {{ margin: 20px 0; border: 1px solid #ddd; padding: 15px; }}
        .image-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; }}
        .image-card {{ border: 1px solid #ccc; padding: 10px; }}
        .image-card img {{ width: 100%; height: 150px; object-fit: cover; }}
        .success {{ color: green; }}
        .failed {{ color: red; }}
        .skipped {{ color: gray; }}
    </style>
</head>
<body>
    <h1>📦 Cafe24 이미지 백업 리포트</h1>
    <div class="stats">
        <h2>통계</h2>
        <p>생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>전체: {self.download_stats['total']}개</p>
        <p class="success">성공: {self.download_stats['success']}개</p>
        <p class="failed">실패: {self.download_stats['failed']}개</p>
        <p class="skipped">건너뜀: {self.download_stats['skipped']}개</p>
    </div>
    
    <h2>백업된 이미지</h2>
"""
        
        # 업체별로 그룹화
        suppliers = {}
        for url, info in self.image_mapping.items():
            supplier = info.get('supplier', 'unknown')
            if supplier not in suppliers:
                suppliers[supplier] = []
            suppliers[supplier].append(info)
        
        for supplier, images in suppliers.items():
            report_html += f"""
    <div class="supplier-section">
        <h3>{supplier} ({len(images)}개)</h3>
        <div class="image-grid">
"""
            for img in images[:10]:  # 처음 10개만 표시
                local_path = img['local_path']
                filename = os.path.basename(local_path)
                relative_path = os.path.relpath(local_path, self.base_folder)
                
                report_html += f"""
            <div class="image-card">
                <img src="../{relative_path.replace(os.sep, '/')}" alt="{filename}">
                <p><small>{filename}</small></p>
                <p><small>{img['product_code']}</small></p>
            </div>
"""
            
            report_html += """
        </div>
    </div>
"""
        
        report_html += """
</body>
</html>
"""
        
        report_path = os.path.join(self.base_folder, 'backup_report.html')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_html)
        
        print(f"[REPORT] 백업 리포트 생성: {report_path}")
        return report_path
    
    def run(self):
        """메인 실행"""
        print("="*60)
        print("Cafe24 이미지 일괄 백업 시작")
        print("="*60)
        
        # 1. 이미지 URL 수집
        all_images = self.collect_image_urls()
        
        if not all_images:
            print("[ERROR] 수집된 이미지가 없습니다")
            return
        
        # 2. 이미지 다운로드
        self.download_all_images(all_images)
        
        # 3. 매핑 정보 저장
        self.save_mapping()
        
        # 4. 백업 리포트 생성
        report_path = self.create_backup_report()
        
        print("\n" + "="*60)
        print("백업 완료!")
        print(f"성공: {self.download_stats['success']}개")
        print(f"실패: {self.download_stats['failed']}개")
        print(f"건너뜀: {self.download_stats['skipped']}개")
        print(f"백업 폴더: {self.base_folder}")
        print("="*60)
        
        # 리포트 열기
        os.startfile(report_path)

if __name__ == "__main__":
    manager = ImageBackupManager()
    manager.run()