#!/bin/bash

# Document Generation App Installation Script

echo "===== Installing Document Generation App ====="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "Setting up directory structure..."
mkdir -p app/exports
mkdir -p app/templates
mkdir -p app/utils
mkdir -p tests

# Check if API files exist
if [ ! -f "app/utils/api.py" ] && [ ! -f "app/utils/gemini_api.py" ]; then
    echo "⚠️ Warning: Missing API implementation files."
    echo "Please ensure that either app/utils/api.py or app/utils/gemini_api.py exists."
fi

# Set up environment file example if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from example"
        echo "⚠️ Please update the API key in the .env file before running the app."
    else
        echo "GEMINI_API_KEY=your_api_key_here" > .env
        echo "✅ Created basic .env file"
        echo "⚠️ Please update the API key in the .env file before running the app."
    fi
fi

echo "===== Installation Complete ====="
echo "To run the app, execute:"
echo "source venv/bin/activate"
echo "python run_app.py" 