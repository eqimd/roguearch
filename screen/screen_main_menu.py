from blessed import Terminal

from screen.screen import Screen


class ScreenMainMenu(Screen):
    # дублирование имен в ControllerMainMenu
    menu_items = [
        'Start Game',
        'Load Game'
    ]

    def __init__(self, terminal: Terminal) -> None:
        self.terminal = terminal

    def draw(self, selection: int) -> None:
        with self.terminal.location(0, 0):
            print('='*self.terminal.width, end='')

        welcome_str = "Welcome to RogueArch!"
        with self.terminal.location((self.terminal.width - len(welcome_str)) // 2, 2):
            print(welcome_str, end='')

        with self.terminal.location(0, self.terminal.height - 1):
            print('='*self.terminal.width, end='')

        for idx, menu_item in enumerate(self.menu_items):
            with self.terminal.location(1, 4 + idx):
                if idx == selection:
                    print(self.terminal.underline(menu_item), end='')
                else:
                    print(menu_item, end='')

    def update(self, new_pos: int, old_pos: int) -> None:
        with self.terminal.location(1, 4 + old_pos):
            print(self.menu_items[old_pos], end='')

        with self.terminal.location(1, 4 + new_pos):
            print(self.terminal.underline(self.menu_items[new_pos]), end='')
