import sys


def load_user_module(usercode):
    '''
    Executes user's code in an isolated namespace,
    and verifies the required function exists.
    '''
    exec_globals = {}
    try:
        # No external modules needed
        exec(usercode, {}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['model_fit_quality']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_model_fit_quality(func):
    '''
    Runs test cases for the model_fit_quality function.
    '''
    cases = [
        # (training_accuracy, test_accuracy, expected_output)
        (0.9, 0.6,  1),   # overfitting
        (0.6, 0.5, -1),   # underfitting
        (0.8, 0.75, 0),   # good fit
        (0.7, 0.7,  0),   # borderline good fit
        (0.9, 0.7,  0),   # borderline overfitting
    ]

    for idx, (train_acc, test_acc, expected) in enumerate(cases, 1):
        try:
            result = func(train_acc, test_acc)
        except Exception as e:
            print(f"Test case {idx} failed: exception during model_fit_quality: {e}")
            sys.exit(1)
        if result != expected:
            print(f"Test case {idx} failed: expected {expected}, got {result}")
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
    func = module['model_fit_quality']
    test_model_fit_quality(func)
    print('All model_fit_quality tests passed.')
