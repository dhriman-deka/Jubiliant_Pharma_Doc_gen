#!/usr/bin/env python3
"""
Script to run the Document Generation App.
Checks the environment first to ensure all requirements are met.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_environment():
    """Check if all the required modules are installed."""
    required_modules = [
        ("streamlit", "streamlit"),
        ("PyPDF2", "PyPDF2"),
        ("docx", "python-docx"),
        ("dotenv", "python-dotenv"),
        ("google.generativeai", "google-generativeai"),
        ("reportlab", "reportlab"),
        ("PIL", "pillow")
    ]
    
    missing_modules = []
    
    for module_name, pip_name in required_modules:
        try:
            __import__(module_name)
            print(f"✓ {pip_name} is installed")
        except ImportError:
            missing_modules.append(pip_name)
            print(f"✗ {pip_name} is missing")
    
    if missing_modules:
        print(f"Missing required modules: {', '.join(missing_modules)}")
        print("Please install them with: pip install " + " ".join(missing_modules))
        return False
    
    return True

def check_paths():
    """Check if all necessary directories exist."""
    required_dirs = [
        "app",
        "app/utils",
        "app/templates",
        "app/exports"
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"Creating directory: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
    
    # Check for API module existence
    api_file_exists = os.path.exists("app/utils/api.py")
    gemini_api_file_exists = os.path.exists("app/utils/gemini_api.py")
    
    if not api_file_exists and not gemini_api_file_exists:
        print("Warning: Neither app/utils/api.py nor app/utils/gemini_api.py exist.")
        print("The app may not function correctly without an API module.")
        return False
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("Warning: .env file not found.")
        print("Creating a sample .env file, please update it with your API key.")
        with open(".env", "w") as f:
            f.write("GEMINI_API_KEY=your_api_key_here\n")
    
    return True

def run_app():
    """Run the Streamlit app."""
    print("Starting Document Generation App...")
    
    # Setup the Python path to ensure imports work correctly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)  # Add to the beginning of the path
        
    print(f"Current directory: {current_dir}")
    print(f"Python path: {sys.path}")
    
    # Create any necessary __init__.py files
    if not os.path.exists("app/__init__.py"):
        print("Creating app/__init__.py")
        with open("app/__init__.py", "w") as f:
            f.write("# Make app a package\n")
            
    if not os.path.exists("app/utils/__init__.py"):
        print("Creating app/utils/__init__.py")
        with open("app/utils/__init__.py", "w") as f:
            f.write("# Make utils a package\n")
    
    # Run the app with streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running app: {e}")
        return False
    except KeyboardInterrupt:
        print("\nApp stopped by user.")
    
    return True

if __name__ == "__main__":
    print("Document Generation App Launcher")
    print("--------------------------------")
    
    if not check_environment():
        print("Environment check failed. Please install the required modules.")
        sys.exit(1)
    
    if not check_paths():
        print("Warning: Some required paths are missing. The app may not function correctly.")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(1)
    
    # Run the app
    if not run_app():
        print("Failed to run the app.")
        sys.exit(1) 