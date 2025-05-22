import sys
import re
import numpy as np


def load_user_module(usercode):
    '''
    Execute user code in a restricted namespace exposing only numpy,
    and verify required function exists.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['phi_transform']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_phi_transform(func):
    '''
    Run test cases on the phi_transform function.
    '''
    # Test Case 1: empty data, valid degree
    if func([], 2) != []:
        print(f"Test Case 1 failed: expected [], got {func([], 2)}")
        sys.exit(1)

    # Test Case 2: non-empty data, negative degree
    if func([1.0, 2.0], -1) != []:
        print(f"Test Case 2 failed: expected [], got {func([1.0, 2.0], -1)}")
        sys.exit(1)

    # Test Case 3: two elements, degree 2
    expected3 = [[1.0, 1.0, 1.0], [1.0, 2.0, 4.0]]
    if func([1.0, 2.0], 2) != expected3:
        print(f"Test Case 3 failed: expected {expected3}, got {func([1.0, 2.0], 2)}")
        sys.exit(1)

    # Test Case 4: two elements, degree 3
    expected4 = [[1.0, 1.0, 1.0, 1.0], [1.0, 3.0, 9.0, 27.0]]
    if func([1.0, 3.0], 3) != expected4:
        print(f"Test Case 4 failed: expected {expected4}, got {func([1.0, 3.0], 3)}")
        sys.exit(1)

    # Test Case 5: single element, degree 4
    expected5 = [[1.0, 2.0, 4.0, 8.0, 16.0]]
    if func([2.0], 4) != expected5:
        print(f"Test Case 5 failed: expected {expected5}, got {func([2.0], 4)}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python solution.py <user_code_file>')
        sys.exit(1)

    user_path = sys.argv[1]
    try:
        with open(user_path, 'r') as f:
            usercode = f.read()
    except Exception as e:
        print(f"Error reading user code file: {e}")
        sys.exit(1)

    module = load_user_module(usercode)
    phi_func = module['phi_transform']
    test_phi_transform(phi_func)
    print('All phi_transform tests passed.')
