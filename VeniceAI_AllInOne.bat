@echo off
setlocal enabledelayedexpansion
title Venice AI - Complete Setup and Launch
color 0B

set "TEMPLATES_DIR=%~dp0templates"
set "BASE_DIR=%~dp0"

:: File URLs
set "HTML_URL=https://raw.githubusercontent.com/IAVARABBASOV/Venice_AI/refs/heads/main/templates/index.html"
set "APP_URL=https://raw.githubusercontent.com/IAVARABBASOV/Venice_AI/refs/heads/main/app.py"
set "REQ_URL=https://raw.githubusercontent.com/IAVARABBASOV/Venice_AI/refs/heads/main/requirements.txt"
set "START_PY_URL=https://raw.githubusercontent.com/IAVARABBASOV/Venice_AI/refs/heads/main/start.py"
set "START_BAT_URL=https://raw.githubusercontent.com/IAVARABBASOV/Venice_AI/refs/heads/main/start.bat"
set "ICO_FILE_URL=https://raw.githubusercontent.com/IAVARABBASOV/Venice_AI/refs/heads/main/venice-keys-red.ico"

set PYTHON_VERSION=3.11.9
set PYTHON_EMBED_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip
set PYTHON_DIR=%BASE_DIR%\python
set SCRIPTS_DIR=%PYTHON_DIR%\Scripts

if not exist "%TEMPLATES_DIR%" mkdir "%TEMPLATES_DIR%"
if not exist "%PYTHON_DIR%" mkdir "%PYTHON_DIR%"

echo Checking and downloading required files...
echo.

if exist "%TEMPLATES_DIR%\index.html" (
    echo [1/6] index.html already exists, skipping...
) else (
    echo [1/6] Downloading index.html...
    powershell -Command "try { Invoke-WebRequest -Uri '%HTML_URL%' -OutFile '%TEMPLATES_DIR%\index.html' -ErrorAction Stop; exit 0 } catch { exit 1 }"
    if !ERRORLEVEL! NEQ 0 (echo Failed! & goto :error)
)

if exist "%BASE_DIR%app.py" (
    echo [2/6] app.py already exists, skipping...
) else (
    echo [2/6] Downloading app.py...
    powershell -Command "try { Invoke-WebRequest -Uri '%APP_URL%' -OutFile '%BASE_DIR%app.py' -ErrorAction Stop; exit 0 } catch { exit 1 }"
    if !ERRORLEVEL! NEQ 0 (echo Failed! & goto :error)
)

if exist "%BASE_DIR%requirements.txt" (
    echo [3/6] requirements.txt already exists, skipping...
) else (
    echo [3/6] Downloading requirements.txt...
    powershell -Command "try { Invoke-WebRequest -Uri '%REQ_URL%' -OutFile '%BASE_DIR%requirements.txt' -ErrorAction Stop; exit 0 } catch { exit 1 }"
    if !ERRORLEVEL! NEQ 0 (echo Failed! & goto :error)
)

if exist "%BASE_DIR%start.py" (
    echo [4/6] start.py already exists, skipping...
) else (
    echo [4/6] Downloading start.py...
    powershell -Command "try { Invoke-WebRequest -Uri '%START_PY_URL%' -OutFile '%BASE_DIR%start.py' -ErrorAction Stop; exit 0 } catch { exit 1 }"
    if !ERRORLEVEL! NEQ 0 (echo Failed! & goto :error)
)

if exist "%BASE_DIR%start.bat" (
    echo [5/6] start.bat already exists, skipping...
) else (
    echo [5/6] Downloading start.bat...
    powershell -Command "try { Invoke-WebRequest -Uri '%START_BAT_URL%' -OutFile '%BASE_DIR%start.bat' -ErrorAction Stop; exit 0 } catch { exit 1 }"
    if !ERRORLEVEL! NEQ 0 (echo Failed! & goto :error)
)

if exist "%BASE_DIR%venice-keys-red.ico" (
    echo [6/6] venice-keys-red.ico already exists, skipping...
) else (
    echo [6/6] Downloading venice-keys-red.ico...
    powershell -Command "try { Invoke-WebRequest -Uri '%ICO_FILE_URL%' -OutFile '%BASE_DIR%venice-keys-red.ico' -ErrorAction Stop; exit 0 } catch { exit 1 }"
    if !ERRORLEVEL! NEQ 0 (echo Failed! & goto :error)
)

if not exist "%PYTHON_DIR%\python.exe" (
	echo.
	echo ========================================
	echo Step 1: Downloading Python %PYTHON_VERSION% embedded...
	echo ========================================
	powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_EMBED_URL%' -OutFile '%BASE_DIR%\python.zip'}"

	if not exist "%BASE_DIR%\python.zip" (
	    echo ERROR: Failed to download Python embedded
	    pause
	    exit /b 1
	)

	echo.
	echo ========================================
	echo Step 2: Extracting Python
	echo ========================================
	echo Extracting Python to %PYTHON_DIR%...

	powershell -Command "& {Expand-Archive -Path '%BASE_DIR%\python.zip' -DestinationPath '%PYTHON_DIR%' -Force}"
	del "%BASE_DIR%\python.zip"

	echo.
	echo ========================================
	echo Step 3: Configuring Python
	echo ========================================
	echo Configuring Python paths...
	powershell -Command "& {(Get-Content '%PYTHON_DIR%\python311._pth') -replace '#import site', 'import site' | Set-Content '%PYTHON_DIR%\python311._pth'}"
	echo Python installation complete!
    echo.

	echo.
	echo ========================================
	echo Step 4: Installing pip
	echo ========================================
	echo Downloading get-pip.py...

	powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%BASE_DIR%\get-pip.py'}"

	echo Installing pip...
	"%PYTHON_DIR%\python.exe" "%BASE_DIR%\get-pip.py"

	if not exist "%SCRIPTS_DIR%\pip.exe" (
    	echo ERROR: Failed to install pip
    	pause
   	    exit /b 1
	)

	del "%BASE_DIR%\get-pip.py"

	echo.
	echo ========================================
	echo Step 5: Installing Required Packages
	echo ========================================
	echo.
	echo Installing Transformers-based setup == lighter than vLLM
	echo.

	"%PYTHON_DIR%\python.exe" -m pip install --upgrade pip

	echo Installing PyTorch...
	"%PYTHON_DIR%\python.exe" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

	echo Installing Transformers and dependencies...
	"%PYTHON_DIR%\python.exe" -m pip install transformers>=4.36.0 accelerate>=0.25.0

	echo Installing additional packages...
	"%PYTHON_DIR%\python.exe" -m pip install huggingface-hub safetensors sentencepiece protobuf bitsandbytes

) else (
    echo Python already exists, skipping installation...
    echo.
)

echo.
echo Setup complete!
echo Launching start.bat...
echo.

call "%BASE_DIR%start.bat"
exit /b 0

:error
echo.
echo Setup failed!
pause
exit /b 1