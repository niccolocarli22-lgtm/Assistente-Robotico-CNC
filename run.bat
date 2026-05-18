@echo off
chcp 65001 > nul
title Assistente Robotico CNC

call venv\Scripts\activate.bat
python main_gui.py
pause
