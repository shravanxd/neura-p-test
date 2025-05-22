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


def test_single_neuron_model(func):
    '''
    Runs test cases against the user-provided single_neuron_model function.
    '''
    # Test case 1
    features = [[0.5, 1.0], [-1.5, -2.0], [2.0, 1.5]]
    labels = [0, 1, 0]
    weights = [0.7, -0.4]
    bias = -0.1
    expected = ([0.4626, 0.4134, 0.6682], 0.3349)
    try:
        result = func(features, labels, weights, bias)
        assert result == expected, f'Test case 1 failed: expected {expected}, got {result}'
    except AssertionError as e:
        print(f'AssertionError: {e}')
        sys.exit(1)

    # Test case 2
    features = [[1, 2], [2, 3], [3, 1]]
    labels = [1, 0, 1]
    weights = [0.5, -0.2]
    bias = 0
    expected = ([0.525, 0.5987, 0.7858], 0.21)
    try:
        result = func(features, labels, weights, bias)
        assert result == expected, f'Test case 2 failed: expected {expected}, got {result}'
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
    test_single_neuron_model(user_func)
    print('All single_neuron_model tests passed.')
