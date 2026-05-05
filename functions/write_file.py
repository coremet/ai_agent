import os
from google import genai
from google.genai import types

# Write File function
def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_filepath = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_filepath = os.path.commonpath([working_dir_abs, target_filepath]) == working_dir_abs
    if not valid_target_filepath:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_filepath):
        return f'Error: Cannot write to {target_filepath}" as it is a directory'
    
    # Overwrites contents of target file
    try:
        os.makedirs(os.path.dirname(target_filepath), exist_ok=True) #creates missing parent directories 
        with open(target_filepath, "w") as file_object:
            file_object.write(content) # .write() returns number of chars written
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except PermissionError:
        return f'Error: permission denied'
    except FileNotFoundError:
        return f'Error: file not found'
    except OSError:
        return f'Error: unexpected OS error occurred'
    
# Write File declaration  
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Overwrites contents of target file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the target file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The material that will replace the current contents of the target file",
            )
        },
    ),
)