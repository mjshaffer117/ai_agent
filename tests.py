from functions.write_file import write_file

def run_manual_tests():
    # Test 1: 
    print("Results for 'lorem.txt'")
    results = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"{results}")

    # Test 2: 
    print("Results for 'pkg/morelorem.txt'")
    results = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"{results}")

    # Test 3: 
    print("Results for '/tmp/temp.txt'")
    results = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"{results}")

if __name__ == "__main__":
    run_manual_tests()