# Cafe24 Complete Content Management System

## 📁 폴더 구조

```
complete_content/
├── config/              # 설정 파일
│   ├── cafe24_config.json
│   └── CONTENT_STRUCTURE.json
├── scripts/             # 실행 스크립트  
│   ├── html_downloader.py      # HTML 다운로더
│   ├── cross_check_system.py   # 교차 검증
│   └── ...
├── reports/             # 분석 리포트
│   ├── csv_html_validation_*.json
│   └── html_download_report_*.json
├── test/               # 테스트 스크립트
│   └── test_html_download.py
├── html/               # 다운로드된 HTML
│   ├── 인생/
│   ├── 반찬단지/
│   ├── 씨씨더블유/
│   ├── 취영루/
│   ├── 인생만두/
│   ├── 만원요리/
│   ├── 해선/
│   ├── 비에스/
│   ├── 기타/
│   └── temp_txt/       # TXT 임시 파일 (239개)
└── backup/             # 백업 파일
```

## 🚀 주요 스크립트

### 1. HTML 다운로더
```bash
python scripts/html_downloader.py
```
- Cafe24 관리자 페이지에서 상품 HTML 다운로드
- 상품번호 기반 파일명 저장 (27.html, 28.html 등)
- 브랜드별 자동 분류

### 2. 교차 검증 시스템
```bash
python scripts/cross_check_system.py
```
- CSV와 HTML 파일 일치성 검증
- 누락된 파일 확인
- 데이터 무결성 체크

### 3. 공급사 분류 업데이트
```bash
python scripts/update_supplier_classification.py
```
- CSV 기준으로 HTML 파일 재분류
- 브랜드별 폴더 정리

### 4. FTP 미러 정리
```bash
python scripts/clean_ftp_mirror.py
```
- FTP 다운로드 파일 정리
- 확장자 수정 (.jpeg → .jpg)
- 중복 제거

## 📊 현재 상태

- **총 상품 수**: 239개
- **다운로드 완료**: 239개 (100%)
- **브랜드 분류**: 
  - 인생: 47개
  - 반찬단지: 39개
  - 씨씨더블유: 28개
  - 취영루: 33개
  - 인생만두: 25개
  - 만원요리: 41개
  - 해선: 18개
  - 비에스: 6개
  - 기타: 2개

## ⚙️ 설정

`config/cafe24_config.json` 파일 구조:
```json
{
  "cafe24": {
    "admin_url": "https://manwonyori.cafe24.com/admin/",
    "mall_id": "manwonyori",
    "username": "manwonyori",
    "password": "****"
  }
}
```

## 📝 파일 설명

### Config 폴더
- `cafe24_config.json`: Cafe24 로그인 정보
- `CONTENT_STRUCTURE.json`: 콘텐츠 구조 정의

### Scripts 폴더  
- `html_downloader.py`: 메인 HTML 다운로더
- `cross_check_system.py`: CSV-HTML 검증
- `csv_html_validator.py`: CSV 데이터 검증
- `deep_corruption_analyzer.py`: 손상 파일 분석
- `extract_image_links.py`: 이미지 링크 추출
- `extract_product_data.py`: 상품 데이터 추출
- `html_content_replacer.py`: HTML 콘텐츠 교체
- `image_backup_manager.py`: 이미지 백업 관리
- `master_integration.py`: 통합 관리
- `sftp_downloader.py`: SFTP 다운로더
- `clean_ftp_mirror.py`: FTP 미러 정리
- `fix_ftp_extensions.py`: 파일 확장자 수정
- `full_ftp_download.py`: 전체 FTP 다운로드

### Reports 폴더
- `csv_html_validation_*.json`: 검증 리포트
- `deep_corruption_analysis_*.json`: 손상 분석 리포트
- `html_download_report_*.json`: 다운로드 리포트
- `organization_report_*.json`: 파일 정리 리포트

## 🔄 워크플로우

1. **CSV 데이터 확인**
   ```bash
   python scripts/csv_html_validator.py
   ```

2. **HTML 다운로드**
   ```bash
   python scripts/html_downloader.py
   ```

3. **교차 검증**
   ```bash
   python scripts/cross_check_system.py
   ```

4. **공급사 분류 업데이트**
   ```bash
   python scripts/update_supplier_classification.py
   ```

## 📌 참고사항

1. HTML 파일은 상품번호로 저장 (예: 338.html)
2. TXT 임시 파일은 `html/temp_txt/`에 보관
3. 모든 리포트는 타임스탬프와 함께 저장
4. FTP 미러는 별도 경로: `../ftp_mirror/`

## 🗓️ 마지막 업데이트
2025-09-01 14:52