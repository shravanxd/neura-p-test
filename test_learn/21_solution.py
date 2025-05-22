import sys
import numpy as np


def load_user_module(usercode):
    '''
    Execute user's code in a restricted namespace exposing only numpy,
    and verify required functions exist.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['linear_kernel', 'rbf_kernel', 'pegasos_kernel_svm']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_pegasos_kernel_svm(func):
    '''
    Runs test cases for pegasos_kernel_svm using linear and RBF kernels.
    '''
    data = np.array([[1, 2], [2, 3], [3, 1], [4, 1]])
    labels = np.array([1, 1, -1, -1])

    # Test case 1: Linear kernel
    expected1 = ([100.0, 0.0, -100.0, -100.0], -937.4755)
    try:
        result1 = func(data, labels, kernel='linear', lambda_val=0.01, iterations=100)
    except Exception as e:
        print(f"Test case 1 failed: exception during pegasos_kernel_svm (linear): {e}")
        sys.exit(1)
    if result1 != expected1:
        print(f"Test case 1 failed: expected {expected1}, got {result1}")
        sys.exit(1)

    # Test case 2: RBF kernel
    expected2 = ([100.0, 99.0, -100.0, -100.0], -115.0)
    try:
        result2 = func(data, labels, kernel='rbf', lambda_val=0.01, iterations=100, sigma=0.5)
    except Exception as e:
        print(f"Test case 2 failed: exception during pegasos_kernel_svm (rbf): {e}")
        sys.exit(1)
    if result2 != expected2:
        print(f"Test case 2 failed: expected {expected2}, got {result2}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python solution.py <user_code_file>')
        sys.exit(1)

    user_file = sys.argv[1]
    try:
        with open(user_file, 'r') as f:
            usercode = f.read()
    except Exception as e:
        print(f"Error reading user code file: {e}")
        sys.exit(1)

    module = load_user_module(usercode)
    pegasos_kernel_svm = module['pegasos_kernel_svm']
    test_pegasos_kernel_svm(pegasos_kernel_svm)
    print('All pegasos_kernel_svm tests passed.')
