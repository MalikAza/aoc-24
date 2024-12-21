import re
from typing import List, Tuple, Literal
from utils.python import get_input_file_from_script_file, MapUtils, solution_print

DIRECTIONS = Literal['down_right', 'down_left', 'up_right', 'up_left', 'down', 'right', 'up', 'left']

class Map(MapUtils):
    def __init__(self, data: str):
        super().__init__(data)

    def __how_many_xmas_or_samx(self, to_search: str) -> int:
        pattern = re.compile(r'(XMAS|SAMX)')
        matches = pattern.findall(to_search)

        return len(matches)
    
    def __regroup_max_four_elements_in_direction_from_position(self, pos: Tuple[int, int], direction: DIRECTIONS):
        positions = [pos]
        current_pos = pos
        for _ in range(3):
            current_pos = self.get_positions_around(current_pos).get(direction)

            if self.is_position_out_of_bounds(current_pos):
                break

            positions.append(current_pos)

        return ''.join(self.get_cell_value_from_position(p) for p in positions)
    
    def __how_many_in_direction_for_position(self, pos: Tuple[int, int], directions: List[DIRECTIONS]) -> int:
        return sum([
            self.__how_many_xmas_or_samx(self.__regroup_max_four_elements_in_direction_from_position(pos, direction))
            for direction in directions
        ])
    
    def __is_position_x_mased(self, pos: Tuple[int, int]) -> bool:
        value = self.get_cell_value_from_position(pos)

        if value != 'A':
            return False
        
        corners = self.get_positions_in_corners(pos)

        # Ms at bottom and Ss at top
        if (self.get_cell_value_from_position(corners.get('down_left')) == 'M'
        and self.get_cell_value_from_position(corners.get('down_right')) == 'M'
        and self.get_cell_value_from_position(corners.get('up_left')) == 'S'
        and self.get_cell_value_from_position(corners.get('up_right')) == 'S'
        ): return True

        # Ms at top and Ss at bottom
        if (self.get_cell_value_from_position(corners.get('down_left')) == 'S'
        and self.get_cell_value_from_position(corners.get('down_right')) == 'S'
        and self.get_cell_value_from_position(corners.get('up_left')) == 'M'
        and self.get_cell_value_from_position(corners.get('up_right')) == 'M'
        ): return True

        # Ms at left and Ss at right
        if (self.get_cell_value_from_position(corners.get('down_left')) == 'M'
        and self.get_cell_value_from_position(corners.get('up_left')) == 'M'
        and self.get_cell_value_from_position(corners.get('down_right')) == 'S'
        and self.get_cell_value_from_position(corners.get('up_right')) == 'S'
        ): return True

        # Ms at right and Ss at left
        if (self.get_cell_value_from_position(corners.get('down_left')) == 'S'
        and self.get_cell_value_from_position(corners.get('up_left')) == 'S'
        and self.get_cell_value_from_position(corners.get('down_right')) == 'M'
        and self.get_cell_value_from_position(corners.get('up_right')) == 'M'
        ): return True

        return False
    
    def solve(self, part: Literal[1, 2]) -> int:
        match part:
            case 1:
                return sum(
                    self.__how_many_in_direction_for_position((x, y), ['down', 'right', 'down_right', 'down_left'])
                    for y, row in enumerate(self.map)
                    for x, _ in enumerate(row)
                )
            case 2:
                return sum(
                    1
                    for y, row in enumerate(self.map)
                    for x, _ in enumerate(row)
                    if self.__is_position_x_mased((x, y))
                )

def run():
    file = get_input_file_from_script_file(__file__)
    map = Map(file.read())

    solution_print(1, map.solve(1))
    solution_print(2, map.solve(2))

if __name__ == '__main__':
    run()