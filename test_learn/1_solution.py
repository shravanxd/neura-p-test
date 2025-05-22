import sys
import re


def get_defined_functions(code_string):
    '''
    Return a list of function names defined in the user code.
    '''
    return re.findall(r'def\s+(\w+)', code_string)


def load_user_module(usercode):
    '''
    Execute user code in a restricted namespace and verify required function exists.
    '''
    exec_globals = {}
    try:
        exec(usercode, {}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['matrix_dot_vector']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_matrix_dot_vector(func):
    '''
    Run test cases on the matrix_dot_vector function.
    '''
    # Test case 1: empty product
    if func([], []) != []:
        print(f"Test case 1 failed: expected [], got {func([], [])}")
        sys.exit(1)

    # Test case 2: invalid products
    invalids = [ ([], [1,2]), ([[1,2]], []), ([[1,2], [2,4]], [1]) ]
    for idx, (a, b) in enumerate(invalids, 2):
        if func(a, b) != -1:
            print(f"Test case {idx} failed: expected -1, got {func(a, b)}")
            sys.exit(1)

    # Test case 3: valid product
    a = [[1, 2], [2, 4]]
    b = [1, 2]
    expected = [5, 10]
    if func(a, b) != expected:
        print(f"Test case 4 failed: expected {expected}, got {func(a, b)}")
        sys.exit(1)

    # Test case 4: rectangular matrix
    a = [[1, 2, 3], [2, 4, 6]]
    b = [1, 2, 3]
    expected = [14, 28]
    if func(a, b) != expected:
        print(f"Test case 5 failed: expected {expected}, got {func(a, b)}")
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
    matrix_dot_vector = module['matrix_dot_vector']
    test_matrix_dot_vector(matrix_dot_vector)
    print('All matrix_dot_vector tests passed.')
