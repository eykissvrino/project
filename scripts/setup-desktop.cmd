@echo off
chcp 65001 >nul
setlocal

echo.
echo ══════════════════════════════════════════════════
echo   데스크탑 초기 설정 스크립트
echo   OneDrive VRIN AI Hub + Git + AI 도구
echo ══════════════════════════════════════════════════
echo.
echo   이 스크립트가 하는 일:
echo     1. Git 저장소 초기화 (junction으로 OneDrive 밖에)
echo     2. .omc/.claude 런타임 폴더 junction 생성
echo     3. 유저 레벨 Claude 설정 복원 (스킬 22개 등)
echo     4. 프로젝트 리소스 배포 (sync-tools.cmd)
echo.

:: ── 경로 설정 ──
set "ONEDRIVE=%USERPROFILE%\OneDrive"
set "WORKSPACE=%ONEDRIVE%\vrin_AI_hub"
set "GIT_LOCAL=%USERPROFILE%\.git-repos\vrin_AI_hub"
set "OMC_LOCAL=%USERPROFILE%\.omc-local\vrin_AI_hub"
set "CLAUDE_LOCAL=%USERPROFILE%\.claude-local\vrin_AI_hub"
set "BACKUP=%WORKSPACE%\.desktop-setup\user-settings-backup"

:: ══════════════════════════════════════════════════
:: [0] 사전 확인
:: ══════════════════════════════════════════════════
echo [0/6] 사전 확인...
echo.

:: OneDrive 확인
if not exist "%ONEDRIVE%" (
    echo   [오류] OneDrive 폴더가 없습니다: %ONEDRIVE%
    echo   OneDrive에 로그인하고 동기화를 완료해주세요.
    goto :error
)

:: Workspace 확인
if not exist "%WORKSPACE%" (
    echo   [오류] OneDrive에 workspace가 없습니다.
    echo   OneDrive 동기화가 아직 진행 중일 수 있습니다.
    echo   OneDrive 아이콘에서 동기화 상태를 확인해주세요.
    goto :error
)

:: _core 확인 (동기화 완료 판단 기준)
if not exist "%WORKSPACE%\_core" (
    echo   [오류] _core 폴더가 없습니다.
    echo   OneDrive 동기화가 아직 완료되지 않았습니다.
    echo.
    echo   해결 방법:
    echo     1. 탐색기에서 OneDrive\vrin_AI_hub 폴더 찾기
    echo     2. 폴더 우클릭 → "항상 이 장치에 유지" 선택
    echo     3. 동기화 완료 후 이 스크립트 다시 실행
    goto :error
)

:: CLAUDE.md 확인 (핵심 파일 동기화 확인)
if not exist "%WORKSPACE%\CLAUDE.md" (
    echo   [경고] CLAUDE.md가 아직 다운로드되지 않았습니다.
    echo   vrin_AI_hub 폴더를 "항상 이 장치에 유지"로 설정했는지 확인하세요.
    echo.
    echo   계속하려면 아무 키나, 취소는 Ctrl+C
    pause >nul
)

:: Git 설치 확인
where git >nul 2>&1
if errorlevel 1 (
    echo   [오류] Git이 설치되어 있지 않습니다.
    echo.
    echo   설치 방법:
    echo     https://git-scm.com/download/win 에서 다운로드
    echo     설치 후 이 스크립트를 다시 실행하세요.
    goto :error
)

echo   OneDrive vrin_AI_hub: OK
echo   _core 폴더:          OK
echo   Git 설치:            OK
echo.

:: ══════════════════════════════════════════════════
:: [1] Git 저장소 설정
:: ══════════════════════════════════════════════════
echo [1/6] Git 저장소 설정 중...

