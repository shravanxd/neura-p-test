import sys
import math


def load_user_module(usercode):
    '''
    Executes user code in an isolated namespace and verifies poisson_probability is defined.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'math': math}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['poisson_probability']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_poisson_probability(func):
    '''
    Runs test cases for the Poisson probability function.
    '''
    cases = [
        # (k, lambda, expected)
        (3, 5, 0.14037),  # test case 1
        (0, 5, 0.00674),  # test case 2
        (2, 10, 0.00045), # test case 3
        (1, 1, 0.36788),  # test case 4
        (20, 20, 0.08505) # test case 5
    ]
    for idx, (k, lam, expected) in enumerate(cases, 1):
        try:
            result = func(k, lam)
        except Exception as e:
            print(f"Test case {idx} failed: exception during poisson_probability({k}, {lam}): {e}")
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
    poisson_probability = module['poisson_probability']
    test_poisson_probability(poisson_probability)
    print('All Poisson distribution tests passed.')
