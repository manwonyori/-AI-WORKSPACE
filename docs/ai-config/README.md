# AI Config (Relay Orchestration)

이 디렉터리는 크롬 확장이 주기적으로 불러오는 **원격 설정**입니다.
- `agents.json`: 에이전트 순서/백오프/루프가드
- `prompts.json`: 공통 프롬프트/핸드오프 표현
- `rules.json`: 허용 액션/레이트리밋/중단 조건
- `selectors.json`: 사이트별 입력/전송 셀렉터(필요 시 오버라이드)

> 사용법: Repo **Settings → Pages**에서 **Branch = `main` / Folder = `/docs`**로 활성화하세요.
> 그러면 다음과 같이 접근 가능합니다 (예시):
> https://manwonyori.github.io/-AI-WORKSPACE/ai-config/agents.json