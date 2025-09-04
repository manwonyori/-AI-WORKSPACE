# MART 공급업체 관리 시스템 - OCR 사용 가이드

## 시스템 개요

사업자등록증 이미지를 자동으로 분석하여 공급업체 정보를 추출하고 관리하는 시스템입니다.

### 주요 기능
- 사업자등록증 이미지 OCR 처리
- 공급업체 정보 자동 추출 및 저장
- 배송 담당자 정보 통합 관리
- 데이터 내보내기 (JSON, Excel)

## 빠른 시작

### 1. 시스템 테스트
```bash
# 시스템 테스트 실행 (OCR 라이브러리 확인)
test_system.bat
```

### 2. 메인 프로그램 실행
```bash
# OCR 시스템 실행
run_ocr.bat
```

## OCR 라이브러리 설치

### 필수 라이브러리 설치
```bash
pip install pytesseract opencv-python pillow
```

### Tesseract OCR 설치
1. [Tesseract 다운로드](https://github.com/UB-Mannheim/tesseract/wiki) 
2. Windows용 설치 파일 다운로드 및 실행
3. 설치 시 한국어 언어팩 선택
4. 환경 변수 PATH에 Tesseract 경로 추가

## 사용 방법

### 1. 사업자등록증 이미지 준비
- 지원 형식: JPG, PNG, GIF, BMP, TIFF
- 권장: 고해상도 스캔 이미지
- 텍스트가 선명하게 보이도록 촬영/스캔

### 2. 프로그램 실행
1. `run_ocr.bat` 실행
2. 메뉴에서 "1. 사업자등록증 이미지 처리 및 공급업체 등록" 선택
3. 이미지 파일 경로 입력 또는 드래그 앤 드롭

### 3. 정보 확인 및 수정
- OCR이 자동 추출한 정보 확인
- 필요시 수정 (Enter를 누르면 OCR 결과 사용)
- 추가 정보 입력 (취급 품목, 이메일 등)

### 4. 데이터 관리
- 등록된 공급업체 목록 조회
- Excel/JSON 형식으로 데이터 내보내기

## 자동 추출되는 정보

### OCR로 자동 추출
- 사업자등록번호
- 상호명
- 대표자명
- 사업장 주소
- 업태
- 종목

### 수동 입력 항목
- 취급 품목 (쉼표로 구분)
- 담당자 이메일
- 비고

### 자동 저장 정보
- 배송지: 경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층 웰빙 푸드마켓
- 담당자: 윤철 대리
- 연락처: 010-7727-8009

## 파일 구조

```
mart-project/
│
├── process_business_license.py   # 메인 실행 파일
├── test_ocr_system.py            # 시스템 테스트
├── run_ocr.bat                   # 실행 배치 파일
├── test_system.bat               # 테스트 배치 파일
│
├── src/
│   ├── image_processor.py       # OCR 처리 모듈
│   ├── supplier_manager.py      # 공급업체 관리
│   └── document_generator.py    # 문서 생성
│
└── data/
    ├── suppliers.json            # 공급업체 데이터
    ├── delivery_contacts.json   # 담당자 정보
    ├── business_licenses/        # 이미지 파일
    └── processed_licenses/       # 처리된 데이터
```

## 문제 해결

### OCR이 작동하지 않는 경우
1. `test_system.bat` 실행하여 라이브러리 설치 확인
2. Tesseract OCR 설치 확인
3. 수동 입력 모드로 진행

### 이미지 인식률이 낮은 경우
- 고해상도 이미지 사용
- 이미지가 기울어지지 않도록 정방향 스캔
- 배경이 깨끗한 이미지 사용

### 한글 인식이 안 되는 경우
- Tesseract 한국어 언어팩 설치 확인
- `tesseract --list-langs` 명령으로 'kor' 확인

## 데이터 백업

정기적으로 `data/` 폴더를 백업하여 데이터 손실을 방지하세요.

## 지원

문제가 있거나 개선 사항이 있으면 담당자에게 문의하세요.

---
MART 공급망 관리 시스템 v1.0
2024년 개발