import importlib.util

PROJECT_PATH = 'C:\Veci\programming\python-utils'


def main():
    choice = hello()
    if choice == "1":
        spec = importlib.util.spec_from_file_location("hasher", f"{PROJECT_PATH}\hasher\hasher.py")
        hasher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hasher)
        hasher.hasher()
    else:
        print("Invalid choice")




def hello() -> str:
    print("python-utils version 0.0.1")
    print("Copyright (c) 2022 Marek Prochazka")
    print("Licence: MIT")
    print("_______________________________________________________________________________")
    print("Select an option:")
    print("1. File encryptor/decryptor")

    return input("Your choise: ")


if __name__ == "__main__":
    main()