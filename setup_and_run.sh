#!/bin/bash
echo "Welcome to MBTIntelligence installation and setup!"
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi
echo "Python is installed."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please check your Python installation and try again."
        exit 1
    fi
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment. Please check your Python installation and try again."
    exit 1
fi
echo "Virtual environment activated."
echo "Installing required packages..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install required packages. Please check your internet connection and try again."
    deactivate
    exit 1
fi
echo "Packages installed successfully."
if [ ! -f ".env" ]; then
    echo ".env file not found. Creating new .env file."
    echo "Please enter your OpenAI API key:"
    read api_key
    echo "OPENAI_API_KEY=$api_key" > .env
    echo ".env file created with API key."
else
    echo ".env file already exists. Skipping API key input."
fi
mkdir -p input output
echo "Starting the MBTIntelligence GUI..."
python3 run.py
deactivate
echo "Setup complete and application closed."