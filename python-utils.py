import importlib.util
import sys
import curses


PROJECT_PATH = list(sys.argv)[1]

# cli_spec = importlib.util.spec_from_file_location(
#     "cli", f"{PROJECT_PATH}/src/cli/cli.py")
# cli = importlib.util.module_from_spec(cli_spec)
# cli_spec.loader.exec_module(cli)

import cli

# CLI COLORS
COLOR__WHITE = 1
COLOR__CYAN = 2
COLOR__GREEN = 3


def init_cli(stdscr) -> cli.CLI:
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    return cli.CLI(stdscr)


def menu_select(controller: cli.CLI) -> cli.SelectOption:
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

    conf = cli.SelectConfig(
        options=options,
        helper_text=helper_text,
        default_color=COLOR__WHITE,
        highlighted_color=COLOR__CYAN,
        start_x=0,
        start_y=5,
    )
    return controller.select(conf)

def end_cli(stdscr):
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def main(stdscr):
    controller = init_cli(stdscr)
    choice = menu_select(controller)
    choice = choice.identifier if choice != None else "None"
    if choice == "1":
        end_cli(stdscr)
        spec = importlib.util.spec_from_file_location(
            "hasher", f"{PROJECT_PATH}\src\hasher\hasher.py")
        hasher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hasher)
        hasher.hasher()
    elif choice == "2":
        spec = importlib.util.spec_from_file_location(
            "folder_admin", f"{PROJECT_PATH}\\src\\folder_admin\\folder_admin.py")
        folder_admin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(folder_admin)
        folder_admin.folder_admin(controller)
        end_cli(stdscr)
    elif choice == "DEV":
        end_cli(stdscr)
        spec = importlib.util.spec_from_file_location(
            "dev_test", f"{PROJECT_PATH}\\src\dev_test\dev_test_rust.py")
        dev_test = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dev_test)
        dev_test.test()
    else:
        end_cli(stdscr)
        print("Programm ended")


if __name__ == "__main__":
    curses.wrapper(main)
