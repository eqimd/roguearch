from blessed import Terminal
from controller.controller_exit import ControllerExit

from controller.input_capture import InputCapture
from controller.controller_main_menu import ControllerMainMenu
from controller.controller_master import ControllerMaster


def init() -> InputCapture:
    terminal = Terminal()

    controller_master = ControllerMaster(terminal)
    controller_main_menu = ControllerMainMenu(terminal, ControllerExit())

    controller_master.set_underlying_controller(controller_main_menu)

    return InputCapture(terminal, controller_master)


def main() -> None:
    capture = init()
    capture.await_and_forward_input()


if __name__ == '__main__':
    main()
