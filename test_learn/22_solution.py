import sys
import re
import math


def get_function_name(code_string):
    """
    Extracts the first function name defined in the user code.
    """
    match = re.search(r"def\s+(\w+)", code_string)
    return match.group(1) if match else None


def load_user_function(usercode):
    """
    Safely execs user code in a restricted namespace and returns the defined function object.
    """
    exec_globals = {}
    try:
        # Provide only the math module in globals
        exec(usercode, {'math': math}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    fn_name = get_function_name(usercode)
    if not fn_name or fn_name not in exec_globals:
        print("Could not find a valid function definition in the submitted code.")
        sys.exit(1)

    return exec_globals[fn_name]


def test_sigmoid(func):
    """
    Runs a suite of assertions against the user-provided sigmoid function.
    Exits with code 1 on first failure.
    """
    try:
        assert func(0) == 0.5, "Test case 1 failed: sigmoid(0) should be 0.5"
        assert func(1) == 0.7311, "Test case 2 failed: sigmoid(1) should be 0.7311"
        assert func(-1) == 0.2689, "Test case 3 failed: sigmoid(-1) should be 0.2689"
    except AssertionError as e:
        print(f"AssertionError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solution.py <user_code_file>")
        sys.exit(1)

    user_file = sys.argv[1]
    try:
        with open(user_file, 'r') as f:
            usercode = f.read()
    except Exception as e:
        print(f"Error reading user code file: {e}")
        sys.exit(1)

    user_func = load_user_function(usercode)
    test_sigmoid(user_func)
    print("All sigmoid tests passed.")