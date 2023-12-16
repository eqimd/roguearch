from blessed import Terminal
from controller.controller_exit import ControllerExit

from controller.input_capture import InputCapture
from controller.controller_main_menu import ControllerMainMenu
from controller.controller_master import ControllerMaster
from dungeon.generator.bsp_map_generator import BSPMapGenerator
from dungeon.generator.map_builder import MapBuilder


def init() -> InputCapture:
    terminal = Terminal()

    controller_master = ControllerMaster(terminal)
    controller_main_menu = ControllerMainMenu(terminal, ControllerExit())

    controller_master.set_underlying_controller(controller_main_menu)

    return InputCapture(terminal, controller_master)


def main() -> None:
    capture = init()
    capture.await_and_forward_input()

# if __name__ == '__main__':
#     main()

if __name__ == '__main__':
    term = Terminal()

    builder = MapBuilder()
    builder.set_map_generator(BSPMapGenerator(48, 10, 2))
    builder.generate()

    print(term.clear)
    for idx, row in enumerate(builder.tiles):
        print(term.move_xy(0, idx) + ''.join(str(x) for x in row))

    start_point = builder.get_start_point()
    end_point = builder.get_end_point()
    print(term.move_xy(start_point[1], start_point[0]) + '@')
    print(term.move_xy(end_point[1], end_point[0]) + 'X')
    print(term.move_xy(0, 49))
