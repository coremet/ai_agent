import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt # type: ignore
from functions.call_function import available_functions # type: ignore
from functions.call_function import call_function # type: ignore

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API KEY NOT FOUND")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    generate_content(client, messages, args)

def generate_content(client, messages, args):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise Exception("The types.Content object returned from call_function does not have a non-empty .parts list")
            if not function_call_result.parts[0].function_response: 
                raise Exception("The .function_response property of the first item in the list of parts is not a FunctionResponse object")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("The actual function result is not present")
            else:
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        if response.usage_metadata is None:
            raise RuntimeError("likely a failed API request")
        else:
            if args.verbose: 
                print(f"User prompt: {args.user_prompt}") 
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    
        print(response.text)

 # If another file imports your file as a module, __name__ is set to the filename instead, so main() won't run automatically. 
 # It's a guard that says "only run this if I'm the entry point, not being imported."

if __name__ == "__main__": 
    main()


