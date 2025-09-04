# Mart Supply Manager 프로젝트

식자재 공급망 관리 자동화 시스템

## 주요 기능

1. **공급업체 관리**
   - 사업자등록증 이미지 인식 및 정보 추출
   - 공급업체 데이터베이스 관리
   - 거래 이력 추적

2. **재고 관리**
   - 실시간 재고 모니터링
   - 자동 발주 시스템
   - 재고 예측 분석

3. **거래 문서 자동화**
   - 발주서 자동 생성
   - 거래명세서 관리
   - 월간 정산 보고서

4. **데이터 분석**
   - 공급 패턴 분석
   - 가격 동향 모니터링
   - 품질 관리 지표

## 프로젝트 구조

```
mart-project/
├── data/           # 데이터 파일
├── docs/           # 문서
├── src/            # 소스 코드
├── tests/          # 테스트 코드
└── config/         # 설정 파일
```

## 시작하기

1. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

2. 설정 파일 구성
```bash
cp config/config.example.yml config/config.yml
```

3. 시스템 실행
```bash
python src/main.py
```