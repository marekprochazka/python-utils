from cryptography.fernet import Fernet, InvalidToken
import base64
import os


def hasher() -> None:
    print("File encryptor by Marek Prochazka")
    print("1. Encrypt")
    print("2. Decrypt")
    choice: int = int(input("Enter choice: "))
    if choice == 1:
        encrypt()
    elif choice == 2:
        decrypt()
    else:
        print("Invalid choice")
    print("Programme finished")


def encrypt() -> None:
    key: str = input("Enter key: ")
    fernet: Fernet = Fernet(base64.b64encode(key.zfill(32).encode('ascii')))

    dr = os.getcwd()
    file_name: str = input("Enter file name: ")
    file_suffix: str = input("Enter file suffix: ")
    with open(f"{dr}\{file_name}.{file_suffix}", "rb") as file:
        data: bytes = file.read()

    encrypted: bytes = fernet.encrypt(data)
    with open(f"{file_name}.encr", "wb") as file:
        file.write(encrypted)

    print("Encrypted")


def decrypt() -> None:
    try:
        key: str = input("Enter key: ")
        fernet: Fernet = Fernet(base64.b64encode(key.zfill(32).encode('ascii')))
        dr = os.getcwd()
        file_name: str = input("Enter .encr file name: ")
        with open(f"{dr}\{file_name}.encr", "rb") as file:
            data: bytes = file.read()

        decrypted: bytes = fernet.decrypt(data)
        with open(f"{file_name}.decr", "wb") as file:
            file.write(decrypted)

        print("Decrypted")
    except InvalidToken:
        print("Invalid key")


if __name__ == "__main__":
    hasher()