from typing import List, Literal, Tuple
from utils.python import get_file

class Map:
    __guard_icon: Literal['^', '>', 'v', '<']
    __guard_possible_icons = ['^', '>', 'v', '<']
    __visited_cells: List[Tuple[int, int]] = []

    def __init__(self, data: str):
        self.__map = [x for x in data.split('\n')]
        self.__guard_position = self.__get_guard_initial_position()

    def __get_guard_initial_position(self):
        for y, row in enumerate(self.__map):
            for x, cell in enumerate(row):
                if cell in self.__guard_possible_icons:
                    self.__guard_icon = cell
                    return x, y

    def __get_next_position(self):
        x, y = self.__guard_position

        match self.__guard_icon:
            case '^':
                return x, y - 1
            case '>':
                return x + 1, y
            case 'v':
                return x, y + 1
            case '<':
                return x - 1, y
            
    def __turn_guard_right(self):
        match self.__guard_icon:
            case '^':
                self.__guard_icon = '>'
            case '>':
                self.__guard_icon = 'v'
            case 'v':
                self.__guard_icon = '<'
            case '<':
                self.__guard_icon = '^'

    def __is_position_out_of_bounds(self, x, y):
        return y < 0 or y >= len(self.__map) or x < 0 or x >= len(self.__map[y])

    def __is_guard_out_of_bounds(self):
        x, y = self.__guard_position
        return self.__is_position_out_of_bounds(x, y)

    def solve_part_one(self):
        while not self.__is_guard_out_of_bounds():
            self.__visited_cells.append(self.__guard_position)
            next_pos_x, next_pos_y = self.__get_next_position()
            if not self.__is_position_out_of_bounds(next_pos_x, next_pos_y) and self.__map[next_pos_y][next_pos_x] == '#':
                self.__turn_guard_right()
                next_pos_x, next_pos_y = self.__get_next_position()

            self.__guard_position = next_pos_x, next_pos_y

        return len(set(self.__visited_cells))

def run():
    file = get_file(__file__)
    map = Map(file.read())

    print("Part one solution is: ", map.solve_part_one())

if __name__ == '__main__':
    run()