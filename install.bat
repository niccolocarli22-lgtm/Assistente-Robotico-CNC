@echo off
chcp 65001 > nul
title Installazione Assistente Robotico CNC

echo.
echo ========================================================
echo    INSTALLAZIONE ASSISTENTE ROBOTICO CNC
echo ========================================================
echo.

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato. Installalo da python.org con "Add to PATH"
    pause
    exit
)

if not exist venv (
    echo Creazione ambiente virtuale...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installazione pacchetti...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ INSTALLAZIONE TERMINATA CON SUCCESSO!
echo.
echo Ora esegui run.bat per avviare il programma.
pause
