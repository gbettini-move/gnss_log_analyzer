@echo off

setlocal ENABLEDELAYEDEXPANSION

set VENV_DIR=.venv
set PROGRAM_NAME=log_analyzer

REM ---- Checking python ----
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found in the PATH
    echo Install Python and retry
    exit /b 1
)

REM ---- Creating virtual environment ----
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment in %VENV_DIR%...
    python -m venv %VENV_DIR%
) else (
    echo Virtual environment already exists
)

REM ---- Activating venv ----
call %VENV_DIR%\Scripts\activate.bat

REM ---- Checking uv ----
python -m pip show uv >nul 2>&1
if errorlevel 1 (
    echo uv not found, proceeding with installation...
    python -m pip install uv
) else (
    echo uv already present in the virtual environment
)

echo.

REM ---- Sync dependencies ----
echo Synchronizing dependencies (uv sync)...
uv sync

REM If dev dependencies needed [dependency-groups], uncomment the following line
REM uv sync --group dev

REM ---- Checking %PROGRAM_NAME%.py ----
if not exist "%PROGRAM_NAME%.py" (
    echo File %PROGRAM_NAME% not founded
    exit /b 1
)

REM ---- Launching the application ----
echo ...
uv run python %PROGRAM_NAME%.py

endlocal