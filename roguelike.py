from blessed import Terminal

from controller.input_capture import InputCapture
from controller.controller_main_menu import ControllerMainMenu
from controller.controller_master import ControllerMaster


def init() -> InputCapture:
    terminal = Terminal()
    main_menu_controller = ControllerMainMenu(terminal)
    master_controller = ControllerMaster(terminal, main_menu_controller)
    return InputCapture(terminal, master_controller)


def main() -> None:
    capture = init()
    capture.await_and_forward_input()


if __name__ == '__main__':
    main()
