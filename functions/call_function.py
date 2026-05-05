from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info # type: ignore
from functions.get_file_content import schema_get_file_content # type: ignore
from functions.run_python_file import schema_run_python_file # type: ignore
from functions.write_file import schema_write_file # type: ignore

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ],
)