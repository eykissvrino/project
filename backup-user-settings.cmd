@echo off
chcp 65001 >nul
setlocal

echo.
echo ══════════════════════════════════════════════════
echo   유저 레벨 Claude 설정 백업 (노트북 → OneDrive)
echo ══════════════════════════════════════════════════
echo.
echo   백업 대상: ~/.claude/ (스킬, 플러그인, 설정, 커맨드)
echo   백업 위치: OneDrive\vrin_AI_hub\.desktop-setup\user-settings-backup\
echo.
echo   ※ 이 백업은 데스크탑/다른 PC에서 setup-desktop.cmd로 복원됨
echo   ※ 캐시, 로그, 임시 파일은 제외함
echo.

set "USER_CLAUDE=%USERPROFILE%\.claude"
set "BACKUP=%USERPROFILE%\OneDrive\vrin_AI_hub\.desktop-setup\user-settings-backup"

if not exist "%USER_CLAUDE%" (
    echo   [오류] %USER_CLAUDE% 가 없습니다.
    goto :error
)

if not exist "%USERPROFILE%\OneDrive\vrin_AI_hub" (
    echo   [오류] OneDrive\vrin_AI_hub 폴더가 없습니다.
    goto :error
)

:: 백업 폴더 생성
if not exist "%BACKUP%" mkdir "%BACKUP%"

echo [1/6] skills/ 백업 중...
if exist "%USER_CLAUDE%\skills" (
    xcopy "%USER_CLAUDE%\skills" "%BACKUP%\skills\" /E /I /Y /Q >nul 2>&1
    echo        완료 (Tier 1 전역 스킬)
) else (
    echo        skills 폴더 없음 - 스킵
)

echo [2/6] plugins/ 백업 중 (캐시 제외)...
if exist "%USER_CLAUDE%\plugins" (
    :: plugins는 cache 폴더 제외하고 복사
    xcopy "%USER_CLAUDE%\plugins" "%BACKUP%\plugins\" /E /I /Y /Q /EXCLUDE:%TEMP%\plugin-exclude.txt 2>nul >nul
    if errorlevel 1 (
        :: exclude 파일이 없으면 그냥 통째로 복사
        echo cache\ > "%TEMP%\plugin-exclude.txt"
        echo .cache\ >> "%TEMP%\plugin-exclude.txt"
        xcopy "%USER_CLAUDE%\plugins" "%BACKUP%\plugins\" /E /I /Y /Q /EXCLUDE:%TEMP%\plugin-exclude.txt >nul 2>&1
    )
    echo        완료 (oh-my-claudecode, mckinsey-pptx 등)
) else (
    echo        plugins 폴더 없음 - 스킵
)

echo [3/6] commands/ 백업 중...
if exist "%USER_CLAUDE%\commands" (
    xcopy "%USER_CLAUDE%\commands" "%BACKUP%\commands\" /E /I /Y /Q >nul 2>&1
    echo        완료
) else (
    echo        commands 폴더 없음 - 스킵
)

echo [4/6] settings.json / CLAUDE.md 백업 중...
if exist "%USER_CLAUDE%\settings.json" (
    copy "%USER_CLAUDE%\settings.json" "%BACKUP%\" /Y >nul 2>&1
    echo        settings.json 완료
)
if exist "%USER_CLAUDE%\CLAUDE.md" (
    copy "%USER_CLAUDE%\CLAUDE.md" "%BACKUP%\" /Y >nul 2>&1
    echo        CLAUDE.md 완료
)

echo [5/6] my-skills-repo/ 백업 중...
if exist "%USER_CLAUDE%\my-skills-repo" (
    xcopy "%USER_CLAUDE%\my-skills-repo" "%BACKUP%\my-skills-repo\" /E /I /Y /Q >nul 2>&1
    echo        완료
) else (
    echo        my-skills-repo 폴더 없음 - 스킵
)

echo [6/6] OMC 설정 백업 중...
if exist "%USER_CLAUDE%\.omc-config.json" (
    copy "%USER_CLAUDE%\.omc-config.json" "%BACKUP%\" /Y >nul 2>&1
    echo        .omc-config.json 완료
) else (
    echo        .omc-config.json 없음 - 스킵
)

echo.
echo ══════════════════════════════════════════════════
echo   백업 완료!
echo ══════════════════════════════════════════════════
echo.
echo   백업 위치: %BACKUP%
echo.
echo   다음 단계 (데스크탑에서):
echo     1. OneDrive 동기화 완료 대기
echo     2. setup-desktop.cmd 실행
echo     → 위 백업이 자동으로 ~/.claude/ 에 복원됨
echo.

goto :end

:error
echo.
echo   백업 실패. 위의 오류 메시지를 확인하세요.
echo.

:end
endlocal
pause
