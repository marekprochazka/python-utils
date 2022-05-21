import importlib.util
import sys

PROJECT_PATH = list(sys.argv)[1]


def main():
    choice = hello()
    if choice == "1":
        spec = importlib.util.spec_from_file_location("hasher", f"{PROJECT_PATH}\hasher\hasher.py")
        hasher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hasher)
        hasher.hasher()
    elif choice == "2":
        spec = importlib.util.spec_from_file_location("folder_admin", f"{PROJECT_PATH}\\folder_admin\\folder_admin.py")
        folder_admin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(folder_admin)
        folder_admin.folder_admin()
    elif choice == "DEV":
        spec = importlib.util.spec_from_file_location("dev_test", f"{PROJECT_PATH}\dev_test\dev_test_rust.py")
        dev_test = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dev_test)
        dev_test.test()
    else:
        print("Invalid choice")




def hello() -> str:
    print("python-utils version 0.0.1")
    print("Copyright (c) 2022 Marek Prochazka")
    print("Licence: MIT")
    print("_______________________________________________________________________________")
    print("Select an option:")
    print("1. File encryptor/decryptor")
    print("2. Folder administrator")
    print("DEV dev test")

    return input("Your choise: ")


if __name__ == "__main__":
    main()