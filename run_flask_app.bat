@echo off
cd /d "%~dp0"

echo Installing Flask...
python -m pip install Flask

start "" cmd /c "timeout /t 2 >nul && start http://127.0.0.1:5000"

python backend.py

pause