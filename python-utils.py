import importlib.util
import sys
from enum import Enum

import cli

PROJECT_PATH = list(sys.argv)[1]


class MainMenuOptionTypes(Enum):
    HELP = 0
    FILE_ENCRYPTOR = 1
    FOLDER_ADMIN = 2
    EXIT = 3
    NO_CHOICE = -1


# Relative imports cannot be used in this case, because the script is run from the command line in a different directory
def absolute_import(module_name: str, file_name: str = None) -> object:
    if not file_name:
        file_name = module_name
    spec = importlib.util.spec_from_file_location(
        module_name, f"{PROJECT_PATH}\\src\\{module_name}\\{file_name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Main menu that will be displayed when the program is started
# Function waits for user to make a choice and then returns the choice
def main_menu(controller: cli.CLI) -> cli.SelectOption[MainMenuOptionTypes]:
    # Text displayed at the top of main menu
    helper_text = [
        cli.WinString("python-window-utils version 0.1.0", cli.COLOR__WHITE, 0, 0),
        cli.WinString("Copyright (c) 2022 Marek Prochazka",
                      cli.COLOR__WHITE, 0, 1),
        cli.WinString("Licence: MIT", cli.COLOR__WHITE, 0, 2),
        cli.WinString("Select option:", cli.COLOR__WHITE, 0, 3),
        cli.WinString(
            "_______________________________________________________________________________", cli.COLOR__WHITE, 0, 4),
    ]
    options = [
        cli.SelectOption("Help", MainMenuOptionTypes.HELP),
        cli.SelectOption("File encryptor/decryptor", MainMenuOptionTypes.FILE_ENCRYPTOR),
        cli.SelectOption("Folder administrator (UNSTABLE!)", MainMenuOptionTypes.FOLDER_ADMIN),
        cli.SelectOption("Exit", MainMenuOptionTypes.EXIT),
    ]

    # Configuration of the main menu component
    conf = cli.SelectConfig(
        options=options,
        helper_text=helper_text,
        default_color=cli.COLOR__WHITE,
        highlighted_color=cli.COLOR__CYAN,
        start_x=0,
        start_y=5,
    )
    # Display the main menu and wait for user to make a choice
    return controller.select(conf)


def main():
    # instance of CLI controller used in menu component
    controller = cli.CLI()
    # Runs in infinite loop until user decides to exit the program
    while True:
        # Display main menu and wait for user to make a choice
        choice = main_menu(controller)
        choice = choice.value if choice is not None else MainMenuOptionTypes.NO_CHOICE
        controller.exit()
        # Runs selected subprogram
        # Each subprogram returns bool
        # True = user wants to go back to main menu
        # False = user wants to exit the program
        if choice == MainMenuOptionTypes.HELP:
            help_module = absolute_import("help")
            if help_module.main():
                continue
            break
        elif choice == MainMenuOptionTypes.FILE_ENCRYPTOR:
            hasher = absolute_import("hasher")
            if hasher.main():
                continue
            break
        elif choice == MainMenuOptionTypes.FOLDER_ADMIN:
            folder_admin = absolute_import("folder_admin")
            if folder_admin.main():
                continue
        break
    print("Programme ended")


if __name__ == "__main__":
    main()
