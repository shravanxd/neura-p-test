import sys
import re
import numpy as np


def get_defined_functions(code_string):
    '''
    Return a list of all function names defined in user code.
    '''
    return re.findall(r'def\s+(\w+)', code_string)


def load_user_module(usercode):
    '''
    Execute user code in a restricted namespace exposing only numpy,
    and verify required function exists.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['train_neuron']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_train_neuron(func):
    '''
    Run test cases on the train_neuron implementation.
    '''
    cases = [
        # (features, labels, initial_weights, initial_bias, learning_rate, epochs, expected)
        (
            [[1.0, 2.0], [2.0, 1.0], [-1.0, -2.0]],
            [1, 0, 0],
            [0.1, -0.2],
            0.0,
            0.1,
            2,
            ([0.1035, -0.1426], -0.0056, [0.3033, 0.2947])
        ),
        (
            [[1, 2], [2, 3], [3, 1]],
            [1, 0, 1],
            [0.5, -0.2],
            0.0,
            0.1,
            3,
            ([0.4893, -0.2301], 0.001, [0.21, 0.2087, 0.2076])
        ),
    ]
    for idx, (features, labels, init_w, init_b, lr, epochs, expected) in enumerate(cases, 1):
        try:
            result = func(features, labels, init_w, init_b, lr, epochs)
            assert result == expected, f"Test case {idx} failed: expected {expected}, got {result}"
        except AssertionError as e:
            print(f"AssertionError: {e}")
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
    train_neuron = module['train_neuron']
    test_train_neuron(train_neuron)
    print('All train_neuron tests passed.')
