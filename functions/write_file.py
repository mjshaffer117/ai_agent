import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    try:
        if os.path.commonpath([abs_working, abs_file]) != abs_working:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        with open(abs_file, 'w') as file:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        # Check that contents were written to file
        with open(abs_file, 'r') as file:
            written = file.read()
        if written == content:
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        return f'Writing contents to file was unsuccessful'
    except Exception as e:
        return f'Error: {str(e)}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to be overwritten, relative to the working directory. The file may be created if the path is not found and is a valid path within the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written to the file.",
            ),
        },
    ),
)