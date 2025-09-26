from functions.get_file_content import get_file_content

def run_manual_tests():
    # Test 1: Current Directory
    #print("Results for lorem.txt:")
    #results = get_file_content("calculator", "lorem.txt")
    #print(f"{results}")

    # Test 2: 
    print("Results for 'main.py'")
    results = get_file_content("calculator", "main.py")
    print(f"{results}")

    # Test 3: 
    print("Results for 'pkg/calculator.py'")
    results = get_file_content("calculator", "pkg/calculator.py")
    print(f"{results}")

    # Test 4: 
    print("Results for '/bin/cat'")
    results = get_file_content("calculator", "/bin/cat")
    print(f"{results}")

    # Test 5: 
    print("Results for 'pkg/does_not_exist.py'")
    results = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"{results}")

if __name__ == "__main__":
    run_manual_tests()