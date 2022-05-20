
set PROJECT_PATH="C:\Veci\programming\python-utils"

cd %PROJECT_PATH%

call %PROJECT_PATH%\venv\Scripts\activate

cd rust_toolkit

maturin build -r

cd %PROJECT_PATH%

xcopy %PROJECT_PATH%\rust_toolkit\target\wheels\rust_toolkit-0.1.0-cp39-none-win_amd64.whl %PROJECT_PATH%\rust_toolkit\rust_lib\rust_toolkit-0.1.0-cp39-none-win_amd64.whl /Y

pip uninstall -y rust_toolkit

poetry install