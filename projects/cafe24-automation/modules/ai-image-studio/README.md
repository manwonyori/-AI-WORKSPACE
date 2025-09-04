# AI Image Studio

고급 AI 이미지 생성 자동화 시스템 - 멀티 플랫폼 지원, 품질 분석, 지능형 최적화

## 🎯 주요 기능

### Phase 3 - 프롬프트 엔진
- **고급 프롬프트 생성**: 템플릿 기반 프롬프트 자동 생성
- **A/B 테스트**: 프롬프트 성능 비교 및 최적화
- **품질 평가**: 자동화된 프롬프트 품질 평가 시스템
- **라이브러리 관리**: 고품질 프롬프트 라이브러리 구축

### Phase 4 - 멀티모달 분석 시스템
- **이미지 품질 분석**: 기술적/미학적 품질 자동 평가
- **프롬프트 매칭**: 생성된 이미지와 원본 프롬프트 일치도 분석
- **자동 태깅**: AI 기반 이미지 태그 자동 생성
- **피드백 루프**: 지속적 개선을 위한 학습 시스템

### Phase 5 - 통합 CLI 인터페이스
- **멀티 플랫폼**: Midjourney, DALL-E, Stable Diffusion 지원
- **배치 처리**: 대량 이미지 생성 자동화
- **실시간 분석**: 생성과 동시에 품질 분석
- **결과 리포팅**: 상세한 성능 및 품질 리포트

### 자동화 워크플로우
- **스케줄링**: 크론 작업 기반 자동화
- **모니터링**: 실시간 시스템 상태 감시
- **알림 시스템**: 이메일/웹훅 기반 알림

### AI Council 통합
- **협업적 프롬프트 생성**: 다중 AI 에이전트 협업
- **품질 검토**: 다중 관점 품질 평가
- **합의 기반 최적화**: AI 에이전트 간 합의를 통한 개선

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone <repository-url>
cd CUA-MASTER/modules/ai-image-studio

# 의존성 설치
pip install -r requirements.txt
```

### 기본 사용법

```bash
# 단일 이미지 생성
python ai_studio_cli.py generate --product "고추장 오돌뼈" --style product_showcase --platform midjourney

# 배치 생성
python ai_studio_cli.py batch --input products.csv --styles product_showcase,lifestyle --platforms midjourney,dalle

# 이미지 분석
python ai_studio_cli.py analyze --image path/to/image.jpg --prompt prompt_data.json

# 프롬프트 최적화
python ai_studio_cli.py optimize --prompt "product photo" --goals higher_quality,more_creative

# A/B 테스트
python ai_studio_cli.py ab-test --prompt-a "photo A" --prompt-b "photo B" --name "test1"
```

### 설정

```bash
# 플랫폼 API 키 설정
python ai_studio_cli.py config --platform dalle --api-key your-api-key

# 모니터링 시작
python monitoring.py

# 스케줄러 시작  
python scheduler.py
```

## 📁 프로젝트 구조

```
ai-image-studio/
├── prompts/                    # 프롬프트 템플릿
│   └── prompt_templates.json   # 기본 템플릿 정의
├── generated/                  # 생성된 이미지
├── analysis/                   # 분석 결과 및 데이터베이스
├── models/                     # 학습된 모델
├── config/                     # 설정 파일
├── logs/                       # 로그 파일
├── prompt_engine.py           # Phase 3: 프롬프트 엔진
├── image_analyzer.py          # Phase 4: 이미지 분석
├── ai_studio_cli.py          # Phase 5: CLI 인터페이스
├── scheduler.py               # 자동화 스케줄러
├── monitoring.py              # 실시간 모니터링
├── ai_council_integration.py  # AI Council 통합
├── test_system.py            # 시스템 테스트
└── requirements.txt          # 의존성 목록
```

## 🎛️ CLI 명령어 상세

### generate - 단일 이미지 생성
```bash
python ai_studio_cli.py generate \
  --product "Korean BBQ" \
  --category food \
  --style product_showcase \
  --platform midjourney \
  --no-analyze  # 분석 건너뛰기
```

### batch - 배치 이미지 생성
```bash
python ai_studio_cli.py batch \
  --input products.csv \
  --category food \
  --styles product_showcase,lifestyle,ingredient_focus \
  --platforms midjourney,dalle \
  --output-report batch_report.json
```

### analyze - 이미지 분석
```bash
python ai_studio_cli.py analyze \
  --image path/to/image.jpg \
  --prompt prompt_data.json \
  --brief  # 간단한 분석만
```

### optimize - 프롬프트 최적화
```bash
python ai_studio_cli.py optimize \
  --prompt "professional product photography" \
  --goals higher_quality,more_creative,faster \
  --variations 5
```

### ab-test - A/B 테스트
```bash
# 테스트 생성
python ai_studio_cli.py ab-test \
  --prompt-a "modern product photo" \
  --prompt-b "artistic product photo" \
  --name "modern_vs_artistic"

# 결과 기록
python ai_studio_cli.py record-ab \
  --test-id test_12345 \
  --variant a \
  --score 85.5

