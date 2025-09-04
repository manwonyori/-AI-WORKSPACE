# 이미지 저장 디렉토리 구조

## 디렉토리 설명

### 📁 pending/ (대기중)
- **용도**: 처리 대기 중인 새로운 사업자등록증 이미지
- **경로**: `C:\Users\8899y\mart-project\data\images\pending`
- **예시**: 새로 받은 사업자등록증 사진을 여기에 저장

### 📁 business_licenses/ (원본 보관)
- **용도**: 처리된 사업자등록증 원본 이미지 보관
- **경로**: `C:\Users\8899y\mart-project\data\images\business_licenses`
- **파일명 규칙**: `{사업자번호}_{날짜}.jpg`
- **예시**: `1234567890_20240128.jpg`

### 📁 processed/ (처리 완료)
- **용도**: OCR 처리가 완료된 이미지
- **경로**: `C:\Users\8899y\mart-project\data\images\processed`
- **보관 기간**: 30일

### 📁 archive/ (보관)
- **용도**: 오래된 이미지 장기 보관
- **경로**: `C:\Users\8899y\mart-project\data\images\archive`
- **구조**: 연도별/월별 하위 폴더

## 권장 사용 방법

1. **새 이미지 추가시**
   ```
   1. pending/ 폴더에 이미지 저장
   2. 시스템이 자동으로 처리
   3. 처리 완료 후 business_licenses/로 이동
   ```

2. **파일명 규칙**
   - 한글 파일명 가능
   - 공백 대신 언더스코어(_) 사용
   - 예: `신선식품유통_사업자등록증.jpg`

3. **지원 형식**
   - JPG, JPEG
   - PNG
   - PDF
   - TIFF

## 빠른 경로 복사

Windows 탐색기에서 바로 가기:
```
Win + R → 다음 경로 입력:

C:\Users\8899y\mart-project\data\images\pending
```