import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes user's code in an isolated namespace exposing only numpy,
    and verifies the required function exists.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['gradient_descent']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_gradient_descent(func):
    '''
    Runs test cases for gradient_descent: batch, stochastic, and mini-batch methods.
    '''
    # Common setup
    X = np.array([[1, 1], [2, 1], [3, 1], [4, 1]])
    y = np.array([2, 3, 4, 5])
    learning_rate = 0.01
    n_iterations = 100

    # Test case 1: Batch Gradient Descent
    init_weights = np.zeros(X.shape[1])
    expected1 = np.array([1.14905239, 0.56176776])
    result1 = func(X, y, init_weights.copy(), learning_rate, n_iterations, method='batch')
    if not np.allclose(result1, expected1, atol=1e-6):
        print(f"Test case 1 failed: expected {expected1}, got {result1}")
        sys.exit(1)

    # Test case 2: Stochastic Gradient Descent
    init_weights = np.zeros(X.shape[1])
    expected2 = np.array([1.0507814, 0.83659454])
    result2 = func(X, y, init_weights.copy(), learning_rate, n_iterations, method='stochastic')
    if not np.allclose(result2, expected2, atol=1e-6):
        print(f"Test case 2 failed: expected {expected2}, got {result2}")
        sys.exit(1)

    # Test case 3: Mini-Batch Gradient Descent
    init_weights = np.zeros(X.shape[1])
    batch_size = 2
    expected3 = np.array([1.10334065, 0.68329431])
    result3 = func(X, y, init_weights.copy(), learning_rate, n_iterations, batch_size, method='mini_batch')
    if not np.allclose(result3, expected3, atol=1e-6):
        print(f"Test case 3 failed: expected {expected3}, got {result3}")
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
    gradient_descent = module['gradient_descent']
    test_gradient_descent(gradient_descent)
    print('All gradient_descent tests passed.')
