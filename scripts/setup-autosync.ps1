<#
  setup-autosync.ps1 — 매일 자동 동기화 작업 등록/해제

  등록:  setup-autosync.cmd            (기본 18:00)
         setup-autosync.cmd 21:30      (시각 지정)
  해제:  setup-autosync.cmd /remove
  상태:  setup-autosync.cmd /status
#>
param(
    [string]$Time   = '18:00',
    [switch]$Remove,
    [switch]$Status
)

$ErrorActionPreference = 'Stop'
$TaskName = 'VRIN-AI-Hub-AutoSync'
$Script   = Join-Path $PSScriptRoot 'git-autosync.ps1'
$LogFile  = Join-Path $env:USERPROFILE '.git-repos\vrin-autosync.log'

function Line { Write-Host ('═' * 50) }

Line
Write-Host '  VRIN AI Hub — 매일 자동 동기화 설정'
Line
Write-Host ''

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

# ── 상태 확인 ─────────────────────────────────────
if ($Status) {
    if (-not $existing) {
        Write-Host '  등록되어 있지 않습니다.'
    } else {
        $info = Get-ScheduledTaskInfo -TaskName $TaskName
        Write-Host "  상태      : $($existing.State)"
        Write-Host "  다음 실행 : $($info.NextRunTime)"
        Write-Host "  마지막 실행: $($info.LastRunTime)  (결과 코드: $($info.LastTaskResult))"
        Write-Host ''
        if (Test-Path $LogFile) {
            Write-Host '  ── 최근 로그 15줄 ──'
            Get-Content $LogFile -Tail 15 | ForEach-Object { Write-Host "  $_" }
        }
    }
    Write-Host ''
    exit 0
}

# ── 해제 ──────────────────────────────────────────
if ($Remove) {
    if (-not $existing) {
        Write-Host '  등록된 작업이 없습니다 — 할 일이 없습니다.'
    } else {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host '  자동 동기화를 해제했습니다.'
        Write-Host '  (앞으로는 scripts\git-sync.cmd 로 직접 올리시면 됩니다)'
    }
    Write-Host ''
    exit 0
}

# ── 등록 ──────────────────────────────────────────
if (-not (Test-Path $Script)) {
    Write-Host "  [오류] git-autosync.ps1 을 찾을 수 없습니다: $Script" -ForegroundColor Red
    exit 1
}

try   { $at = [datetime]::ParseExact($Time, 'HH:mm', $null) }
catch { Write-Host "  [오류] 시각 형식이 잘못됐습니다: '$Time' (예: 18:00)" -ForegroundColor Red; exit 1 }

$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument ('-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File "{0}"' -f $Script)

$trigger = New-ScheduledTaskTrigger -Daily -At $at

# StartWhenAvailable: PC가 꺼져 있어 놓친 경우 켜자마자 실행
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -MultipleInstances IgnoreNew

try {
    Register-ScheduledTask `
        -TaskName    $TaskName `
        -Description 'OneDrive\vrin_AI_hub 의 변경사항을 매일 커밋하고 GitHub(eykissvrino/project)에 푸시합니다.' `
        -Action      $action `
        -Trigger     $trigger `
        -Settings    $settings `
        -Force | Out-Null
} catch {
    Write-Host "  [오류] 작업 등록 실패: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host '  이 창을 마우스 오른쪽 클릭 → "관리자 권한으로 실행" 으로 다시 시도해보세요.'
    exit 1
}

$next = (Get-ScheduledTaskInfo -TaskName $TaskName).NextRunTime

Write-Host '  등록 완료.'
Write-Host ''
Write-Host "  실행 시각 : 매일 $Time"
Write-Host "  다음 실행 : $next"
Write-Host "  대상      : $env:USERPROFILE\OneDrive\vrin_AI_hub  →  origin/main"
Write-Host "  로그      : $LogFile"
Write-Host ''
Write-Host '  ※ PC가 꺼져 있어 건너뛴 날은, 다음에 켤 때 자동으로 실행됩니다.'
Write-Host '  ※ 변경사항이 없는 날은 아무 커밋도 만들지 않습니다.'
Write-Host ''
Write-Host '  상태 확인 : scripts\setup-autosync.cmd /status'
Write-Host '  해제      : scripts\setup-autosync.cmd /remove'
Write-Host ''

# 지금 한 번 시험 실행
$answer = Read-Host '  지금 한 번 시험 삼아 돌려볼까요? (Y/N)'
if ($answer -match '^[Yy]') {
    Write-Host ''
    Write-Host '  실행 중...'
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 8
    Write-Host ''
    if (Test-Path $LogFile) {
        Write-Host '  ── 로그 ──'
        Get-Content $LogFile -Tail 20 | ForEach-Object { Write-Host "  $_" }
    } else {
        Write-Host '  아직 로그가 생성되지 않았습니다. 잠시 후 /status 로 확인해주세요.'
    }
    Write-Host ''
}
