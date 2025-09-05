/**
 * 자동 AI 협업 릴레이 시스템
 * 4개 AI 플랫폼 간 순환 대화 및 협업 자동화
 */

class AutoAIRelay {
    constructor() {
        this.platforms = {
            claude: {
                name: 'Claude',
                role: '전략 기획자',
                selector: 'div[contenteditable="true"].ProseMirror',
                sendButton: 'button[aria-label*="Send"]'
            },
            chatgpt: {
                name: 'ChatGPT', 
                role: '실무 개발자',
                selector: '#prompt-textarea',
                sendButton: 'button[aria-label="프롬프트 보내기"]'
            },
            gemini: {
                name: 'Google AI Studio',
                role: '창의적 디자이너', 
                selector: 'textarea.textarea',
                sendButton: 'button[aria-label*="Run"]'
            },
            perplexity: {
                name: 'Perplexity',
                role: '트렌드 분석가',
                selector: 'textarea',
                sendButton: 'button[type="submit"]'
            }
        };
        
        this.currentRound = 0;
        this.maxRounds = 5;
        this.conversationHistory = [];
        this.isRunning = false;
    }

    // 현재 플랫폼 감지
    detectCurrentPlatform() {
        const hostname = window.location.hostname;
        if (hostname.includes('claude.ai')) return 'claude';
        if (hostname.includes('chatgpt.com')) return 'chatgpt';
        if (hostname.includes('aistudio.google.com')) return 'gemini';
        if (hostname.includes('perplexity.ai')) return 'perplexity';
        return null;
    }

    // 역할별 프롬프트 생성
    generateRolePrompt(platform, topic, round, previousResponses) {
        const roles = {
            claude: `당신은 전략 기획자입니다. ${topic}에 대해 전체적인 방향과 전략을 제시해주세요.`,
            chatgpt: `당신은 실무 개발자입니다. ${topic}에 대해 구체적인 구현 방안과 기술적 해결책을 제시해주세요.`,
            gemini: `당신은 창의적 디자이너입니다. ${topic}에 대해 혁신적이고 창의적인 아이디어를 제시해주세요.`,
            perplexity: `당신은 트렌드 분석가입니다. ${topic}에 대해 최신 동향과 검증된 사례를 바탕으로 분석해주세요.`
        };

        let prompt = `=== AI 협업 Round ${round} ===\n`;
        prompt += `${roles[platform]}\n\n`;
        
        if (round > 1 && previousResponses.length > 0) {
            prompt += `=== 이전 라운드 다른 AI들의 의견 ===\n`;
            previousResponses.forEach((resp, i) => {
                prompt += `${i + 1}. ${resp.platform}: ${resp.response.substring(0, 200)}...\n`;
            });
            prompt += `\n`;
        }
        
        prompt += `=== 현재 과제 ===\n${topic}\n\n`;
        prompt += `=== 협업 지시사항 ===\n`;
        prompt += `1. 이전 의견들을 검토하고 개선점을 제시하세요\n`;
        prompt += `2. 구체적인 개선 방안을 제안하세요\n`;  
        prompt += `3. 다음 AI에게 전달할 질문을 포함하세요\n`;
        prompt += `4. 협업이 완료되었다면 "협업완료"라고 명시하세요\n\n`;
        prompt += `응답 형식:\n- 현재 상태 평가:\n- 개선 제안:\n- 다음 단계 요청:\n- 협업 상태: [진행중/협업완료]`;
        
        return prompt;
    }

    // 메시지 입력 및 전송
    async sendMessage(platform, message) {
        console.log(`📤 ${this.platforms[platform].name}에 메시지 전송...`);
        
        const config = this.platforms[platform];
        const inputElement = document.querySelector(config.selector);
        
        if (!inputElement) {
            console.error(`❌ ${config.name} 입력창을 찾을 수 없음`);
            return false;
        }

        // 입력창 활성화 (ChatGPT의 경우)
        if (platform === 'chatgpt') {
            inputElement.readOnly = false;
            inputElement.disabled = false;
            inputElement.removeAttribute('readonly');
            inputElement.removeAttribute('disabled');
        }

        // 메시지 입력
        inputElement.focus();
        if (inputElement.tagName === 'TEXTAREA') {
            inputElement.value = message;
        } else {
            inputElement.innerHTML = `<p>${message}</p>`;
        }

        // 이벤트 발생
        inputElement.dispatchEvent(new Event('input', { bubbles: true }));
        inputElement.dispatchEvent(new Event('change', { bubbles: true }));

        console.log(`✅ ${config.name} 입력 완료`);
        
        // 전송 버튼 클릭 (3초 후)
        setTimeout(() => {
            const sendButton = document.querySelector(config.sendButton) ||
                             this.findSendButton(platform);
            
            if (sendButton && !sendButton.disabled) {
                sendButton.click();
                console.log(`🚀 ${config.name} 전송 완료`);
            } else {
                console.log(`⚠️ ${config.name} 전송 버튼을 찾지 못함. 수동으로 전송해주세요.`);
            }
        }, 3000);

        return true;
    }

