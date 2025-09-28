import os, sys

from prompts import system_prompt
from functions.call_function import available_functions

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    args = sys.argv[1:]
    if not args:
        print("Missing command line arguments.")
        print("\nFunction usage: python main.py 'Your prompt here.'")
        sys.exit(1)
    user_prompt = " ".join([arg for arg in args if not arg.startswith("--")])
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    verbose = "--verbose" in args
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if verbose:
        print(f'\nUser prompt: {user_prompt}')
        print(f'\nPrompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'\nResponse tokens: {response.usage_metadata.candidates_token_count}')
    
    function_specifications = response.function_calls
    if function_specifications:
        for function_spec in function_specifications:
            print(f"Calling function: {function_spec.name}({function_spec.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
