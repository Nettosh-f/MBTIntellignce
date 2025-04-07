@echo off
setlocal enabledelayedexpansion

echo Welcome to MBTIntelligence installation and setup!

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)
echo Python is installed.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment. Please check your Python installation and try again.
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment. Please check your Python installation and try again.
    exit /b 1
)
echo Virtual environment activated.

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install required packages. Please check your internet connection and try again.
    call venv\Scripts\deactivate
    exit /b 1
)
echo Packages installed successfully.

REM Create .env file with API key only if it doesn't exist
if not exist ".env" (
    echo .env file not found. Creating new .env file.
    echo Please enter your OpenAI API key:
    set /p api_key=
    echo OPENAI_API_KEY=!api_key!> .env
    echo .env file created with API key.
) else (
    echo .env file already exists. Skipping API key input.
)

REM Create input and output folders
if not exist "input" mkdir input
if not exist "output" mkdir output

REM Run the GUI
echo Starting the MBTIntelligence GUI...
python run.py

REM Deactivate virtual environment
call venv\Scripts\deactivate

endlocal