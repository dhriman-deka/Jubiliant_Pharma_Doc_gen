"""
Run all tests for the document generation app.
"""
import os
import sys
import subprocess
from pathlib import Path

# Get the directory of this script
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent

def print_header(message):
    """Print a header with the given message."""
    print("\n" + "=" * 80)
    print(f" {message} ".center(80, "="))
    print("=" * 80)

def run_command(command):
    """Run a command and print the output."""
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    if process.stdout:
        print(process.stdout)
    
    if process.stderr:
        print("ERRORS:")
        print(process.stderr)
    
    return process.returncode

def main():
    """Run all tests."""
    print_header("STARTING TEST SUITE")
    
    # 1. Create test documents if they don't exist
    print_header("CREATING TEST DOCUMENTS")
    if not (SCRIPT_DIR / "documents" / "test_proposal.docx").exists():
        run_command(f"python3 {SCRIPT_DIR}/create_test_docx.py")
    
    if not (SCRIPT_DIR / "documents" / "test_document.pdf").exists():
        run_command(f"python3 {SCRIPT_DIR}/create_test_pdf.py")
    
    # 2. Run the mock API tests
    print_header("RUNNING MOCK API TESTS")
    mock_test_result = run_command(f"python3 {SCRIPT_DIR}/run_mock_tests.py")
    
    # 3. Run Streamlit app tests
    print_header("RUNNING STREAMLIT APP TESTS")
    streamlit_test_result = run_command(f"python3 {SCRIPT_DIR}/test_streamlit_app.py")
    
    # 4. Fix any issues
    if mock_test_result != 0 or streamlit_test_result != 0:
        print_header("ATTEMPTING TO FIX TEST ISSUES")
        
        # Try to fix common issues
        if not os.path.exists("app/templates/test_contract.txt"):
            print("Copying test contract to app templates directory...")
            run_command(f"cp {SCRIPT_DIR}/templates/test_contract.txt app/templates/")
        
        # Create necessary directories
        for dir_path in ["app/exports", "app/templates", "tests/output"]:
            if not os.path.exists(dir_path):
                print(f"Creating directory: {dir_path}")
                run_command(f"mkdir -p {dir_path}")
        
        # Add more automatic fixes here if needed
        print("Basic fixes applied. Retrying tests...")
    
    # 5. Verify the fixes
    if mock_test_result != 0:
        print_header("VERIFYING MOCK API TESTS")
        mock_test_result = run_command(f"python3 {SCRIPT_DIR}/run_mock_tests.py")
    
    if streamlit_test_result != 0:
        print_header("VERIFYING STREAMLIT APP TESTS")
        streamlit_test_result = run_command(f"python3 {SCRIPT_DIR}/test_streamlit_app.py")
    
    # 6. Print summary
    print_header("TEST SUMMARY")
    
    all_tests_passed = mock_test_result == 0 and streamlit_test_result == 0
    
    if all_tests_passed:
        print("All tests passed! ✅")
    else:
        if mock_test_result != 0:
            print("❌ Mock API tests failed.")
        if streamlit_test_result != 0:
            print("❌ Streamlit app tests failed.")
    
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 