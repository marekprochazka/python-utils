from typing import List

import cli
from enum import Enum


class OptionTypes(Enum):
    ENCRYPTOR = 1
    FOLDER_ADMIN = 2
    EXIT = 0


OPTIONS = [
    cli.SelectOption("Encryptor", OptionTypes.ENCRYPTOR),
    cli.SelectOption("Folder Admin", OptionTypes.FOLDER_ADMIN),
    cli.SelectOption("Exit", OptionTypes.EXIT),
]

ENCRYPTOR_HELP_TEXT = [
    cli.WinString("Encryptor help:", cli.COLOR__WHITE, 0, 0),
    cli.WinString("TODO", cli.COLOR__RED, 0, 1),
]

FOLDER_ADMIN_HELO_TEXT = [
    cli.WinString("Folder admin help:", cli.COLOR__WHITE, 0, 0),
    cli.WinString("TODO", cli.COLOR__RED, 0, 1),
]


def select_option() -> OptionTypes:
    controller = cli.CLI()
    helper_text = [
        cli.WinString("PWU help module:", cli.COLOR__WHITE, 0, 0)
    ]

    conf = cli.SelectConfig(
        options=OPTIONS,
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


def run_help():
    while True:
        choice = select_option()
        if choice == OptionTypes.EXIT:
            break
        elif choice == OptionTypes.ENCRYPTOR:
            if show_help(ENCRYPTOR_HELP_TEXT):
                continue
            break
        elif choice == OptionTypes.FOLDER_ADMIN:
            if show_help(FOLDER_ADMIN_HELO_TEXT):
                continue
            break
