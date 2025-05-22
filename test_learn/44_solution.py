import sys
import re
import math


def get_function_name(code_string):
    '''
    Extracts the first function name defined in the user code.
    '''
    match = re.search(r'def\s+(\w+)', code_string)
    return match.group(1) if match else None


def load_user_function(usercode):
    '''
    Executes user code in a minimal namespace and returns the user-defined function object.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'math': math}, exec_globals)
    except Exception as e:
        print(f'Error executing user code: {e}')
        sys.exit(1)

    fn_name = get_function_name(usercode)
    if not fn_name or fn_name not in exec_globals:
        print('Could not find a valid function definition in the submitted code.')
        sys.exit(1)

    return exec_globals[fn_name]


def test_leaky_relu(func):
    '''
    Runs test cases against the user-provided leaky_relu function.
    '''
    cases = [
        (0, None, 0, 'Test case 1 failed: leaky_relu(0) should be 0'),
        (1, None, 1, 'Test case 2 failed: leaky_relu(1) should be 1'),
        (-1, None, -0.01, 'Test case 3 failed: leaky_relu(-1) should be -0.01'),
        (-2, 0.1, -0.2, 'Test case 4 failed: leaky_relu(-2, alpha=0.1) should be -0.2'),
    ]
    for z, alpha, expected, err_msg in cases:
        try:
            result = func(z, alpha) if alpha is not None else func(z)
            assert result == expected, f"{err_msg}, got {result}"
        except AssertionError as e:
            print(f'AssertionError: {e}')
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
        print(f'Error reading user code file: {e}')
        sys.exit(1)

    user_func = load_user_function(usercode)
    test_leaky_relu(user_func)
    print('All Leaky ReLU tests passed.')
