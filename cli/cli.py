import curses
from typing import List, Optional


class WinString:
    def __init__(self, text: str, color: int, start_x: int, start_y: int):
        self.text = text
        self.color = color
        self.start_x = start_x
        self.start_y = start_y


class SelectOption:
    def __init__(self, text: str, identifier: str):
        self.text = text
        self.identifier = identifier


class SelectConfig:
    def __init__(self, options: List[SelectOption], helper_text: List[WinString], default_color: int, highlighted_color: int, start_x: int, start_y: int):
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

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.erase()
        self.stdscr.refresh()

    def multi_select(self, config: SelectConfig) -> List[SelectOption]:
        # Initialize variables
        selected_options = []
        num_options = len(config.options)
        higlighted_option = 0
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
                if config.multiselect:
                    if config.options[higlighted_option] in selected_options:
                        selected_options.remove(
                            config.options[higlighted_option])
                    else:
                        selected_options.append(
                            config.options[higlighted_option])
                else:
                    selected_options = [config.options[higlighted_option]]
                self.pressed_key = None

            if self.pressed_key == curses.KEY_UP:
                higlighted_option = higlighted_option - 1
                if higlighted_option < 0:
                    higlighted_option = num_options - 1
                self.pressed_key = None

            if self.pressed_key == curses.KEY_DOWN:
                higlighted_option = higlighted_option + 1
                if higlighted_option >= num_options:
                    higlighted_option = 0
                self.pressed_key = None

            # Draw the window
            # Draw helper text
            for txt in config.helper_text:
                self.stdscr.addstr(txt.start_y, txt.start_x,
                                   txt.text, txt.color)
            # Draw options
            for num_option, option in enumerate(config.options):
                color = curses.color_pair(
                    config.highlighted_color) if num_option == higlighted_option else curses.color_pair(config.default_color)
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
        curses.cur_set(1)
        return selected_options

    def select(self, config: SelectConfig) -> Optional[SelectOption]:
        # Initialize variables
        selected_option = None
        num_options = len(config.options)
        higlighted_option = 0
        curses.curs_set(0)

        while True:
            self.stdscr.erase()
            self.stdscr.refresh()

            # Handle last key input
            if self.pressed_key == self.KEY_ENTER:
                selected_option = config.options[higlighted_option]
                break
            if self.pressed_key == self.KEY_ESC:
                selected_option = None
                break
            if self.pressed_key == self.KEY_SPACE:
                selected_option = config.options[higlighted_option]
                break

            if self.pressed_key == curses.KEY_UP:
                higlighted_option = higlighted_option - 1
                if higlighted_option < 0:
                    higlighted_option = num_options - 1
                self.pressed_key = None

            if self.pressed_key == curses.KEY_DOWN:
                higlighted_option = higlighted_option + 1
                if higlighted_option >= num_options:
                    higlighted_option = 0
                self.pressed_key = None

            # Draw the window
            # Draw helper text
            for txt in config.helper_text:
                self.stdscr.attron(curses.color_pair(txt.color))
                self.stdscr.addstr(txt.start_y, txt.start_x,
                                   txt.text)
                self.stdscr.attroff(curses.color_pair(txt.color))
            # Draw options
            for num_option, option in enumerate(config.options):
                color = curses.color_pair(
                    config.highlighted_color) if num_option == higlighted_option else curses.color_pair(config.default_color)
                self.stdscr.addstr(config.start_y + num_option,
                                   config.start_x, option.text, color)

            # wait for key input
            self.pressed_key = self.stdscr.getch()

        self.stdscr.erase()
        self.stdscr.refresh()
        curses.curs_set(1)
        return selected_option
