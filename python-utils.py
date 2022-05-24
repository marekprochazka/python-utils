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



def menu_select(controller: cli.CLI) -> cli.SelectOption:
    options = [
        cli.SelectOption("File encryptor/decryptor", "1"),
        cli.SelectOption("Folder administrator", "2"),
        cli.SelectOption("DEV dev test", "DEV"),
    ]
    helper_text = [
        cli.WinString("python-utils version 0.0.1", cli.COLOR__WHITE, 0, 0),
        cli.WinString("Copyright (c) 2022 Marek Prochazka",
                      cli.COLOR__GREEN, 0, 1),
        cli.WinString("Licence: MIT", cli.COLOR__WHITE, 0, 2),
        cli.WinString("Select option:", cli.COLOR__WHITE, 0, 3),
        cli.WinString(
            "_______________________________________________________________________________", cli.COLOR__WHITE, 0, 4),
    ]

    conf = cli.SelectConfig(
        options=options,
        helper_text=helper_text,
        default_color=cli.COLOR__WHITE,
        highlighted_color=cli.COLOR__CYAN,
        start_x=0,
        start_y=5,
    )
    return controller.select(conf)



def main():
    controller = cli.CLI()
    choice = menu_select(controller)
    choice = choice.identifier if choice != None else "None"
    controller.exit()

    if choice == "1":
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
    elif choice == "DEV":
        spec = importlib.util.spec_from_file_location(
            "dev_test", f"{PROJECT_PATH}\\src\dev_test\dev_test_rust.py")
        dev_test = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dev_test)
        dev_test.test(controller)
    else:
        print("Programm ended")


if __name__ == "__main__":
    main()
