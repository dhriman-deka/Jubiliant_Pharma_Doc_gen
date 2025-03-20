import os
import sys
import importlib.util
import subprocess
from pathlib import Path

def check_package(package_name):
    """Check if a package is installed using multiple methods."""
    # Method 1: Try to find the spec
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is not None:
            return True
    except (ImportError, AttributeError):
        pass
    
    # Method 2: Try to import the package
    try:
        __import__(package_name)
        return True
    except ImportError:
        pass
    
    # Method 3: Use pip to check if package is installed
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        pass
    
    return False

def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)

def check_environment():
    """Check if the environment is properly set up."""
    print("\n===== ENVIRONMENT CHECK =====\n")
    
    # Check required packages
    required_packages = [
        "streamlit",
        "PyPDF2",
        "python-docx",
        "python-dotenv",
        "google.generativeai",
        "reportlab",
        "Pillow"
    ]
    
    all_packages_installed = True
    missing_packages = []
    
    # Map package names to import names
    package_imports = {
        "streamlit": "streamlit",
        "PyPDF2": "PyPDF2",
        "python-docx": "docx",
        "python-dotenv": "dotenv",
        "google.generativeai": "google.generativeai",
        "reportlab": "reportlab",
        "Pillow": "PIL"
    }
    
    for package in required_packages:
        # Use the appropriate import name
        import_name = package_imports.get(package, package)
        
        is_installed = check_package(import_name)
        if is_installed:
            print(f"✅ Package {package} is installed")
        else:
            print(f"❌ Package {package} is missing")
            all_packages_installed = False
            missing_packages.append(package)
    
    # Check required files
    required_files = [
        "app.py",
        "app/utils/gemini_api.py",
        "app/utils/document_processor.py",
        "app/utils/template_manager.py",
        "app/templates/business_letter.txt",
        "app/templates/invoice.txt",
        ".env.example"
    ]
    
    all_files_exist = True
    missing_files = []
    
    for file_path in required_files:
        if check_file_exists(file_path):
            print(f"✅ File {file_path} exists")
        else:
            print(f"❌ File {file_path} is missing")
            all_files_exist = False
            missing_files.append(file_path)
    
    # Check if the app directory structure is correct
    directories = [
        "app",
        "app/utils",
        "app/templates",
        "app/exports",
        "tests"
    ]
    
    all_directories_exist = True
    missing_directories = []
    
    for directory in directories:
        if os.path.isdir(directory):
            print(f"✅ Directory {directory} exists")
        else:
            print(f"❌ Directory {directory} is missing")
            all_directories_exist = False
            missing_directories.append(directory)
    
    # Print summary
    print("\n===== SUMMARY =====\n")
    
    if all_packages_installed and all_files_exist and all_directories_exist:
        print("✅ Environment is properly set up!")
        return True
    else:
        if not all_packages_installed:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("To install missing packages, run:")
            print(f"pip install {' '.join(missing_packages)}")
        
        if not all_files_exist:
            print(f"❌ Missing files: {', '.join(missing_files)}")
        
        if not all_directories_exist:
            print(f"❌ Missing directories: {', '.join(missing_directories)}")
            print("To create missing directories, run:")
            for directory in missing_directories:
                print(f"mkdir -p {directory}")
        
        return False

if __name__ == "__main__":
    success = check_environment()
    if not success:
        sys.exit(1) 