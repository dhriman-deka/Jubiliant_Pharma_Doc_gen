"""
Check if the environment is properly set up for the application.
"""
import os
import sys
import subprocess
from pathlib import Path

def print_status(message, success):
    """Print a status message with appropriate emoji."""
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")
    return success

def check_package_installed(package_name):
    """Check if a Python package is installed."""
    try:
        # Use pip to check if the package is installed
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True, text=True
        )
        return print_status(f"Package '{package_name}' is installed", result.returncode == 0)
    except Exception as e:
        return print_status(f"Package '{package_name}' check failed: {str(e)}", False)

def check_file_exists(file_path, required=True):
    """Check if a file exists."""
    exists = os.path.exists(file_path)
    status_msg = f"File '{file_path}'" + (" exists" if exists else " does NOT exist")
    if not exists and not required:
        status_msg += " (optional)"
    return print_status(status_msg, exists or not required)

def check_env_variable(var_name, required=True):
    """Check if an environment variable is set."""
    exists = var_name in os.environ
    status_msg = f"Environment variable '{var_name}'" + (" is set" if exists else " is NOT set")
    if not exists and not required:
        status_msg += " (optional)"
    return print_status(status_msg, exists or not required)

def check_directory_structure():
    """Check if the required directory structure exists."""
    required_dirs = [
        "app",
        "app/templates",
        "app/utils",
        "app/exports"
    ]
    
    all_dirs_exist = True
    for dir_path in required_dirs:
        exists = os.path.isdir(dir_path)
        if not exists:
            all_dirs_exist = False
        print_status(f"Directory '{dir_path}' exists", exists)
    
    return all_dirs_exist

def check_requirements():
    """Check if all required packages from requirements.txt are installed."""
    required_packages = [
        "streamlit",
        "google-generativeai",
        "PyPDF2",
        "python-docx",
        "reportlab",
        "python-dotenv",
        "Pillow"
    ]
    
    all_installed = True
    for package in required_packages:
        if not check_package_installed(package):
            all_installed = False
    
    return all_installed

def check_api_key():
    """Check if the Gemini API key is available."""
    # Check for .env file
    env_file_exists = check_file_exists(".env", required=False)
    
    # Check for environment variable
    api_key_set = check_env_variable("GEMINI_API_KEY", required=False)
    
    # If neither exists, suggest creating .env file
    if not env_file_exists and not api_key_set:
        print("\nSuggestion: Create a .env file with your Gemini API key:")
        print("echo 'GEMINI_API_KEY=your_api_key_here' > .env")
    
    return env_file_exists or api_key_set

def main():
    """Run all environment checks."""
    print("\n" + "=" * 80)
    print(" ENVIRONMENT CHECK ".center(80, "="))
    print("=" * 80 + "\n")
    
    # Check directory structure
    print("Checking directory structure...")
    dir_check = check_directory_structure()
    print()
    
    # Check required packages
    print("Checking required packages...")
    pkg_check = check_requirements()
    print()
    
    # Check required files
    print("Checking required files...")
    files_check = True
    files_check &= check_file_exists("app.py")
    files_check &= check_file_exists("requirements.txt")
    files_check &= check_file_exists("app/utils/gemini_api.py")
    files_check &= check_file_exists("app/utils/document_processor.py")
    files_check &= check_file_exists("app/utils/template_manager.py")
    print()
    
    # Check API key
    print("Checking API key setup...")
    api_check = check_api_key()
    print()
    
    # Print summary
    print("\n" + "=" * 80)
    print(" ENVIRONMENT CHECK SUMMARY ".center(80, "="))
    print("=" * 80 + "\n")
    
    all_checks_passed = dir_check and pkg_check and files_check
    
    if all_checks_passed:
        if api_check:
            print("✅ All checks passed! The environment is properly set up.")
        else:
            print("⚠️ Basic checks passed, but the API key is not set up.")
            print("   The app will run but AI features won't work without the API key.")
    else:
        print("❌ Some checks failed. Please address the issues above.")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 