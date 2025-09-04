# Cafe24 모듈
**최종 업데이트**: 2025-09-01

## 📊 현황
- **총 HTML 파일**: 249개
- **complete_content**: 226개
- **product_html_management**: 13개

## 🚀 핵심 시스템

### CUA Agent
- `core/unified_cua_agent.py` - 통합 자동화
- `core/direct_url_cua_agent.py` - URL 직접 접근
- `core/html_content_replacer.py` - HTML 콘텐츠 관리

### 학습 시스템
- `cafe24_unified_learner.py` - 통합 학습
- `cafe24_deep_section_learner.py` - 심층 학습
- `section_structure_viewer.py` - 구조 분석

### 이미지 관리
- `image_backup_manager.py` - 백업 관리
- `enhanced_image_matching_verification.py` - 매칭 검증

## 📁 구조
```
cafe24/
├── complete_content/    # 완성 HTML (226개)
├── product_html_management/  # 최신 관리 (13개)
├── core/               # CUA Agent
├── learning/           # 학습 데이터
├── download/           # CSV 다운로드
└── config/            # 설정
```

## ✅ 사용법
```bash
# CUA Agent 실행
python core/unified_cua_agent.py

# 학습 시스템
python cafe24_unified_learner.py
```
  HTML 다운로드 관련 파일들:

  1. Excel/CSV 다운로드 파일들:

  - C:\Users\8899y\CUA-MASTER\modules\cafe24\download\study.cafe24.py - Excel 다운로드
  - C:\Users\8899y\CUA-MASTER\modules\cafe24\download\direct_url_cua_agent.py - URL 직접 접근 다운로드
  - C:\Users\8899y\CUA-MASTER\modules\cafe24\auto_excel_download.py - 자동 Excel 다운로드

  2. HTML 콘텐츠 처리 파일들:

  - C:\Users\8899y\CUA-MASTER\modules\cafe24\core\html_content_replacer.py - HTML 편집기 콘텐츠 대체
  - C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html_content_replacer.py - HTML 콘텐츠 완전 대체 시스템

  3. 통합 다운로드 시스템:

  - C:\Users\8899y\CUA-MASTER\modules\cafe24\core\unified_cua_agent.py - 통합 CUA 에이전트

  실제 HTML 다운로드를 수행하는 메인 파일은:
  - html_content_replacer.py - Cafe24 관리자 페이지에서 HTML 편집기에 접근하여 콘텐츠를 다운로드/업로드하는 파일입니다.

  이 파일이 Selenium을 사용하여:
  1. Cafe24 관리자 로그인
  2. 상품 편집 페이지 접근
  3. HTML 편집기(Froala Editor iframe) 탐색
  4. HTML 콘텐츠 추출/대체
  5. 저장 기능

  을 수행합니다.

   C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\
  ├── scripts\                      # Python 스크립트들 (9개)
  │   ├── complete_reclassification.py    # 핵심 분류 스크립트
  │   ├── organize_files.py
  │   ├── extract_and_verify_images.py
  │   ├── apply_txt_to_html.py
  │   ├── classify_by_brand_name.py
  │   ├── classify_by_product_name.py
  │   ├── clean_and_consolidate_folders.py
  │   ├── complete_verification.py
  │   └── README.md
  ├── test\                         # 테스트 파일들
  │   └── dashboard.html
  ├── reports\                      # 리포트들
  │   ├── FINAL_CLASSIFICATION_REPORT.md
  │   └── complete_reclassification_20250901_153014.txt
  ├── html\                         # 브랜드별 HTML 파일들
  │   ├── temp_txt\                # 239개 TXT 원본 보존
  │   ├── 기타\, 단지식품유통\, 만원요리\ 등 12개 브랜드 폴더
  │   └── 237개 HTML 파일 (브랜드별 분류 완료)
  ├── images\                       # 브랜드별 이미지
  ├── config\, database\, backup\, modified\ # 기타 폴더들
  └── README.md, FINAL_SUMMARY.md   # 문서들

  🎯 중요한 보존 사항:
  - temp_txt 폴더: 239개 원본 TXT 파일 완전 보존
  - 브랜드별 HTML 폴더: 12개 브랜드, 237개 HTML 파일
  - 핵심 스크립트: complete_reclassification.py (완전한 재분류)

  요청하신 대로 완전한 파일 구조가 복구되었습니다!