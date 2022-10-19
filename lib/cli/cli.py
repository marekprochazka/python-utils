import curses
from curses.textpad import Textbox, rectangle
from typing import List, Optional, Any, TypeVar, Generic

T = TypeVar('T')

COLOR__WHITE = 1
COLOR__CYAN = 2
COLOR__RED = 3


class WinString:
    def __init__(self, text: str, color: int, start_x: int, start_y: int):
        self.text = text
        self.color = color
        self.start_x = start_x
        self.start_y = start_y


class SelectOption(Generic[T]):
    def __init__(self, text: str, value: T):
        self.text = text
        self.value = value


class SelectConfig(Generic[T]):
    def __init__(self, options: List[SelectOption[T]], helper_text: List[WinString], default_color: int,
                 highlighted_color: int, start_x: int, start_y: int):
        self.options = options
        self.helper_text = helper_text
        self.default_color = default_color
        self.highlighted_color = highlighted_color
        self.start_x = start_x
        self.start_y = start_y


class CLI:
    pressed_key = None
    KEY_ENTER: int = 10
    KEY_ESC: int = 27
    KEY_SPACE: int = 32
    KEY_BACKSPACE: int = 8
    KEY_LEFT: int = 260
    KEY_RIGHT: int = 261
    stdscr = None

    def __init__(self):
        self.__init_cli()
        self.stdscr.erase()
        self.stdscr.refresh()

    def __init_cli(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        self.stdscr.keypad(True)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    def __end_cli(self):
        curses.endwin()

    def exit(self) -> None:
        self.__end_cli()

    def multi_select(self, config: SelectConfig) -> List[SelectOption]:
        # Initialize variables
        selected_options = []
        num_options = len(config.options)
        highlighted_option = 0
        curses.curs_set(0)

        while True:
            self.stdscr.erase()
            self.stdscr.refresh()

            # Handle last key input
            if self.pressed_key == self.KEY_ENTER:
                break
            if self.pressed_key == self.KEY_ESC:
                selected_options = [None]
                break
            if self.pressed_key == self.KEY_SPACE:
                if config.options[highlighted_option] in selected_options:
                    selected_options.remove(
                        config.options[highlighted_option])
                else:
                    selected_options.append(
                        config.options[highlighted_option])
                self.pressed_key = None

            if self.pressed_key == curses.KEY_UP:
                highlighted_option = highlighted_option - 1
                if highlighted_option < 0:
                    highlighted_option = num_options - 1
                self.pressed_key = None

            if self.pressed_key == curses.KEY_DOWN:
                highlighted_option = highlighted_option + 1
                if highlighted_option >= num_options:
                    highlighted_option = 0
                self.pressed_key = None

            # Draw the window
            # Draw helper text
            for txt in config.helper_text:
                self.stdscr.addstr(txt.start_y, txt.start_x,
                                   txt.text, txt.color)
            # Draw options
            for num_option, option in enumerate(config.options):
                color = curses.color_pair(
                    config.highlighted_color) if num_option == highlighted_option else curses.color_pair(
                    config.default_color)
                if option in selected_options:
                    self.stdscr.addstr(config.start_y + num_option, config.start_x,
                                       f'[x] - {option.text}', color)
                else:
                    self.stdscr.addstr(config.start_y + num_option, config.start_x,
                                       f'[ ] - {option.text}', color)

            # wait for key input
            self.pressed_key = self.stdscr.getch()

        self.stdscr.erase()
        self.stdscr.refresh()
        curses.curs_set(1)
        return selected_options

    def select(self, config: SelectConfig) -> Optional[SelectOption]:
        # Initialize variables
        self.pressed_key = None
        selected_option = None
        num_options = len(config.options)
        highlighted_option = 0
        curses.curs_set(0)

        while True:
            self.stdscr.clear()
            self.stdscr.refresh()

            # Handle last key input
            if self.pressed_key == self.KEY_ENTER:
                selected_option = config.options[highlighted_option]
                self.pressed_key = None
                break
            if self.pressed_key == self.KEY_ESC:
                selected_option = None
                self.pressed_key = None
                break
            if self.pressed_key == self.KEY_SPACE:
                selected_option = config.options[highlighted_option]
                self.pressed_key = None
                break

            if self.pressed_key == curses.KEY_UP:
                highlighted_option = highlighted_option - 1
                if highlighted_option < 0:
                    highlighted_option = num_options - 1

            if self.pressed_key == curses.KEY_DOWN:
                highlighted_option = highlighted_option + 1
                if highlighted_option >= num_options:
                    highlighted_option = 0

            # Draw the window

            # debug
            # import time
            # self.stdscr.addstr(9, 0, "debug")
            # self.stdscr.addstr(10, 0, f'{highlighted_option}')
            # self.stdscr.addstr(11, 0, f'{self.pressed_key}')
            # self.stdscr.addstr(12, 0, f'{time.time()}')

            # Draw helper text
            for txt in config.helper_text:
                self.stdscr.attron(curses.color_pair(txt.color))
                self.stdscr.addstr(txt.start_y, txt.start_x,
                                   txt.text)
                self.stdscr.attroff(curses.color_pair(txt.color))
            # Draw options
            for num_option, option in enumerate(config.options):
                color = curses.color_pair(
                    config.highlighted_color) if num_option == highlighted_option else curses.color_pair(
                    config.default_color)
                self.stdscr.addstr(config.start_y + num_option,
                                   config.start_x, option.text, color)

            # wait for key input
            self.pressed_key = self.stdscr.getch()

        self.stdscr.clear()
        self.stdscr.refresh()
        curses.curs_set(1)
        return selected_option

    def text(self, text: List[WinString]) -> None:
        self.pressed_key = None

        while True:
            self.stdscr.erase()
            self.stdscr.refresh()

            # Handle last key input
            if self.pressed_key == self.KEY_ENTER:
                break
            if self.pressed_key == self.KEY_ESC:
                break

            # Draw the window
            # Draw helper text
            for txt in text:
                self.stdscr.addstr(txt.start_y, txt.start_x,
                                   txt.text, txt.color)

            # wait for key input
            self.pressed_key = self.stdscr.getch()

    def text_input(self, help_text: List[WinString]) -> str:
        # Initialize variables
        input_text = ""
        curses.curs_set(1)
        self.pressed_key = None

        while True:
            self.stdscr.erase()
            self.stdscr.refresh()

            # Handle last key input
            if self.pressed_key:
                if self.pressed_key == self.KEY_ENTER:
                    break
                if self.pressed_key == self.KEY_ESC:
                    input_text = ""
                    break
                if self.pressed_key == self.KEY_BACKSPACE:
                    self.pressed_key = None
                    input_text = input_text[:-1]
                    continue
                if self.pressed_key == curses.KEY_DC:
                    input_text = ""
                    self.pressed_key = None
                    continue
                if 32 <= self.pressed_key <= 126:
                    input_text += chr(self.pressed_key)
                    self.pressed_key = None
                    continue
            # Draw the window
            # Draw helper text
            for txt in help_text:
                self.stdscr.addstr(txt.start_y, txt.start_x,
                                   txt.text, txt.color)
            # Draw input
            self.stdscr.addstr(help_text[-1].start_y + 1, help_text[-1].start_x,
                               input_text)

            # Wait for key input
            self.pressed_key = self.stdscr.getch()
        curses.curs_set(0)
        return input_text


class CliUtils:
    @staticmethod
    def yes_no(question: List[WinString], answers_start_x: int = None, answers_start_y: int = None,
               yes_string: str = "Yes", no_string: str = "No", controller: CLI = None) -> bool:
        controller = CLI() if not controller else controller
        answers_start_x = answers_start_x if answers_start_x else 0
        answers_start_y = answers_start_y if answers_start_y else len(question) + 1

        options = [
            SelectOption(text=yes_string, value=True),
            SelectOption(text=no_string, value=False)
        ]

        config = SelectConfig(
            options=options,
            helper_text=question,
            start_x=answers_start_x,
            start_y=answers_start_y,
            highlighted_color=COLOR__CYAN,
            default_color=COLOR__WHITE
        )
        answer = controller.select(config)
        controller.exit()
        return answer.value
