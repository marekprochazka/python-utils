from rust_toolkit import Hello
import cli


def test():
    text = [
        cli.WinString("python-utils version 0.0.1", 1, 0, 0),
        cli.WinString("Copyright (c) 2022 Marek Prochazka", 1, 0, 1),
        cli.WinString("Licence: MIT", 1, 0, 2),
        cli.WinString("Press enter or esc to continue:", 1, 0, 3),
    ]
    controller = cli.CLI()
    controller.text(text)
    print(Hello.hello_world())
    