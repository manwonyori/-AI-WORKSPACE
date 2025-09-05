/**
 * ULTIMATE Popup Controller v3.0
 * 완벽한 제어 및 모니터링
 */

console.log('🚀 Ultimate Popup Controller Starting...');

// ==================== STATE ====================
const UI = {
    platforms: ['chatgpt', 'claude', 'gemini', 'perplexity'],
    relayActive: false,
    monitorVisible: false,
    stats: {
        success: 0,
        fail: 0,
        round: 0
    },
    logs: []
};

// ==================== UTILITIES ====================
function $(id) {
    return document.getElementById(id);
}

function log(message, type = 'info') {
    const time = new Date().toLocaleTimeString();
    const entry = { time, message, type };
    
    UI.logs.unshift(entry);
    if (UI.logs.length > 50) UI.logs.pop();
    
    updateMonitor();
    console.log(`[${type}] ${message}`);
}

function updateMonitor() {
    const monitor = $('monitorContent');
    if (!monitor) return;
    
    const html = UI.logs.map(entry => {
        const className = entry.type === 'error' ? 'error' : 
                         entry.type === 'warning' ? 'warning' : '';
        return `<div class="log-entry ${className}">[${entry.time}] ${entry.message}</div>`;
    }).join('');
    
    monitor.innerHTML = html || '<div class="log-entry">대기 중...</div>';
}

// ==================== CHROME API ====================
async function sendMessage(action, data = {}) {
    try {
        const response = await chrome.runtime.sendMessage({
            action,
            ...data,
            timestamp: Date.now()
        });
        return response;
    } catch (error) {
        log(`오류: ${error.message}`, 'error');
        return null;
    }
}

// ==================== STATUS MANAGEMENT ====================
async function updateStatus() {
    log('상태 확인 중...');
    
    const response = await sendMessage('GET_STATUS');
    
    if (response && response.success) {
        // Update platform status
        for (const platform of UI.platforms) {
            const indicator = $(`status-${platform}`);
            if (indicator) {
                const isOnline = response.platforms && response.platforms[platform];
                indicator.className = `indicator ${isOnline ? 'online' : 'offline'}`;
            }
        }
        
        // Update relay status
        if (response.relay) {
            UI.relayActive = response.relay.active;
            updateRelayUI();
            
            if (response.relay.currentRound) {
                UI.stats.round = response.relay.currentRound;
                updateStats();
            }
        }
        
        // Update monitor stats
        if (response.monitor) {
            UI.stats.success = response.monitor.successCount || 0;
            UI.stats.fail = response.monitor.failCount || 0;
            updateStats();
        }
        
        log('✅ 상태 업데이트 완료');
    } else {
        log('상태 확인 실패', 'error');
    }
}

function updateStats() {
    $('statSuccess').textContent = UI.stats.success;
    $('statFail').textContent = UI.stats.fail;
    $('statRound').textContent = UI.stats.round;
}

function updateRelayUI() {
    const startBtn = $('btnStartRelay');
    const stopBtn = $('btnStopRelay');
    const indicator = $('relayIndicator');
    const progress = $('relayProgress');
    
    if (UI.relayActive) {
        startBtn.disabled = true;
        stopBtn.disabled = false;
        indicator.classList.add('active');
        
        // Update progress
        const progressPercent = (UI.stats.round / 10) * 100;
        progress.style.width = `${Math.min(progressPercent, 100)}%`;
    } else {
        startBtn.disabled = false;
        stopBtn.disabled = true;
        indicator.classList.remove('active');
        progress.style.width = '0%';
    }
}

// ==================== ACTIONS ====================
async function openAllPlatforms() {
    log('모든 플랫폼 열기...');
    
    // Show loading on all indicators
    UI.platforms.forEach(platform => {
        const indicator = $(`status-${platform}`);
        if (indicator) indicator.className = 'indicator loading';
    });
    
    const response = await sendMessage('OPEN_ALL');
    
    if (response && response.success) {
        log('✅ 모든 플랫폼 열기 완료');
        
        // Wait for tabs to load
        setTimeout(updateStatus, 3000);
    } else {
        log('플랫폼 열기 실패', 'error');
    }
}

async function sendToAll() {
    const input = $('messageInput');
    const message = input.value.trim();
    
    if (!message) {
        log('메시지를 입력하세요', 'warning');
        return;
    }
    
    log(`전체 전송: "${message.substring(0, 50)}..."`);
    
    const response = await sendMessage('SEND_TO_ALL', { message });
    
    if (response && response.success) {
        log('✅ 메시지 전송 완료');
        
        // Report per-platform results
        if (response.platforms) {
            for (const [platform, success] of Object.entries(response.platforms)) {
                if (success) {
                    log(`✅ ${platform}: 성공`);
                } else {
                    log(`❌ ${platform}: 실패`, 'warning');
                }
            }
        }
        
        input.value = '';
    } else {
        log('메시지 전송 실패', 'error');
    }
}

