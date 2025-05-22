import sys
import re


def load_user_module(usercode):
    '''
    Executes user's code in an isolated namespace and verifies required function exists.
    '''
    exec_globals = {}
    try:
        exec(usercode, {}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['calculate_eigenvalues']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_calculate_eigenvalues(func):
    '''
    Runs test cases for calculate_eigenvalues on 2x2 matrices.
    '''
    cases = [
        ([[2, 1], [1, 2]], [3.0, 1.0]),
        ([[4, -2], [1, 1]], [3.0, 2.0]),
    ]

    for idx, (matrix, expected) in enumerate(cases, 1):
        try:
            result = func(matrix)
        except Exception as e:
            print(f"Test case {idx} failed: exception during calculate_eigenvalues: {e}")
            sys.exit(1)
        if result != expected:
            print(f"Test case {idx} failed: expected {expected}, got {result}")
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
    calculate_eigenvalues = module['calculate_eigenvalues']
    test_calculate_eigenvalues(calculate_eigenvalues)
    print('All calculate_eigenvalues tests passed.')
