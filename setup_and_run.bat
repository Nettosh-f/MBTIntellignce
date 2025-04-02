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

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install required packages. Please check your internet connection and try again.
    exit /b 1
)
echo Packages installed successfully.

REM Create .env file with API key
echo Please enter your OpenAI API key:
set /p api_key=
echo OPENAI_API_KEY=!api_key!> .env
echo .env file created with API key.

REM Run the GUI
echo Starting the MBTIntelligence GUI...
python run.py

endlocal