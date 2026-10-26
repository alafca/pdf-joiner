@echo off
setlocal
cd /d "%~dp0"

if not exist .venv (
    echo Creating virtual environment...
    REM Use standard CPython (py launcher), not Anaconda's python — Anaconda's
    REM tkinter layout breaks PyInstaller's _tkinter DLL bundling.
    py -3 -m venv .venv
    if errorlevel 1 (
        echo Falling back to 'python' on PATH...
        python -m venv .venv
    )
    if errorlevel 1 goto :fail
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 goto :fail

if exist build rmdir /s /q build
if exist "dist\PDF Joiner.exe" del /q "dist\PDF Joiner.exe"

pyinstaller --noconfirm --onefile --windowed ^
    --name "PDF Joiner" ^
    --collect-all tkinterdnd2 ^
    pdf_joiner.py
if errorlevel 1 goto :fail

echo.
echo ============================================
echo Build complete.
echo Executable: dist\PDF Joiner.exe
echo ============================================
goto :eof

:fail
echo.
echo Build failed.
exit /b 1
