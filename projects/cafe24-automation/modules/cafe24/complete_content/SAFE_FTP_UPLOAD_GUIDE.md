# 🔒 안전한 FTP 업로드 가이드

## 폴더 구조 (기존 파일 보호)

```
/web/product/
├── [기존 파일들] - 건드리지 않음 ✅
├── [기존 폴더들] - 건드리지 않음 ✅
└── ai_optimization_20250901/  ← 새로 생성되는 전용 폴더
    ├── manwon/      # 만원요리 상품
    ├── insaeng/     # 인생만두 상품
    ├── ccw/         # 씨씨더블유 상품
    ├── banchan/     # 반찬단지 상품
    ├── chwiyoung/   # 취영루 상품
    ├── mobidick/    # 모비딕 상품
    ├── pizza/       # 피자코리아 상품
    ├── bs/          # BS 상품
    ├── choi/        # 최씨남매 상품
    └── etc/         # 기타 상품
```

## 안전 장치

1. **날짜별 프로젝트 폴더**: `ai_optimization_YYYYMMDD` 형식으로 자동 생성
2. **카테고리별 분류**: 브랜드/카테고리별 하위 폴더 자동 생성
3. **기존 파일 보호**: `/web/product/` 바로 아래 파일들은 절대 건드리지 않음
4. **로컬 미러링**: 모든 업로드 파일 로컬 백업

## 실행 명령

```bash
# 안전한 FTP 업로드 실행
cd C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content
python ftp_image_upload_system.py
```

## URL 예시

```
기존: https://manwonyori.cafe24.com/web/product/[기존파일].jpg
새로: https://manwonyori.cafe24.com/web/product/ai_optimization_20250901/manwon/product_20250901_123456.jpg
```

## 장점

- ✅ 기존 파일 100% 보호
- ✅ 프로젝트별 독립적 관리
- ✅ 브랜드별 체계적 분류
- ✅ 날짜별 버전 관리
- ✅ 롤백 가능한 구조

## 주의사항

- 절대 `/web/product/` 바로 아래에 파일을 업로드하지 않음
- 항상 프로젝트 전용 폴더 사용
- 카테고리별 분류 자동화