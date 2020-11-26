
import os
import sys
import json
import time
import subprocess
from bundles import unpack_all_bundles

lint_history = None

def load_lint_history():
    global lint_history
    try:
        with open('.backend_linter_history', 'r') as history_file:
            lint_history = json.loads(history_file.read())
    except:
        lint_history = {}

def save_lint_history():
    global lint_history
    with open('.backend_linter_history', 'w') as history_file:
        history_file.write(json.dumps(lint_history))

def file_never_linted_before(filename):
    return filename not in lint_history

def get_last_successful_lint_time(filename):
    if file_never_linted_before(filename):
        return -1
    return lint_history[filename]

def set_last_successful_lint_time(filename, lint_time):
    lint_history[filename] = lint_time

def file_changed_since_last_successful_lint(filename):
    last_modified = os.path.getmtime(filename)
    last_lint = get_last_successful_lint_time(filename)
    return last_lint < last_modified

def pylintrc_changed_after_last_successful_lint(filename):
    last_lint = get_last_successful_lint_time(filename)
    pylintrc_changed = os.path.getmtime('pylintrc')
    return last_lint < pylintrc_changed

def run_pylint(filename):
    p = subprocess.Popen(['pylint', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(b'')
    exit_code = p.returncode
    out_lines = [line for line in out.decode('utf-8').split('\n') if line]
    err_lines = [line for line in err.decode('utf-8').split('\n') if line]
    return exit_code, out_lines, err_lines

def evaluate_file(filename):
    print('Linting ' + filename + '...')
    exit_code, out_lines, err_lines = run_pylint(filename)
    if exit_code == 0:
        return True
    for line in out_lines:
        print(line)
    for line in err_lines:
        print(line)
    return False

def successful_ending():
    print('Success! Everything looks good.')
    save_lint_history()

def unsuccessful_ending():
    save_lint_history()


if __name__ == '__main__':
    should_lint_all = len(sys.argv) >= 2 and sys.argv[1] == '--all'
    load_lint_history()
    try:
        filenames = [filename for filename in unpack_all_bundles() if filename.endswith('.py')]
        for filename in filenames:
            should_lint = should_lint_all
            should_lint = should_lint or file_never_linted_before(filename)
            should_lint = should_lint or file_changed_since_last_successful_lint(filename)
            should_lint = should_lint or pylintrc_changed_after_last_successful_lint(filename)
            if not should_lint:
                continue
            # Go ahead and do the linting.
            if evaluate_file(filename):
                set_last_successful_lint_time(filename, time.time())
            else:
                # Stop, we've found a bad file.
                unsuccessful_ending()
                exit()
    except:
        print('Saving lint history before exit...')
        save_lint_history()
        raise
    successful_ending()
