@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0SoDDev.ps1" %*
exit /b %ERRORLEVEL%
