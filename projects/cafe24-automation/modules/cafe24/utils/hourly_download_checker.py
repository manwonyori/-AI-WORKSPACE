# -*- coding: utf-8 -*-
"""
Hourly Download Checker - download 폴더 시간별 다운로드 체크
download 폴더에서 시간별로 파일 체크
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import time
import glob
import json
from datetime import datetime, timedelta
from pathlib import Path

class HourlyDownloadChecker:
    """시간별 다운로드 체크 시스템"""
    
    def __init__(self):
        """초기화"""
        self.download_folder = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\download"
        self.file_extensions = ['.xlsx', '.xls', '.csv', '.txt', '.json', '.html', '.xml', '.pdf']
        self.hourly_files = {}
        
        # download 폴더 생성
        os.makedirs(self.download_folder, exist_ok=True)
        
        print("[HOURLY-CHECKER] 시간별 다운로드 체크 시스템")
        print(f"[TARGET-FOLDER] {self.download_folder}")
        
    def scan_download_folder(self):
        """download 폴더 전체 스캔"""
        print(f"\n[SCAN] download 폴더 전체 스캔...")
        
        all_files = []
        total_size = 0
        
        # 모든 확장자 파일 찾기
        for ext in self.file_extensions:
            pattern = os.path.join(self.download_folder, f"*{ext}")
            files = glob.glob(pattern)
            
            for file_path in files:
                try:
                    stat_info = os.stat(file_path)
                    
                    file_info = {
                        'file_path': file_path,
                        'filename': os.path.basename(file_path),
                        'extension': ext,
                        'size': stat_info.st_size,
                        'size_mb': round(stat_info.st_size / 1024 / 1024, 2),
                        'created_time': datetime.fromtimestamp(stat_info.st_ctime),
                        'modified_time': datetime.fromtimestamp(stat_info.st_mtime),
                        'created_hour': datetime.fromtimestamp(stat_info.st_ctime).strftime("%Y-%m-%d %H:00"),
                        'age_hours': round((time.time() - stat_info.st_ctime) / 3600, 1)
                    }
                    
                    all_files.append(file_info)
                    total_size += stat_info.st_size
                    
                except Exception as e:
                    print(f"   [ERROR] {file_path}: {e}")
                    continue
        
        # 생성 시간 순으로 정렬 (최신순)
        all_files.sort(key=lambda x: x['created_time'], reverse=True)
        
        print(f"   [FOUND] 총 {len(all_files)}개 파일")
        print(f"   [SIZE] 총 크기: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
        
        return all_files
    
    def group_by_hour(self, files):
        """시간별로 파일 그룹화"""
        print(f"\n[GROUP] 시간별 파일 그룹화...")
        
        hourly_groups = {}
        
        for file_info in files:
            hour_key = file_info['created_hour']
            
            if hour_key not in hourly_groups:
                hourly_groups[hour_key] = {
                    'files': [],
                    'count': 0,
                    'total_size': 0,
                    'extensions': set()
                }
            
            hourly_groups[hour_key]['files'].append(file_info)
            hourly_groups[hour_key]['count'] += 1
            hourly_groups[hour_key]['total_size'] += file_info['size']
            hourly_groups[hour_key]['extensions'].add(file_info['extension'])
        
        # 시간순 정렬
        sorted_hours = sorted(hourly_groups.keys(), reverse=True)
        
        print(f"   [HOURS] {len(sorted_hours)}개 시간대에 걸쳐 다운로드")
        
        self.hourly_files = hourly_groups
        return hourly_groups, sorted_hours
    
    def analyze_download_patterns(self, hourly_groups, sorted_hours):
        """다운로드 패턴 분석"""
        print(f"\n[PATTERN-ANALYSIS] 다운로드 패턴 분석...")
        
        analysis = {
            'total_files': sum(group['count'] for group in hourly_groups.values()),
            'total_size': sum(group['total_size'] for group in hourly_groups.values()),
            'active_hours': len(sorted_hours),
            'busiest_hour': None,
            'largest_hour': None,
            'extension_stats': {},
            'recent_activity': []
        }
        
        # 가장 바쁜 시간 (파일 수 기준)
        if hourly_groups:
            busiest = max(hourly_groups.items(), key=lambda x: x[1]['count'])
            analysis['busiest_hour'] = {
                'hour': busiest[0],
                'file_count': busiest[1]['count']
            }
            
            # 가장 큰 다운로드 시간 (크기 기준)
            largest = max(hourly_groups.items(), key=lambda x: x[1]['total_size'])
            analysis['largest_hour'] = {
                'hour': largest[0],
                'size_mb': round(largest[1]['total_size'] / 1024 / 1024, 1)
            }
        
        # 확장자 통계
        for group in hourly_groups.values():
            for ext in group['extensions']:
                analysis['extension_stats'][ext] = analysis['extension_stats'].get(ext, 0) + 1
        
        # 최근 24시간 활동
        cutoff_time = datetime.now() - timedelta(hours=24)
        for hour, group in hourly_groups.items():
            hour_dt = datetime.strptime(hour, "%Y-%m-%d %H:00")
            if hour_dt > cutoff_time:
                analysis['recent_activity'].append({
                    'hour': hour,
                    'files': group['count'],
                    'size_mb': round(group['total_size'] / 1024 / 1024, 1)
                })
        
        analysis['recent_activity'].sort(key=lambda x: x['hour'], reverse=True)
        
        print(f"   [TOTAL] 총 {analysis['total_files']}개 파일, {analysis['total_size']/1024/1024:.1f} MB")
        if analysis['busiest_hour']:
            print(f"   [BUSIEST] {analysis['busiest_hour']['hour']}: {analysis['busiest_hour']['file_count']}개 파일")
        if analysis['largest_hour']:
            print(f"   [LARGEST] {analysis['largest_hour']['hour']}: {analysis['largest_hour']['size_mb']} MB")
        
        return analysis
    
    def generate_hourly_report(self, hourly_groups, sorted_hours, analysis):
        """시간별 상세 리포트 생성"""
        print("\n" + "="*80)
        print("[HOURLY-REPORT] download 폴더 시간별 다운로드 분석")
        print("="*80)
        
        if not hourly_groups:
            print("[NO-FILES] download 폴더에 파일이 없습니다")
            return
        
        # 1. 전체 요약
        print(f"\n[SUMMARY] 전체 요약")
        print(f"   - 총 파일: {analysis['total_files']}개")
        print(f"   - 총 크기: {analysis['total_size']:,} bytes ({analysis['total_size']/1024/1024:.1f} MB)")
        print(f"   - 활동 시간대: {analysis['active_hours']}개")
        
        if analysis['busiest_hour']:
            print(f"   - 가장 바쁜 시간: {analysis['busiest_hour']['hour']} ({analysis['busiest_hour']['file_count']}개)")
        if analysis['largest_hour']:
            print(f"   - 가장 큰 다운로드: {analysis['largest_hour']['hour']} ({analysis['largest_hour']['size_mb']} MB)")
        
        # 2. 확장자별 통계
        print(f"\n[EXTENSIONS] 파일 형식별")
        for ext, count in sorted(analysis['extension_stats'].items()):
            print(f"   - {ext}: {count}개")
        
        # 3. 시간별 상세 내역 (최근 24시간)
        print(f"\n[HOURLY-DETAILS] 시간별 상세 내역 (최근부터)")
        recent_hours = sorted_hours[:24]  # 최근 24시간
        
        for hour in recent_hours:
            group = hourly_groups[hour]
            size_mb = group['total_size'] / 1024 / 1024
            extensions = ', '.join(sorted(group['extensions']))
            
            print(f"\n   {hour}")
            print(f"     파일: {group['count']}개, 크기: {size_mb:.1f} MB")
            print(f"     형식: {extensions}")
            
            # 파일 목록 (최대 5개)
            for file_info in group['files'][:5]:
                age = file_info['age_hours']
                age_str = f"{age:.1f}h" if age < 24 else f"{age/24:.1f}d"
                print(f"     - {file_info['filename']} ({file_info['size_mb']} MB) - {age_str} ago")
            
            if len(group['files']) > 5:
                print(f"     ... 및 {len(group['files'])-5}개 더")
        
        # 4. 최근 활동 (24시간 내)
        if analysis['recent_activity']:
            print(f"\n[RECENT-ACTIVITY] 최근 24시간 활동")
            for activity in analysis['recent_activity']:
                print(f"   {activity['hour']}: {activity['files']}개 파일, {activity['size_mb']} MB")
    
    def save_hourly_analysis(self, hourly_groups, analysis):
        """시간별 분석 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hourly_download_analysis_{timestamp}.json"
        
        # JSON 직렬화를 위해 datetime 변환
        json_data = {
            'analysis': analysis,
            'hourly_groups': {}
        }
        
        for hour, group in hourly_groups.items():
            json_group = {
                'count': group['count'],
                'total_size': group['total_size'],
                'extensions': list(group['extensions']),
                'files': []
            }
            
            for file_info in group['files']:
                json_file = file_info.copy()
                json_file['created_time'] = file_info['created_time'].isoformat()
                json_file['modified_time'] = file_info['modified_time'].isoformat()
                json_group['files'].append(json_file)
            
            json_data['hourly_groups'][hour] = json_group
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"\n[SAVED] 시간별 분석 결과 저장: {filename}")
        except Exception as e:
            print(f"\n[ERROR] 저장 실패: {e}")
    
    def run_hourly_check(self):
        """시간별 체크 전체 실행"""
        print("\n" + "="*80)
        print("[HOURLY-CHECK] download 폴더 시간별 다운로드 체크 시작")
        print("="*80)
        
        # 1. 폴더 스캔
        all_files = self.scan_download_folder()
        
        if not all_files:
            print("\n[RESULT] download 폴더에 파일이 없습니다")
            return None
        
        # 2. 시간별 그룹화
        hourly_groups, sorted_hours = self.group_by_hour(all_files)
        
        # 3. 패턴 분석
        analysis = self.analyze_download_patterns(hourly_groups, sorted_hours)
        
        # 4. 상세 리포트 생성
        self.generate_hourly_report(hourly_groups, sorted_hours, analysis)
        
        # 5. 결과 저장
        self.save_hourly_analysis(hourly_groups, analysis)
        
        print("\n" + "="*80)
        print("[HOURLY-CHECK-COMPLETE] 시간별 다운로드 체크 완료")
        print("="*80)
        
        return analysis

def main():
    """메인 실행"""
    print("="*80)
    print("HOURLY DOWNLOAD CHECKER")
    print("download 폴더 시간별 다운로드 체크 및 분석 시스템")
    print("="*80)
    
    checker = HourlyDownloadChecker()
    analysis = checker.run_hourly_check()
    
    if analysis:
        print(f"\n[RESULT] {analysis['total_files']}개 파일 시간별 분석 완료!")
        print(f"활동 시간대: {analysis['active_hours']}개")
        print("시간별 다운로드 패턴이 완전히 분석되었습니다")
    else:
        print(f"\n[RESULT] download 폴더가 비어있습니다")
        print("다운로드 후 다시 실행해주세요")

if __name__ == "__main__":
    main()