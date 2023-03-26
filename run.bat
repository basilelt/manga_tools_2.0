@echo off
CLS

cd /D "%~dp0"

:start
python mango.py
goto start