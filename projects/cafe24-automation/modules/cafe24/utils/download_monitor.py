# -*- coding: utf-8 -*-
"""
Download Monitor - 사용자 다운로드 방식 전체 체크 시스템
로그인 후 사용자가 다운로드하는 모든 방식을 추적하고 분석
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import time
import glob
import json
from datetime import datetime, timedelta
from pathlib import Path

class DownloadMonitor:
    """사용자 다운로드 방식 전체 모니터링 시스템"""
    
    def __init__(self):
        """초기화"""
        self.download_paths = [
            "C:\\Users\\8899y\\Downloads",
            "C:\\Users\\8899y\\Downloads\\CUA_Excel_Cafe24", 
            "C:\\Users\\8899y\\Desktop",
            "D:\\주문취합\\주문_배송",
            "C:\\Users\\8899y\\Documents",
            "C:\\Users\\8899y",  # 사용자 홈 디렉토리
        ]
        self.monitor_extensions = ['.xlsx', '.xls', '.csv', '.txt', '.json', '.html']
        self.baseline_files = {}
        self.new_downloads = []
        
        print("[DOWNLOAD-MONITOR] 다운로드 모니터링 시스템 시작")
        print(f"[MONITORING] {len(self.download_paths)}개 경로 모니터링")
        
    def capture_baseline(self):
        """기준선 파일 목록 캡처"""
        print("\n[BASELINE] 기준선 파일 목록 캡처 중...")
        
        for path in self.download_paths:
            if os.path.exists(path):
                path_files = {}
                for ext in self.monitor_extensions:
                    files = glob.glob(os.path.join(path, f"*{ext}"))
                    for file in files:
                        try:
                            stat = os.stat(file)
                            path_files[file] = {
                                'size': stat.st_size,
                                'mtime': stat.st_mtime,
                                'created': stat.st_ctime
                            }
                        except:
                            continue
                            
                self.baseline_files[path] = path_files
                print(f"   [PATH] {path}: {len(path_files)}개 파일")
            else:
                self.baseline_files[path] = {}
                print(f"   [PATH] {path}: 경로 없음")
        
        print(f"[BASELINE-COMPLETE] 총 {sum(len(files) for files in self.baseline_files.values())}개 파일 기준선 설정")
        
    def detect_new_downloads(self):
        """새로운 다운로드 파일 탐지"""
        print("\n[DETECTION] 새로운 다운로드 파일 탐지...")
        
        current_time = time.time()
        new_files = []
        
        for path in self.download_paths:
            if not os.path.exists(path):
                continue
                
            baseline = self.baseline_files.get(path, {})
            
            for ext in self.monitor_extensions:
                files = glob.glob(os.path.join(path, f"*{ext}"))
                for file in files:
                    try:
                        stat = os.stat(file)
                        
                        # 새 파일이거나 수정된 파일 체크
                        if file not in baseline:
                            # 최근 2시간 내 생성된 파일 (사용자가 방금 다운로드했다고 함)
                            if current_time - stat.st_ctime < 7200:  # 2시간
                                new_files.append({
                                    'file': file,
                                    'path': path,
                                    'size': stat.st_size,
                                    'created': datetime.fromtimestamp(stat.st_ctime),
                                    'modified': datetime.fromtimestamp(stat.st_mtime),
                                    'extension': ext,
                                    'status': 'NEW'
                                })
                        else:
                            # 파일 크기나 수정 시간이 변경된 경우
                            old_stat = baseline[file]
                            if (stat.st_size != old_stat['size'] or 
                                stat.st_mtime != old_stat['mtime']):
                                new_files.append({
                                    'file': file,
                                    'path': path,
                                    'size': stat.st_size,
                                    'created': datetime.fromtimestamp(stat.st_ctime),
                                    'modified': datetime.fromtimestamp(stat.st_mtime),
                                    'extension': ext,
                                    'status': 'MODIFIED'
                                })
                    except:
                        continue
        
        self.new_downloads = new_files
        print(f"[DETECTED] {len(new_files)}개 새로운/수정된 파일 발견")
        
        return new_files
    
    def analyze_download_patterns(self):
        """다운로드 패턴 분석"""
        print("\n[ANALYSIS] 다운로드 패턴 분석...")
        
        if not self.new_downloads:
            print("   [INFO] 분석할 새 다운로드 파일이 없습니다")
            return {}
        
        analysis = {
            'total_downloads': len(self.new_downloads),
            'by_extension': {},
            'by_path': {},
            'by_size': {},
            'timeline': [],
            'largest_files': [],
            'cafe24_related': []
        }
        
        # 확장자별 분석
        for download in self.new_downloads:
            ext = download['extension']
            analysis['by_extension'][ext] = analysis['by_extension'].get(ext, 0) + 1
        
        # 경로별 분석
        for download in self.new_downloads:
            path = download['path']
            analysis['by_path'][path] = analysis['by_path'].get(path, 0) + 1
        
        # 크기별 분석
        total_size = sum(d['size'] for d in self.new_downloads)
        analysis['total_size'] = total_size
        analysis['average_size'] = total_size / len(self.new_downloads) if self.new_downloads else 0
        
        # 큰 파일들 (1MB 이상)
        large_files = [d for d in self.new_downloads if d['size'] > 1024*1024]
        analysis['largest_files'] = sorted(large_files, key=lambda x: x['size'], reverse=True)[:5]
        
        # Cafe24 관련 파일들
        cafe24_keywords = ['cafe24', 'manwonyori', 'product', '상품', 'excel', '다운로드']
        for download in self.new_downloads:
            filename = os.path.basename(download['file']).lower()
            if any(keyword in filename for keyword in cafe24_keywords):
                analysis['cafe24_related'].append(download)
        
        # 타임라인
        sorted_downloads = sorted(self.new_downloads, key=lambda x: x['created'])
        analysis['timeline'] = sorted_downloads
        
        print(f"   [TOTAL] {analysis['total_downloads']}개 파일")
        print(f"   [SIZE] 총 크기: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
        print(f"   [EXTENSIONS] {', '.join(analysis['by_extension'].keys())}")
        print(f"   [CAFE24-RELATED] {len(analysis['cafe24_related'])}개 Cafe24 관련 파일")
        
        return analysis
    
    def generate_detailed_report(self, analysis):
        """상세 리포트 생성"""
        print("\n" + "="*80)
        print("[DETAILED-REPORT] 사용자 다운로드 방식 전체 분석 결과")
        print("="*80)
        
        if not analysis or analysis['total_downloads'] == 0:
            print("[NO-DOWNLOADS] 새로운 다운로드가 없습니다")
            return
        
        # 1. 전체 요약
        print(f"\n📊 [SUMMARY] 다운로드 요약")
        print(f"   • 총 다운로드 파일: {analysis['total_downloads']}개")
        print(f"   • 총 크기: {analysis['total_size']:,} bytes ({analysis['total_size']/1024/1024:.1f} MB)")
        print(f"   • 평균 파일 크기: {analysis['average_size']:,.0f} bytes")
        
        # 2. 확장자별 분석
        print(f"\n📁 [BY-EXTENSION] 파일 형식별 분석")
        for ext, count in sorted(analysis['by_extension'].items()):
            print(f"   • {ext}: {count}개")
        
        # 3. 경로별 분석  
        print(f"\n📂 [BY-PATH] 저장 위치별 분석")
        for path, count in analysis['by_path'].items():
            print(f"   • {path}: {count}개")
        
        # 4. 큰 파일들
        if analysis['largest_files']:
            print(f"\n📦 [LARGE-FILES] 큰 파일들 (1MB 이상)")
            for i, file_info in enumerate(analysis['largest_files'], 1):
                filename = os.path.basename(file_info['file'])
                size_mb = file_info['size'] / 1024 / 1024
                print(f"   {i}. {filename}: {size_mb:.1f} MB")
        
        # 5. Cafe24 관련 파일들
        if analysis['cafe24_related']:
            print(f"\n☕ [CAFE24-RELATED] Cafe24 관련 파일들")
            for file_info in analysis['cafe24_related']:
                filename = os.path.basename(file_info['file'])
                size_mb = file_info['size'] / 1024 / 1024
                created = file_info['created'].strftime("%H:%M:%S")
                print(f"   • {filename}: {size_mb:.1f} MB (생성: {created})")
        
        # 6. 타임라인
        print(f"\n⏰ [TIMELINE] 다운로드 타임라인")
        for file_info in analysis['timeline'][-10:]:  # 최근 10개
            filename = os.path.basename(file_info['file'])
            created = file_info['created'].strftime("%H:%M:%S")
            status = file_info['status']
            print(f"   {created} | {status} | {filename}")
    
    def save_analysis_report(self, analysis):
        """분석 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"download_analysis_{timestamp}.json"
        
        # JSON 직렬화를 위해 datetime 객체 변환
        json_analysis = analysis.copy()
        for item in json_analysis.get('timeline', []):
            if 'created' in item:
                item['created'] = item['created'].isoformat()
            if 'modified' in item:
                item['modified'] = item['modified'].isoformat()
        
        for item in json_analysis.get('largest_files', []):
            if 'created' in item:
                item['created'] = item['created'].isoformat()
            if 'modified' in item:
                item['modified'] = item['modified'].isoformat()
        
        for item in json_analysis.get('cafe24_related', []):
            if 'created' in item:
                item['created'] = item['created'].isoformat()
            if 'modified' in item:
                item['modified'] = item['modified'].isoformat()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_analysis, f, ensure_ascii=False, indent=2)
            print(f"\n[SAVED] 분석 결과 저장: {filename}")
        except Exception as e:
            print(f"\n[ERROR] 분석 결과 저장 실패: {e}")
    
    def run_monitoring_cycle(self):
        """모니터링 사이클 실행"""
        print("\n" + "="*80)
        print("[MONITORING-CYCLE] 다운로드 모니터링 사이클 시작")
        print("="*80)
        
        # 1. 기준선 캡처
        self.capture_baseline()
        
        # 2. 새 다운로드 탐지 
        new_files = self.detect_new_downloads()
        
        # 3. 패턴 분석
        analysis = self.analyze_download_patterns()
        
        # 4. 상세 리포트 생성
        self.generate_detailed_report(analysis)
        
        # 5. 결과 저장
        if analysis and analysis['total_downloads'] > 0:
            self.save_analysis_report(analysis)
        
        print("\n" + "="*80)
        print("[MONITORING-COMPLETE] 다운로드 모니터링 완료")
        print("="*80)
        
        return analysis

def main():
    """메인 실행"""
    print("="*80)
    print("DOWNLOAD MONITOR")
    print("사용자 다운로드 방식 전체 체크 및 분석 시스템")
    print("="*80)
    
    monitor = DownloadMonitor()
    analysis = monitor.run_monitoring_cycle()
    
    if analysis and analysis['total_downloads'] > 0:
        print(f"\n[RESULT] {analysis['total_downloads']}개 다운로드 파일 분석 완료")
        print("다운로드 패턴과 사용자 방식이 완전히 분석되었습니다")
    else:
        print(f"\n[RESULT] 새로운 다운로드 파일이 없습니다")
        print("기준선이 설정되어 다음 실행 시 새 파일을 탐지합니다")

if __name__ == "__main__":
    main()