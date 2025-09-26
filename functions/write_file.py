import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    try:
        if os.path.commonpath([abs_working, abs_file]) != abs_working:
            return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"
        with open(abs_file, 'w') as file:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        # Check that contents were written to file
        with open(abs_file, 'r') as file:
            written = file.read()
        if written == content:
            return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
        return f"Writing contents to file was unsuccessful"
    except Exception as e:
        return f"Error: {str(e)}"
    