/**
 * 🎼 마스터 AI 오케스트레이터 시스템
 * 메인 헤더 AI가 다른 AI들에게 최적화된 임무를 부여하고 결과를 분석/통합하는 시스템
 */

class MasterAIOrchestrator {
    constructor() {
        this.masterAI = 'claude'; // 메인 헤더 역할 (객관적 분석 결과 최적)
        
        this.workerAIs = {
            chatgpt: {
                name: 'ChatGPT',
                specialty: '코딩/구현',
                strengths: ['프로그래밍', '기술적 솔루션', '디버깅', '알고리즘'],
                currentTask: null,
                lastResponse: null
            },
            gemini: {
                name: 'Google AI Studio', 
                specialty: '창의/디자인',
                strengths: ['창의적 아이디어', '사용자 경험', '비주얼 디자인', '혁신'],
                currentTask: null,
                lastResponse: null
            },
            perplexity: {
                name: 'Perplexity',
                specialty: '리서치/검증',
                strengths: ['최신 정보', '시장 조사', '트렌드 분석', '사실 검증'],
                currentTask: null,
                lastResponse: null
            }
        };
        
        this.projectStatus = {
            phase: 'initialization',
            round: 0,
            maxRounds: 10,
            objective: '',
            completedTasks: [],
            pendingTasks: []
        };
        
        this.knowledgeBase = []; // 축적되는 지식
    }

    // 🎯 프로젝트 시작 - 마스터 AI가 전체 기획
    async initiateProject(userRequest) {
        console.log("🎼 마스터 AI 오케스트레이터 시작...");
        
        const masterPrompt = this.generateMasterInitialPrompt(userRequest);
        
        return `
=== 🎼 마스터 AI 오케스트레이터 모드 ===
역할: 전체 프로젝트 총괄 지휘자

사용자 요청: "${userRequest}"

당신의 임무:
1. 이 프로젝트를 성공적으로 완수하기 위한 전체 전략 수립
2. 각 AI 전문가들에게 부여할 구체적인 임무 설계  
3. 최적의 작업 순서와 협업 방식 결정
4. 각 AI의 장점을 최대한 활용하는 역할 분담

사용 가능한 AI 전문가들:
- ChatGPT: 코딩/구현 전문 (프로그래밍, 기술적 솔루션, 디버깅, 알고리즘)
- Google AI Studio: 창의/디자인 전문 (창의적 아이디어, UX, 비주얼 디자인, 혁신)  
- Perplexity: 리서치/검증 전문 (최신 정보, 시장 조사, 트렌드 분석, 검증)

응답 형식:
## 전체 프로젝트 분석
- 프로젝트 목표: 
- 성공 기준:
- 예상 난이도:

## Phase 1 작업 분담
### ChatGPT 임무:
- 구체적 작업: 
- 전달할 프롬프트: "[여기에 ChatGPT에게 보낼 최적화된 프롬프트 작성]"
- 기대 결과:

### Google AI Studio 임무:  
- 구체적 작업:
- 전달할 프롬프트: "[여기에 Google AI Studio에게 보낼 최적화된 프롬프트 작성]"
- 기대 결과:

### Perplexity 임무:
- 구체적 작업: 
- 전달할 프롬프트: "[여기에 Perplexity에게 보낼 최적화된 프롬프트 작성]"
- 기대 결과:

## 다음 단계 계획
1. 1차 결과 수집 후 분석 방향:
2. 2차 라운드 예상 임무:
3. 최종 통합 전략:

## 품질 관리 체크포인트
- [ ] 각 AI가 최적의 역할을 맡았는가?
- [ ] 프롬프트가 구체적이고 실행 가능한가? 
- [ ] 결과물이 통합 가능한 형태인가?

마스터 AI로서 이 프로젝트를 성공으로 이끌어주세요!
        `;
    }

    // 🔄 결과 수집 및 다음 단계 지시
    generateMasterAnalysisPrompt(collectedResults) {
        return `
=== 🎼 마스터 AI 분석 모드 ===
역할: 결과 분석 및 다음 단계 지휘

## 수집된 결과물 분석

### ChatGPT 결과:
${collectedResults.chatgpt || '아직 미완료'}

### Google AI Studio 결과:  
${collectedResults.gemini || '아직 미완료'}

### Perplexity 결과:
${collectedResults.perplexity || '아직 미완료'}

## 마스터 AI 분석 임무:
1. 각 AI의 결과물을 종합 평가
2. 부족한 부분이나 개선점 파악  
3. 다음 라운드에서 필요한 추가 작업 설계
4. 각 AI에게 보낼 구체적이고 개선된 프롬프트 작성

## 응답 형식:

### 🔍 현재 진행 상황 분석
- 전체 진행률: ___% 
- 우수한 부분:
- 부족한 부분: 
- 예상치 못한 이슈:

### 🎯 다음 라운드 전략

#### ChatGPT 다음 임무:
- 이전 결과 평가: 
- 개선/추가 작업:
- 최적화된 프롬프트: "[구체적이고 실행 가능한 프롬프트]"

#### Google AI Studio 다음 임무:
- 이전 결과 평가:
- 개선/추가 작업: 
- 최적화된 프롬프트: "[구체적이고 실행 가능한 프롬프트]"

#### Perplexity 다음 임무:
- 이전 결과 평가:
- 개선/추가 작업:
- 최적화된 프롬프트: "[구체적이고 실행 가능한 프롬프트]"

### 📊 품질 체크
- [ ] 각 결과물이 프로젝트 목표에 기여하는가?
- [ ] AI들 간의 협업이 원활히 이루어지고 있는가?
- [ ] 다음 단계로 진행할 준비가 되었는가?

### 🎼 마스터 지휘
- 협업 완료 예정 라운드: 
- 최종 결과물 형태:
- 성공 가능성 평가:

전체 프로젝트를 성공으로 이끌기 위한 마스터 전략을 제시해주세요!
        `;
    }