if exist "%WORKSPACE%\.git" (
    :: .git이 이미 존재 (junction이거나 디렉토리)
    cd /d "%WORKSPACE%"
    git status >nul 2>&1
    if errorlevel 1 (
        echo   .git이 존재하지만 작동하지 않습니다. 재설정합니다...
        rmdir "%WORKSPACE%\.git" >nul 2>&1
        del "%WORKSPACE%\.git" >nul 2>&1
    ) else (
        echo   Git 이미 설정됨 - 스킵
        goto :skip_git
    )
)

:: 로컬 .git 디렉토리 생성
if not exist "%USERPROFILE%\.git-repos" mkdir "%USERPROFILE%\.git-repos"

if exist "%GIT_LOCAL%" (
    echo   기존 .git-repos 발견 - 재사용합니다.
) else (
    echo   GitHub에서 저장소 데이터 가져오는 중...
    echo   (파일은 이미 OneDrive에 있으므로 git 이력만 가져옵니다)
    echo.

    :: 임시 위치에 클론 (--no-checkout: 파일 체크아웃 안 함)
    git clone --no-checkout https://github.com/eykissvrino/project.git "%TEMP%\workspace-git-temp" >nul 2>&1
    if errorlevel 1 (
        echo   [오류] Git clone 실패
        echo   네트워크 연결을 확인하고 다시 시도해주세요.
        goto :error
    )

    :: .git 디렉토리만 로컬로 이동
    move "%TEMP%\workspace-git-temp\.git" "%GIT_LOCAL%" >nul 2>&1

    :: 임시 폴더 삭제
    rmdir /s /q "%TEMP%\workspace-git-temp" >nul 2>&1

    echo   Git 이력 다운로드 완료
)

:: Junction 생성 (.git → 로컬)
mklink /J "%WORKSPACE%\.git" "%GIT_LOCAL%" >nul 2>&1
if errorlevel 1 (
    echo   [오류] .git junction 생성 실패
    echo   관리자 권한으로 실행해보세요.
    goto :error
)

:: Git worktree를 OneDrive workspace로 설정
cd /d "%WORKSPACE%"
git config core.worktree "%WORKSPACE%"

:: 인덱스를 현재 커밋에 맞춤 (파일은 건드리지 않음)
git reset HEAD >nul 2>&1

echo   .git → %GIT_LOCAL% (junction 생성)
echo.

:: Git 상태 확인
echo   Git 상태 확인:
git status --short 2>&1
echo.

:skip_git

:: ══════════════════════════════════════════════════
:: [2] .omc junction 생성
:: ══════════════════════════════════════════════════
echo [2/6] .omc 런타임 폴더 설정 중...

if exist "%WORKSPACE%\.omc" (
    :: 이미 존재 (OneDrive가 동기화했을 수 있음)
    :: junction이 아니면 로컬로 이동
    fsutil reparsepoint query "%WORKSPACE%\.omc" >nul 2>&1
    if errorlevel 1 (
        :: junction이 아님 → OneDrive가 동기화한 일반 폴더
        if not exist "%USERPROFILE%\.omc-local" mkdir "%USERPROFILE%\.omc-local"
        if exist "%OMC_LOCAL%" rmdir /s /q "%OMC_LOCAL%" >nul 2>&1
        move "%WORKSPACE%\.omc" "%OMC_LOCAL%" >nul 2>&1
        mklink /J "%WORKSPACE%\.omc" "%OMC_LOCAL%" >nul 2>&1
        echo   .omc → %OMC_LOCAL% (기존 폴더를 junction으로 변환)
    ) else (
        echo   .omc junction 이미 존재 - 스킵
    )
) else (
    if not exist "%USERPROFILE%\.omc-local" mkdir "%USERPROFILE%\.omc-local"
    if not exist "%OMC_LOCAL%" mkdir "%OMC_LOCAL%"
    mklink /J "%WORKSPACE%\.omc" "%OMC_LOCAL%" >nul 2>&1
    echo   .omc → %OMC_LOCAL% (junction 생성)
)
echo.

