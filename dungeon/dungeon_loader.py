import json

from typing import Any, Dict, List, Optional, Tuple

from dungeon.dungeon import Dungeon
from dungeon.inventory import Inventory
from dungeon.units.enemy import Enemy
from dungeon.units.hero import Hero, HeroAttributes
from dungeon.units.items.item import ItemOnScreen
from dungeon.units.items.wearable.weapon import WeaponArthurSword
from dungeon.units.unit import Unit

import dungeon.tiles as Tiles


class DungeonLoaderException(Exception):
    def __init__(self, message: Optional[str] = None, data: Optional[Any] = None) -> None:
        self.message = message
        self.data = data

    def __str__(self) -> str:
        if self.message:
            msg = f'Error occurred during map loading: {self.message}'
        else:
            msg = 'An error occurred during map loading'

        if self.data:
            return f'{msg} with data {self.data}'
        return msg


class DungeonLoader:
    @staticmethod
    def load(path: str) -> Dungeon:
        # map = List[List[Tile]]
        # units = List[Unit]
        # entities: items...

        with open(path, 'r') as data_in:
            data: List[Dict[str, Any]] = json.load(data_in)

        rooms: List[Tuple[int, int, int, int]] = list()
        doors: List[Tuple[int, int]] = list()
        start: Optional[Tuple[int, int]] = None
        exits: List[Tuple[int, int]] = list()
        units: List[Unit] = list()

        # TODO: items is a stub currently
        dungeon = Dungeon([], [ItemOnScreen(WeaponArthurSword(), 1, 1)], None, [])

        for item in data:
            match item['type']:
                case "room":
                    try:
                        rooms.append((item['top'], item['left'], item['bottom'], item['right']))
                    except KeyError:
                        raise DungeonLoaderException('Could not parse a room item', item)

                case "door":
                    try:
                        doors.append((item['x'], item['y']))
                    except KeyError:
                        raise DungeonLoaderException('Could not parse a door item', item)

                case "start":
                    if start is not None:
                        raise DungeonLoaderException('Multiple starting point items encountered')
                    try:
                        start = (item['x'], item['y'])
                    except KeyError:
                        raise DungeonLoaderException('Could not parse a starting point item', item)

                case "exit":
                    try:
                        exits.append((item['x'], item['y']))
                    except KeyError:
                        raise DungeonLoaderException('Could not parse an exit point item', item)

                case "enemy":
                    enemy_name = item.get('name')
                    match enemy_name:
                        case "basic":
                            try:
                                units.append(Enemy.make_basic_enemy_by_level(dungeon, item['x'], item['y'], item['level']))
                            except KeyError:
                                raise DungeonLoaderException('Could not parse an enemy item', item)
                        case _:
                            raise DungeonLoaderException('Tried to create enemy of unknown type', item)

                case _:
                    raise DungeonLoaderException('Unknown type encountered during map loading', item)

        if start is None:
            raise DungeonLoaderException('')
        # TODO: add means of loading a hero from state
        hero = Hero(*start, HeroAttributes(0, 0, 0, 0, 0, 0), Inventory([]))
        # units.insert(0, hero)

        map = DungeonLoader.__items_to_map(rooms, doors, exits)
        dungeon.map = map
        dungeon.hero = hero
        dungeon.units = units

        return dungeon

    @staticmethod
    def __items_to_map(
        rooms: List[Tuple[int, int, int, int]],
        doors: List[Tuple[int, int]],
        exits: List[Tuple[int, int]],
    ) -> List[List[Tiles.Tile]]:
        min_x = min(room[0] for room in rooms)
        min_y = min(room[1] for room in rooms)
        max_x = max(room[2] for room in rooms)
        max_y = max(room[3] for room in rooms)

        map: List[List[Tiles.Tile]] = list()
        for _ in range(min_x, max_x + 1):
            map.append([Tiles.Empty]*(max_y + 1 - min_y))

        for room in rooms:
            offset_top = room[0] - min_x
            offset_left = room[1] - min_y
            offset_bottom = room[2] - min_x
            offset_right = room[3] - min_y

            for x in range(offset_top, offset_bottom + 1):
                for y in range(offset_left, offset_right + 1):
                    if x == offset_top or x == offset_bottom or y == offset_left or y == offset_right:
                        map[x][y] = Tiles.Wall
                    else:
                        map[x][y] = Tiles.Floor

        for door_x, door_y in doors:
            if map[door_x][door_y] == Tiles.Empty:
                raise DungeonLoaderException('A door cannot be placed on an empty tile')

            map[door_x][door_y] = Tiles.Door

        for exit_x, exit_y in exits:
            if map[exit_x][exit_y] == Tiles.Empty:
                raise DungeonLoaderException('An exit cannot be placed on an empty tile')

            map[exit_x][exit_y] = Tiles.Exit

        return map
