import sys


def load_user_module(usercode):
    '''
    Executes user code in an isolated namespace and verifies calculate_covariance_matrix is defined.
    '''
    exec_globals = {}
    try:
        exec(usercode, {}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['calculate_covariance_matrix']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_calculate_covariance_matrix(func):
    '''
    Runs test cases for calculate_covariance_matrix.
    '''
    cases = [
        (
            [[1, 2, 3], [4, 5, 6]],
            [[1.0, 1.0], [1.0, 1.0]]
        ),
        (
            [[1, 5, 6], [2, 3, 4], [7, 8, 9]],
            [[7.0, 2.5, 2.5], [2.5, 1.0, 1.0], [2.5, 1.0, 1.0]]
        )
    ]
    for idx, (vectors, expected) in enumerate(cases, 1):
        try:
            result = func(vectors)
        except Exception as e:
            print(f"Test case {idx} failed: exception during calculate_covariance_matrix: {e}")
            sys.exit(1)
        if result != expected:
            print(f"Test case {idx} failed: expected {expected}, got {result}")
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
    calculate_covariance_matrix = module['calculate_covariance_matrix']
    test_calculate_covariance_matrix(calculate_covariance_matrix)
    print('All calculate_covariance_matrix tests passed.')
