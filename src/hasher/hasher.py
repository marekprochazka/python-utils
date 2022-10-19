from cryptography.fernet import Fernet, InvalidToken
import base64
import os
import cli
from enum import Enum


class OptionTypes(Enum):
    ENCRYPTOR = 1
    DECRYPTOR = 2
    GO_BACK = 0
    EXIT = -1


HELP_OPTIONS = [
    cli.SelectOption("Encryptor", OptionTypes.ENCRYPTOR),
    cli.SelectOption("Decryptor", OptionTypes.DECRYPTOR),
    cli.SelectOption("Go back", OptionTypes.GO_BACK),
    cli.SelectOption("Exit", OptionTypes.EXIT),
]


def select_option() -> OptionTypes:
    controller = cli.CLI()
    helper_text = [
        cli.WinString("PWU Encrypt/decrypt module:", cli.COLOR__WHITE, 0, 0)
    ]

    conf = cli.SelectConfig[OptionTypes](
        options=HELP_OPTIONS,
        helper_text=helper_text,
        default_color=cli.COLOR__WHITE,
        highlighted_color=cli.COLOR__CYAN,
        start_x=0,
        start_y=1,
    )
    choice = controller.select(conf).value
    controller.exit()
    return choice


# Makes user select file to encrypt, write code and then encrypts the file
def encrypt_ui() -> bool:
    controller = cli.CLI()
    key_helper_text = [
        cli.WinString("Write key phrase you want to use to decrypt once encrypted file:", cli.COLOR__WHITE, 0, 0),
    ]
    key_user_input = controller.text_input(help_text=key_helper_text)

    file_helper_text = [
        cli.WinString("Select file to encrypt:", cli.COLOR__WHITE, 0, 0)]
    file_options = [cli.SelectOption(f, f) for f in os.listdir('.') if os.path.isfile(f)]
    file_options.append(cli.SelectOption("Cancel", "Cancel"))
    file_conf = cli.SelectConfig[str](
        options=file_options,
        helper_text=file_helper_text,
        default_color=cli.COLOR__WHITE,
        highlighted_color=cli.COLOR__CYAN,
        start_x=0,
        start_y=1,
    )
    file_choice = controller.select(file_conf).value
    if file_choice == "Cancel":
        controller.exit()
        return True
    file_name, file_suffix = file_choice.split(".")
    do_encrypt(key_user_input, file_name, file_suffix)
    controller.text([cli.WinString("File was successfully encrypted", cli.COLOR__WHITE, 0, 0),
                     cli.WinString("Press [Enter] key to continue", cli.COLOR__WHITE, 0, 1)])
    controller.exit()
    return True


def do_encrypt(key: str, file_name: str, file_suffix: str) -> None:
    fernet: Fernet = Fernet(base64.b64encode(key.zfill(32).encode('ascii')))

    dr = os.getcwd()
    with open(f"{dr}\{file_name}.{file_suffix}", "rb") as file:
        data: bytes = file.read()

    encrypted: bytes = fernet.encrypt(data)
    with open(f"{file_name}.{file_suffix}.encr", "wb") as file:
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


def main() -> bool:
    while True:
        choice = select_option()
        if choice == OptionTypes.EXIT:
            return False
        elif choice == OptionTypes.GO_BACK:
            return True
        elif choice == OptionTypes.ENCRYPTOR:
            if encrypt_ui():
                continue
            return True
        elif choice == OptionTypes.DECRYPTOR:
            decrypt()
            return True


if __name__ == "__main__":
    main()
