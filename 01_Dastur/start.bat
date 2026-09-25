@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :fail
if not exist weights\yolox_s.onnx .venv\Scripts\python.exe weights\download.py
if errorlevel 1 goto :fail
.venv\Scripts\python.exe scripts\start.py
exit /b
:fail
pause
exit /b 1
