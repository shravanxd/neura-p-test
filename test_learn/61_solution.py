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

    required = ['f_score']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_f_score(func):
    '''
    Runs test cases for the F-score function (f_score).
    '''
    cases = [
        # (y_true, y_pred, beta, expected_score)
        (np.array([1,0,1,1,0,1]), np.array([1,0,1,0,0,1]), 1, 0.857),
        (np.array([1,0,1,1,0,0]), np.array([1,0,0,0,0,1]), 1, 0.4),
        (np.array([1,0,1,1,0,0]), np.array([1,0,1,1,0,0]), 2, 1.0),
        (np.array([1,0,1,1,0,1]), np.array([0,0,0,1,0,1]), 2, 0.556),
        (np.array([1,0,1,1,0,1]), np.array([0,1,0,0,1,0]), 0.5, 0.0),
        (np.array([1,0,0,1,0,1]), np.array([1,0,1,1,0,0]), 0.5, 0.667),
        (np.array([1,0,1,1,0,1]), np.array([0,1,0,0,1,0]), 3, 0.0),
        (np.array([1,0,0,1,0,1]), np.array([1,0,1,1,0,0]), 0, 0.667),
    ]
    for idx, (y_true, y_pred, beta, expected) in enumerate(cases, 1):
        try:
            result = func(y_true, y_pred, beta)
        except Exception as e:
            print(f"Test case {idx} failed: exception during f_score: {e}")
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
        usercode = open(path, 'r').read()
    except Exception as e:
        print(f"Error reading user code file: {e}")
        sys.exit(1)

    module = load_user_module(usercode)
    f_score = module['f_score']
    test_f_score(f_score)
    print('All F-score tests passed.')
