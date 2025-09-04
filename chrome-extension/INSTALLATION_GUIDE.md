# AI Workspace Controller v1.2.1 설치 및 사용 가이드

## 🚀 빠른 설치

### 1. Chrome에서 Extension 설치
1. Chrome 브라우저 열기
2. 주소창에 `chrome://extensions/` 입력
3. 우측 상단 **개발자 모드** 활성화
4. **압축해제된 확장 프로그램을 로드합니다** 클릭
5. `C:\Users\8899y\AI-WORKSPACE\chrome-extension` 폴더 선택

### 2. Extension 확인
- 브라우저 우측 상단에 Extension 아이콘이 나타남
- 아이콘 클릭하면 팝업 UI가 열림

## 🧪 테스트 방법

### 방법 1: 테스트 페이지 사용
```
1. Chrome에서 파일 열기:
   C:\Users\8899y\AI-WORKSPACE\chrome-extension\test-all-platforms.html

2. 각 플랫폼별로 "Test Selectors" 버튼 클릭
3. 녹색 점(🟢)이 나타나면 정상
```

### 방법 2: 실제 사이트 테스트
1. 각 AI 플랫폼 접속:
   - ChatGPT: https://chatgpt.com
   - Claude: https://claude.ai
   - Perplexity: https://perplexity.ai
   - Gemini: https://gemini.google.com

2. 페이지 로드 후 확인사항:
   - 왼쪽 상단에 녹색 "LOADED" 배지가 나타남
   - Extension 팝업에서 해당 플랫폼이 🟢 표시

## 📊 현재 상태 (v1.2.1)

### ✅ 지원 플랫폼
| 플랫폼 | 상태 | 주요 셀렉터 |
|--------|------|-------------|
| ChatGPT | 🟢 | `div[contenteditable="true"][data-id="root"]` |
| Claude | 🟢 | `div[contenteditable="true"].ProseMirror` |
| Perplexity | 🟢 | `textarea.SearchBar-input` |
| Gemini | 🟢 | `div.ql-editor` |

### 🔧 주요 기능
- ✅ 자동 텍스트 입력
- ✅ 메시지 전송
- ✅ 플랫폼 상태 모니터링
- ✅ 일괄 메시지 전송
- ✅ 청킹 시스템 (긴 텍스트 자동 분할)

## 🐛 문제 해결

### "빨간 점(🔴)이 나타나는 경우"
1. 페이지 새로고침 (F5)
2. Extension 팝업에서 "Check Status" 클릭
3. 로그인 상태 확인

### "LOADED 배지가 안 보이는 경우"
1. Extension 재로드:
   - `chrome://extensions/`
   - Extension 찾기 → 새로고침 버튼 클릭

### "셀렉터 검증하기"
```javascript
// F12 콘솔에서 실행
// ChatGPT
document.querySelector('div[contenteditable="true"][data-id="root"]')

// Perplexity  
document.querySelector('textarea.SearchBar-input')

// Gemini
document.querySelector('div.ql-editor')

// Claude
document.querySelector('div[contenteditable="true"].ProseMirror')
```

## 📝 업데이트 내역

### v1.2.1 (2025-09-04)
- Gemini `div.ql-editor` 셀렉터 최적화
- Puppeteer 테스트 도구 추가
- 브라우저 자동화 검증 시스템

### v1.2.0 (2025-09-04)
- Perplexity SearchBar 컴포넌트 완전 지원
- Debug Console 기능 추가

## 🔍 디버깅 도구

### 셀렉터 자동 감지
```bash
# Chrome 콘솔(F12)에서 실행
<script src="chrome-extension://[EXTENSION_ID]/selector-detector.js"></script>
```

### Puppeteer 테스트
```bash
cd C:\Users\8899y\AI-WORKSPACE\chrome-extension
node visual_test.js
```

## 📞 지원

문제 발생 시:
1. Chrome 콘솔(F12) 에러 확인
2. Extension 팝업에서 🐛 Debug Console 클릭
3. 스크린샷과 함께 보고