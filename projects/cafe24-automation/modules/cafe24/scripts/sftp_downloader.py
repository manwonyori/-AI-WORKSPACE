"""
SFTP 완벽 미러링 다운로더
- FTP 서버와 완전히 동일한 구조로 다운로드
- 수정 후 업로드 시 경로 체크 가능
"""
import os
import json
import paramiko
import hashlib
from datetime import datetime
from pathlib import Path

class SFTPMirrorDownloader:
    def __init__(self):
        # 설정 로드
        with open('FTP_CONFIG.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.sftp_config = self.config['sftp_server']
        self.local_config = self.config['local_mirror']
        
        # 로컬 미러 폴더 생성
        self.download_path = Path(self.local_config['structure']['download_path'])
        self.upload_path = Path(self.local_config['structure']['upload_path'])
        self.backup_path = Path(self.local_config['structure']['backup_path'])
        
        for path in [self.download_path, self.upload_path, self.backup_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        self.sftp = None
        self.transport = None
        self.file_mapping = {}
        self.stats = {
            'total_files': 0,
            'downloaded': 0,
            'skipped': 0,
            'failed': 0,
            'total_size': 0
        }
    
    def connect(self):
        """SFTP 연결"""
        try:
            print(f"[CONNECT] {self.sftp_config['host']}:{self.sftp_config['port']} 연결 중...")
            
            # Transport 생성
            self.transport = paramiko.Transport((
                self.sftp_config['host'], 
                self.sftp_config['port']
            ))
            
            # 연결
            self.transport.connect(
                username=self.sftp_config['username'],
                password=self.sftp_config['password']
            )
            
            # SFTP 클라이언트 생성
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            
            print("[SUCCESS] SFTP 연결 성공!")
            return True
            
        except Exception as e:
            print(f"[ERROR] SFTP 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """SFTP 연결 종료"""
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()
        print("[CLOSE] SFTP 연결 종료")
    
    def get_remote_structure(self, remote_path='/', level=0, max_level=5):
        """원격 디렉토리 구조 탐색"""
        structure = {}
        
        if level > max_level:
            return structure
        
        try:
            items = self.sftp.listdir_attr(remote_path)
            
            for item in items:
                item_path = f"{remote_path}/{item.filename}".replace('//', '/')
                
                # 디렉토리인 경우
                if item.st_mode & 0o40000:
                    print(f"{'  ' * level}[DIR] {item_path}")
                    structure[item.filename] = {
                        'type': 'directory',
                        'path': item_path,
                        'children': self.get_remote_structure(item_path, level + 1, max_level)
                    }
                # 파일인 경우
                else:
                    # 이미지 파일만 처리
                    if item.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        print(f"{'  ' * level}[FILE] {item.filename} ({item.st_size:,} bytes)")
                        structure[item.filename] = {
                            'type': 'file',
                            'path': item_path,
                            'size': item.st_size,
                            'mtime': item.st_mtime
                        }
                        self.stats['total_files'] += 1
                        
        except Exception as e:
            print(f"[ERROR] 디렉토리 탐색 실패 {remote_path}: {e}")
        
        return structure
    
    def download_file(self, remote_path, local_path):
        """파일 다운로드 (구조 유지)"""
        try:
            # 로컬 디렉토리 생성
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 이미 존재하는 파일 체크
            if local_path.exists():
                # 크기 비교
                remote_stat = self.sftp.stat(remote_path)
                local_stat = local_path.stat()
                
                if remote_stat.st_size == local_stat.st_size:
                    print(f"  [SKIP] 이미 존재: {local_path.name}")
                    self.stats['skipped'] += 1
                    return True
            
            # 다운로드
            print(f"  [DOWNLOAD] {remote_path} → {local_path}")
            self.sftp.get(remote_path, str(local_path))
            
            # 체크섬 생성
            with open(local_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            # 매핑 저장
            self.file_mapping[remote_path] = {
                'local_path': str(local_path),
                'remote_path': remote_path,
                'size': local_path.stat().st_size,
                'hash': file_hash,
                'downloaded_at': datetime.now().isoformat()
            }
            
            self.stats['downloaded'] += 1
            self.stats['total_size'] += local_path.stat().st_size
            
            return True
            
        except Exception as e:
            print(f"  [ERROR] 다운로드 실패: {e}")
            self.stats['failed'] += 1
            return False
    
    def mirror_download(self, remote_path='/', local_base=None):
        """전체 구조 미러링 다운로드"""
        if local_base is None:
            local_base = self.download_path
        
        print(f"\n[MIRROR] {remote_path} 미러링 시작...")
        
        try:
            items = self.sftp.listdir_attr(remote_path)
            
            for item in items:
                item_remote = f"{remote_path}/{item.filename}".replace('//', '/')
                item_local = local_base / item.filename
                
                # 디렉토리
                if item.st_mode & 0o40000:
                    item_local.mkdir(exist_ok=True)
                    self.mirror_download(item_remote, item_local)
                
                # 파일
                else:
                    if item.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        self.download_file(item_remote, item_local)
                        
        except Exception as e:
            print(f"[ERROR] 미러링 실패 {remote_path}: {e}")
    
    def save_mapping(self):
        """다운로드 매핑 저장"""
        mapping_file = self.download_path.parent / 'download_mapping.json'
        
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump({
                'download_info': {
                    'date': datetime.now().isoformat(),
                    'server': self.sftp_config['host'],
                    'stats': self.stats
                },
                'file_mapping': self.file_mapping
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[SAVE] 매핑 파일 저장: {mapping_file}")
    
    def create_upload_structure(self):
        """업로드용 구조 생성 (수정 작업용)"""
        print("\n[CREATE] 업로드 구조 생성 중...")
        
        # download 폴더 구조를 upload 폴더로 복사
        for src_path in self.download_path.rglob('*'):
            if src_path.is_file():
                # 상대 경로 계산
                rel_path = src_path.relative_to(self.download_path)
                dst_path = self.upload_path / rel_path
                
                # 디렉토리 생성
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 구조만 생성 (파일은 복사하지 않음)
                # 실제 작업 시 여기서 파일을 복사하거나 수정
                with open(dst_path.with_suffix('.txt'), 'w') as f:
                    f.write(f"원본: {rel_path}\n")
                    f.write(f"수정 후 이 위치에 파일 저장\n")
        
        print(f"[COMPLETE] 업로드 구조 생성 완료: {self.upload_path}")
    
    def verify_structure(self):
        """다운로드된 구조 검증"""
        print("\n[VERIFY] 구조 검증 중...")
        
        # 폴더별 파일 수 계산
        folder_stats = {}
        
        for path in self.download_path.rglob('*'):
            if path.is_file():
                folder = path.parent.relative_to(self.download_path)
                folder_name = str(folder) if str(folder) != '.' else 'root'
                
                if folder_name not in folder_stats:
                    folder_stats[folder_name] = 0
                folder_stats[folder_name] += 1
        
        print("\n[폴더별 파일 수]")
        for folder, count in sorted(folder_stats.items()):
            print(f"  {folder}: {count}개")
        
        return folder_stats
    
    def run(self):
        """전체 프로세스 실행"""
        print("="*60)
        print("SFTP 완벽 미러링 다운로더")
        print("="*60)
        
        # 1. 연결
        if not self.connect():
            return
        
        try:
            # 2. 원격 구조 탐색
            print("\n[SCAN] 원격 서버 구조 탐색 중...")
            structure = self.get_remote_structure('/', max_level=3)
            
            # 구조 저장
            with open(self.download_path.parent / 'remote_structure.json', 'w', encoding='utf-8') as f:
                json.dump(structure, f, ensure_ascii=False, indent=2)
            
            print(f"\n[FOUND] 총 {self.stats['total_files']}개 파일 발견")
            
            # 3. 미러링 다운로드
            if input("\n다운로드를 시작하시겠습니까? (y/n): ").lower() == 'y':
                self.mirror_download()
                
                # 4. 매핑 저장
                self.save_mapping()
                
                # 5. 업로드 구조 생성
                self.create_upload_structure()
                
                # 6. 검증
                self.verify_structure()
                
                # 7. 최종 통계
                print("\n" + "="*60)
                print("[최종 통계]")
                print(f"  총 파일: {self.stats['total_files']}개")
                print(f"  다운로드: {self.stats['downloaded']}개")
                print(f"  건너뜀: {self.stats['skipped']}개")
                print(f"  실패: {self.stats['failed']}개")
                print(f"  총 크기: {self.stats['total_size']:,} bytes")
                print("="*60)
                
        finally:
            # 연결 종료
            self.disconnect()

if __name__ == "__main__":
    downloader = SFTPMirrorDownloader()
    downloader.run()