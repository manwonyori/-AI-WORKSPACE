"""이모지 제거 스크립트"""

import re

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
    
    return emoji_pattern.sub(r'', text)

# MASTER_INTEGRATION_SYSTEM.py 파일 처리
file_path = r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\MASTER_INTEGRATION_SYSTEM.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 이모지 제거
clean_content = remove_emojis(content)

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
    '🔄': '[SYNC]'
}

for emoji, text in replacements.items():
    clean_content = clean_content.replace(emoji, text)

# 저장
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(clean_content)

print(f"이모지 제거 완료: {file_path}")