import sys
import re


def get_defined_functions(code_string):
    '''
    Return a list of function names defined in the user code.
    '''
    return re.findall(r'def\s+(\w+)', code_string)


def load_user_module(usercode):
    '''
    Execute user code in a restricted namespace and verify required functions exist.
    '''
    exec_globals = {}
    try:
        # Execute without exposing any extra modules
        exec(usercode, {}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['dot', 'scalar_mult', 'orthogonal_projection']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_orthogonal_projection(func):
    '''
    Run test cases on the orthogonal_projection function.
    '''
    # Test case 1: 2D vectors
    v1 = [3, 4]
    L1 = [1, 0]
    expected1 = [3, 0]
    result1 = func(v1, L1)
    if result1 != expected1:
        print(f"Test case 1 failed: {result1} != {expected1}")
        sys.exit(1)

    # Test case 2: 3D vectors
    v2 = [1, 2, 3]
    L2 = [0, 0, 1]
    expected2 = [0, 0, 3]
    result2 = func(v2, L2)
    if result2 != expected2:
        print(f"Test case 2 failed: {result2} != {expected2}")
        sys.exit(1)

    # Test case 3: arbitrary 3D vectors
    v3 = [5, 6, 7]
    L3 = [2, 0, 0]
    expected3 = [5, 0, 0]
    result3 = func(v3, L3)
    if result3 != expected3:
        print(f"Test case 3 failed: {result3} != {expected3}")
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
    proj_func = module['orthogonal_projection']
    test_orthogonal_projection(proj_func)
    print('All orthogonal_projection tests passed.')