async function startRelay() {
    const input = $('relayObjective');
    const objective = input.value.trim();
    
    if (!objective) {
        log('프로젝트 목표를 입력하세요', 'warning');
        return;
    }
    
    log(`자동 릴레이 시작: "${objective}"`);
    
    const response = await sendMessage('START_RELAY', { objective });
    
    if (response && response.success) {
        log('✅ 자동 릴레이 시작됨');
        UI.relayActive = true;
        updateRelayUI();
        
        input.value = '';
    } else {
        log('자동 릴레이 시작 실패', 'error');
    }
}

async function stopRelay() {
    log('자동 릴레이 중지...');
    
    const response = await sendMessage('STOP_RELAY');
    
    if (response && response.success) {
        log('✅ 자동 릴레이 중지됨');
        UI.relayActive = false;
        updateRelayUI();
    } else {
        log('자동 릴레이 중지 실패', 'error');
    }
}

async function testAll() {
    log('전체 테스트 시작...');
    
    for (const platform of UI.platforms) {
        log(`테스트: ${platform}`);
        
        const response = await sendMessage('TEST_PLATFORM', { platform });
        
        if (response && response.success) {
            log(`✅ ${platform}: 정상`);
        } else {
            log(`❌ ${platform}: 오류`, 'error');
        }
    }
    
    log('테스트 완료');
}

async function exportData() {
    log('데이터 내보내기...');
    
    const response = await sendMessage('EXPORT_DATA');
    
    if (response && response.success) {
        log('✅ 데이터 내보내기 완료');
    } else {
        log('데이터 내보내기 실패', 'error');
    }
}

async function clearData() {
    if (!confirm('모든 데이터를 삭제하시겠습니까?')) return;
    
    log('데이터 초기화...');
    
    const response = await sendMessage('CLEAR_DATA');
    
    if (response && response.success) {
        log('✅ 데이터 초기화 완료');
        UI.stats = { success: 0, fail: 0, round: 0 };
        UI.logs = [];
        updateStats();
        updateMonitor();
    } else {
        log('데이터 초기화 실패', 'error');
    }
}

function openMonitorWindow() {
    chrome.tabs.create({
        url: chrome.runtime.getURL('monitor.html')
    });
}

// ==================== EVENT LISTENERS ====================
function setupEventListeners() {
    // Buttons
    $('btnOpenAll').addEventListener('click', openAllPlatforms);
    $('btnCheckStatus').addEventListener('click', updateStatus);
    $('btnTestAll').addEventListener('click', testAll);
    $('btnMonitor').addEventListener('click', openMonitorWindow);
    $('btnSendAll').addEventListener('click', sendToAll);
    $('btnStartRelay').addEventListener('click', startRelay);
    $('btnStopRelay').addEventListener('click', stopRelay);
    $('btnExport').addEventListener('click', exportData);
    $('btnClear').addEventListener('click', clearData);
    
    // Monitor toggle
    $('toggleMonitor').addEventListener('click', () => {
        UI.monitorVisible = !UI.monitorVisible;
        const content = $('monitorContent');
        const toggle = $('toggleMonitor');
        
        if (UI.monitorVisible) {
            content.classList.add('active');
            toggle.textContent = '숨기기';
        } else {
            content.classList.remove('active');
            toggle.textContent = '표시';
        }
    });
    
    // Platform status clicks
    document.querySelectorAll('.platform-status').forEach(element => {
        element.addEventListener('click', async () => {
            const platform = element.dataset.platform;
            log(`${platform} 테스트...`);
            
            const response = await sendMessage('TEST_PLATFORM', { platform });
            
            if (response && response.success) {
                log(`✅ ${platform} 정상`);
            } else {
                log(`❌ ${platform} 오류`, 'error');
            }
        });
    });
    
    // Enter key for message input
    $('messageInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendToAll();
        }
    });
    
    // Enter key for relay objective
    $('relayObjective').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!UI.relayActive) startRelay();
        }
    });
}

// ==================== INITIALIZATION ====================
async function initialize() {
    log('시스템 초기화...');
    
    // Setup event listeners
    setupEventListeners();
    
    // Initial status check
    await updateStatus();
    
    // Auto-refresh status
    setInterval(updateStatus, 10000);
    
    log('✅ 시스템 준비 완료');
}

// ==================== START ====================
document.addEventListener('DOMContentLoaded', initialize);

console.log('✅ Ultimate Popup Controller Ready');