@echo off
set PROJECT_PATH="C:\Veci\programming\python-utils"

call %PROJECT_PATH%\venv\Scripts\activate

python %PROJECT_PATH%\python-utils.py %PROJECT_PATH% %*

call deactivate