from blessed import Terminal
from dataclasses import dataclass
from time import sleep
from numpy.random import poisson
from random import randint
from typing import List, Tuple, Optional, cast

from dungeon.generator.map_generator import MapGenerator
import dungeon.tiles as Tiles


@dataclass
class Room:
    top: int
    left: int
    bottom: int
    right: int


@dataclass
class Cell:
    top: int
    left: int
    bottom: int
    right: int
    depth: int
    room: Optional[Room] = None
    children: Optional[Tuple[int, int]] = None


class BSPMapGenerator(MapGenerator):
    def __init__(self, map_size, rooms_amount, room_size_factor):
        super().__init__(map_size, map_size)

        self.map_size = map_size
        self.rooms_amount = rooms_amount
        self.room_size_factor = room_size_factor

    def make_floor(self):
        cells: List[Cell] = list()
        cells.append(Cell(0, 0, self.map_size - 1, self.map_size - 1, 0))

        rooms = 1
        idx = 0
        while rooms < self.rooms_amount:
            print(rooms, idx)
            if idx >= len(cells):
                break

            cell_to_split = cells[idx]

            # even depth: split vertically, odd depth: split horizontally
            if cell_to_split.depth % 2:
                try:
                    split = randint(cell_to_split.top + 7, cell_to_split.bottom - 7)
                except:
                    idx += 1
                    continue
                cells.append(Cell(cell_to_split.top, cell_to_split.left, split, cell_to_split.right, cell_to_split.depth + 1))
                cells.append(Cell(split, cell_to_split.left, cell_to_split.bottom, cell_to_split.right, cell_to_split.depth + 1))
                cell_to_split.children = (len(cells) - 2, len(cells) - 1)
            else:
                try:
                    split = randint(cell_to_split.left + 5, cell_to_split.right - 5)
                except:
                    idx += 1
                    continue
                cells.append(Cell(cell_to_split.top, cell_to_split.left, cell_to_split.bottom, split, cell_to_split.depth + 1))
                cells.append(Cell(cell_to_split.top, split, cell_to_split.bottom, cell_to_split.right, cell_to_split.depth + 1))
                cell_to_split.children = (len(cells) - 2, len(cells) - 1)
            rooms += 1
            idx += 1
        
        for cell in cells:
            if cell.children is None:
                # width_x = randint(3, cell.right - cell.left - 1)
                # width_y = randint(3, cell.bottom - cell.top - 1)
                width_x = min(3 + poisson(lam=self.room_size_factor), cell.right - cell.left - 1)
                width_y = min(3 + poisson(lam=self.room_size_factor), cell.bottom - cell.top - 1)
                left = randint(cell.left + 1, cell.right - width_x)
                top = randint(cell.top + 1, cell.bottom - width_y)
                cell.room = Room(top, left, top + width_y - 1, left + width_x - 1)
        
        for cell in cells:
            if cell.room is not None:
                for y in range(cell.room.top, cell.room.bottom + 1):
                    for x in range(cell.room.left, cell.room.right + 1):
                        self.tiles[x][y] = Tiles.Floor

        for idx in range(len(cells) - 1, -1, -1):
            parent_cell = cells[idx]
            if parent_cell.children is not None:
                child_left = cells[parent_cell.children[0]]
                child_right = cells[parent_cell.children[1]]
                child_left_room = cast(Room, child_left.room)
                child_right_room = cast(Room, child_right.room)
                
                # even depth: split vertically, odd depth: split horizontally
                if parent_cell.depth % 2:
                    left_bound = max(child_left_room.left, child_right_room.left)
                    right_bound = min(child_left_room.right, child_right_room.right)
                    if left_bound <= right_bound:
                        road_x = randint(left_bound, right_bound)
                        min_y = min(child_left.top, child_right.top)
                        max_y = max(child_left.bottom, child_right.bottom)
                        min_y_valid = min([y for y in range(min_y, max_y + 1) if self.tiles[road_x][y] == Tiles.Floor])
                        max_y_valid = max([y for y in range(min_y, max_y + 1) if self.tiles[road_x][y] == Tiles.Floor])
                        for y in range(min_y_valid, max_y_valid + 1):
                            self.tiles[road_x][y] = Tiles.Floor
                    else:
                        left_x = randint(child_left_room.left, child_left_room.right)
                        right_x = randint(child_right_room.left, child_right_room.right)
                        top_y = min(child_left_room.bottom, child_right_room.bottom)
                        bottom_y = max(child_left_room.top, child_right_room.top)

                        # if it works, then don't touch it
                        if child_left_room.bottom < child_right_room.bottom:
                            while self.tiles[left_x][top_y] != Tiles.Floor:
                                top_y -= 1
                            while self.tiles[right_x][bottom_y] != Tiles.Floor:
                                bottom_y += 1
                        else:
                            while self.tiles[right_x][top_y] != Tiles.Floor:
                                top_y -= 1
                            while self.tiles[left_x][bottom_y] != Tiles.Floor:
                                bottom_y += 1
                        
                        road_y = randint(top_y + 1, bottom_y - 1)
                        for y in range(top_y, road_y + 1):
                            self.tiles[left_x][y] = Tiles.Floor
                        for x in range(min(left_x, right_x), max(left_x, right_x) + 1):
                            self.tiles[x][road_y] = Tiles.Floor
                        for y in range(road_y, bottom_y + 1):
                            self.tiles[right_x][y] = Tiles.Floor

                else:
                    top_bound = max(child_left_room.top, child_right_room.top)
                    bottom_bound = min(child_left_room.bottom, child_right_room.bottom)
                    if top_bound <= bottom_bound:
                        road_y = randint(top_bound, bottom_bound)
                        min_x = min(child_left.left, child_right.left)
                        max_x = max(child_left.right, child_right.right)
                        min_x_valid = min([x for x in range(min_x, max_x + 1) if self.tiles[x][road_y] == Tiles.Floor])
                        max_x_valid = max([x for x in range(min_x, max_x + 1) if self.tiles[x][road_y] == Tiles.Floor])
                        for x in range(min_x_valid, max_x_valid + 1):
                            self.tiles[x][road_y] = Tiles.Floor
                    else:
                        left_y = randint(child_left_room.top, child_left_room.bottom)
                        right_y = randint(child_right_room.top, child_right_room.bottom)
                        top_x = min(child_left_room.right, child_right_room.right)
                        bottom_x = max(child_left_room.left, child_right_room.left)

                        # if it works, then don't touch it
                        if child_left_room.right < child_right_room.right:
                            while self.tiles[top_x][left_y] != Tiles.Floor:
                                top_x -= 1
                            while self.tiles[bottom_x][right_y] != Tiles.Floor:
                                bottom_x += 1
                        else:
                            while self.tiles[top_x][right_y] != Tiles.Floor:
                                top_x -= 1
                            while self.tiles[bottom_x][left_y] != Tiles.Floor:
                                bottom_x += 1

                        road_x = randint(top_x + 1, bottom_x - 1)
                        for x in range(top_x, road_x + 1):
                            self.tiles[x][left_y] = Tiles.Floor
                        for y in range(min(left_y, right_y), max(left_y, right_y) + 1):
                            self.tiles[road_x][y] = Tiles.Floor
                        for x in range(road_x, bottom_x + 1):
                            self.tiles[x][right_y] = Tiles.Floor

                parent_cell.room = Room(
                    min(child_left_room.top, child_right_room.top),
                    min(child_left_room.left, child_right_room.left),
                    max(child_left_room.bottom, child_right_room.bottom),
                    max(child_left_room.right, child_right_room.right),
                )
    
    def make_doors(self):
        for y in range(0, self.map_size):
            for x in range(0, self.map_size):
                l_orient = self.__get_l_shape_orientation(x, y, self.map_size)
                if l_orient == 0 and not self.__is_angle_shape(x, y - 1, self.map_size):
                    self.tiles[y][x] = Tiles.Door
                if l_orient == 1 and not self.__is_angle_shape(x - 1, y, self.map_size):
                    self.tiles[y][x] = Tiles.Door
                if l_orient == 2 and not self.__is_angle_shape(x, y + 1, self.map_size):
                    self.tiles[y][x] = Tiles.Door
                if l_orient == 3 and not self.__is_angle_shape(x + 1, y, self.map_size):
                    self.tiles[y][x] = Tiles.Door

                t_orient = self.__get_t_shape_orientation(x, y, self.map_size)
                if t_orient == 0 and not self.__is_cross_shape(x, y - 1, self.map_size):
                    self.tiles[y][x] = Tiles.Door
                if t_orient == 1 and not self.__is_cross_shape(x - 1, y, self.map_size):
                    self.tiles[y][x] = Tiles.Door
                if t_orient == 2 and not self.__is_cross_shape(x, y + 1, self.map_size):
                    self.tiles[y][x] = Tiles.Door
                if t_orient == 3 and not self.__is_cross_shape(x + 1, y, self.map_size):
                    self.tiles[y][x] = Tiles.Door
    
    def make_walls(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                if self.tiles[x][y] == Tiles.Empty and self.__has_floor_nearby(y, x, self.map_size):
                    self.tiles[x][y] = Tiles.Wall

    def __get_l_shape_orientation(self, center_x, center_y, map_size) -> int:
        tl, t, tr, l, c, r, bl, b, br = self.__get_tile_square(center_x, center_y, map_size)

        if tl + t + tr + l + c + r + bl + b + br != 4:
            return -1
        if (tl or tr) and t and c and b:
            return 0
        if (tl or bl) and l and c and r:
            return 1
        if (bl or br) and t and c and b:
            return 2
        if (tr or br) and l and c and r:
            return 3
        return -1
    
    def __get_t_shape_orientation(self, center_x, center_y, map_size) -> int:
        tl, t, tr, l, c, r, bl, b, br = self.__get_tile_square(center_x, center_y, map_size)

        if tl + t + tr + l + c + r + bl + b + br != 4:
            return -1
        if c and tl and t and tr:
            return 0
        if c and tl and l and bl:
            return 1
        if c and bl and b and br:
            return 2
        if c and tr and t and br:
            return 3
        return -1

    def __is_cross_shape(self, center_x, center_y, map_size) -> bool:
        tl, t, tr, l, c, r, bl, b, br = self.__get_tile_square(center_x, center_y, map_size)

        return t and l and c and r and b and (not tl) and (not tr) and (not bl) and (not br)
    
    def __is_angle_shape(self, center_x, center_y, map_size) -> bool:
        tl, t, tr, l, c, r, bl, b, br = self.__get_tile_square(center_x, center_y, map_size)

        if tl + t + tr + l + c + r + bl + b + br != 3:
            return False
        if t and c and l:
            return True
        if b and c and l:
            return True
        if b and c and r:
            return True
        if t and c and r:
            return True
        return False

    def __has_floor_nearby(self, center_x, center_y, map_size) -> bool:
        tl, t, tr, l, c, r, bl, b, br = self.__get_tile_square(center_x, center_y, map_size)

        return tl + t + tr + l + c + r + bl + b + br > 0

    def __get_tile_square(self, center_x, center_y, map_size):
        tl = self.tiles[center_y - 1][center_x - 1] == Tiles.Floor if center_x > 0 and center_y > 0 else False
        t = self.tiles[center_y - 1][center_x] == Tiles.Floor if center_y > 0 else False
        tr = self.tiles[center_y - 1][center_x + 1] == Tiles.Floor if center_y > 0 and center_x < map_size - 1 else False
        l = self.tiles[center_y][center_x - 1] == Tiles.Floor if center_x > 0 else False
        c = self.tiles[center_y][center_x] == Tiles.Floor
        r = self.tiles[center_y][center_x + 1] == Tiles.Floor if center_x < map_size - 1 else False
        bl = self.tiles[center_y + 1][center_x - 1] == Tiles.Floor if center_y < map_size - 1 and center_x > 0 else False
        b = self.tiles[center_y + 1][center_x] == Tiles.Floor if center_y < map_size - 1 else False
        br = self.tiles[center_y + 1][center_x + 1] == Tiles.Floor if center_y < map_size - 1 and center_x < map_size - 1 else False
        
        return tl, t, tr, l, c, r, bl, b, br