:: ══════════════════════════════════════════════════
:: [3] .claude (workspace 루트) junction 생성
:: ══════════════════════════════════════════════════
echo [3/6] .claude (workspace) 런타임 폴더 설정 중...

if exist "%WORKSPACE%\.claude" (
    fsutil reparsepoint query "%WORKSPACE%\.claude" >nul 2>&1
    if errorlevel 1 (
        if not exist "%USERPROFILE%\.claude-local" mkdir "%USERPROFILE%\.claude-local"
        if exist "%CLAUDE_LOCAL%" rmdir /s /q "%CLAUDE_LOCAL%" >nul 2>&1
        move "%WORKSPACE%\.claude" "%CLAUDE_LOCAL%" >nul 2>&1
        mklink /J "%WORKSPACE%\.claude" "%CLAUDE_LOCAL%" >nul 2>&1
        echo   .claude → %CLAUDE_LOCAL% (기존 폴더를 junction으로 변환)
    ) else (
        echo   .claude junction 이미 존재 - 스킵
    )
) else (
    if not exist "%USERPROFILE%\.claude-local" mkdir "%USERPROFILE%\.claude-local"
    if not exist "%CLAUDE_LOCAL%" mkdir "%CLAUDE_LOCAL%"
    mklink /J "%WORKSPACE%\.claude" "%CLAUDE_LOCAL%" >nul 2>&1
    echo   .claude → %CLAUDE_LOCAL% (junction 생성)
)
echo.

:: ══════════════════════════════════════════════════
:: [4] 유저 레벨 Claude 설정 복원
:: ══════════════════════════════════════════════════
echo [4/6] 유저 레벨 Claude 설정 복원 중...

if not exist "%BACKUP%" (
    echo   [경고] 백업 파일이 없습니다: %BACKUP%
    echo   노트북에서 migrate-to-onedrive.cmd를 먼저 실행해야 합니다.
    echo   또는 수동으로 ~/.claude/ 설정을 복사해주세요.
    echo.
    goto :skip_restore
)

:: ~/.claude/ 디렉토리 확인
if not exist "%USERPROFILE%\.claude" mkdir "%USERPROFILE%\.claude"

:: 스킬 복원
if exist "%BACKUP%\skills" (
    xcopy "%BACKUP%\skills" "%USERPROFILE%\.claude\skills\" /E /I /Y /Q >nul 2>&1
    echo   - skills/ (유저 스킬 22개) 복원됨
)

:: settings.json 복원
if exist "%BACKUP%\settings.json" (
    copy "%BACKUP%\settings.json" "%USERPROFILE%\.claude\" /Y >nul 2>&1
    echo   - settings.json 복원됨
)

:: 커맨드 복원
if exist "%BACKUP%\commands" (
    xcopy "%BACKUP%\commands" "%USERPROFILE%\.claude\commands\" /E /I /Y /Q >nul 2>&1
    echo   - commands/ 복원됨
)

:: CLAUDE.md 복원
if exist "%BACKUP%\CLAUDE.md" (
    copy "%BACKUP%\CLAUDE.md" "%USERPROFILE%\.claude\" /Y >nul 2>&1
    echo   - CLAUDE.md 복원됨
)

:: 플러그인 복원
if exist "%BACKUP%\plugins" (
    xcopy "%BACKUP%\plugins" "%USERPROFILE%\.claude\plugins\" /E /I /Y /Q >nul 2>&1
    echo   - plugins/ 복원됨
)

:: OMC 설정 복원
if exist "%BACKUP%\.omc-config.json" (
    copy "%BACKUP%\.omc-config.json" "%USERPROFILE%\.claude\" /Y >nul 2>&1
    echo   - .omc-config.json 복원됨
)

:: my-skills-repo 복원
if exist "%BACKUP%\my-skills-repo" (
    xcopy "%BACKUP%\my-skills-repo" "%USERPROFILE%\.claude\my-skills-repo\" /E /I /Y /Q >nul 2>&1
    echo   - my-skills-repo/ 복원됨
)

