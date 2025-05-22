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
    and verify required functions exist.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['compute_qkv', 'self_attention', 'multi_head_attention']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_multi_head_attention(compute_qkv, multi_head_attention):
    '''
    Run test cases on the multi-head attention implementation.
    '''
    # Test case 1: basic multi-head
    m, d_model, n_heads = 6, 8, 4
    np.random.seed(42)
    X = np.random.permutation(np.arange(m * d_model)).reshape(m, d_model)
    W_q = np.random.randint(0, 4, size=(d_model, d_model))
    W_k = np.random.randint(0, 5, size=(d_model, d_model))
    W_v = np.random.randint(0, 6, size=(d_model, d_model))
    Q, K, V = compute_qkv(X, W_q, W_k, W_v)

    actual1 = multi_head_attention(Q, K, V, n_heads)
    expected1 = np.array([[500, 463, 399, 495, 377, 450, 531, 362]] * m)
    if not np.allclose(actual1, expected1, atol=1e-6):
        print(f"Test case 1 failed: {actual1} != {expected1}")
        sys.exit(1)

    # Test case 2: fewer heads
    n_heads = 2
    actual2 = multi_head_attention(Q, K, V, n_heads)
    expected2 = np.array([[547, 490, 399, 495, 377, 450, 531, 362]] * m)
    if not np.allclose(actual2, expected2, atol=1e-6):
        print(f"Test case 2 failed: {actual2} != {expected2}")
        sys.exit(1)

    # Test case 3: smaller dimensions
    m, d_model, n_heads = 4, 4, 2
    np.random.seed(42)
    X = np.random.permutation(np.arange(m * d_model)).reshape(m, d_model)
    W_q = np.random.randint(0, 4, size=(d_model, d_model))
    W_k = np.random.randint(0, 5, size=(d_model, d_model))
    W_v = np.random.randint(0, 6, size=(d_model, d_model))
    Q, K, V = compute_qkv(X, W_q, W_k, W_v)
    actual3 = multi_head_attention(Q, K, V, n_heads)
    expected3 = np.array([[103, 109, 46, 99]] * m)
    if not np.allclose(actual3, expected3, atol=1e-6):
        print(f"Test case 3 failed: {actual3} != {expected3}")
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
    compute_qkv = module['compute_qkv']
    multi_head_attention = module['multi_head_attention']
    test_multi_head_attention(compute_qkv, multi_head_attention)
    print('All multi-head-attention tests passed.')
