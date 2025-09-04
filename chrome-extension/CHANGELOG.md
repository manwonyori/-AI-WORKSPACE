# 📋 Changelog - AI Workspace Controller

## [1.3.0] - 2025-01-04 🚀

### Major Update: Platform-Specific Input Methods
- **ChatGPT**: Implemented React-compatible setter method
  - Uses `Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set`
  - Dispatches both `input` and `change` events for full compatibility
  - Clears existing value before setting new text
  
- **Gemini/AI Studio**: Enhanced Quill editor support
  - Special handling for `div.ql-editor` with blur/focus cycle
  - Fallback to textarea for AI Studio variations
  - Proper innerHTML formatting with `<p>` tags
  
- **Claude**: Optimized contenteditable handling
  - Proper InputEvent with `inputType` and `data` parameters
  - Standard contenteditable method maintained
  
- **Perplexity**: Dual mode support
  - Supports both textarea and contenteditable
  - Automatic detection of input type

### Technical Improvements
- **New Platform-Specific Functions**:
  - `inputForChatGPT()` - React setter method
  - `inputForGemini()` - Quill editor + textarea handling
  - `inputForClaude()` - ContentEditable with InputEvent
  - `inputForPerplexity()` - Dual mode support
  
- **Enhanced Error Handling**:
  - Try-catch blocks for all input methods
  - Fallback mechanisms for each platform
  - Better error logging with platform context
  
- **Visibility Checks**:
  - Added `offsetParent !== null` checks
  - Ensures element is actually visible before interaction
  
- **Chunked Input Improvements**:
  - Platform-aware chunking logic
  - React setter support for ChatGPT chunks
  - Quill-specific HTML appending for Gemini

### Testing Tools Added
- `chatgpt_simple_test.js` - 4 different input methods test
- `chatgpt_deep_investigation.js` - Deep DOM and React analysis
- `platform_investigation.js` - Universal platform tester
- `TEST_VERIFICATION.md` - Complete verification guide
- `INPUT_TEST_GUIDE.md` - Step-by-step testing instructions

### Bug Fixes
- Fixed ChatGPT input not working (React-controlled textarea issue)
- Fixed Gemini/AI Studio Quill editor input
- Resolved async message handler warnings
- Fixed clear function for each platform

## [1.2.6] - 2025-09-04

### 📚 **Documentation & Organization**
- **플랫폼 URL 가이드 추가**:
  - Google AI Studio: `https://aistudio.google.com/prompts/new_chat`
  - 각 플랫폼별 정확한 채팅 URL 명시
  - 로그인 계정: 8899you@gmail.com 통일

- **Python 조사 내용 적용**:
  - Chrome 자동화 패턴 분석
  - Selenium WebDriver 패턴 참고
  - UI 자동화 경험 반영

- **폴더 구조 정리**:
  - 테스트 도구 → test_tools/ 폴더
  - 문서 파일 정리

## [1.2.5] - 2025-09-04

### 🐛 **Input Fix for ChatGPT & Gemini**
- **ChatGPT 입력 개선**:
  - `textarea#prompt-textarea` 전용 처리 추가
  - composed: true 이벤트 속성 추가
  - 직접 value 설정 방식 사용

- **Gemini 입력 개선**:
  - Quill editor (`div.ql-editor`) 전용 처리
  - innerHTML 사용으로 줄바꿈 처리
  - blur/focus 이벤트 추가로 입력 활성화

- **플랫폼별 최적화**:
  - Claude & Perplexity: ✅ 정상 작동 유지
  - ChatGPT & Gemini: 입력 메소드 개선

## [1.2.4] - 2025-09-04

### 🔄 **Revert to Working Version**
- **Perplexity 셀렉터를 성공했던 버전으로 복원**:
  - 간단한 셀렉터로 변경: `textarea[placeholder*="Ask"], textarea, [contenteditable="true"]`
  - 버튼: `button[aria-label="Submit"], button.bg-super, form button[type="submit"]`
  - 복잡한 로직 제거, 원래의 간단한 입력 방식으로 복원

### 🧹 **폴더 정리**:
  - 테스트 파일들을 `test_tools/` 폴더로 이동
  - 불필요한 스크린샷 정리
  - 핵심 파일만 메인 폴더에 유지

## [1.2.3] - 2025-09-04

### 🎯 **Perplexity Full Support**
- **Enhanced Perplexity selectors** for better compatibility
- **Microphone mode prevention** with proper input handling
- **Real-time input validation** for Perplexity

## [1.2.2] - 2025-09-04

### 🔍 **Async Message Handler Fix**
- **Fixed Chrome runtime error**: "A listener indicated an asynchronous response by returning true, but the message channel closed"
- **Restructured message handler** with proper async/await pattern
- **Improved error handling** in all message cases

## [1.2.1] - 2025-09-04

### 🐛 **Critical Selector Fix**
- **Fixed selector detection logic**: Now iterates through selectors properly
- **Resolved red dot issue**: ChatGPT and Perplexity now show green status
- **Improved selector parsing**: Split comma-separated selectors for individual testing

## [1.2.0] - 2025-09-04

### 🎨 **Major UI Update & Platform Selectors**
- **Updated ChatGPT selectors** for 2025 UI
- **Updated Perplexity selectors** with Pro interface support
- **Updated Gemini selectors** for AI Studio compatibility
- **Improved Claude selectors** with ProseMirror support

## [1.1.3] - 2025-09-04

### ✨ **Initial Chrome Extension Release**
- **Multi-platform support**: ChatGPT, Claude, Gemini, Perplexity
- **Chunked input** for large text
- **Visual indicators**: Green badges and status dots
- **Command relay system** for AI collaboration