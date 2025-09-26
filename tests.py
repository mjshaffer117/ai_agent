from functions.run_python_file import run_python_file

def run_manual_tests():
    # Test 1: 
    print("Results for 'calculator/main.py'")
    results = run_python_file("calculator", "main.py")
    print(f"{results}")

    # Test 2: 
    print("Results for 'calculator/main.py [3 + 5]'")
    results = run_python_file("calculator", "main.py", ["3 + 5"])
    print(f"{results}")

    # Test 3: 
    print("Results for 'calculator/tests.py'")
    results = run_python_file("calculator", "tests.py")
    print(f"{results}")

    # Test 4: 
    print("Results for '../main.py'")
    results = run_python_file("calculator", "../main.py")
    print(f"{results}")

    # Test 5: 
    print("Results for 'nonexistent.py'")
    results = run_python_file("calculator", "nonexistent.py")
    print(f"{results}")

if __name__ == "__main__":
    run_manual_tests()