# 분석
python ai_studio_cli.py analyze-ab --test-id test_12345
```

### export - 라이브러리 내보내기
```bash
python ai_studio_cli.py export \
  --output high_quality_prompts.json \
  --min-quality 80
```

## 🔧 고급 설정

### 프롬프트 템플릿 커스터마이징
`prompts/prompt_templates.json` 파일을 편집하여 새로운 템플릿 추가:

```json
{
  "categories": {
    "food": {
      "base_templates": {
        "custom_style": "Your custom prompt template with {product_name}"
      }
    }
  }
}
```

### 모니터링 설정
`config/monitoring_config.json`에서 임계값 및 알림 설정:

```json
{
  "thresholds": {
    "cpu_usage_percent": 80,
    "memory_usage_percent": 85,
    "avg_quality_score": 70
  },
  "alerts": {
    "email": {
      "smtp_server": "smtp.gmail.com",
      "username": "your-email@gmail.com",
      "to_addresses": ["admin@company.com"]
    }
  }
}
```

### AI Council 통합 설정
`config/ai_council_integration.json`에서 AI 에이전트 설정:

```json
{
  "agents": {
    "claude": {
      "enabled": true,
      "role": "prompt_optimization",
      "weight": 0.4
    },
    "gpt4": {
      "enabled": true,
      "role": "creative_direction", 
      "weight": 0.3
    }
  }
}
```

## 📊 성능 및 모니터링

### 실시간 모니터링
시스템 상태, 생성 성능, 품질 메트릭을 실시간으로 모니터링:

```python
from monitoring import SystemMonitor

monitor = SystemMonitor()
monitor.start_monitoring()

# 상태 확인
status = monitor.get_current_status()
print(f"시스템 상태: {status['health_status']}")
```

### 성능 벤치마크
```python
from test_system import run_performance_tests

results = run_performance_tests()
print(f"평균 프롬프트 생성 시간: {results['avg_prompt_generation_time']:.4f}초")
print(f"처리량: {results['throughput_per_second']:.1f} prompts/sec")
```

## 🔄 자동화 워크플로우

### 일일 배치 생성 스케줄링
```python
from scheduler import TaskScheduler

scheduler = TaskScheduler()

# 매일 오전 9시 배치 생성
job_id = scheduler.schedule_batch_generation(
    name="Daily Product Generation",
    products_file="daily_products.csv",
    schedule_type="daily",
    schedule_value="09:00"
)

scheduler.start()
```

### 품질 모니터링 자동화
```python
# 매시간 품질 체크
monitor_id = scheduler.schedule_quality_monitoring(
    name="Hourly Quality Check",
    interval_minutes=60,
    quality_threshold=75
)
```

## 🤖 AI Council 협업

### 협업적 프롬프트 생성
```python
import asyncio
from ai_council_integration import AICouncilImageStudioBridge

bridge = AICouncilImageStudioBridge()

async def collaborative_generation():
    result = await bridge.collaborative_prompt_generation(
        product_data={"name": "Korean Traditional Food"},
        category="food",
        style="product_showcase"
    )
    return result

# 실행
result = asyncio.run(collaborative_generation())
```

### 다중 에이전트 품질 검토
```python
async def multi_agent_review():
    analysis = await bridge.multi_agent_quality_review(
        image_path="generated_image.jpg",
        prompt_data=prompt_data
    )
    return analysis
```

## 🔗 통합 시스템

### Cafe24 연동
기존 Cafe24 시스템과 자동 연동:

```python
# Cafe24 상품 이미지 자동 분석 및 개선
integration_result = bridge.integrate_with_cafe24_workflow()

print(f"분석된 이미지: {integration_result['analyzed_images']}")
print(f"개선 필요 이미지: {integration_result['images_needing_improvement']}")
```

## 🧪 테스트

### 전체 시스템 테스트
```bash
# 단위 테스트 및 통합 테스트
python test_system.py

# 성능 테스트
python -c "from test_system import run_performance_tests; run_performance_tests()"
```

### 개별 컴포넌트 테스트
```bash
# 프롬프트 엔진 테스트
python -m unittest test_system.TestPromptEngine

# 이미지 분석기 테스트  
python -m unittest test_system.TestImageAnalyzer
```

## 📈 품질 메트릭

시스템이 추적하는 주요 메트릭:

- **기술적 품질**: 선명도, 노이즈, 밝기, 대비
- **미학적 품질**: 색상 조화, 구성, 시각적 균형
- **프롬프트 일치도**: 생성된 이미지와 프롬프트 일치 정도
- **전체 점수**: 가중 평균 종합 점수

## 🚀 배포 및 확장

### Docker 배포
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "ai_studio_cli.py"]
```

### 클라우드 배포
GitHub Actions를 통한 CI/CD 파이프라인이 자동으로:
- 테스트 실행
- 보안 스캔
- 성능 벤치마크
- Docker 이미지 빌드
- 문서 배포

## 🤝 기여하기

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🆘 지원 및 문의

- 이슈: GitHub Issues 탭에서 버그 리포트 및 기능 요청
- 문서: [AI Image Studio Docs](https://your-docs-url.com)
- 이메일: support@your-domain.com

---

**AI Image Studio** - 차세대 AI 이미지 생성 자동화 플랫폼 🚀