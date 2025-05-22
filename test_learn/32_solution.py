import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes user's code in an isolated namespace exposing only numpy,
    and verifies required function exists.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['polynomial_features']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_polynomial_features(func):
    '''
    Runs test cases for polynomial_features function.
    '''
    cases = [
        # (X, degree, expected_output)
        (
            np.array([[2, 3], [3, 4], [5, 6]]),
            2,
            np.array([
                [1., 2., 3., 4., 6., 9.],
                [1., 3., 4., 9.,12.,16.],
                [1., 5., 6.,25.,30.,36.]
            ])
        ),
        (
            np.array([[1, 2], [3, 4], [5, 6]]),
            3,
            np.array([
                [ 1.,  1.,  2.,  1.,  2.,  4.,  1.,  2.,  4.,  8.],
                [ 1.,  3.,  4.,  9., 12., 16., 27., 36., 48., 64.],
                [ 1.,  5.,  6., 25., 30., 36.,125.,150.,180.,216.]
            ])
        ),
        (
            np.array([[1,2,3],[3,4,5],[5,6,9]]),
            3,
            np.array([
                [  1.,  1.,  2.,  3.,   1.,   2.,   3.,   4.,   6.,   9.,   1.,   2.,   3.,   4.,   6.,   9.,   8.,  12.,  18.,  27.],
                [  1.,  3.,  4.,  5.,   9.,  12.,  15.,  16.,  20.,  25.,  27.,  36.,  45.,  48.,  60.,  75.,  64.,  80., 100., 125.],
                [  1.,  5.,  6.,  9.,  25.,  30.,  45.,  36.,  54.,  81., 125., 150., 225., 180., 270., 405., 216., 324., 486., 729.]
            ])
        )
    ]

    for idx, (X, degree, expected) in enumerate(cases, 1):
        try:
            result = func(X, degree)
        except Exception as e:
            print(f"Test case {idx} failed: exception during polynomial_features: {e}")
            sys.exit(1)
        if not np.allclose(result, expected, atol=1e-4):
            print(f"Test case {idx} failed:\nExpected:\n{expected}\nGot:\n{result}")
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
    func = module['polynomial_features']
    test_polynomial_features(func)
    print('All polynomial_features tests passed.')
