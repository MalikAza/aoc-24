from copy import deepcopy
from functools import cache
from typing import Tuple
from utils.python import get_input_file_from_script_file, MapUtils

class Map(MapUtils):
    __slots__ = ['map', 'directions', 'robot_position', 'walls']

    def __init__(self, data: str):
        map, directions = data.split('\n\n')

        self.map = [list(row) for row in map.split('\n')]
        self.directions = tuple([x for x in directions.replace('\n', '')])
        self.robot_position: Tuple[int, int] = self.get_robot_position()
        self.walls: Tuple[Tuple[int, int]] = self.get_walls()

    @property
    def ROBOT_SYMBOL(self):
        return '@'
    
    @property
    def WALL_SYMBOL(self):
        return '#'
    
    @property
    def BOX_SYMBOL(self):
        return 'O'
    
    @property
    def EMPTY_SYMBOL(self):
        return '.'
    
    @cache
    def is_position_wall(self, position: Tuple[int, int]):
        return position in self.walls

    def get_robot_position(self) -> Tuple[int, int]:
        return self.search_value(self.ROBOT_SYMBOL)[0]
                
    def get_walls(self) -> Tuple[Tuple[int, int]]:
        return self.search_value(self.WALL_SYMBOL)
    
    def get_boxes(self) -> Tuple[Tuple[int, int]]:
        return self.search_value(self.BOX_SYMBOL)
    
    def how_much_distance_before_walls(self, position: Tuple[int, int], direction: str):
        distance = 1
        next_pos = self.get_position_to_direction(position, direction)

        while True:
            if self.get_cell_value_from_position(next_pos) == self.WALL_SYMBOL:
                break

            next_pos = self.get_position_to_direction(next_pos, direction)
            distance += 1

        return distance

    def get_gps_coordinates_from_position(self, position: Tuple[int, int]) -> int:
        # from_top = self.how_much_distance_before_walls(position, '^')
        # from_left = self.how_much_distance_before_walls(position, '<')
        from_top = position[1]
        from_left = position[0]

        return 100 * from_top + from_left
    
    def set_robot_position(self, position: Tuple[int, int]):
        self.map[self.robot_position[1]][self.robot_position[0]] = self.EMPTY_SYMBOL
        self.map[position[1]][position[0]] = self.ROBOT_SYMBOL
        self.robot_position = position

    def robot_attempt_to_push(self, box_position: Tuple[int, int], direction: str):
        next_pos = self.get_position_to_direction(box_position, direction)
        next_pos_value = self.get_cell_value_from_position(next_pos)

        while True:
            match next_pos_value:
                case self.WALL_SYMBOL:
                    break
                case self.EMPTY_SYMBOL:
                    robot_position = self.robot_position
                    self.map[robot_position[1]][robot_position[0]] = self.EMPTY_SYMBOL

                    self.set_robot_position(box_position)
                    self.map[next_pos[1]][next_pos[0]] = self.BOX_SYMBOL
                    break
                case self.BOX_SYMBOL:
                    next_pos = self.get_position_to_direction(next_pos, direction)
                    next_pos_value = self.get_cell_value_from_position(next_pos)
                    continue

    def move_robot_in_direction(self, direction: str):
        next_pos = self.get_position_to_direction(self.robot_position, direction)
        next_pos_value = self.get_cell_value_from_position(next_pos)

        match next_pos_value:
            case self.WALL_SYMBOL:
                pass
            case self.EMPTY_SYMBOL:
                self.set_robot_position(next_pos)
            case self.BOX_SYMBOL:
                self.robot_attempt_to_push(next_pos, direction)

    def run(self):
        for direction in self.directions:
            self.move_robot_in_direction(direction)

    def solve_part_one(self):
        self.run()
        return sum(self.get_gps_coordinates_from_position(box) for box in self.get_boxes())

def run():
    file = get_input_file_from_script_file(__file__)
    map = Map(file.read())

    print(f'Part one solution is: {map.solve_part_one()}')

if __name__ == '__main__':
    run()