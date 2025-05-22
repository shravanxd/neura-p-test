import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes user code in an isolated namespace exposing only numpy,
    and verifies that gen_text is defined.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['gen_text']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_gen_text(gen_text):
    '''
    Runs test cases for the gen_text function.
    '''
    # Test case 1
    try:
        result1 = gen_text("hello", n_tokens_to_generate=5)
    except Exception as e:
        print(f"Test case 1 failed: exception during gen_text('hello'): {e}")
        sys.exit(1)
    expected1 = "hello hello hello <UNK> <UNK>"
    if result1 != expected1:
        print(f"Test case 1 failed: expected '{expected1}', got '{result1}'")
        sys.exit(1)

    # Test case 2
    try:
        result2 = gen_text("hello world", n_tokens_to_generate=10)
    except Exception as e:
        print(f"Test case 2 failed: exception during gen_text('hello world'): {e}")
        sys.exit(1)
    expected2 = "world world world world world world world world world world"
    if result2 != expected2:
        print(f"Test case 2 failed: expected '{expected2}', got '{result2}'")
        sys.exit(1)

    # Test case 3
    try:
        result3 = gen_text("world", n_tokens_to_generate=3)
    except Exception as e:
        print(f"Test case 3 failed: exception during gen_text('world'): {e}")
        sys.exit(1)
    expected3 = "world world world"
    if result3 != expected3:
        print(f"Test case 3 failed: expected '{expected3}', got '{result3}'")
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
    gen_text = module['gen_text']
    test_gen_text(gen_text)
    print('All gen_text tests passed.')
