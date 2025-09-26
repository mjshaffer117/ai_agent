from functions.get_files_info import get_files_info

def run_manual_tests():
    # Test 1: Current Directory
    print("Results for current directory:")
    results = get_files_info("calculator", ".")
    print(f"{results}")

    # Test 2: 'pkg' Directory
    print("Results for 'pkg' directory:")
    results = get_files_info("calculator", "pkg")
    print(f"{results}")

    # Test 3: '/bin' Directory
    print("Results for '/bin' directory")
    results = get_files_info("calculator", "/bin")
    print(f"{results}")

    # Test 4: '../' Directory
    print("Results for '../' directory")
    results = get_files_info("calculator", "../")
    print(f"{results}")
    
if __name__ == "__main__":
    run_manual_tests()