/**
 * Google AI Studio 전송 버튼 정확한 감지 및 클릭
 * 
 * 전송 버튼은 나타나지만 기존 선택자로 찾지 못하는 문제 해결
 */

console.clear();
console.log("%c🎯 Google AI Studio 전송 버튼 수정", "color: #4285f4; font-size: 18px; font-weight: bold;");

// 1. 모든 버튼을 스캔해서 전송 버튼 찾기
function findActualSendButton() {
    console.log("\n🔍 실제 전송 버튼 정밀 탐색...");
    
    const allButtons = document.querySelectorAll('button');
    console.log(`📊 총 ${allButtons.length}개 버튼 스캔 중...`);
    
    let candidates = [];
    
    allButtons.forEach((btn, i) => {
        const rect = btn.getBoundingClientRect();
        const isVisible = rect.width > 0 && rect.height > 0;
        const isEnabled = !btn.disabled && !btn.hasAttribute('disabled');
        
        if (isVisible && isEnabled) {
            const ariaLabel = btn.getAttribute('aria-label') || '';
            const title = btn.getAttribute('title') || '';
            const text = btn.textContent?.trim() || '';
            const dataTestId = btn.getAttribute('data-testid') || '';
            const className = btn.className || '';
            
            // 아이콘들 체크
            const hasMatIcon = btn.querySelector('mat-icon');
            const hasSvg = btn.querySelector('svg');
            const hasPath = btn.querySelector('path');
            
            let iconInfo = '';
            if (hasMatIcon) {
                const fonticon = hasMatIcon.getAttribute('fonticon') || '';
                const iconText = hasMatIcon.textContent || '';
                iconInfo = `mat-icon(${fonticon || iconText})`;
            } else if (hasSvg || hasPath) {
                iconInfo = 'svg-icon';
            }
            
            // 전송 버튼 가능성 점수
            let score = 0;
            if (ariaLabel.toLowerCase().includes('send')) score += 10;
            if (title.toLowerCase().includes('send')) score += 10;
            if (text.toLowerCase().includes('send')) score += 5;
            if (iconInfo.includes('send')) score += 10;
            if (className.includes('send')) score += 5;
            if (dataTestId.includes('send')) score += 10;
            if (iconInfo.includes('arrow') || iconInfo.includes('chevron')) score += 3;
            if (hasMatIcon || hasSvg) score += 2; // 아이콘이 있으면 가능성 증가
            
            // 입력창 근처에 있는지 체크
            const textarea = document.querySelector('textarea.textarea');
            if (textarea) {
                const textareaRect = textarea.getBoundingClientRect();
                const distance = Math.abs(rect.top - textareaRect.bottom);
                if (distance < 200) score += 5; // 입력창 근처면 점수 추가
            }
            
            candidates.push({
                element: btn,
                index: i,
                score,
                ariaLabel,
                title,
                text: text.slice(0, 30),
                className: className.slice(0, 50),
                dataTestId,
                iconInfo,
                rect: { width: rect.width, height: rect.height, top: rect.top, left: rect.left }
            });
        }
    });
    
    // 점수 순으로 정렬
    candidates.sort((a, b) => b.score - a.score);
    
    console.log(`\n🎯 전송 버튼 후보들 (점수 순):`);
    candidates.slice(0, 10).forEach((candidate, i) => {
        console.log(`${i+1}. 점수: ${candidate.score}`);
        console.log(`   AriaLabel: "${candidate.ariaLabel}"`);
        console.log(`   Text: "${candidate.text}"`);
        console.log(`   Icon: ${candidate.iconInfo}`);
        console.log(`   Class: ${candidate.className}`);
        console.log(`   위치: ${Math.round(candidate.rect.top)}px from top`);
        console.log("");
    });
    
    return candidates;
}

