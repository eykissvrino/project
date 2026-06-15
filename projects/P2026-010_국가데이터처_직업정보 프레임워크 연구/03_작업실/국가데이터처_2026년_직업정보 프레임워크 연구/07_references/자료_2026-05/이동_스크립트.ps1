# ============================================================
# 다운로드 파일 자동 정리 스크립트
# ------------------------------------------------------------
# 목적: $env:USERPROFILE\Downloads\ 에 있는 자료들을
#       07_references\자료_2026-05\ 의 카테고리 폴더로 이동
#
# 사용법:
#   1. PowerShell을 관리자 권한 없이 일반 모드로 실행
#   2. 이 스크립트가 있는 폴더로 이동 후
#      .\이동_스크립트.ps1
# ============================================================

# 기본 경로 설정
$Downloads = Join-Path $env:USERPROFILE "Downloads"
$BaseFolder = "C:\Users\eykis\OneDrive\vrin_AI_hub\projects\P2026-010_국가데이터처_직업정보 프레임워크 연구\국가데이터처_2026년_직업정보 프레임워크 연구\07_references\자료_2026-05"

# 카테고리별 폴더 매핑 (파일명 prefix → 대상 폴더)
$Categories = @{
    "A" = "A_ONET_공식"
    "B" = "B_국제프레임워크"
    "C" = "C_한국자료"
    "D" = "D_AI영향연구"
    "E" = "E_정부인프라"
    "F" = "F_기초자료"
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "다운로드 파일 자동 정리 스크립트" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Downloads 경로: $Downloads"
Write-Host "대상 폴더: $BaseFolder"
Write-Host ""

# 카테고리별 폴더가 없으면 생성
foreach ($cat in $Categories.Keys) {
    $targetDir = Join-Path $BaseFolder $Categories[$cat]
    if (-not (Test-Path $targetDir)) {
        New-Item -Path $targetDir -ItemType Directory -Force | Out-Null
        Write-Host "폴더 생성: $($Categories[$cat])" -ForegroundColor Yellow
    }
}

# 이동할 파일 패턴: A1_, A2_, B1_, ..., F2_ 등으로 시작
$movedCount = 0
$totalSize = 0

foreach ($cat in $Categories.Keys) {
    $pattern = "$cat[0-9]*_*"
    $files = Get-ChildItem -Path $Downloads -Filter $pattern -File -ErrorAction SilentlyContinue

    if ($files.Count -eq 0) {
        continue
    }

    $targetDir = Join-Path $BaseFolder $Categories[$cat]
    Write-Host ""
    Write-Host "[$cat] $($Categories[$cat]) ($($files.Count)개)" -ForegroundColor Green

    foreach ($file in $files) {
        $destPath = Join-Path $targetDir $file.Name
        try {
            Move-Item -Path $file.FullName -Destination $destPath -Force
            $sizeKB = [math]::Round($file.Length / 1KB, 0)
            Write-Host "  ✓ $($file.Name) ($sizeKB KB)" -ForegroundColor Gray
            $movedCount++
            $totalSize += $file.Length
        } catch {
            Write-Host "  ✗ $($file.Name) - 실패: $_" -ForegroundColor Red
        }
    }
}

# KECO 항목표 별도 처리 (파일명이 다양할 수 있음)
$kecoFiles = Get-ChildItem -Path $Downloads -Filter "*KECO*" -File -ErrorAction SilentlyContinue
$kecoFiles += Get-ChildItem -Path $Downloads -Filter "*고용직업분류*" -File -ErrorAction SilentlyContinue
$kecoFiles += Get-ChildItem -Path $Downloads -Filter "C1_*" -File -ErrorAction SilentlyContinue

$kecoTarget = Join-Path $BaseFolder $Categories["C"]
foreach ($file in $kecoFiles | Sort-Object Name -Unique) {
    $destPath = Join-Path $kecoTarget $file.Name
    if (-not (Test-Path $destPath)) {
        try {
            Move-Item -Path $file.FullName -Destination $destPath -Force
            $sizeKB = [math]::Round($file.Length / 1KB, 0)
            Write-Host "  ✓ $($file.Name) ($sizeKB KB) [KECO]" -ForegroundColor Gray
            $movedCount++
            $totalSize += $file.Length
        } catch { }
    }
}

# moel.go.kr 자동 다운로드 파일 처리 (한글 파일명일 수 있음)
$moelFiles = Get-ChildItem -Path $Downloads -Filter "*항목표*" -File -ErrorAction SilentlyContinue
$moelFiles += Get-ChildItem -Path $Downloads -Filter "*직업분류*" -File -ErrorAction SilentlyContinue
foreach ($file in $moelFiles | Sort-Object Name -Unique) {
    $destPath = Join-Path $kecoTarget $file.Name
    if (-not (Test-Path $destPath)) {
        try {
            Move-Item -Path $file.FullName -Destination $destPath -Force
            $sizeKB = [math]::Round($file.Length / 1KB, 0)
            Write-Host "  ✓ $($file.Name) ($sizeKB KB) [MoEL]" -ForegroundColor Gray
            $movedCount++
            $totalSize += $file.Length
        } catch { }
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "완료: $movedCount 개 파일 이동 (총 $([math]::Round($totalSize / 1MB, 2)) MB)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Yellow
Write-Host "  - 폴더 열기: explorer '$BaseFolder'"
Write-Host "  - 파일 누락 확인: Downloads 폴더에 A_, B_, ... 등이 남아있는지"
Write-Host ""
