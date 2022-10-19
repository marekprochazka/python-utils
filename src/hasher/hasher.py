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


# Options displayed in the main menu of help subprogram
HELP_OPTIONS = [
    cli.SelectOption("Encryptor", OptionTypes.ENCRYPTOR),
    cli.SelectOption("Decryptor", OptionTypes.DECRYPTOR),
    cli.SelectOption("Go back", OptionTypes.GO_BACK),
    cli.SelectOption("Exit", OptionTypes.EXIT),
]


# Function waits for user to make a choice and then returns the choice (option)
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


# Makes user select file to encrypt, write key and then encrypts the file
def encrypt_ui() -> bool:
    controller = cli.CLI()

    file_helper_text = [
        cli.WinString("Select file to encrypt:", cli.COLOR__WHITE, 0, 0)]
    # list of files in current directory
    file_options = [cli.SelectOption(f, f) for f in os.listdir('.') if os.path.isfile(f)]
    # add cancel option
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

    key_helper_text = [
        cli.WinString("Write key phrase you want to use to decrypt once encrypted file:", cli.COLOR__WHITE, 0, 0),
    ]
    key_user_input = controller.text_input(help_text=key_helper_text)

    do_encrypt(key_user_input, file_name, file_suffix)

    # ask user if he wants to delete original file
    if cli.CliUtils.yes_no(controller=controller, question=[
        cli.WinString("File was successfully encrypted", cli.COLOR__WHITE, 0, 0),
        cli.WinString("Do you want to delete not encrypted file?", cli.COLOR__WHITE, 0, 1)]):
        os.remove(file_choice)

    controller.exit()
    return True


# encrypt function
def do_encrypt(key: str, file_name: str, file_suffix: str) -> None:
    fernet: Fernet = Fernet(base64.b64encode(key.zfill(32).encode('ascii')))

    dr = os.getcwd()
    with open(f"{dr}\{file_name}.{file_suffix}", "rb") as file:
        data: bytes = file.read()

    encrypted: bytes = fernet.encrypt(data)
    with open(f"{file_name}.{file_suffix}.encr", "wb") as file:
        file.write(encrypted)


# Makes user select file to decrypt, write key and then decrypts the file
def decrypt_ui() -> bool:
    controller = cli.CLI()

    file_helper_text = [
        cli.WinString("Select file to decrypt:", cli.COLOR__WHITE, 0, 0)]
    # list of files in current directory
    file_options = [cli.SelectOption(f, f) for f in os.listdir('.') if os.path.isfile(f)]
    # add cancel option
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

    key_helper_text = [
        cli.WinString("Write key phrase you used to encrypt file:", cli.COLOR__WHITE, 0, 0),
    ]
    key_user_input = controller.text_input(help_text=key_helper_text)

    if do_decrypt(key_user_input, file_choice):
        if cli.CliUtils.yes_no(controller=controller,
                               question=[
                                   cli.WinString("File was successfully decrypted", cli.COLOR__WHITE, 0, 0),
                                   cli.WinString("Do you want to delete encrypted file?", cli.COLOR__WHITE, 0, 1)]):
            os.remove(file_choice)
    else:
        controller.text([cli.WinString("File was not decrypted -> Invalid key", cli.COLOR__WHITE, 0, 0),
                         cli.WinString("Press [Enter] key to continue", cli.COLOR__WHITE, 0, 1)])

    controller.exit()

    return True


# decrypt function
def do_decrypt(key: str, file_name: str) -> bool:
    try:
        fernet: Fernet = Fernet(base64.b64encode(key.zfill(32).encode('ascii')))
        dr = os.getcwd()
        with open(f"{dr}\{file_name}", "rb") as file:
            data: bytes = file.read()

        decrypted: bytes = fernet.decrypt(data)
        new_file_name = file_name.split(".encr")[0]
        with open(f"{dr}\{new_file_name}", "wb") as file:
            file.write(decrypted)

        return True
    except InvalidToken:
        return False


# Main function
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
            if decrypt_ui():
                continue
            return True


# used for testing purposes
if __name__ == "__main__":
    main()
