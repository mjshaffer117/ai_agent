import os, sys

from prompts import system_prompt
from functions.call_function import available_functions, call_function
from functions.config import MAX_ITERATIONS

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

    for candidate_response in response.candidates:
        messages.append(candidate_response.content)

    if verbose:
        print(f'\nUser prompt: {user_prompt}')
        print(f'\nPrompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'\nResponse tokens: {response.usage_metadata.candidates_token_count}')
    
    function_call_part = response.function_calls
    if function_call_part:
        for function_call in function_call_part:
            ##print(f"Calling function: {function_call.name}({function_call.args})")
            try:
                function_call_result = call_function(function_call, verbose)
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses = function_call_result.parts
                messages.append(
                    types.Content(
                        role="user",
                        parts=function_responses
                    )
                )
            except Exception as e:
                return f'Error: {str(e)}'
            
            iteration = 0
            while iteration < MAX_ITERATIONS:
                response = client.models.generate_content(
                    model='gemini-2.0-flash-001',
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=system_prompt
                    )
                )

                if not response.function_calls and response.text:
                    print(response.text)
                    break

                function_call_part = response.function_calls
                if function_call_part:
                    for function_call in function_call_part:
                        function_call_result = call_function(function_call, verbose)
                        if verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                        messages.append(
                            types.Content(
                                role='user',
                                parts=function_call_result.parts
                            )
                        )
                iteration += 1
    else:
        print(response.text)


if __name__ == "__main__":
    main()
