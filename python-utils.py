import importlib.util
import sys
import curses

PROJECT_PATH = list(sys.argv)[1]

cli_spec = importlib.util.spec_from_file_location(
    "cli", f"{PROJECT_PATH}/cli/cli.py")
cli = importlib.util.module_from_spec(cli_spec)
cli_spec.loader.exec_module(cli)

# CLI COLORS
COLOR__WHITE = 1
COLOR__CYAN = 2
COLOR__GREEN = 3


def setup_cli() -> cli.SelectConfig:
    options = [
        cli.SelectOption("File encryptor/decryptor", "1"),
        cli.SelectOption("Folder administrator", "2"),
        cli.SelectOption("DEV dev test", "DEV"),
    ]
    helper_text = [
        cli.WinString("python-utils version 0.0.1", COLOR__WHITE, 0, 0),
        cli.WinString("Copyright (c) 2022 Marek Prochazka",
                      COLOR__GREEN, 0, 1),
        cli.WinString("Licence: MIT", COLOR__WHITE, 0, 2),
        cli.WinString("Select option:", COLOR__WHITE, 0, 3),
        cli.WinString(
            "_______________________________________________________________________________", COLOR__WHITE, 0, 4),
    ]

    return cli.SelectConfig(
        multiselect=False,
        options=options,
        helper_text=helper_text,
        default_color=COLOR__WHITE,
        highlighted_color=COLOR__CYAN,
        start_x=0,
        start_y=5,
    )


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    controller = cli.CLI(stdscr)
    choice = controller.select(setup_cli())[0].identifier
    stdscr.keypad(0)
    curses.echo() ; curses.nocbreak()
    curses.endwin()
    if choice == "1":
        spec = importlib.util.spec_from_file_location(
            "hasher", f"{PROJECT_PATH}\hasher\hasher.py")
        hasher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hasher)
        hasher.hasher()
    elif choice == "2":
        spec = importlib.util.spec_from_file_location(
            "folder_admin", f"{PROJECT_PATH}\\folder_admin\\folder_admin.py")
        folder_admin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(folder_admin)
        folder_admin.folder_admin()
    elif choice == "DEV":
        spec = importlib.util.spec_from_file_location(
            "dev_test", f"{PROJECT_PATH}\dev_test\dev_test_rust.py")
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
    curses.wrapper(main)
