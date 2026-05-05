import os
from google import genai
from google.genai import types

# Get File's Information function
def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Read directory contents
    try:
        with os.scandir(target_dir) as entries:
            contents = []
            for entry in entries:
                is_dir = 'True' if entry.is_dir() else 'False'
                size = entry.stat().st_size
                contents.append(f'- {entry.name}: file_size={size} bytes, is_dir={is_dir}')
        return "\n\t".join(contents) if contents else f'Target directory is empty'
    except PermissionError:
        return f'Error: permission denied'
    except FileNotFoundError:
        return f'Error: directory not found'
    except OSError:
        return f'Error: unexpected OS error occurred'

# Get File's Information declaration
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
