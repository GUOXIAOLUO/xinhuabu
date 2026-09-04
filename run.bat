@echo off
cd /d "%~dp0"

set "PYEXE=%~dp0python\python.exe"
if not exist "%PYEXE%" set "PYEXE=python"
if not defined WORKBENCH_HOST set "WORKBENCH_HOST=127.0.0.1"
if not defined WORKBENCH_PORT set "WORKBENCH_PORT=3000"

echo Starting ComfyUI-API-Modelscope...
echo Visit: http://127.0.0.1:%WORKBENCH_PORT%/
echo LAN is disabled by default. For a trusted network: set WORKBENCH_HOST=0.0.0.0
echo Press Ctrl+C to stop.
echo.

start /b cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:%WORKBENCH_PORT%/"
"%PYEXE%" main.py

echo.
echo Server stopped.
pause
