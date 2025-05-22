import os
import json
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)

# Load all questions at startup
with open('./neuracamp-problems/questions.json', 'r') as f:
    QUESTIONS = json.load(f)


@app.route('/questions', methods=['GET'])
def list_questions():
    """
    Returns the full list of questions from questions.json
    """
    return jsonify(QUESTIONS)

@app.route('/submissions', methods=['POST'])
def run_submission():
    """
    Expects JSON with:
      - qid: integer question ID
      - code: string of user-submitted Python code
    Executes the associated <qid>_solution.py, passing user code in a temp file.
    Returns JSON with success flag, stdout, stderr.
    """
    data = request.get_json()
    qid = data.get('qid')
    user_code = data.get('code')

    if qid is None or user_code is None:
        return jsonify({'error': 'Missing qid or code'}), 400

    # Path to the solution script for this question
    solution_script = f"./test_learn/{qid}_solution.py"
    if not os.path.isfile(solution_script):
        return jsonify({'error': f'Solution script {solution_script} not found.'}), 404

    # Write user code into a temporary file
    import tempfile
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
    try:
        tmp.write(user_code)
        tmp.flush()
        tmp_path = tmp.name
    finally:
        tmp.close()

    try:
        # Call the solution script, passing the temp file path as argument
        proc = subprocess.run(
            ['python', solution_script, tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        return jsonify({
            'success': proc.returncode == 0,
            'stdout': proc.stdout,
            'stderr': proc.stderr
        })

    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Execution timed out.'}), 500

    finally:
        os.unlink(tmp_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
