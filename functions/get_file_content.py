import os
from functions.config import *

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    try:
        if os.path.commonpath([abs_working, abs_file]) != abs_working:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_file, 'r') as file:
            contents = file.read()
        if len(contents) > MAX_CHAR_LEN:
            message = f' [File... "{file_path}" truncated at 10000 characters]'
            contents = contents[:MAX_CHAR_LEN] + message
        return contents
    except Exception as e:
        return f'Error: {str(e)}'
    