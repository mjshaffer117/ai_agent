import os, sys, subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    try:
        if os.path.commonpath([abs_working, abs_file]) != abs_working:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file):
            return f'Error: File "{file_path}" not found'
        if os.path.splitext(file_path)[1] != '.py':
            return f'Error: "{file_path}" is not a python file'
        cmd = [sys.executable, abs_file, *args]
        completed_process = subprocess.run(
            cmd, cwd=abs_working, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8'
            )
        out, err, code = completed_process.stdout, completed_process.stderr, completed_process.returncode
        message = 'No output produced' if code == 0 else f'Process exited with code {code}'
        return f'STDOUT: {out}\nSTDERR: {err}\nResult: {message}'
    except Exception as e:
        return f'Error: {str(e)}'
