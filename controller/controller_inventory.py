from blessed import Terminal
from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from dungeon.inventory import Inventory
from meta.result import ChangeToPrevController, ForwardInput, Result

from screen.screen_inventory import ScreenInventory


class ControllerInventory(Controller):
    id = ControllerEnum.Inventory

    def __init__(self, terminal: Terminal, inventory: Inventory, prev_controller: Controller):
        self.screen = ScreenInventory(terminal, inventory)
        self.terminal = terminal
        self.inventory = inventory
        self.prev_ctrl = prev_controller

    def draw_screen(self) -> None:
        self.screen.draw()
    
    def parse_key(self, key: str) -> Result:
        match key:
            case 'q':
                return ChangeToPrevController()
            
        return ForwardInput()
    
    def prev_controller(self) -> Controller:
        return self.prev_ctrl
    
    def next_controller(self) -> Controller:
        return self