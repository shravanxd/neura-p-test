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

    required = ['compressed_row_sparse_matrix']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_compressed_row_sparse_matrix(func):
    '''
    Run test cases on the compressed_row_sparse_matrix function.
    '''
    # Test case 1: all zeros matrix
    matrix1 = [[0,0,0],[0,0,0],[0,0,0]]
    vals1, cols1, ptr1 = func(matrix1)
    if vals1 != []:
        print(f"Test 1 failed: vals {vals1} != []")
        sys.exit(1)
    if cols1 != []:
        print(f"Test 1 failed: cols {cols1} != []")
        sys.exit(1)
    if ptr1 != [0,0,0,0]:
        print(f"Test 1 failed: ptr {ptr1} != [0,0,0,0]")
        sys.exit(1)

    # Test case 2: mixed zeros
    matrix2 = [[0,0,0],[1,2,0],[0,3,4]]
    vals2, cols2, ptr2 = func(matrix2)
    if vals2 != [1,2,3,4]:
        print(f"Test 2 failed: vals {vals2} != [1,2,3,4]")
        sys.exit(1)
    if cols2 != [0,1,1,2]:
        print(f"Test 2 failed: cols {cols2} != [0,1,1,2]")
        sys.exit(1)
    if ptr2 != [0,0,2,4]:
        print(f"Test 2 failed: ptr {ptr2} != [0,0,2,4]")
        sys.exit(1)

    # Test case 3: varied non-zeros
    matrix3 = [
        [0,0,3,0,0],
        [0,4,0,0,0],
        [5,0,0,6,0],
        [0,0,0,0,0],
        [0,7,0,0,8]
    ]
    vals3, cols3, ptr3 = func(matrix3)
    if vals3 != [3,4,5,6,7,8]:
        print(f"Test 3 failed: vals {vals3} != [3,4,5,6,7,8]")
        sys.exit(1)
    if cols3 != [2,1,0,3,1,4]:
        print(f"Test 3 failed: cols {cols3} != [2,1,0,3,1,4]")
        sys.exit(1)
    if ptr3 != [0,1,2,4,4,6]:
        print(f"Test 3 failed: ptr {ptr3} != [0,1,2,4,4,6]")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python solution.py <user_code_file>')
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            usercode = f.read()
    except Exception as e:
        print(f"Error reading user code file: {e}")
        sys.exit(1)

    module = load_user_module(usercode)
    func = module['compressed_row_sparse_matrix']
    test_compressed_row_sparse_matrix(func)
    print('All Compressed Row Tests passed.')
