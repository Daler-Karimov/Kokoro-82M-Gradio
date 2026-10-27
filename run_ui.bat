@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

title Kokoro-82M TTS

REM 1. Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH. Please install Python.
    pause
    exit /b 1
)

REM 2. Create venv if missing
if not exist "venv\Scripts\activate.bat" (
    echo [1/4] Creating virtual environment venv...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM 3. Activate venv
call venv\Scripts\activate.bat

REM 4. Install dependencies
echo [2/4] Checking dependencies...
if exist "wheels" (
    echo Installing dependencies from local wheels ^(offline mode^)...
    pip install --no-index --find-links=wheels -r requirements.txt --quiet
) else (
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
)
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

REM 5. Check model files
echo [3/4] Checking model files...

if not exist "kokoro-v1.0.onnx" (
    if exist "kokoro-v1.0.onnx.part0" (
        echo Assembling kokoro-v1.0.onnx from parts...
        copy /b kokoro-v1.0.onnx.part* kokoro-v1.0.onnx >nul
        if %errorlevel% neq 0 (
            echo [ERROR] Failed to assemble kokoro-v1.0.onnx
            pause
            exit /b 1
        )
    )
)

if not exist "voices-v1.0.bin" (
    echo Downloading voices-v1.0.bin...
    curl -L -o voices-v1.0.bin "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to download voices-v1.0.bin
        pause
        exit /b 1
    )
)

if not exist "kokoro-v1.0.onnx" (
    echo Downloading kokoro-v1.0.onnx...
    curl -L -o kokoro-v1.0.onnx "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to download kokoro-v1.0.onnx
        pause
        exit /b 1
    )
)

REM 6. Launch web UI
echo [4/4] Starting Kokoro Web UI...
python app.py
if %errorlevel% neq 0 (
    echo [ERROR] Application exited with error.
    pause
)
