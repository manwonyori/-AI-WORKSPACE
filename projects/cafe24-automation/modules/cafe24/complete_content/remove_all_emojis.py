"""모든 파일에서 이모지 제거"""

import re
from pathlib import Path

def remove_emojis(text):
    """텍스트에서 이모지 제거"""
    # 이모지 패턴
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u200d"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\u3030"
        u"\ufe0f"
        "]+", flags=re.UNICODE)
    
    # 제거
    text = emoji_pattern.sub(r'', text)
    
    # 특정 이모지 텍스트로 변환
    replacements = {
        '✅': '[OK]',
        '❌': '[ERROR]',
        '📊': '[STATUS]',
        '📦': '[PACKAGE]',
        '🚀': '[START]',
        '🎯': '[TARGET]',
        '🤖': '[BOT]',
        '🎨': '[ART]',
        '📝': '[DOC]',
        '📤': '[UPLOAD]',
        '💾': '[SAVE]',
        '⏳': '[WAIT]',
        '📈': '[CHART]',
        '✨': '[DONE]',
        '🧪': '[TEST]',
        '🕐': '[TIME]',
        '🖼️': '[IMAGE]',
        '🔄': '[SYNC]',
        '📄': '[FILE]',
        '📋': '[CLIP]',
        '🔒': '[LOCK]',
        '⚡': '[FAST]',
        '🏷️': '[TAG]',
        '📱': '[MOBILE]',
        '🔧': '[TOOL]',
        '📏': '[RULER]',
        '🆘': '[HELP]',
        '📞': '[PHONE]',
        '📍': '[PIN]',
        '🌟': '[STAR]',
        '💡': '[IDEA]'
    }
    
    for emoji, text_replacement in replacements.items():
        text = text.replace(emoji, text_replacement)
    
    return text

# 처리할 파일들
base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")

files_to_clean = [
    "ultimate_image_workflow.py",
    "complete_detail_page_system.py",
    "claude_bridge_template_system.py",
    "ftp_image_upload_system.py",
    "html_design_optimizer.py",
    "html_image_integration.py",
    "image_size_optimizer.py",
    "cafe24_bridge_integration.py"
]

print("Removing emojis from Python files...")
print("-" * 40)

for filename in files_to_clean:
    file_path = base_path / filename
    
    if file_path.exists():
        try:
            # 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 이모지 제거
            clean_content = remove_emojis(content)
            
            # 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
            
            print(f"[OK] {filename}")
            
        except Exception as e:
            print(f"[ERROR] {filename}: {e}")
    else:
        print(f"[SKIP] {filename} - not found")

print("-" * 40)
print("Complete!")