import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes the user's code in a restricted namespace exposing only numpy,
    and verifies the required function exists.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['rref']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_rref(func):
    '''
    Runs test cases for the rref function.
    '''
    cases = []
    # Test case 1
    A1 = np.array([
        [1, 2, -1, -4],
        [2, 3, -1, -11],
        [-2, 0, -3, 22]
    ], dtype=float)
    E1 = np.array([
        [1., 0.,  0., -8.],
        [0., 1.,  0.,  1.],
        [0., 0.,  1., -2.]
    ], dtype=float)
    cases.append((A1, E1))

    # Test case 2
    A2 = np.array([
        [2, 4, -2],
        [4, 9, -3],
        [-2, -3, 7]
    ], dtype=float)
    E2 = np.eye(3)
    cases.append((A2, E2))

    # Test case 3
    A3 = np.array([
        [0,  2, -1, -4],
        [2,  0, -1, -11],
        [-2, 0,  0, 22]
    ], dtype=float)
    E3 = np.array([
        [1., 0., 0., -11.],
        [0., 1., 0., -7.5],
        [0., 0., 1., -11.]
    ], dtype=float)
    cases.append((A3, E3))

    # Test case 4
    A4 = np.array([
        [1, 2, -1],
        [2, 4, -1],
        [-2, -4, -3]
    ], dtype=float)
    E4 = np.array([
        [1., 2.,  0.],
        [0., 0.,  0.],
        [0., 0.,  1.]
    ], dtype=float)
    cases.append((A4, E4))

    for idx, (A, expected) in enumerate(cases, 1):
        try:
            # work on a copy to avoid in-place modifications affecting future tests
            result = func(A.copy())
        except Exception as e:
            print(f"Test case {idx} failed: exception during rref: {e}")
            sys.exit(1)
        if not np.allclose(result, expected, atol=1e-4):
            print(f"Test case {idx} failed: expected\n{expected}\ngot\n{result}")
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python solution.py <user_code_file>')
        sys.exit(1)

    path = sys.argv[1]
    try:
        usercode = open(path, 'r').read()
    except Exception as e:
        print(f"Error reading user code file: {e}")
        sys.exit(1)

    module = load_user_module(usercode)
    rref = module['rref']
    test_rref(rref)
    print('All rref tests passed.')
