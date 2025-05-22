import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes user's code in an isolated namespace exposing only numpy,
    and verifies the required function exists.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['linear_regression_normal_equation']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_linear_regression_normal_equation(func):
    '''
    Runs test cases for linear_regression_normal_equation.
    '''
    cases = [
        (
            [[1, 1], [1, 2], [1, 3]],
            [1, 2, 3],
            [-0.0, 1.0]
        ),
        (
            [[1, 3, 4], [1, 2, 5], [1, 3, 2]],
            [1, 2, 1],
            [4.0, -1.0, -0.0]
        )
    ]
    for idx, (X, y, expected) in enumerate(cases, 1):
        try:
            result = func(X, y)
        except Exception as e:
            print(f"Test case {idx} failed: exception during linear_regression_normal_equation: {e}")
            sys.exit(1)
        if result != expected:
            print(f"Test case {idx} failed: expected {expected}, got {result}")
            sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python solution.py <user_code_file>')
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, 'r') as f:
            usercode = f.read()
    except Exception as e:
        print(f"Error reading user code file: {e}")
        sys.exit(1)

    module = load_user_module(usercode)
    func = module['linear_regression_normal_equation']
    test_linear_regression_normal_equation(func)
    print('All linear_regression_normal_equation tests passed.')
