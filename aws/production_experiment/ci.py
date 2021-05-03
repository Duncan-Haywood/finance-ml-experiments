import os
from pylint import epylint as lint
import shutil


def main():
    files = os.listdir('.')
    files = [file for file in files if '.py' in file]

    pylint_stdout, pylint_stderr = lint.py_run(' '.join(files), return_std=True)
    with open('lint.txt', 'w') as f:
        pylint_stdout.seek(0)
        shutil.copyfileobj(pylint_stdout, f)
        pylint_stderr.seek(0)
        shutil.copyfileobj(pylint_stderr, f)
if __name__ == '__main__':
    main()