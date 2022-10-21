@echo off
:: Change this to the path where you installed python-windows-utils
set PROJECT_PATH="C:\python-windows-utils"
:: ---------------------------------------------------------------
call %PROJECT_PATH%\venv\Scripts\activate

python %PROJECT_PATH%\python-utils.py %PROJECT_PATH%

call deactivate