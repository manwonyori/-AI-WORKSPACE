# -*- coding: utf-8 -*-
"""
Recent Downloads Checker - 최근 다운로드 파일 전체 확인
사용자가 다운로드한 모든 파일을 시간별로 체크하고 분석
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import time
import glob
import json
from datetime import datetime, timedelta
from pathlib import Path

class RecentDownloadsChecker:
    """최근 다운로드 파일 전체 체크 시스템"""
    
    def __init__(self):
        """초기화"""
        self.search_paths = [
            "C:\\Users\\8899y\\Downloads",
            "C:\\Users\\8899y\\Desktop", 
            "C:\\Users\\8899y\\Documents",
            "C:\\Users\\8899y",
            "D:\\주문취합\\주문_배송"
        ]
        self.file_extensions = ['.xlsx', '.xls', '.csv', '.txt', '.json', '.html', '.xml']
        self.recent_files = []
        
        print("[RECENT-CHECKER] 최근 다운로드 파일 체크 시스템")
        print(f"[SEARCH-PATHS] {len(self.search_paths)}개 경로 검색")
        
    def find_recent_files(self, hours_back=6):
        """최근 N시간 내 파일 찾기"""
        print(f"\n[SEARCH] 최근 {hours_back}시간 내 파일 검색...")
        
        cutoff_time = time.time() - (hours_back * 3600)
        recent_files = []
        
        for search_path in self.search_paths:
            if not os.path.exists(search_path):
                print(f"   [SKIP] {search_path} - 경로 없음")
                continue
            
            path_files = []
            
            # 각 확장자별로 검색
            for ext in self.file_extensions:
                pattern = os.path.join(search_path, f"*{ext}")
                files = glob.glob(pattern)
                
                for file_path in files:
                    try:
                        stat_info = os.stat(file_path)
                        
                        # 생성 시간 또는 수정 시간이 최근인 파일들
                        if (stat_info.st_ctime > cutoff_time or 
                            stat_info.st_mtime > cutoff_time):
                            
                            file_info = {
                                'file_path': file_path,
                                'filename': os.path.basename(file_path),
                                'directory': search_path,
                                'extension': ext,
                                'size': stat_info.st_size,
                                'created_time': datetime.fromtimestamp(stat_info.st_ctime),
                                'modified_time': datetime.fromtimestamp(stat_info.st_mtime),
                                'size_mb': round(stat_info.st_size / 1024 / 1024, 2)
                            }
                            path_files.append(file_info)
                            
                    except Exception as e:
                        print(f"   [ERROR] {file_path}: {e}")
                        continue
            
            if path_files:
                print(f"   [FOUND] {search_path}: {len(path_files)}개 파일")
                recent_files.extend(path_files)
            else:
                print(f"   [EMPTY] {search_path}: 최근 파일 없음")
        
        # 생성 시간 순으로 정렬 (최신순)
        recent_files.sort(key=lambda x: x['created_time'], reverse=True)
        self.recent_files = recent_files
        
        print(f"[TOTAL-FOUND] 총 {len(recent_files)}개 최근 파일 발견")
        return recent_files
    
    def analyze_cafe24_files(self):
        """Cafe24 관련 파일 분석"""
        print(f"\n[CAFE24-ANALYSIS] Cafe24 관련 파일 분석...")
        
        cafe24_keywords = ['cafe24', 'manwonyori', '상품', 'product', 'excel', '다운로드', 
                          'download', '관리', 'manage', '판매', 'sell']
        
        cafe24_files = []
        for file_info in self.recent_files:
            filename_lower = file_info['filename'].lower()
            
            # 파일명에 Cafe24 키워드가 포함된 경우
            if any(keyword in filename_lower for keyword in cafe24_keywords):
                file_info['cafe24_match'] = True
                cafe24_files.append(file_info)
            
            # Excel 파일이면서 크기가 큰 경우 (상품 데이터일 가능성)
            elif (file_info['extension'] in ['.xlsx', '.xls'] and 
                  file_info['size'] > 10000):  # 10KB 이상
                file_info['cafe24_match'] = 'possible'
                cafe24_files.append(file_info)
        
        print(f"   [CAFE24-FILES] {len(cafe24_files)}개 Cafe24 관련 파일")
        return cafe24_files
    
    def generate_detailed_report(self):
        """상세 리포트 생성"""
        print("\n" + "="*80)
        print("[DETAILED-REPORT] 최근 다운로드 파일 전체 분석")
        print("="*80)
        
        if not self.recent_files:
            print("[NO-FILES] 최근 다운로드 파일이 없습니다")
            return
        
        # 1. 전체 요약
        total_size = sum(f['size'] for f in self.recent_files)
        print(f"\n📊 [SUMMARY] 다운로드 요약")
        print(f"   • 총 파일 수: {len(self.recent_files)}개")
        print(f"   • 총 크기: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
        print(f"   • 시간 범위: {self.recent_files[-1]['created_time'].strftime('%m-%d %H:%M')} ~ {self.recent_files[0]['created_time'].strftime('%m-%d %H:%M')}")
        
        # 2. 확장자별 분석
        ext_stats = {}
        for file_info in self.recent_files:
            ext = file_info['extension']
            ext_stats[ext] = ext_stats.get(ext, 0) + 1
        
        print(f"\n📁 [BY-EXTENSION] 파일 형식별")
        for ext, count in sorted(ext_stats.items()):
            print(f"   • {ext}: {count}개")
        
        # 3. 경로별 분석
        path_stats = {}
        for file_info in self.recent_files:
            path = file_info['directory']
            path_stats[path] = path_stats.get(path, 0) + 1
        
        print(f"\n📂 [BY-PATH] 저장 위치별")
        for path, count in sorted(path_stats.items()):
            print(f"   • {path}: {count}개")
        
        # 4. 큰 파일들 (1MB 이상)
        large_files = [f for f in self.recent_files if f['size_mb'] > 1.0]
        if large_files:
            print(f"\n📦 [LARGE-FILES] 큰 파일들 (1MB 이상)")
            for file_info in large_files[:10]:  # 상위 10개
                print(f"   • {file_info['filename']}: {file_info['size_mb']} MB ({file_info['created_time'].strftime('%H:%M')})")
        
        # 5. Cafe24 관련 파일들
        cafe24_files = self.analyze_cafe24_files()
        if cafe24_files:
            print(f"\n☕ [CAFE24-RELATED] Cafe24 관련 파일들")
            for file_info in cafe24_files:
                match_type = "확실" if file_info.get('cafe24_match') == True else "가능성"
                print(f"   • {file_info['filename']}: {file_info['size_mb']} MB ({match_type}) - {file_info['created_time'].strftime('%m-%d %H:%M')}")
        
        # 6. 최근 파일들 타임라인 (최근 20개)
        print(f"\n⏰ [TIMELINE] 최근 다운로드 타임라인 (최근 20개)")
        for file_info in self.recent_files[:20]:
            created = file_info['created_time'].strftime("%m-%d %H:%M")
            size = f"{file_info['size_mb']} MB" if file_info['size_mb'] > 0.01 else f"{file_info['size']} bytes"
            print(f"   {created} | {file_info['extension']} | {size} | {file_info['filename']}")
    
    def save_analysis(self):
        """분석 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recent_downloads_analysis_{timestamp}.json"
        
        # JSON 직렬화를 위해 datetime 변환
        json_data = []
        for file_info in self.recent_files:
            json_file = file_info.copy()
            json_file['created_time'] = file_info['created_time'].isoformat()
            json_file['modified_time'] = file_info['modified_time'].isoformat()
            json_data.append(json_file)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"\n[SAVED] 분석 결과 저장: {filename}")
        except Exception as e:
            print(f"\n[ERROR] 저장 실패: {e}")
    
    def run_complete_check(self, hours_back=6):
        """완전한 최근 파일 체크 실행"""
        print("\n" + "="*80)
        print(f"[COMPLETE-CHECK] 최근 {hours_back}시간 다운로드 파일 전체 체크")
        print("="*80)
        
        # 1. 최근 파일 찾기
        recent_files = self.find_recent_files(hours_back)
        
        # 2. 상세 리포트 생성
        self.generate_detailed_report()
        
        # 3. 결과 저장
        if recent_files:
            self.save_analysis()
        
        print("\n" + "="*80)
        print("[CHECK-COMPLETE] 최근 다운로드 체크 완료")
        print("="*80)
        
        return recent_files

def main():
    """메인 실행"""
    print("="*80)
    print("RECENT DOWNLOADS CHECKER")
    print("사용자 다운로드 파일 전체 발견 및 분석 시스템")
    print("="*80)
    
    checker = RecentDownloadsChecker()
    
    # 최근 6시간 내 파일 체크 (사용자가 "방금 다 다운로드 받았다"고 했으므로)
    recent_files = checker.run_complete_check(hours_back=6)
    
    if recent_files:
        print(f"\n[RESULT] {len(recent_files)}개 최근 다운로드 파일 발견!")
        print("모든 다운로드 방식과 패턴이 분석되었습니다")
    else:
        print(f"\n[RESULT] 최근 6시간 내 다운로드 파일 없음")
        print("시간 범위를 늘려서 다시 확인해보세요")

if __name__ == "__main__":
    main()