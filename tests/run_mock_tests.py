"""
Test script that uses the mock Gemini API to test the application.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import mock API utilities
from tests.mock_gemini_api import apply_mocks, restore_mocks

# Apply mocks
print("Applying mock API implementations...")
originals = apply_mocks()

try:
    # Now import the test functionality
    from tests.test_app_functionality import run_tests
    
    # Run the tests
    run_tests()
    
finally:
    # Restore original implementations
    print("\nRestoring original API implementations...")
    restore_mocks(originals)
    print("Mock testing complete.") 