import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes user code in an isolated namespace exposing only numpy,
    and verifies descriptive_statistics is defined.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['descriptive_statistics']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_descriptive_statistics(func):
    '''
    Runs test cases for descriptive_statistics function.
    '''
    cases = [
        (
            [10, 20, 30, 40, 50],
            {
                "mean": 30.0,
                "median": 30.0,
                "mode": 10,
                "variance": 200.0,
                "standard_deviation": 14.142135623730951,
                "25th_percentile": 20.0,
                "50th_percentile": 30.0,
                "75th_percentile": 40.0,
                "interquartile_range": 20.0
            }
        ),
        (
            [1, 2, 2, 3, 4, 4, 4, 5],
            {
                "mean": 3.125,
                "median": 3.5,
                "mode": 4,
                "variance": 1.609375,
                "standard_deviation": 1.268857754044952,
                "25th_percentile": 2.0,
                "50th_percentile": 3.5,
                "75th_percentile": 4.0,
                "interquartile_range": 2.0
            }
        ),
        (
            [100],
            {
                "mean": 100.0,
                "median": 100.0,
                "mode": 100,
                "variance": 0.0,
                "standard_deviation": 0.0,
                "25th_percentile": 100.0,
                "50th_percentile": 100.0,
                "75th_percentile": 100.0,
                "interquartile_range": 0.0
            }
        )
    ]

    for idx, (data, expected) in enumerate(cases, 1):
        try:
            result = func(data)
        except Exception as e:
            print(f"Test case {idx} failed: exception during descriptive_statistics: {e}")
            sys.exit(1)
        for key, exp_val in expected.items():
            res_val = result.get(key)
            if not np.isclose(res_val, exp_val, atol=1e-5):
                print(f"Test case {idx} failed: for '{key}', expected {exp_val}, got {res_val}")
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
    descriptive_statistics = module['descriptive_statistics']
    test_descriptive_statistics(descriptive_statistics)
    print('All descriptive_statistics tests passed.')
