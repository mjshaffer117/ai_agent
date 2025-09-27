import os, sys
from prompts import system_prompt
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
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    print(response.text)
    if verbose:
        print(f'\nUser prompt: {user_prompt}')
        print(f'\nPrompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'\nResponse tokens: {response.usage_metadata.candidates_token_count}')


if __name__ == "__main__":
    main()
