# AI-WORKSPACE Remote Config

## Configuration Files

### 🔧 Core Settings
- [agents.json](./ai-config/agents.json) - AI 에이전트 순서 및 설정
- [prompts.json](./ai-config/prompts.json) - 프롬프트 템플릿
- [rules.json](./ai-config/rules.json) - 실행 규칙 및 제한
- [selectors.json](./ai-config/selectors.json) - DOM 선택자 정의

## How to Use

Chrome 확장 프로그램이 이 설정 파일들을 자동으로 읽어옵니다:

```javascript
// Example fetch
fetch('https://manwonyori.github.io/-AI-WORKSPACE/ai-config/agents.json')
  .then(r => r.json())
  .then(config => console.log(config));
```

## Repository

- GitHub: [manwonyori/-AI-WORKSPACE](https://github.com/manwonyori/-AI-WORKSPACE)
- Status: Active ✅

---
*Last updated: 2025-09-04*