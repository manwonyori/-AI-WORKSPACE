import re
from pathlib import Path

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 상세정보 섹션 삭제
    content = re.sub(r'        <!-- 상세정보 -->.*?        </div>\n        ', '', content, flags=re.DOTALL)
    
    # 2. 알레르기 박스 삭제
    content = re.sub(r'            <!-- 알레르기 정보.*?</div>\n            ', '', content, flags=re.DOTALL)
    
    # 3. 보관 박스 삭제  
    content = re.sub(r'            <!-- 보관.*?</div>', '', content, flags=re.DOTALL)
    
    # 4. 직접 div 박스들도 삭제
    content = re.sub(r'<div style="background: #fff3cd.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div style="background: #e7f3ff.*?</div>', '', content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

files = ['132_final_clean.html', '133_final_clean.html', '134_final_clean.html', '135_final_clean.html', '140_final_clean.html']
for file_name in files:
    clean_file(file_name)
    print(f"정리완료: {file_name}")