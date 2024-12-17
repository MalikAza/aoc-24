from copy import deepcopy
from functools import cache
from typing import Tuple
from utils.python import get_file

class Map:
    __slots__ = ['map', 'directions', 'robot_position', 'walls']

    def __init__(self, data: str):
        map, directions = data.split('\n\n')

        self.map = [list(row) for row in map.split('\n')]
        self.directions = tuple([x for x in directions.replace('\n', '')])
        self.robot_position: Tuple[int, int] = self.get_robot_position()
        self.walls: Tuple[Tuple[int, int]] = self.get_walls()

    def get_next_position(self, position: Tuple[int, int], direction: str):
        x, y = position

        match direction:
            case '^':
                return x, y - 1
            case '>':
                return x + 1, y
            case 'v':
                return x, y + 1
            case '<':
                return x - 1, y

    @cache
    def is_position_out_of_bounds(self, position: Tuple[int, int]):
        x, y = position
        return y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[y])
    
    @cache
    def is_position_wall(self, position: Tuple[int, int]):
        return position in self.walls
    
    def get_position_value(self, position: Tuple[int, int]):
        x, y = position
        return self.map[y][x]

    def get_robot_position(self) -> Tuple[int, int]:
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == '@':
                    return (x, y)
                
    def get_walls(self) -> Tuple[Tuple[int, int]]:
        walls = []
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == '#':
                    walls.append((x, y))

        return tuple(walls)
    
    def get_boxes(self) -> Tuple[Tuple[int, int]]:
        boxes = []
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == 'O':
                    boxes.append((x, y))

        return tuple(boxes)
    
    def how_much_distance_before_walls(self, position: Tuple[int, int], direction: str):
        distance = 1
        next_pos = self.get_next_position(position, direction)

        while True:
            if self.get_position_value(next_pos) == '#':
                break

            next_pos = self.get_next_position(next_pos, direction)
            distance += 1

        return distance

    def get_gps_coordinates_from_position(self, position: Tuple[int, int]) -> int:
        # from_top = self.how_much_distance_before_walls(position, '^')
        # from_left = self.how_much_distance_before_walls(position, '<')
        from_top = position[1]
        from_left = position[0]

        return 100 * from_top + from_left
    
    def set_robot_position(self, position: Tuple[int, int]):
        x, y = position
        self.map[self.robot_position[1]][self.robot_position[0]] = '.'
        self.map[y][x] = '@'
        self.robot_position = position

    def robot_attempt_to_push(self, box_position: Tuple[int, int], direction: str):
        next_pos = self.get_next_position(box_position, direction)
        next_pos_value = self.get_position_value(next_pos)

        while True:
            match next_pos_value:
                case '#':
                    break
                case '.':
                    robot_position = self.robot_position
                    self.map[robot_position[1]][robot_position[0]] = '.'

                    self.set_robot_position(box_position)
                    self.map[next_pos[1]][next_pos[0]] = 'O'
                    break
                case 'O':
                    next_pos = self.get_next_position(next_pos, direction)
                    next_pos_value = self.get_position_value(next_pos)
                    continue

    def move_robot_in_direction(self, direction: str):
        next_pos = self.get_next_position(self.robot_position, direction)
        next_pos_value = self.get_position_value(next_pos)

        match next_pos_value:
            case '#':
                pass
            case '.':
                self.set_robot_position(next_pos)
            case 'O':
                self.robot_attempt_to_push(next_pos, direction)

    def run(self):
        for direction in self.directions:
            self.move_robot_in_direction(direction)

    def solve_part_one(self):
        self.run()
        return sum(self.get_gps_coordinates_from_position(box) for box in self.get_boxes())

def run():
    file = get_file(__file__)
    map = Map(file.read())

    print(f'Part one solution is: {map.solve_part_one()}')

if __name__ == '__main__':
    run()