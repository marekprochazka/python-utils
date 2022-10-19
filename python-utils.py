import importlib.util
import sys
import cli

PROJECT_PATH = list(sys.argv)[1]


def absolute_import(module_name: str, file_name: str = None) -> object:
    if not file_name:
        file_name = module_name
    spec = importlib.util.spec_from_file_location(
        module_name, f"{PROJECT_PATH}\\src\\{module_name}\\{file_name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def menu_select(controller: cli.CLI) -> cli.SelectOption:
    options = [
        cli.SelectOption("Help", "0"),
        cli.SelectOption("File encryptor/decryptor", "1"),
        cli.SelectOption("Folder administrator", "2"),
    ]
    helper_text = [
        cli.WinString("python-window-utils version 0.1.0", cli.COLOR__WHITE, 0, 0),
        cli.WinString("Copyright (c) 2022 Marek Prochazka",
                      cli.COLOR__WHITE, 0, 1),
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
    while True:
        controller = cli.CLI()
        choice = menu_select(controller)
        choice = choice.value if choice != None else "None"
        controller.exit()

        if choice == "1":
            hasher = absolute_import("hasher")
            if hasher.hasher():
                continue
            break
        elif choice == "2":
            folder_admin = absolute_import("folder_admin")
            if folder_admin.folder_admin():
                continue
            break
        elif choice == "0":
            help_module = absolute_import("help")
            if help_module.run_help():
                continue
        break

    print("Programme ended")


if __name__ == "__main__":
    main()
