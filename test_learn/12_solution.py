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

    required = ['svd_2x2_singular_values']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_svd_2x2_singular_values(func):
    '''
    Run test cases on svd_2x2_singular_values: check singular values are ordered descending
    and that U @ diag(s) @ Vt reconstructs A.
    '''
    # Case 1: diagonal matrix [3,4]
    A = np.diag([3.0, 4.0])
    u, s, vt = func(A)
    if not (isinstance(s, np.ndarray) and s.shape == (2,)):  # s should be length-2 array
        print(f"Test 1 failed: singular values s has wrong shape {getattr(s,'shape',None)}")
        sys.exit(1)
    if not s[0] >= s[1]:
        print(f"Test 1 failed: singular values not descending {s}")
        sys.exit(1)
    recon = u @ np.diag(s) @ vt
    if not np.allclose(recon, A, atol=1e-6):
        print(f"Test 1 failed: reconstruction {recon} != {A}")
        sys.exit(1)

    # Case 2: general matrix
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    u, s, vt = func(A)
    recon = u @ np.diag(s) @ vt
    if not np.allclose(recon, A, atol=1e-6):
        print(f"Test 2 failed: reconstruction {recon} != {A}")
        sys.exit(1)

    # Case 3: swap matrix
    A = np.array([[0.0, 1.0], [1.0, 0.0]])
    u, s, vt = func(A)
    recon = u @ np.diag(s) @ vt
    if not np.allclose(recon, A, atol=1e-6):
        print(f"Test 3 failed: reconstruction {recon} != {A}")
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
    func = module['svd_2x2_singular_values']
    test_svd_2x2_singular_values(func)
    print('All svd_2x2_singular_values tests passed.')
