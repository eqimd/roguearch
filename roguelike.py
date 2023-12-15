from blessed import Terminal
from controller.controller_exit import ControllerExit

from controller.input_capture import InputCapture
from controller.controller_main_menu import ControllerMainMenu
from controller.controller_master import ControllerMaster
from dungeon.generator.bsp_map_generator import BSPMapGenerator
from dungeon.generator.dungeon_generator import DungeonGenerator


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

    generator = DungeonGenerator()
    generator.set_map_generator(BSPMapGenerator(48, 10, 2))
    generator.generate()
    tiles = generator.tiles

    print(term.clear)
    for idx, row in enumerate(tiles):
        print(term.move_xy(0, idx) + ''.join(str(x) for x in row))

    print(term.move_xy(0, 49))
