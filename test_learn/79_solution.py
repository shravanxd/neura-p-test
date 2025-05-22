import sys
import math


def load_user_module(usercode):
    '''
    Executes user code in an isolated namespace exposing only math,
    and verifies binomial_probability is defined.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'math': math}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['binomial_probability']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_binomial_probability(func):
    '''
    Runs test cases for the Binomial probability function.
    '''
    cases = [
        # (n, k, p, expected)
        (6, 2, 0.5, 0.23438),  # test case 1
        (6, 4, 0.7, 0.32413),  # test case 2
        (3, 3, 0.9, 0.729),    # test case 3
        (5, 0, 0.3, 0.16807),  # test case 4
        (7, 2, 0.1, 0.12106)   # test case 5
    ]
    for idx, (n, k, p, expected) in enumerate(cases, 1):
        try:
            result = func(n, k, p)
        except Exception as e:
            print(f"Test case {idx} failed: exception during binomial_probability({n}, {k}, {p}): {e}")
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
    binomial_probability = module['binomial_probability']
    test_binomial_probability(binomial_probability)
    print('All Binomial distribution tests passed.')
