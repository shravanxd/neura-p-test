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

    required = ['train_softmaxreg']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_train_softmaxreg(func):
    '''
    Runs test cases for the train_softmaxreg function.
    '''
    # Test case 1
    X1 = np.array([[ 2.52569869,  2.33335813,  1.77303921,  0.41061103, -1.66484491],
                   [ 1.51013861,  1.30237106,  1.31989315,  1.36087958,  0.46381252],
                   [-2.09699866, -1.35960405, -1.04035503, -2.25481082, -0.32359947],
                   [-0.96660088, -0.60680633, -0.72017167, -1.73257187, -1.12811486],
                   [-0.38096611, -0.24852455,  0.18789426,  0.52359424,  1.30725962],
                   [ 0.54828787,  0.33156614,  0.10676247,  0.30694669, -0.37555384],
                   [-3.03393135, -2.01966141, -0.65468580, -0.90330912,  2.89185791],
                   [ 0.28602304, -0.12650000, -0.52209915,  0.28309144, -0.58658820],
                   [-0.26268117,  0.76017979,  1.84095557, -0.23245038,  1.80716891],
                   [ 0.30283562, -0.40231495, -1.29550644, -0.14227270, -1.78121713]])
    y1 = np.array([2, 3, 0, 0, 1, 3, 0, 1, 2, 1])
    lr1 = 3e-2
    it1 = 10
    expected_b1 = [[-0.0841, -0.5693, -0.3651, -0.2423, -0.5344,  0.0339],
                    [ 0.2566,  0.0535, -0.2104, -0.4004,  0.2709, -0.1461],
                    [-0.1318,  0.2109,  0.3998,  0.5230, -0.1001,  0.0545],
                    [-0.0407,  0.3049,  0.1757,  0.1197,  0.3637,  0.0576]]
    expected_losses1 = [13.8629, 10.7201,  9.3163,  8.4942,  7.9132,
                         7.4598,  7.0854,  6.7653,  6.4851,  6.2358]

    b1, losses1 = func(X1, y1, lr1, it1)
    if b1 != expected_b1 or losses1 != expected_losses1:
        print(f"Test case 1 failed:\nExpected B: {expected_b1}\nGot B:      {b1}\nExpected losses: {expected_losses1}\nGot losses:      {losses1}")
        sys.exit(1)

    # Test case 2
    X2 = np.array([[-0.55605887, -0.74922526, -0.19133450,  0.41584056],
                   [-1.05481124, -1.13763371, -1.28685937, -1.07101150],
                   [-1.17111877, -1.46866663, -0.75898143,  0.15915148],
                   [-1.21725723, -1.55590285, -0.69318542,  0.35806150],
                   [-1.90316075, -2.06075824, -2.29524220, -1.87885386],
                   [-0.79089629, -0.98662696, -0.52955027,  0.07329079],
                   [ 1.97170638,  2.65609694,  0.68023770, -1.47090364],
                   [ 1.46907396,  1.61396429,  1.69602021,  1.29791351],
                   [ 0.03095068,  0.15148081, -0.34698116, -0.74306029],
                   [-1.40292946, -1.99308861, -0.14782810,  1.72332995]])
    y2 = np.array([1., 0., 0., 1., 0., 1., 0., 1., 0., 1.])
    lr2 = 1e-2
    it2 = 7
    expected_b2 = [[-0.0052,  0.0148,  0.0562, -0.1130, -0.2488],
                    [ 0.0052, -0.0148, -0.0562,  0.1130,  0.2488]]
    expected_losses2 = [6.9315, 6.4544, 6.0487, 5.7025, 5.4055, 5.1493, 4.9269]

    b2, losses2 = func(X2, y2, lr2, it2)
    if b2 != expected_b2 or losses2 != expected_losses2:
        print(f"Test case 2 failed:\nExpected B: {expected_b2}\nGot B:      {b2}\nExpected losses: {expected_losses2}\nGot losses:      {losses2}")
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
    train_softmaxreg = module['train_softmaxreg']
    test_train_softmaxreg(train_softmaxreg)
    print('All train_softmaxreg tests passed.')
