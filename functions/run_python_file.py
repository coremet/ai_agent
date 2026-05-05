import os
import subprocess
from google import genai
from google.genai import types

# Run Python File function
def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_filepath = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_file = os.path.commonpath([working_dir_abs, target_filepath]) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_filepath):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    # Run target file
    try:
        command = ["python", target_filepath] 
        if args:
            command.extend(args)
        completed_process_object = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        output_string = []
        if completed_process_object.returncode != 0:
            output_string.append(f"Process exited with code {completed_process_object.returncode}")
        if completed_process_object.stdout == '' and completed_process_object.stderr == '':
            output_string.append("No output produced")
        if completed_process_object.stdout: 
            output_string.append(f"STDOUT: {completed_process_object.stdout}")
        if completed_process_object.stderr: 
         output_string.append(f"STDERR: {completed_process_object.stderr}")
        return "\n".join(output_string)
    except subprocess.TimeoutExpired as e:
        return f"Error: The command timed out after {e.timeout} seconds"
    except FileNotFoundError:
        return f"Error: The executable was not found"

# Run Python File declaration  
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Runs executable Python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the target file",
            ),
            "args":types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Any optional arguments added"
            )
        },
    ),
)
 