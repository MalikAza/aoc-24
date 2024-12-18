from typing import List, Literal, Tuple
from utils.python import get_input_file_from_script_file, MapUtils

class Map(MapUtils):
    __guard_icon: Literal['^', '>', 'v', '<']
    __visited_cells: List[Tuple[int, int]] = []

    def __init__(self, data: str):
        super().__init__(data, start_value='^')
        self.__guard_position = self.start
        self.__guard_icon = '^'

    def __get_next_guard_position(self) -> Tuple[int, int]:
        return self.get_position_to_direction(self.__guard_position, self.__guard_icon)
            
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

    def __is_guard_out_of_bounds(self):
        return self.is_position_out_of_bounds(self.__guard_position)

    def solve_part_one(self):
        while not self.__is_guard_out_of_bounds():
            self.__visited_cells.append(self.__guard_position)
            next_guard_pos = self.__get_next_guard_position()
            if not self.is_position_out_of_bounds(next_guard_pos) and self.get_cell_value_from_position(next_guard_pos) == '#':
                self.__turn_guard_right()
                next_guard_pos = self.get_position_to_direction(self.__guard_position, self.__guard_icon)

            self.__guard_position = next_guard_pos

        return len(set(self.__visited_cells))

def run():
    file = get_input_file_from_script_file(__file__)
    map = Map(file.read())

    print("Part one solution is: ", map.solve_part_one())

if __name__ == '__main__':
    run()