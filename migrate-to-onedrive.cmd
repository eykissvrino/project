@echo off
chcp 949 >nul
setlocal

echo.
echo ========================================
echo   VRIN AI Hub - OneDrive Migration
echo ========================================
echo.

set "SOURCE=%USERPROFILE%\workspace"
set "ONEDRIVE=%USERPROFILE%\OneDrive"
set "TARGET=%ONEDRIVE%\vrin_AI_hub"
set "GIT_LOCAL=%USERPROFILE%\.git-repos\vrin_AI_hub"
set "OMC_LOCAL=%USERPROFILE%\.omc-local\vrin_AI_hub"
set "CLAUDE_LOCAL=%USERPROFILE%\.claude-local\vrin_AI_hub"

echo [0/7] Pre-check...
if not exist "%SOURCE%" (echo   [ERROR] %SOURCE% not found & goto :error)
if not exist "%SOURCE%\.git" (echo   [ERROR] .git not found & goto :error)
if not exist "%ONEDRIVE%" (echo   [ERROR] OneDrive not found & goto :error)
if exist "%TARGET%" (echo   [ERROR] %TARGET% already exists & goto :error)

echo   Source: %SOURCE%
echo   Target: %TARGET%
echo.
echo   Close all editors/terminals first!
echo   Press any key to continue (Ctrl+C = cancel)
pause >nul
echo.

echo [1/7] Git backup...
cd /d "%SOURCE%"
git add -A >nul 2>&1
git diff --cached --quiet 2>nul
if errorlevel 1 (git commit -m "OneDrive migration backup" >nul 2>&1 & echo   Committed) else (echo   No changes)
git push origin main >nul 2>&1
if errorlevel 1 (echo   [WARN] Push failed) else (echo   Push OK)
echo.

echo [2/7] Moving to OneDrive...
cd /d "%USERPROFILE%"
move "%SOURCE%" "%TARGET%" >nul 2>&1
if errorlevel 1 (echo   [ERROR] Move failed & goto :error)
echo   Done
echo.

echo [3/7] .git junction...
if not exist "%USERPROFILE%\.git-repos" mkdir "%USERPROFILE%\.git-repos"
move "%TARGET%\.git" "%GIT_LOCAL%" >nul 2>&1
if errorlevel 1 (echo   [ERROR] .git move failed & move "%TARGET%" "%SOURCE%" >nul 2>&1 & goto :error)
mklink /J "%TARGET%\.git" "%GIT_LOCAL%" >nul 2>&1
if errorlevel 1 (echo   [ERROR] mklink failed - run as Admin & goto :error)
echo   .git junction OK
echo.

echo [4/7] .omc junction...
if not exist "%USERPROFILE%\.omc-local" mkdir "%USERPROFILE%\.omc-local"
if exist "%TARGET%\.omc" (move "%TARGET%\.omc" "%OMC_LOCAL%" >nul 2>&1) else (if not exist "%OMC_LOCAL%" mkdir "%OMC_LOCAL%")
mklink /J "%TARGET%\.omc" "%OMC_LOCAL%" >nul 2>&1
echo   .omc junction OK
echo.

echo [5/7] .claude junction...
if not exist "%USERPROFILE%\.claude-local" mkdir "%USERPROFILE%\.claude-local"
if exist "%TARGET%\.claude" (move "%TARGET%\.claude" "%CLAUDE_LOCAL%" >nul 2>&1) else (if not exist "%CLAUDE_LOCAL%" mkdir "%CLAUDE_LOCAL%")
mklink /J "%TARGET%\.claude" "%CLAUDE_LOCAL%" >nul 2>&1
echo   .claude junction OK
echo.

echo [6/7] Verify...
cd /d "%TARGET%"
git status --short 2>&1
if errorlevel 128 (echo   [ERROR] Git broken! & goto :error)
echo.
dir /b "%TARGET%\projects\" 2>nul
echo.
fsutil reparsepoint query "%TARGET%\.git" >nul 2>&1 && (echo   .git: junction OK) || (echo   .git: WARN)
fsutil reparsepoint query "%TARGET%\.omc" >nul 2>&1 && (echo   .omc: junction OK) || (echo   .omc: WARN)
fsutil reparsepoint query "%TARGET%\.claude" >nul 2>&1 && (echo   .claude: junction OK) || (echo   .claude: WARN)
echo.

echo [7/7] Desktop settings backup...
set "BACKUP=%TARGET%\.desktop-setup\user-settings-backup"
if not exist "%TARGET%\.desktop-setup" mkdir "%TARGET%\.desktop-setup"
if not exist "%BACKUP%" mkdir "%BACKUP%"
if exist "%USERPROFILE%\.claude\skills" (xcopy "%USERPROFILE%\.claude\skills" "%BACKUP%\skills\" /E /I /Y /Q >nul 2>&1 & echo   skills OK)
if exist "%USERPROFILE%\.claude\settings.json" (copy "%USERPROFILE%\.claude\settings.json" "%BACKUP%\" /Y >nul 2>&1 & echo   settings.json OK)
if exist "%USERPROFILE%\.claude\commands" (xcopy "%USERPROFILE%\.claude\commands" "%BACKUP%\commands\" /E /I /Y /Q >nul 2>&1 & echo   commands OK)
if exist "%USERPROFILE%\.claude\CLAUDE.md" (copy "%USERPROFILE%\.claude\CLAUDE.md" "%BACKUP%\" /Y >nul 2>&1 & echo   CLAUDE.md OK)
if exist "%USERPROFILE%\.claude\plugins" (xcopy "%USERPROFILE%\.claude\plugins" "%BACKUP%\plugins\" /E /I /Y /Q >nul 2>&1 & echo   plugins OK)
if exist "%USERPROFILE%\.claude\.omc-config.json" (copy "%USERPROFILE%\.claude\.omc-config.json" "%BACKUP%\" /Y >nul 2>&1 & echo   omc-config OK)
if exist "%USERPROFILE%\.claude\my-skills-repo" (xcopy "%USERPROFILE%\.claude\my-skills-repo" "%BACKUP%\my-skills-repo\" /E /I /Y /Q >nul 2>&1 & echo   my-skills-repo OK)
echo.

echo ========================================
echo   DONE! Location: %TARGET%
echo ========================================
echo.
echo   NOW: Explorer - OneDrive\vrin_AI_hub
echo        Right-click - "Always keep on this device"
echo.
echo   HOME: setup-desktop.cmd double-click
echo.
echo   Claude: cd %TARGET% then claude
echo.
goto :end

:error
echo.
echo   FAILED - check errors above
echo   Try: Run as Administrator
echo.

:end
endlocal
pause
