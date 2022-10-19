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
    cli.WinString("TODO", cli.COLOR__RED, 0, 1),
]

# Text displayed when user selects "Folder Admin" option in help subprogram
FOLDER_ADMIN_HELP_TEXT = [
    cli.WinString("Folder admin help:", cli.COLOR__WHITE, 0, 0),
    cli.WinString("TODO", cli.COLOR__RED, 0, 1),
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
        start_y=len(helper_text)+1,
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
