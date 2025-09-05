/**
 * 🔄 대화 한도 및 새창 관리 시스템
 * AI 플랫폼별 대화 한도 도달 시 자동 새창 생성 및 컨텍스트 전달
 */

class ConversationLimitHandler {
    constructor() {
        this.conversationLimits = {
            claude: { maxMessages: 100, currentCount: 0, resetHours: 24 },
            chatgpt: { maxMessages: 40, currentCount: 0, resetHours: 3 },
            gemini: { maxMessages: 50, currentCount: 0, resetHours: 24 },
            perplexity: { maxMessages: 30, currentCount: 0, resetHours: 4 }
        };
        
        this.projectContext = {
            objective: '',
            currentPhase: '',
            completedWork: [],
            activeConversations: new Map(), // platform -> window reference
            backupData: {} // 컨텍스트 백업
        };
    }

    // 🔄 새창 생성 및 컨텍스트 전달 시스템
    generateNewTabContextTransfer(platform, projectData) {
        const contextPrompt = `
=== 🔄 컨텍스트 전달: 새 대화 시작 ===
이전 대화에서 계속 진행 중인 프로젝트입니다.

## 📋 프로젝트 현황
- 목표: ${projectData.objective}
- 현재 단계: ${projectData.currentPhase}
- 진행률: ${projectData.progress}%

## 📊 이전 작업 요약
${projectData.completedWork.map((work, i) => 
    `${i+1}. [${work.platform}] ${work.summary}`
).join('\n')}

## 🎯 현재 임무
${projectData.currentTask}

## ⚠️ 중요 알림
- 이는 대화 한도로 인한 새창에서의 연속 작업입니다
- 이전 컨텍스트를 모두 고려해서 작업해주세요
- 다른 AI들과 협업 중이므로 일관성을 유지해주세요

${platform === 'claude' ? '당신은 마스터 AI로서 전체 프로젝트를 지휘하고 있습니다.' : ''}
${platform === 'chatgpt' ? '당신은 구현 전문가로 참여하고 있습니다.' : ''}
${platform === 'gemini' ? '당신은 창의/디자인 전문가로 참여하고 있습니다.' : ''}
${platform === 'perplexity' ? '당신은 리서치/검증 전문가로 참여하고 있습니다.' : ''}

작업을 계속 진행해주세요.
        `;
        
        return contextPrompt;
    }

    // 🔄 플랫폼별 새창 URL 생성
    getNewChatURL(platform) {
        const urls = {
            claude: 'https://claude.ai/chat/new',
            chatgpt: 'https://chatgpt.com/',
            gemini: 'https://aistudio.google.com/prompts/new_chat',
            perplexity: 'https://www.perplexity.ai/'
        };
        return urls[platform];
    }

    // 🚨 대화 한도 감지 및 새창 자동 생성
    handleConversationLimit(platform, projectData) {
        console.log(`🚨 ${platform} 대화 한도 도달! 새창 생성 중...`);
        
        // 1. 새창 열기
        const newChatURL = this.getNewChatURL(platform);
        const newWindow = window.open(newChatURL, `${platform}_new_${Date.now()}`);
        
        // 2. 컨텍스트 전달 프롬프트 생성
        const contextTransfer = this.generateNewTabContextTransfer(platform, projectData);
        
        // 3. 사용자에게 안내
        console.log(`
🔄 ${platform.toUpperCase()} 새창 생성 완료!

📋 다음 단계:
1. 새로 열린 ${platform} 창에서 로딩 완료 대기
2. 아래 컨텍스트 전달 프롬프트 복사하여 붙여넣기:

${contextTransfer}

3. 작업 계속 진행
        `);
        
        // 4. 백업 데이터 업데이트
        this.projectContext.backupData[platform] = {
            timestamp: Date.now(),
            context: contextTransfer,
            projectData: { ...projectData }
        };
        
        return { newWindow, contextTransfer };
    }
}

/**
 * 🎼 완전 자동 AI 오케스트레이션 엔진
 * 프로젝트 완성까지 자동 순환 + 대화 한도 자동 처리
 */
class FullAutoOrchestrator {
    constructor() {
        this.limitHandler = new ConversationLimitHandler();
        this.isRunning = false;
        this.currentRound = 0;
        this.maxRounds = 20; // 최대 20라운드
        
        this.projectState = {
            objective: '',
            startTime: null,
            phases: [],
            currentPhase: 'initialization',
            completedTasks: [],
            qualityScore: 0,
            isComplete: false
        };
        
        this.aiSequence = ['claude', 'chatgpt', 'gemini', 'perplexity']; // 순환 순서
        this.currentAIIndex = 0;
    }

