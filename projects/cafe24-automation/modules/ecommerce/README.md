# 한국 이커머스 상품 처리 시스템

## 시작하기
```bash
1. 초기설치.bat    # 처음 한 번만
2. 처리시스템.bat  # 메인 프로그램
```

## 기능
- **빠른 처리**: API 없이 40개 키워드 생성 (초당 20개)
- **AI 처리**: OpenAI/Claude API로 고품질 키워드

## 폴더 구조
```
├── 처리시스템.bat      # 메인
├── 초기설치.bat       # 설치
├── data/
│   ├── input/        # 입력 CSV
│   └── output/       # 결과 CSV
└── src/
    ├── quick_processor.py    # 빠른 처리
    └── main_system.py        # AI 처리
```