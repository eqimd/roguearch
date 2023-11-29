from blessed import Terminal
from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from controller.controller_inventory import ControllerInventory
from dungeon.dungeon import Dungeon
from dungeon.units.actions.actions import MoveAction
from meta.result import ChangeToNextController, ChangeToPrevController, ForwardInput, Ok, Result
from screen.screen_dungeon import ScreenDungeon


class ControllerDungeon(Controller):
    id = ControllerEnum.Dungeon

    def __init__(self, terminal: Terminal, dungeon: Dungeon, prev_controller: Controller):
        super().__init__
        self.prev_ctrl = prev_controller
        self.next_ctrl = self
        self.screen = ScreenDungeon(terminal, dungeon)
        self.terminal = terminal
        self.set_underlying_dungeon(dungeon)

    def draw_screen(self) -> None:
        self.screen.draw()

    def prev_controller(self) -> Controller:
        return self.prev_ctrl

    def next_controller(self) -> Controller:
        return self.next_ctrl
    
    def parse_key(self, key: str) -> Result:
        match key:
            case 'w':
                hero = self.dungeon.hero
                hero.set_action(MoveAction(hero, (0, -1), self.dungeon.units, self.dungeon.map))

                self.perform_game_move()

                return Ok('')
            case 's':
                hero = self.dungeon.hero
                hero.set_action(MoveAction(hero, (0, 1), self.dungeon.units, self.dungeon.map))

                self.perform_game_move()

                return Ok('')
            case 'a':
                hero = self.dungeon.hero
                hero.set_action(MoveAction(hero, (-1, 0), self.dungeon.units, self.dungeon.map))

                self.perform_game_move()

                return Ok('')
            case 'd':
                hero = self.dungeon.hero
                hero.set_action(MoveAction(hero, (1, 0), self.dungeon.units, self.dungeon.map))

                self.perform_game_move()

                return Ok('')
            case 'q':
                return ChangeToPrevController()
            case 'e':
                controller_inventory = ControllerInventory(self.terminal, self.dungeon.hero.inventory, self)
                self.next_ctrl = controller_inventory

                return ChangeToNextController()
            
        return ForwardInput()
    

    def perform_game_move(self) -> None:
        hero_res = self.dungeon.hero.perform_action()

        # for unit in self.dungeon.units:
        #     unit.perform_action()
        # 

        self.draw_screen()
        self.screen.draw_msg(hero_res.msg)


    def set_underlying_dungeon(self, dungeon: Dungeon):
        self.dungeon = dungeon