    // 🏁 최종 통합 및 완성
    generateMasterFinalPrompt(allRounds) {
        return `
=== 🎼 마스터 AI 최종 통합 모드 ===
역할: 전체 프로젝트 완성 및 품질 보증

## 전체 협업 과정 리뷰
${this.formatAllRoundsData(allRounds)}

## 마스터 AI 최종 임무:
1. 모든 AI들의 결과물을 하나로 통합
2. 사용자가 요청한 최종 목표 달성 여부 확인
3. 완성된 결과물의 품질 검증 및 개선
4. 실제 사용 가능한 형태로 최종 정리

## 응답 형식:

### 🎯 프로젝트 완성도 평가
- 목표 달성률: ___%
- 품질 수준: 
- 실용성 평가:

### 🏆 최종 통합 결과물
[여기에 모든 AI의 결과를 통합한 완성된 최종 결과물 제시]

### 📋 상세 구성 요소
1. ChatGPT 기여 부분:
2. Google AI Studio 기여 부분: 
3. Perplexity 기여 부분:

### 🔧 추가 개선 제안
- 단기 개선점:
- 장기 발전 방향:
- 확장 가능성:

### 📊 마스터 AI 총평
- 협업 효율성:
- 각 AI 활용도: 
- 프로젝트 성공 요인:
- 향후 유사 프로젝트 권장사항:

사용자가 즉시 활용할 수 있는 완성된 결과물을 제공해주세요!
        `;
    }

    // 📋 사용 가이드 생성
    generateUsageGuide(projectName) {
        return `
🎼 마스터 AI 오케스트레이터 사용 가이드
프로젝트: "${projectName}"

## 🚀 Phase 1: 프로젝트 시작 (Claude/마스터 AI)
1. Claude 탭에서 다음 실행:
   - 위의 "마스터 초기 프롬프트" 붙여넣기
   - 마스터 AI가 전체 계획과 각 AI별 임무 배정

## 🔄 Phase 2: 작업자 AI들 실행
2. ChatGPT 탭: 마스터가 지정한 "ChatGPT 임무 프롬프트" 실행
3. Google AI Studio 탭: 마스터가 지정한 "Google AI Studio 임무 프롬프트" 실행  
4. Perplexity 탭: 마스터가 지정한 "Perplexity 임무 프롬프트" 실행

## 🔄 Phase 3: 결과 분석 (Claude/마스터 AI)
5. Claude 탭에서 "마스터 분석 프롬프트" + 모든 AI 결과물 입력
   - 마스터가 결과 분석 및 다음 라운드 지시

## 🔄 Phase 4-N: 반복 개선
6. 마스터 지시에 따라 각 AI에서 개선된 프롬프트 실행
7. 품질이 만족스러울 때까지 반복

## 🏁 Phase Final: 최종 통합
8. Claude 탭에서 "마스터 최종 통합 프롬프트" 실행
   - 완성된 최종 결과물 산출

## 💡 핵심 포인트
- ✅ 마스터 AI(Claude)가 모든 것을 지휘
- ✅ 각 AI는 자신의 전문 분야에만 집중  
- ✅ 프롬프트는 마스터가 최적화해서 제공
- ✅ 지속적인 품질 관리 및 개선

이제 진정한 AI 오케스트라가 시작됩니다! 🎼
        `;
    }

    // 유틸리티 함수들
    formatAllRoundsData(allRounds) {
        return allRounds.map((round, i) => 
            `Round ${i+1}:\n${Object.entries(round).map(([ai, result]) => 
                `- ${ai}: ${result.substring(0, 200)}...`
            ).join('\n')}`
        ).join('\n\n');
    }
}

// 전역 인스턴스
window.masterOrchestrator = new MasterAIOrchestrator();

console.log(`
🎼 마스터 AI 오케스트레이터 시스템 준비 완료!

📋 사용법:
1. masterOrchestrator.initiateProject("프로젝트 설명")
2. 생성된 프롬프트를 Claude(마스터)에서 실행
3. 마스터의 지시에 따라 각 AI에서 작업 수행
4. 결과를 마스터가 분석 및 통합

🎯 지금 바로 시작:
masterOrchestrator.initiateProject("혁신적인 쇼핑몰 앱 개발")
`);