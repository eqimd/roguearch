from controller.controller_dungeon import ControllerDungeon
from dungeon.dungeon_loader import DungeonLoader
from dungeon.generator.bsp_dungeon_generator import BSPDungeonGenerator
from dungeon.generator.dungeon_builder import DungeonBuilder
from dungeon.inventory import Inventory
from dungeon.units.hero import Hero, HeroAttributes
from dungeon.units.mobs.mob_factory import ScifiMobFactory
from meta.result import *

from blessed import Terminal

from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from screen.screen_main_menu import ScreenMainMenu


class ControllerMainMenu(Controller):
    id = ControllerEnum.MainMenu

    def __init__(self, terminal: Terminal, prev_controller: Controller) -> None:
        super().__init__()
        self.prev_ctrl: Controller = prev_controller
        self.next_ctrl: Controller = self
        self.terminal = terminal
        self.screen = ScreenMainMenu(terminal)
        self.selection = 0

    def draw_screen(self) -> None:
        self.screen.draw(self.selection)

    def prev_controller(self) -> Controller:
        return self.prev_ctrl

    def next_controller(self) -> Controller:
        return self.next_ctrl

    def parse_key(self, key: str) -> Result:
        match key:
            case "w" | "KEY_UP":
                new_selection = (self.selection - 1) % len(self.screen.menu_items)
                self.screen.update(new_selection, self.selection)
                self.selection = new_selection

                return Ok("")
            case "s" | "KEY_DOWN":
                new_selection = (self.selection + 1) % len(self.screen.menu_items)
                self.screen.update(new_selection, self.selection)
                self.selection = new_selection

                return Ok("")
            case "KEY_ENTER":
                match self.selection:
                    case 0:
                        builder = DungeonBuilder(level=0)
                        hero = Hero(0, 0, HeroAttributes(0, 0, 0, 0, 0, 0), Inventory([]))
                        builder.set_map_generator(BSPDungeonGenerator(
                            hero=hero,
                            map_size=48,
                            rooms_amount=10,
                            room_size_factor=2,
                            enemy_count_factor=1,
                            enemy_strategy_probs={
                                'aggressive': 0.5,
                                'coward': 0.25,
                                'passive': 0.25,
                                'basic': 0
                            }
                        ))
                        builder.set_mob_factory(ScifiMobFactory())
                        builder.generate()
                        hero.x, hero.y = builder.get_start_point()
                        self.next_ctrl = ControllerDungeon(self.terminal, builder.dungeon, self)

                        return ChangeToNextController()
                    case 1:
                        dungeon = DungeonLoader.load('./assets/basic_map.json')
                        self.next_ctrl = ControllerDungeon(self.terminal, dungeon, self)
                        
                        return ChangeToNextController()
                    case _:
                        return Fail("Unexpected") # should be never reached
            case _:
                return ForwardInput()
