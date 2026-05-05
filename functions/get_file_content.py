import os
from config import MAX_CHARS # type: ignore
from google import genai
from google.genai import types

# Get File Content function
def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_filepath = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_file = os.path.commonpath([working_dir_abs, target_filepath]) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_filepath):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Print contents of file:
    try:
        with open(target_filepath, "r") as file_object:
            content = file_object.read(MAX_CHARS)
            if file_object.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        #return f"Content length: {len(content)}\nEnd of content: {content[-100:]}" #Uncomment to test trunc logic (slices the content string)
        return content
    except PermissionError:
        return f'Error: permission denied'
    except FileNotFoundError:
        return f'Error: file not found'
    except OSError:
        return f'Error: unexpected OS error occurred'

# Get File Content declaration  
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Prints the contents of the file, restricted to a maximum of {MAX_CHARS} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the target file",
            ),
        },
    ),
)