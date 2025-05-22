import sys


def load_user_module(usercode):
    '''
    Executes user code in an isolated namespace and verifies phi_corr is defined.
    '''
    exec_globals = {}
    try:
        exec(usercode, {}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    if 'phi_corr' not in exec_globals:
        print('Missing required function: phi_corr')
        sys.exit(1)

    return exec_globals


def test_phi_corr(func):
    '''
    Runs test cases for the Phi correlation coefficient implementation.
    '''
    cases = [
        ([1,1,0,0], [0,0,1,1], -1),
        ([1,1,0,0], [1,0,1,1], -0.5774)
    ]

    for idx, (x, y, expected) in enumerate(cases, 1):
        try:
            result = func(x, y)
        except Exception as e:
            print(f"Test case {idx} failed: exception during phi_corr: {e}")
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
    phi_corr = module['phi_corr']
    test_phi_corr(phi_corr)
    print('All phi correlation coefficient tests passed.')
