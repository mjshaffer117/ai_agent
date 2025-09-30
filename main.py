import os, sys

from prompts import system_prompt
from functions.call_function import available_functions, call_function
from functions.config import MAX_ITERATIONS

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    args = sys.argv[1:]
    verbose = "--verbose" in args
    
    if not args:
        print("Missing command line arguments.")
        print("\nFunction usage: python main.py 'Your prompt here.'")
        sys.exit(1)
    
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join([arg for arg in args if not arg.startswith("--")])

    if verbose:
        print(f'\nUser prompt: {user_prompt}')

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    iteration = 0
    while True:
        iteration += 1
        if iteration > MAX_ITERATIONS:
            print(f"Maximum iterations reached: {MAX_ITERATIONS}")
            sys.exit(1)

        try:
            response = generate_content(client, messages, verbose)
            if response:
                print(f"Final response: {response}")
                break
        except Exception as e:
            print(f"Error generating content: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception("Empty function call result.")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()
