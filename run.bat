@echo off
set PYTHONPATH=%~dp0

if not exist ".venv\Scripts\activate.bat" (
    py -m venv .venv
    
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r src\requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

python src\main.py

pause