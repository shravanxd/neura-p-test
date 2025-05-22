import sys


def load_user_module(usercode):
    '''
    Executes user code in an isolated namespace and verifies meteor_score is defined.
    '''
    exec_globals = {}
    try:
        exec(usercode, {}, exec_globals)
    except Exception as e:
        print(f"Error executing user code: {e}")
        sys.exit(1)

    required = ['meteor_score']
    missing = [fn for fn in required if fn not in exec_globals]
    if missing:
        print(f"Missing required function(s): {', '.join(missing)}")
        sys.exit(1)

    return exec_globals


def test_meteor_score(func):
    '''
    Runs test cases for the METEOR score implementation.
    '''
    # Test Case 1: Identical translations
    ref1 = "The cat sits on the mat"
    cand1 = "The cat sits on the mat"
    if func(ref1, cand1) != 1.0:
        print(f"Test Case 1 failed: expected 1.0, got {func(ref1, cand1)}")
        sys.exit(1)

    # Test Case 2: Similar translations
    ref2 = "The quick brown fox jumps over the lazy dog"
    cand2 = "A quick brown fox jumps over a lazy dog"
    if func(ref2, cand2) != 0.991:
        print(f"Test Case 2 failed: expected 0.991, got {func(ref2, cand2)}")
        sys.exit(1)

    # Test Case 3: Completely different
    ref3 = "The cat sits on the mat"
    cand3 = "Dogs run in the park"
    if func(ref3, cand3) != 0.0:
        print(f"Test Case 3 failed: expected 0.0, got {func(ref3, cand3)}")
        sys.exit(1)

    # Test Case 4: Partially matching
    ref4 = "Machine learning is an exciting field"
    cand4 = "Machine learning algorithms are fascinating"
    if func(ref4, cand4) != 0.667:
        print(f"Test Case 4 failed: expected 0.667, got {func(ref4, cand4)}")
        sys.exit(1)

    # Test Case 5: Empty input handling
    try:
        func("", "Some text")
        print("Test Case 5 failed: expected ValueError")
        sys.exit(1)
    except ValueError:
        pass

    # Test Case 6: Partial match with penalty
    ref6 = "The cat sits on the mat"
    cand6 = "The cat on the mat sits"
    if func(ref6, cand6) != 0.933:
        print(f"Test Case 6 failed: expected 0.933, got {func(ref6, cand6)}")
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
    meteor_score = module['meteor_score']
    test_meteor_score(meteor_score)
    print('All METEOR score tests passed.')