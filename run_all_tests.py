import unittest
import os
import sys

def run_tests():
    print("\n===== RUNNING ALL TESTS =====\n")
    
    # Add the project root to the path
    sys.path.insert(0, os.path.abspath('.'))
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1) 