// 2. 최고 점수 후보로 전송 시도
async function sendWithBestCandidate(text = `전송 버튼 수정 테스트 ${Date.now()}`) {
    console.log(`\n📤 최적 후보로 전송 시도: "${text}"`);
    
    // 먼저 텍스트 입력
    const textarea = document.querySelector('textarea.textarea');
    if (textarea) {
        textarea.focus();
        textarea.value = text;
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        textarea.dispatchEvent(new Event('change', { bubbles: true }));
        textarea.dispatchEvent(new Event('blur', { bubbles: true }));
        console.log("✅ 텍스트 입력 완료");
    }
    
    // 버튼 활성화 대기
    console.log("⏰ 전송 버튼 활성화 대기 (10초)...");
    await new Promise(resolve => setTimeout(resolve, 10000));
    
    // 최적 후보 찾기
    const candidates = findActualSendButton();
    
    if (candidates.length === 0) {
        console.error("❌ 전송 가능한 버튼이 없습니다");
        return false;
    }
    
    // 상위 3개 후보로 차례대로 시도
    for (let i = 0; i < Math.min(3, candidates.length); i++) {
        const candidate = candidates[i];
        console.log(`\n🎯 시도 ${i+1}: 점수 ${candidate.score} 버튼`);
        console.log(`   AriaLabel: "${candidate.ariaLabel}"`);
        console.log(`   Text: "${candidate.text}"`);
        
        try {
            // 다양한 클릭 방법 시도
            console.log("   🖱️ 클릭 시도...");
            
            // 방법 1: 표준 클릭
            candidate.element.click();
            
            // 방법 2: 이벤트 기반 클릭
            const clickEvents = [
                new MouseEvent('mousedown', { bubbles: true }),
                new MouseEvent('mouseup', { bubbles: true }),
                new MouseEvent('click', { bubbles: true }),
                new PointerEvent('pointerdown', { bubbles: true }),
                new PointerEvent('pointerup', { bubbles: true })
            ];
            
            clickEvents.forEach(event => {
                try {
                    candidate.element.dispatchEvent(event);
                } catch (e) {}
            });
            
            console.log("   ✅ 클릭 완료");
            
            // 전송 확인을 위해 잠시 대기
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // 전송 성공했는지 확인 (입력창이 비워졌는지)
            const currentValue = textarea.value || '';
            if (currentValue.trim() === '' || !currentValue.includes(text)) {
                console.log("   🎉 전송 성공! (입력창이 비워짐)");
                return true;
            } else {
                console.log("   ⚠️ 전송 확인 불가, 다음 후보 시도...");
            }
            
        } catch (error) {
            console.log(`   ❌ 클릭 실패: ${error.message}`);
        }
    }
    
    console.log("❌ 모든 후보로 시도했지만 전송 실패");
    return false;
}

// 3. 수동 버튼 선택 도구
function showButtonSelector() {
    console.log("\n🎯 수동 버튼 선택 도구");
    console.log("화면에서 전송 버튼을 확인한 후 수동으로 선택할 수 있습니다.");
    
    const candidates = findActualSendButton();
    
    candidates.slice(0, 5).forEach((candidate, i) => {
        const funcName = `clickButton${i + 1}`;
        window[funcName] = () => {
            console.log(`🖱️ 버튼 ${i+1} 클릭 시도...`);
            try {
                candidate.element.click();
                console.log("✅ 클릭 완료");
            } catch (e) {
                console.log("❌ 클릭 실패:", e.message);
            }
        };
        
        console.log(`${i+1}번 버튼: ${funcName}() - "${candidate.ariaLabel || candidate.text}"`);
    });
    
    console.log("\n💡 사용법: clickButton1(), clickButton2(), ... 으로 각 버튼 테스트");
}

// 4. 실시간 버튼 변화 감지
function monitorButtonChanges() {
    console.log("\n👁️ 실시간 버튼 변화 감지 시작...");
    
    let lastButtonCount = 0;
    let lastCandidateCount = 0;
    
    const monitor = setInterval(() => {
        const allButtons = document.querySelectorAll('button:not([disabled])');
        const candidates = findActualSendButton();
        const topCandidates = candidates.filter(c => c.score >= 5);
        
        if (allButtons.length !== lastButtonCount || topCandidates.length !== lastCandidateCount) {
            console.log(`📊 버튼 상태 변화:`);
            console.log(`   전체 활성 버튼: ${lastButtonCount} → ${allButtons.length}`);
            console.log(`   전송 후보 버튼: ${lastCandidateCount} → ${topCandidates.length}`);
            
            if (topCandidates.length > 0) {
                console.log(`🎯 최고 후보: 점수 ${topCandidates[0].score} - "${topCandidates[0].ariaLabel || topCandidates[0].text}"`);
            }
            
            lastButtonCount = allButtons.length;
            lastCandidateCount = topCandidates.length;
        }
    }, 1000);
    
    setTimeout(() => {
        clearInterval(monitor);
        console.log("👁️ 버튼 모니터링 종료");
    }, 30000);
}

// 전역 함수 등록
window.findActualSendButton = findActualSendButton;
window.sendWithBestCandidate = sendWithBestCandidate;
window.showButtonSelector = showButtonSelector;
window.monitorButtonChanges = monitorButtonChanges;

console.log("\n💡 사용법:");
console.log("1. sendWithBestCandidate('메시지')  - 자동으로 최적 버튼 찾아서 전송");
console.log("2. findActualSendButton()         - 모든 버튼 분석하여 전송 후보 찾기");
console.log("3. showButtonSelector()           - 수동 버튼 선택 도구");
console.log("4. monitorButtonChanges()         - 실시간 버튼 변화 감지");

console.log("\n🎯 지금 바로 실행해보세요:");
console.log("sendWithBestCandidate('전송 버튼 수정 테스트 - 이제 작동하나요?')");

console.log("\n" + "=".repeat(60));
console.log("🎯 실제로 보이는 전송 버튼을 정확히 찾아서 클릭합니다!");
console.log("모든 버튼을 점수화하여 가장 가능성 높은 전송 버튼을 선택합니다.");
console.log("=".repeat(60));