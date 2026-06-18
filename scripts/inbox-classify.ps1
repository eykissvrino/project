<#
.SYNOPSIS
  VRIN _INBOX 자동분류 정기 실행기 (헤드리스).
  _INBOX 에 새 파일이 있을 때만 Claude 를 깨워 file-classification 스킬을 돌린다.

.DESCRIPTION
  - 예약(Windows Task Scheduler)에서 호출되거나, 수동으로 실행할 수 있다.
  - 무인 실행이므로: 확신(High) 건만 자동 이동, 애매(Low) 건은 _INBOX/_미분류/ 로 보류하고
    질문을 _INBOX/_질문대기.md 에 적재한다(다음 대화 때 대표님이 답).
  - 모든 이동은 _INBOX/_분류로그.md 에 기록 → 되돌리기 가능.

.PARAMETER Workspace
  vrin_AI_hub 루트 경로. 기본값은 OneDrive 본체.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\inbox-classify.ps1
#>
param(
  [string]$Workspace = "$env:USERPROFILE\OneDrive\vrin_AI_hub"
)

$ErrorActionPreference = "Stop"
$inbox = Join-Path $Workspace "_INBOX"
$claude = Join-Path $env:USERPROFILE ".local\bin\claude.exe"
if (-not (Test-Path $claude)) { $claude = "claude" }  # PATH 폴백

# 예약 대상 외 예약파일(README/로그/큐/_미분류)을 제외하고 실제 분류 대상이 있는지 확인
$reserved = @("README.md", "_분류로그.md", "_질문대기.md", "_미분류")
if (-not (Test-Path $inbox)) {
  Write-Host "[inbox-classify] _INBOX 없음: $inbox"; exit 0
}
$targets = Get-ChildItem -LiteralPath $inbox -Force |
  Where-Object { $reserved -notcontains $_.Name -and $_.Name -notlike ".*" }

if (-not $targets -or $targets.Count -eq 0) {
  Write-Host "[inbox-classify] 분류할 새 파일 없음. 종료."; exit 0
}

Write-Host "[inbox-classify] 대상 $($targets.Count)건 발견 → Claude 호출"

$prompt = @'
file-classification 스킬을 실행해 _INBOX 를 분류하라. 지금은 무인(예약) 실행이다:
- 확신(High) 건만 자동 이동하고 _INBOX/_분류로그.md 에 기록한다.
- 애매(Low/질문) 건은 절대 추측 이동하지 말고 _INBOX/_미분류/ 로 옮긴 뒤,
  무엇이 애매한지 _INBOX/_질문대기.md 에 표로 적재한다(다음 대화에서 대표님이 답할 것).
- 삭제·덮어쓰기 금지. 이름 충돌은 suffix.
- 끝나면 한 줄 요약(자동 n / 보류 k)을 출력한다.
'@

# 무인 이동을 위해 워크스페이스 범위로 권한 허용. 비대화형이므로 질문은 큐로 우회.
& $claude -p $prompt `
  --add-dir $Workspace `
  --permission-mode acceptEdits `
  --allowedTools "Read,Write,Edit,Glob,Grep,Bash,Skill,mcp__hwp-mcp__read_hwp_text" 2>&1 |
  Tee-Object -FilePath (Join-Path $inbox "_예약실행.log") -Append

Write-Host "[inbox-classify] 완료."
