"""
빠른 다운로드 상태 체크
"""
import os
from datetime import datetime

html_folder = r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html"

# 파일 수 계산
total_files = 0
recent_files = []

for root, dirs, files in os.walk(html_folder):
    for file in files:
        if file.endswith('.html'):
            total_files += 1
            file_path = os.path.join(root, file)
            mtime = os.path.getmtime(file_path)
            recent_files.append((file, mtime))

# 최근 파일 정렬
recent_files.sort(key=lambda x: x[1], reverse=True)

print("="*60)
print(f"다운로드 상태 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
print("="*60)
print(f"총 다운로드: {total_files}/239개 ({total_files/239*100:.1f}%)")
print(f"남은 상품: {239-total_files}개")

print("\n최근 다운로드 (최신 10개):")
for file, mtime in recent_files[:10]:
    mod_time = datetime.fromtimestamp(mtime).strftime('%H:%M:%S')
    print(f"  {mod_time} - {file}")

# 마지막 다운로드 시간
if recent_files:
    last_time = datetime.fromtimestamp(recent_files[0][1])
    time_diff = datetime.now() - last_time
    minutes = int(time_diff.total_seconds() / 60)
    print(f"\n마지막 다운로드: {minutes}분 전")
    
    if minutes > 5:
        print("⚠️ 다운로드가 중단된 것 같습니다.")
    else:
        print("✓ 다운로드 진행 중")