<#
  git-autosync.ps1 — VRIN AI Hub 자동 동기화 (작업 스케줄러 전용)

  매일 1회 자동 실행되어 OneDrive\vrin_AI_hub 의 변경사항을
  커밋하고 GitHub 에 푸시합니다. 화면에 아무것도 띄우지 않고,
  결과는 로그 파일에만 기록합니다.

  등록/해제:  scripts\setup-autosync.cmd
  수동 실행 :  scripts\git-sync.cmd
#>

$ErrorActionPreference = 'Continue'

$Workspace = Join-Path $env:USERPROFILE 'OneDrive\vrin_AI_hub'
$LogDir    = Join-Path $env:USERPROFILE '.git-repos'
$LogFile   = Join-Path $LogDir 'vrin-autosync.log'
$MaxRetry  = 4

# ── 로그 ──────────────────────────────────────────
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

function Write-Log {
    param([string]$Message, [string]$Level = 'INFO')
    $line = "{0} [{1}] {2}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Level, $Message
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

# 로그가 2000줄 넘으면 최근 800줄만 남김
if ((Test-Path $LogFile) -and ((Get-Content $LogFile).Count -gt 2000)) {
    (Get-Content $LogFile | Select-Object -Last 800) | Set-Content $LogFile -Encoding UTF8
}

Write-Log '───────── 자동 동기화 시작 ─────────'

function Stop-Run {
    param([string]$Message, [string]$Level = 'ERROR', [int]$Code = 1)
    Write-Log $Message $Level
    Write-Log ('───────── 종료 (코드 {0}) ─────────' -f $Code)
    exit $Code
}

# ── [1] 사전 확인 ─────────────────────────────────
if (-not (Test-Path $Workspace)) {
    Stop-Run "워크스페이스를 찾을 수 없습니다: $Workspace"
}
Set-Location $Workspace

git rev-parse --git-dir 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Stop-Run 'Git 저장소가 아닙니다 (.git junction 깨짐). setup-desktop.cmd 를 실행하세요.'
}

# 진행 중인 rebase/merge 가 있으면 절대 건드리지 않는다
$gitDir = (git rev-parse --git-dir).Trim()
foreach ($m in @('rebase-merge', 'rebase-apply', 'MERGE_HEAD', 'CHERRY_PICK_HEAD')) {
    if (Test-Path (Join-Path $gitDir $m)) {
        Stop-Run "작업이 진행 중입니다 ($m). 대표님이 직접 마무리하신 뒤 다시 실행됩니다." 'WARN' 2
    }
}

# 커밋 신원 확인
$userName  = (git config user.name)
$userEmail = (git config user.email)
if ([string]::IsNullOrWhiteSpace($userName) -or [string]::IsNullOrWhiteSpace($userEmail)) {
    Stop-Run 'git user.name / user.email 이 설정되지 않아 커밋할 수 없습니다.'
}

$Branch = (git rev-parse --abbrev-ref HEAD).Trim()
if ($Branch -eq 'HEAD') { Stop-Run 'detached HEAD 상태입니다. 브랜치를 체크아웃해주세요.' }
Write-Log "브랜치: $Branch"

# ── [2] 변경사항 커밋 ─────────────────────────────
git add -A 2>&1 | Out-Null
git diff --cached --quiet
$hasChanges = ($LASTEXITCODE -ne 0)

if ($hasChanges) {
    $files = @(git diff --cached --name-only).Count
    Write-Log "변경 파일 ${files}개 — 커밋합니다."
    $msg = 'chore: 자동 동기화 ({0})' -f (Get-Date -Format 'yyyy-MM-dd HH:mm')
    git commit -m $msg 2>&1 | ForEach-Object { Write-Log $_ 'git' }
    if ($LASTEXITCODE -ne 0) { Stop-Run '커밋 실패.' }
} else {
    Write-Log '변경사항 없음 — 커밋 생략.'
}

# ── [3] 원격 최신 반영 ────────────────────────────
Write-Log 'GitHub 최신 내용 반영 중 (pull --rebase)...'
git pull --rebase origin $Branch 2>&1 | ForEach-Object { Write-Log $_ 'git' }
if ($LASTEXITCODE -ne 0) {
    # 충돌 시 저장소를 원상복구해 대표님 작업을 막지 않는다
    git rebase --abort 2>&1 | Out-Null
    Stop-Run '충돌로 pull --rebase 실패 — 원상복구했습니다. 직접 확인이 필요합니다.'
}

# ── [4] 푸시 (네트워크 실패 시 재시도) ────────────
$ahead = (git rev-list --count "origin/$Branch..$Branch" 2>$null)
if ($ahead) { $ahead = $ahead.ToString().Trim() }
if ($LASTEXITCODE -eq 0 -and $ahead -eq '0') {
    Write-Log '올릴 커밋이 없습니다 — 이미 최신입니다.'
    Write-Log '───────── 정상 종료 ─────────'
    exit 0
}

for ($try = 1; $try -le ($MaxRetry + 1); $try++) {
    git push origin $Branch 2>&1 | ForEach-Object { Write-Log $_ 'git' }
    if ($LASTEXITCODE -eq 0) {
        Write-Log "푸시 완료 — GitHub 반영됨 (커밋 ${ahead}개)."
        Write-Log '───────── 정상 종료 ─────────'
        exit 0
    }
    if ($try -gt $MaxRetry) { break }
    $wait = [math]::Pow(2, $try)   # 2, 4, 8, 16초
    Write-Log "푸시 실패 — ${wait}초 후 재시도 ($try/$MaxRetry)" 'WARN'
    Start-Sleep -Seconds $wait
}

Stop-Run "푸시 실패 ($MaxRetry회 재시도 후). 네트워크 또는 GitHub 인증을 확인해주세요."
