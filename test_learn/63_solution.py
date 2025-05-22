import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes the user's code in a restricted namespace exposing only numpy,
    and verifies required functions exist.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['conjugate_gradient', 'residual', 'alpha', 'beta']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_conjugate_gradient(func):
    '''
    Runs test cases for conjugate_gradient.
    '''
    cases = []
    # Case 1
    A1 = np.array([[4, 1], [1, 3]])
    b1 = np.array([1, 2])
    expected1 = np.array([0.09090909, 0.63636364])
    cases.append((A1, b1, 5, expected1))
    # Case 2
    A2 = np.array([[4, 1, 2], [1, 3, 0], [2, 0, 5]])
    b2 = np.array([7, 8, 5])
    expected2 = np.array([1.2627451, 1.44313725, 0.90196078])
    cases.append((A2, b2, 1, expected2))
    # Case 3
    A3 = np.array([[6,2,1,1,0],[2,5,2,1,1],[1,2,6,1,2],[1,1,1,7,1],[0,1,2,1,8]])
    b3 = np.array([1,2,3,4,5])
    expected3 = np.array([0.01666667,0.11666667,0.21666667,0.45,0.5])
    cases.append((A3, b3, 100, expected3))

    for idx, (A, b, n, expected) in enumerate(cases, 1):
        try:
            result = func(A, b, n)
        except Exception as e:
            print(f"Test case {idx} failed: exception during conjugate_gradient: {e}")
            sys.exit(1)
        if not np.allclose(result, expected, atol=1e-2):
            print(f"Test case {idx} failed: expected {expected}, got {result}")
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python solution.py <user_code_file>')
        sys.exit(1)

    path = sys.argv[1]
    try:
        usercode = open(path).read()
    except Exception as e:
        print(f"Error reading user code file: {e}")
        sys.exit(1)

    module = load_user_module(usercode)
    conjugate_gradient = module['conjugate_gradient']
    test_conjugate_gradient(conjugate_gradient)
    print('All Conjugate Gradient tests passed.')