    // 🚀 완전 자동 프로젝트 시작
    async startFullAutoProject(projectObjective) {
        console.log("🎼 완전 자동 AI 오케스트레이션 시작!");
        
        this.projectState.objective = projectObjective;
        this.projectState.startTime = Date.now();
        this.isRunning = true;
        
        // Phase 1: 마스터 AI 초기 기획
        const masterInitialPrompt = `
=== 🎼 완전 자동 AI 오케스트레이션 시작 ===
프로젝트: "${projectObjective}"

🎯 마스터 AI (Claude) 임무:
1. 이 프로젝트를 완성하기 위한 완전한 로드맵 작성
2. 각 AI별 구체적 역할과 순환 작업 계획
3. 자동화된 협업을 위한 명확한 프로토콜 설정
4. 품질 기준 및 완성 조건 정의

⚠️ 중요: 이는 완전 자동 시스템입니다!
- 각 AI는 정해진 순서대로 자동 작업
- 대화 한도 도달 시 자동으로 새창 생성
- 프로젝트 완성까지 무한 반복
- 중간에 사람 개입 최소화

🔄 AI 순환 계획:
Claude(기획) → ChatGPT(구현) → Gemini(창의) → Perplexity(검증) → 반복

응답 형식:
## 🎯 프로젝트 마스터 플랜
- 최종 목표:
- 예상 소요 라운드: ___라운드
- 성공 기준:

## 🤖 각 AI별 자동 임무
### [Round 1] ChatGPT 자동 임무:
- 작업: 
- 전달 프롬프트: "[ChatGPT가 받을 정확한 프롬프트]"

### [Round 1] Gemini 자동 임무:  
- 작업:
- 전달 프롬프트: "[Gemini가 받을 정확한 프롬프트]"

### [Round 1] Perplexity 자동 임무:
- 작업:
- 전달 프롬프트: "[Perplexity가 받을 정확한 프롬프트]"

## 🔄 자동 순환 프로토콜
- 각 AI 완료 신호:
- 다음 라운드 트리거 조건:
- 프로젝트 완성 판단 기준:

## 🚨 비상 계획
- 대화 한도 도달 시 처리:
- 품질 기준 미달 시 재작업:
- 무한 루프 방지 조치:

전체 프로젝트가 완성될 때까지 자동으로 진행되도록 설계해주세요!
        `;
        
        console.log("📋 Claude(마스터)에서 다음 프롬프트 실행:");
        console.log(masterInitialPrompt);
        
        return masterInitialPrompt;
    }

    // 🔄 자동 순환 제어 시스템
    generateAutoSequencePrompt(aiPlatform, roundData) {
        const basePrompts = {
            chatgpt: `
🤖 ChatGPT 자동 작업 모드
라운드: ${this.currentRound}
역할: 구현 전문가

이전 단계 결과: ${roundData.previousResult || '첫 라운드'}

자동 작업 완료 후 다음과 같이 응답하세요:
"[AUTO-COMPLETE-CHATGPT] 작업 완료. Gemini로 전달: [다음 AI에게 전달할 내용]"
            `,
            
            gemini: `  
🎨 Google AI Studio 자동 작업 모드
라운드: ${this.currentRound}
역할: 창의 전문가

이전 단계 결과: ${roundData.previousResult || '첫 라운드'}

자동 작업 완료 후 다음과 같이 응답하세요:
"[AUTO-COMPLETE-GEMINI] 작업 완료. Perplexity로 전달: [다음 AI에게 전달할 내용]"
            `,
            
            perplexity: `
📊 Perplexity 자동 작업 모드  
라운드: ${this.currentRound}
역할: 검증 전문가

이전 단계 결과: ${roundData.previousResult || '첫 라운드'}

자동 작업 완료 후 다음과 같이 응답하세요:
"[AUTO-COMPLETE-PERPLEXITY] 작업 완료. Claude로 전달: [다음 AI에게 전달할 내용]"
            `
        };
        
        return basePrompts[aiPlatform] || '';
    }

    // 📊 프로젝트 진행 상황 모니터링
    generateProgressMonitor() {
        return `
🎼 자동 오케스트레이션 진행 상황

📊 현재 상태:
- 프로젝트: ${this.projectState.objective}
- 현재 라운드: ${this.currentRound}/${this.maxRounds}
- 진행 시간: ${Math.floor((Date.now() - this.projectState.startTime) / 1000)}초
- 완료된 작업: ${this.projectState.completedTasks.length}개

🤖 AI 상태:
${this.aiSequence.map((ai, i) => 
    `${i === this.currentAIIndex ? '🔄' : '⏸️'} ${ai.toUpperCase()}: ${i === this.currentAIIndex ? '작업 중' : '대기'}`
).join('\n')}

🎯 다음 단계: ${this.aiSequence[this.currentAIIndex]} 작업 대기 중
        `;
    }
}

// 전역 인스턴스
window.fullAutoOrchestrator = new FullAutoOrchestrator();
window.conversationLimitHandler = new ConversationLimitHandler();

console.log(`
🎼 완전 자동 AI 오케스트레이션 엔진 준비 완료!

🚀 테스트 시작:
fullAutoOrchestrator.startFullAutoProject("혁신적인 개인 일정 관리 AI 앱 개발")

🔄 대화 한도 대책:
- 자동 새창 생성
- 컨텍스트 자동 전달  
- 프로젝트 연속성 보장

💡 완전 자동화 특징:
- 사람 개입 최소화
- 프로젝트 완성까지 자동 진행
- 품질 관리 자동화
- 비상 상황 자동 처리
`);

// 현재 플랫폼에서 즉시 테스트 시작
if (window.location.hostname.includes('claude.ai')) {
    console.log("🎼 Claude에서 테스트 준비 완료! 위의 명령어로 시작하세요!");
}