echo   유저 설정 복원 완료!
echo.

:skip_restore

:: ══════════════════════════════════════════════════
:: [5] 프로젝트 리소스 배포
:: ══════════════════════════════════════════════════
echo [5/6] 프로젝트 리소스 배포 중...

if exist "%WORKSPACE%\sync-tools.cmd" (
    cd /d "%WORKSPACE%"
    call "%WORKSPACE%\sync-tools.cmd"
) else (
    echo   [경고] sync-tools.cmd를 찾을 수 없습니다.
    echo   OneDrive 동기화가 완료되면 수동으로 실행해주세요.
)
echo.

:: ══════════════════════════════════════════════════
:: [6] 최종 검증
:: ══════════════════════════════════════════════════
echo [6/6] 최종 검증...
echo.

cd /d "%WORKSPACE%"

echo   --- Git ---
git log --oneline -3 2>&1
echo.

echo   --- 프로젝트 ---
dir /b "%WORKSPACE%\projects\" 2>nul
echo.

echo   --- Junction ---
echo   [.git]
fsutil reparsepoint query "%WORKSPACE%\.git" >nul 2>&1 && echo     OK: junction || echo     [경고] junction 아님
echo   [.omc]
fsutil reparsepoint query "%WORKSPACE%\.omc" >nul 2>&1 && echo     OK: junction || echo     [경고] junction 아님
echo   [.claude]
fsutil reparsepoint query "%WORKSPACE%\.claude" >nul 2>&1 && echo     OK: junction || echo     [경고] junction 아님
echo.

echo   --- 유저 스킬 ---
if exist "%USERPROFILE%\.claude\skills" (
    dir /b "%USERPROFILE%\.claude\skills\" 2>nul | find /c /v "" 2>nul
    echo     개 유저 스킬 설치됨
) else (
    echo     [경고] 유저 스킬이 없습니다
)
echo.

:: ══════════════════════════════════════════════════
:: 완료!
:: ══════════════════════════════════════════════════
echo ══════════════════════════════════════════════════
echo   데스크탑 설정 완료!
echo ══════════════════════════════════════════════════
echo.
echo   워크스페이스: %WORKSPACE%
echo.
echo   Junction (OneDrive 밖):
echo     .git    → %GIT_LOCAL%
echo     .omc    → %OMC_LOCAL%
echo     .claude → %CLAUDE_LOCAL%
echo.
echo   ┌──────────────────────────────────────────────────┐
echo   │                                                   │
echo   │  [아직 안했다면 - 도구 설치]                      │
echo   │                                                   │
echo   │  1. Node.js 설치:                                 │
echo   │     https://nodejs.org/ (LTS 버전)                │
echo   │                                                   │
echo   │  2. Python 설치:                                  │
echo   │     https://www.python.org/downloads/             │
echo   │                                                   │
echo   │  3. Claude Code 설치 (터미널에서):                │
echo   │     npm install -g @anthropic-ai/claude-code      │
echo   │                                                   │
echo   │  [도구 설치 후]                                   │
echo   │                                                   │
echo   │  4. Claude Code 인증:                             │
echo   │     cd %WORKSPACE%                                │
echo   │     claude                                        │
echo   │     → 브라우저에서 Anthropic 로그인               │
echo   │                                                   │
echo   │  5. OMC 설치 (Claude Code 안에서):                │
echo   │     /oh-my-claudecode:omc-setup                   │
echo   │                                                   │
echo   │  6. OneDrive에서 workspace 폴더 우클릭            │
echo   │     → "항상 이 장치에 유지" 선택                  │
echo   │                                                   │
echo   └──────────────────────────────────────────────────┘
echo.

goto :end

:error
echo.
echo   ══════════════════════════════════════════════════
echo   설정 실패 - 위의 오류 메시지를 확인하세요.
echo   ══════════════════════════════════════════════════
echo.

:end
endlocal
pause
