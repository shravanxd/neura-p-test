import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes user code in a restricted namespace exposing only numpy,
    and verifies required functions exist.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['svd_2x2', 'check_svd']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_svd_2x2(svd_func, check_func):
    '''
    Runs test cases for svd_2x2 and validates using check_svd.
    '''
    cases = [
        np.array([[-10, 8], [10, -1]]),
        np.array([[1, 2], [3, 4]])
    ]
    for idx, A in enumerate(cases, 1):
        try:
            U, S, V = svd_func(A)
        except Exception as e:
            print(f"Test case {idx} failed: exception during svd_2x2: {e}")
            sys.exit(1)
        try:
            if not check_func(U, S, V, A):
                print(f"Test case {idx} failed: check_svd returned False for input {A}")
                sys.exit(1)
        except Exception as e:
            print(f"Test case {idx} failed: exception during check_svd: {e}")
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
    svd_2x2 = module['svd_2x2']
    check_svd = module['check_svd']

    test_svd_2x2(svd_2x2, check_svd)
    print('All svd_2x2 tests passed.')