    // 플랫폼별 전송 버튼 찾기
    findSendButton(platform) {
        const buttons = Array.from(document.querySelectorAll('button'));
        
        switch(platform) {
            case 'claude':
                return buttons.find(btn => 
                    btn.getAttribute('aria-label')?.includes('Send') ||
                    btn.textContent?.includes('Send')
                );
                
            case 'chatgpt':
                return buttons.find(btn => 
                    btn.getAttribute('aria-label') === '프롬프트 보내기'
                );
                
            case 'gemini':
                return buttons.find(btn => {
                    const label = btn.getAttribute('aria-label') || '';
                    return label.toLowerCase().includes('run') ||
                           btn.querySelector('mat-icon')?.textContent?.includes('play_arrow');
                });
                
            case 'perplexity':
                return buttons.find(btn => btn.type === 'submit');
                
            default:
                return null;
        }
    }

    // 수동 협업 시작 (현재 플랫폼에서)
    startManualCollaboration(topic) {
        const currentPlatform = this.detectCurrentPlatform();
        if (!currentPlatform) {
            console.error('❌ 지원되지 않는 플랫폼입니다.');
            return;
        }

        console.log(`🚀 ${this.platforms[currentPlatform].name}에서 AI 협업 시작: "${topic}"`);
        
        const prompt = this.generateRolePrompt(currentPlatform, topic, 1, []);
        this.sendMessage(currentPlatform, prompt);
        
        console.log(`💡 다음 단계: 다른 AI 플랫폼 탭으로 이동해서 continueCollaboration("${topic}", 1) 실행`);
    }

    // 협업 계속하기 (다음 라운드)
    continueCollaboration(topic, currentRound, previousResponse = '') {
        const currentPlatform = this.detectCurrentPlatform();
        if (!currentPlatform) {
            console.error('❌ 지원되지 않는 플랫폼입니다.');
            return;
        }

        // 이전 응답 기록
        if (previousResponse) {
            this.conversationHistory.push({
                round: currentRound,
                platform: currentPlatform,
                response: previousResponse
            });
        }

        const nextRound = currentRound + 1;
        if (nextRound > this.maxRounds) {
            console.log('✅ 최대 라운드 도달. 협업 완료.');
            return;
        }

        const prompt = this.generateRolePrompt(
            currentPlatform, 
            topic, 
            nextRound, 
            this.conversationHistory.slice(-3) // 최근 3개 응답만
        );
        
        this.sendMessage(currentPlatform, prompt);
        
        console.log(`💡 Round ${nextRound} 시작. 응답 후 다른 플랫폼에서 continueCollaboration("${topic}", ${nextRound}, "응답내용") 실행`);
    }

    // 협업 상태 확인
    getCollaborationStatus() {
        return {
            currentRound: this.currentRound,
            maxRounds: this.maxRounds,
            history: this.conversationHistory,
            isRunning: this.isRunning
        };
    }

    // 최종 결과 요약 생성
    generateFinalSummary() {
        if (this.conversationHistory.length === 0) {
            return "협업 기록이 없습니다.";
        }

        let summary = "🎯 AI 협업 최종 결과 요약\n\n";
        
        // 라운드별 요약
        const rounds = {};
        this.conversationHistory.forEach(item => {
            if (!rounds[item.round]) rounds[item.round] = [];
            rounds[item.round].push(item);
        });

        Object.keys(rounds).forEach(round => {
            summary += `=== Round ${round} ===\n`;
            rounds[round].forEach(item => {
                summary += `${this.platforms[item.platform].name}: ${item.response.substring(0, 150)}...\n`;
            });
            summary += '\n';
        });

        return summary;
    }
}

// 전역 인스턴스 생성
window.aiRelay = new AutoAIRelay();

// 사용법 안내
console.log(`
🤖 자동 AI 협업 릴레이 시스템 로드 완료!

📋 사용법:
1. aiRelay.startManualCollaboration("주제") - 협업 시작
2. aiRelay.continueCollaboration("주제", 라운드, "이전응답") - 다음 라운드
3. aiRelay.getCollaborationStatus() - 현재 상태 확인
4. aiRelay.generateFinalSummary() - 최종 결과 요약

🎯 예시:
aiRelay.startManualCollaboration("혁신적인 날씨 앱 개발")

💡 각 플랫폼에서 응답을 받은 후, 다음 플랫폼에서 continueCollaboration() 실행하세요!
`);

// 현재 플랫폼 표시
const currentPlatform = window.aiRelay.detectCurrentPlatform();
if (currentPlatform) {
    console.log(`✅ 현재 플랫폼: ${window.aiRelay.platforms[currentPlatform].name} (${window.aiRelay.platforms[currentPlatform].role})`);
} else {
    console.log(`⚠️ 지원되지 않는 플랫폼입니다.`);
}