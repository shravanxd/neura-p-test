import sys
import numpy as np


def load_user_module(usercode):
    '''
    Executes user's code in an isolated namespace exposing only numpy,
    and verifies required functions exist.
    '''
    exec_globals = {}
    try:
        exec(usercode, {'np': np}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['euclidean_distance', 'k_means_clustering']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_k_means_clustering(func):
    '''
    Runs test cases for k_means_clustering.
    '''
    cases = []
    # Test case 1
    points1 = [(1,2), (1,4), (1,0), (10,2), (10,4), (10,0)]
    k1 = 2
    init1 = [(1,1), (10,1)]
    exp1 = [(1.0,2.0), (10.0,2.0)]
    cases.append((points1, k1, init1, 10, exp1))
    # Test case 2
    points2 = [(0,0,0), (2,2,2), (1,1,1), (9,10,9), (10,11,10), (12,11,12)]
    k2 = 2
    init2 = [(1,1,1), (10,10,10)]
    exp2 = [(1.0,1.0,1.0), (10.3333,10.6667,10.3333)]
    cases.append((points2, k2, init2, 10, exp2))
    # Test case 3
    points3 = [(1,1), (2,2), (3,3), (4,4)]
    k3 = 1
    init3 = [(0,0)]
    exp3 = [(2.5,2.5)]
    cases.append((points3, k3, init3, 10, exp3))
    # Test case 4
    points4 = [(0,0),(1,0),(0,1),(1,1),(5,5),(6,5),(5,6),(6,6),
               (0,5),(1,5),(0,6),(1,6),(5,0),(6,0),(5,1),(6,1)]
    k4 = 4
    init4 = [(0,0),(0,5),(5,0),(5,5)]
    exp4 = [(0.5,0.5),(0.5,5.5),(5.5,0.5),(5.5,5.5)]
    cases.append((points4, k4, init4, 10, exp4))
    # Test case 5
    points5 = [(0,0),(0.5,0),(0,0.5),(0.5,0.5),(4,4),(6,6)]
    k5 = 2
    init5 = [(0,0),(5,5)]
    exp5 = [(0.25,0.25),(5.0,5.0)]
    cases.append((points5, k5, init5, 10, exp5))

    for idx, (pts, k, init, iters, expected) in enumerate(cases, 1):
        try:
            result = func(pts, k, init, iters)
        except Exception as e:
            print(f"Test case {idx} failed: exception during k_means_clustering: {e}")
            sys.exit(1)
        if len(result) != len(expected) or not all(np.allclose(res, exp, atol=1e-4)
                                                   for res, exp in zip(result, expected)):
            print(f"Test case {idx} failed:\nExpected: {expected}\nGot:      {result}")
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
    k_means = module['k_means_clustering']
    test_k_means_clustering(k_means)
    print('All k_means_clustering tests passed.')
