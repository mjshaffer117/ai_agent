import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_dir = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    try:
        if os.path.commonpath([abs_dir, abs_working]) != abs_working:
            return f"Error: Cannot list '{full_path}' as it is outside the permitted working directory"
        if not os.path.isdir(full_path):
            return f"Error: '{full_path}' is not a directory"
        files = []
        dir_items = os.listdir(full_path)
        for filename in dir_items:
            file_path = os.path.join(full_path, filename)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            files.append(f" - {filename}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"
    