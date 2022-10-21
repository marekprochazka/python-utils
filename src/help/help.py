from typing import List

import cli
from enum import Enum


class OptionTypes(Enum):
    ENCRYPTOR = 1
    FOLDER_ADMIN = 2
    GO_BACK = 0
    EXIT = -1


# Options displayed in the main menu of help subprogram
HELP_OPTIONS = [
    cli.SelectOption("Encryptor", OptionTypes.ENCRYPTOR),
    cli.SelectOption("Folder Admin", OptionTypes.FOLDER_ADMIN),
    cli.SelectOption("Go back", OptionTypes.GO_BACK),
    cli.SelectOption("Exit", OptionTypes.EXIT),
]

# Text displayed when user selects "Encryptor" option in help subprogram
ENCRYPTOR_HELP_TEXT = [
    cli.WinString("Encryptor help:", cli.COLOR__WHITE, 0, 0),
    cli.WinString(
        "This util is used as a tool to safely encrypt files with a custom key (passphrase) and to later decrypt the file",
        cli.COLOR__WHITE, 0, 1),
    cli.WinString(
        "The encryption is done using Fernet algorithm, which is a symmetric encryption algorithm",
        cli.COLOR__RED, 0, 2),
    cli.WinString(
        "Use case (Encryption):",
        cli.COLOR__CYAN, 0, 4),
    cli.WinString(
        "1. Run pwu in directory with files you want to encrypt",
        cli.COLOR__WHITE, 0, 5),
    cli.WinString(
        "2. Select 'File encryptor/decryptor' option",
        cli.COLOR__WHITE, 0, 6),
    cli.WinString(
        "3. Select 'Encryptor' option",
        cli.COLOR__WHITE, 0, 7),
    cli.WinString(
        "4. Select file to encrypt",
        cli.COLOR__WHITE, 0, 8),
    cli.WinString(
        "5. Enter passphrase you want to use to encrypt the file",
        cli.COLOR__WHITE, 0, 9),
    cli.WinString("(If you forget your passphrase it will be impossible to recover file!)", cli.COLOR__RED, 56, 9),
    cli.WinString(
        "6. Choose if you want to delete the original file or not",
        cli.COLOR__WHITE, 0, 10),
    cli.WinString(
        "7. File is encrypted and saved in the same directory with .enc extension",
        cli.COLOR__WHITE, 0, 11),
    cli.WinString(
        "Use case (Decryption):",
        cli.COLOR__CYAN, 0, 13),
    cli.WinString(
        "1. Run pwu in directory with files you want to decrypt",
        cli.COLOR__WHITE, 0, 14),
    cli.WinString(
        "2. Select 'File encryptor/decryptor' option",
        cli.COLOR__WHITE, 0, 15),
    cli.WinString(
        "3. Select 'Decryptor' option",
        cli.COLOR__WHITE, 0, 16),
    cli.WinString(
        "4. Select file to decrypt",
        cli.COLOR__WHITE, 0, 17),
    cli.WinString(
        "5. Enter passphrase you used to encrypt the file",
        cli.COLOR__WHITE, 0, 18),
    cli.WinString(
        "6. Choose if you want to delete the original (.encr) file or not",
        cli.COLOR__WHITE, 0, 19),
    cli.WinString(
        "7. File is decrypted and saved in the same directory with original name",
        cli.COLOR__WHITE, 0, 20),
    cli.WinString("", cli.COLOR__WHITE, 0, 21),
]

# Text displayed when user selects "Folder Admin" option in help subprogram
FOLDER_ADMIN_HELP_TEXT = [
    cli.WinString("Folder admin help:", cli.COLOR__WHITE, 0, 0),
    cli.WinString("DOCUMENTATION WILL BE ADDED AFTER UTIL WILL BE FIXED AND REFACTORED", cli.COLOR__RED, 0, 1),
]


# Function waits for user to make a choice and then returns the choice
def select_option() -> OptionTypes:
    controller = cli.CLI()
    helper_text = [
        cli.WinString("PWU help module:", cli.COLOR__WHITE, 0, 0)
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


def show_help(helper_text: List[cli.WinString]) -> bool:
    options = [
        cli.SelectOption("Go back", True),
        cli.SelectOption("Exit", False),
    ]
    conf = cli.SelectConfig(
        options=options,
        helper_text=helper_text,
        default_color=cli.COLOR__WHITE,
        highlighted_color=cli.COLOR__CYAN,
        start_x=0,
        start_y=len(helper_text) + 1,
    )
    controller = cli.CLI()
    choice = controller.select(conf).value
    controller.exit()
    return choice


# main function of the help subprogram
def main():
    while True:
        choice = select_option()
        # Display help for selected option
        if choice == OptionTypes.EXIT:
            return False
        elif choice == OptionTypes.GO_BACK:
            return True
        elif choice == OptionTypes.ENCRYPTOR:
            if show_help(ENCRYPTOR_HELP_TEXT):
                continue
            return False
        elif choice == OptionTypes.FOLDER_ADMIN:
            if show_help(FOLDER_ADMIN_HELP_TEXT):
                continue
            return False
