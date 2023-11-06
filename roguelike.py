from blessed import Terminal

from controller.input_capture import InputCapture
from controller.controller_main_menu import ControllerMainMenu
from controller.controller_master import ControllerMaster


def init() -> InputCapture:
    terminal = Terminal()
    controller_main_menu = ControllerMainMenu(terminal)
    controller_master = ControllerMaster(terminal, controller_main_menu)
    return InputCapture(terminal, controller_master)


def main() -> None:
    capture = init()
    capture.await_and_forward_input()


if __name__ == '__main__':
    main()
