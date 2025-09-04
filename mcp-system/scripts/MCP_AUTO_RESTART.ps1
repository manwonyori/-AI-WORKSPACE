# MCP SuperAssistant 자동 재시작 스크립트
# UTF-8 인코딩
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "MCP SuperAssistant Auto-Restart Monitor"

# 설정
$ConfigFile = "C:\Users\8899y\AI-WORKSPACE\mcp-system\configs\mcp_superassistant_config.json"
$LogFile = "C:\Users\8899y\AI-WORKSPACE\mcp-system\logs\mcp_auto_restart.log"
$ServerPort = 3006
$MaxRestarts = 50
$RestartDelay = 5
$HealthCheckInterval = 30

# 로그 함수
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Host $LogEntry -ForegroundColor $(
        switch ($Level) {
            "ERROR" { "Red" }
            "WARNING" { "Yellow" }
            "SUCCESS" { "Green" }
            default { "White" }
        }
    )
    Add-Content -Path $LogFile -Value $LogEntry -Encoding UTF8
}

# 로그 디렉토리 생성
$LogDir = Split-Path $LogFile -Parent
if (!(Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# Node.js 확인
function Test-NodeInstalled {
    try {
        $null = node --version
        return $true
    } catch {
        return $false
    }
}

# 서버 상태 확인
function Test-ServerHealth {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$ServerPort" -TimeoutSec 5 -ErrorAction SilentlyContinue
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

# 기존 프로세스 종료
function Stop-ExistingServers {
    Write-Log "기존 MCP 프로세스 종료 중..."
    
    # Node 프로세스 중 MCP 관련 프로세스 찾기
    Get-Process | Where-Object {
        $_.ProcessName -like "*node*" -and 
        ($_.CommandLine -like "*mcp*" -or $_.CommandLine -like "*superassistant*")
    } | ForEach-Object {
        try {
            Stop-Process -Id $_.Id -Force
            Write-Log "프로세스 종료: $($_.ProcessName) (PID: $($_.Id))"
        } catch {
            Write-Log "프로세스 종료 실패: $($_.ProcessName)" "WARNING"
        }
    }
    
    Start-Sleep -Seconds 2
}

# 서버 시작
function Start-MCPServer {
    Write-Log "MCP 서버 시작 중..."
    
    $Arguments = @(
        "@srbhptl39/mcp-superassistant-proxy@latest",
        "--config", "`"$ConfigFile`"",
        "--outputTransport", "sse",
        "--port", "$ServerPort"
    )
    
    $ProcessInfo = New-Object System.Diagnostics.ProcessStartInfo
    $ProcessInfo.FileName = "npx"
    $ProcessInfo.Arguments = $Arguments -join " "
    $ProcessInfo.UseShellExecute = $false
    $ProcessInfo.RedirectStandardOutput = $true
    $ProcessInfo.RedirectStandardError = $true
    $ProcessInfo.CreateNoWindow = $false
    $ProcessInfo.WorkingDirectory = "C:\Users\8899y\AI-WORKSPACE"
    
    try {
        $Process = [System.Diagnostics.Process]::Start($ProcessInfo)
        Write-Log "서버 프로세스 시작됨 (PID: $($Process.Id))" "SUCCESS"
        return $Process
    } catch {
        Write-Log "서버 시작 실패: $_" "ERROR"
        return $null
    }
}

# 메인 모니터링 루프
function Start-Monitoring {
    Write-Log "=" * 50
    Write-Log "MCP SuperAssistant 자동 재시작 모니터 시작"
    Write-Log "설정 파일: $ConfigFile"
    Write-Log "포트: $ServerPort"
    Write-Log "=" * 50
    
    if (!(Test-NodeInstalled)) {
        Write-Log "Node.js가 설치되지 않았습니다!" "ERROR"
        Write-Log "https://nodejs.org 에서 설치해주세요." "ERROR"
        exit 1
    }
    
    $RestartCount = 0
    $ServerProcess = $null
    $ConsecutiveFailures = 0
    
    while ($RestartCount -lt $MaxRestarts) {
        try {
            # 서버 상태 확인
            if (Test-ServerHealth) {
                if ($ConsecutiveFailures -gt 0) {
                    Write-Log "서버가 정상 작동 중입니다" "SUCCESS"
                    $ConsecutiveFailures = 0
                }
                
                # 프로세스 상태 확인
                if ($ServerProcess -and !$ServerProcess.HasExited) {
                    try {
                        $ProcInfo = Get-Process -Id $ServerProcess.Id -ErrorAction Stop
                        $CpuPercent = [math]::Round($ProcInfo.CPU, 2)
                        $MemoryMB = [math]::Round($ProcInfo.WorkingSet64 / 1MB, 2)
                        
                        if ($CpuPercent -gt 80) {
                            Write-Log "높은 CPU 사용률: $CpuPercent%" "WARNING"
                        }
                        if ($MemoryMB -gt 500) {
                            Write-Log "높은 메모리 사용: ${MemoryMB}MB" "WARNING"
                        }
                    } catch {
                        # 프로세스 정보를 가져올 수 없음
                    }
                }
            } else {
                # 서버 응답 없음
                $ConsecutiveFailures++
                Write-Log "서버 응답 없음 (연속 실패: $ConsecutiveFailures)" "WARNING"
                
                if ($ConsecutiveFailures -ge 3) {
                    Write-Log "연속 실패 임계값 도달. 서버 재시작..." "WARNING"
                    
                    Stop-ExistingServers
                    $ServerProcess = Start-MCPServer
                    
                    if ($ServerProcess) {
                        $RestartCount++
                        Write-Log "서버 재시작 완료 (총 재시작: $RestartCount회)"
                        Start-Sleep -Seconds $RestartDelay
                        
                        # 재시작 후 상태 확인
                        if (Test-ServerHealth) {
                            Write-Log "서버가 성공적으로 재시작되었습니다" "SUCCESS"
                            $ConsecutiveFailures = 0
                        }
                    } else {
                        Write-Log "서버 재시작 실패" "ERROR"
                        Start-Sleep -Seconds ($RestartDelay * 2)
                    }
                }
            }
            
            # 대기
            Start-Sleep -Seconds $HealthCheckInterval
            
        } catch {
            if ($_.Exception.GetType().Name -eq "PipelineStoppedException") {
                Write-Log "사용자에 의해 중단됨"
                break
            } else {
                Write-Log "모니터링 오류: $_" "ERROR"
                Start-Sleep -Seconds 5
            }
        }
    }
    
    if ($RestartCount -ge $MaxRestarts) {
        Write-Log "최대 재시작 횟수($MaxRestarts)에 도달했습니다" "CRITICAL"
    }
    
    # 정리
    if ($ServerProcess -and !$ServerProcess.HasExited) {
        Stop-Process -Id $ServerProcess.Id -Force
    }
}

# 실행
try {
    Start-Monitoring
} finally {
    Write-Log "Monitoring stopped"
}