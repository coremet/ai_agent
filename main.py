import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("API KEY NOT FOUND")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="AI Agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=args.user_prompt)
if response.usage_metadata is None:
    raise RuntimeError("likely a failed API request")
else:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    
print(response.text)

#def main():
#    print("Hello from ai-agent!")


#if __name__ == "__main__":
#    main()
