from functools import cache
import random
from typing import Dict, Literal, Tuple, List, Set
from utils.python import get_input_file_from_script_file, MapUtils, solution_print
import collections

class Region:
    __slots__ = ['cells', 'search_nodes']
    def __init__(self, first_cell: Tuple[int, int]):
        self.cells: List[Tuple[int, int]] = [first_cell]
        self.search_nodes: List[Tuple[int, int]] = [first_cell]

class Map(MapUtils):
    def __init__(self, data: str):
        super().__init__(data)
        self.__regions: Dict[str, Region] = {}
        self.__region_lookup: Dict[Tuple[int, int], str] = {}
        self.__parse_regions()

    @cache
    def __get_next_cell_id(self, cell_id: str) -> str:
        random.seed(cell_id)
        return f"{cell_id}{random.randint(0, 9)}"

    def __get_corners_around_cell(self, cell: Tuple[int, int]):
        cell_letter = self.get_cell_value_from_position(cell)
        around_positions = self.get_positions_around(cell)

        down = self.get_cell_value_from_position(around_positions['down'])
        right = self.get_cell_value_from_position(around_positions['right'])
        up = self.get_cell_value_from_position(around_positions['up'])
        left = self.get_cell_value_from_position(around_positions['left'])

        corners = 0

        match [left != cell_letter, up != cell_letter].count(True):
            case 2: # convex
                corners += 1
            case 0:
                up_left = self.get_cell_value_from_position(around_positions['up_left'])
                if up_left != cell_letter: # concave
                    corners += 1
                
        match [up != cell_letter, right != cell_letter].count(True):
            case 2:
                corners += 1
            case 0:
                up_right = self.get_cell_value_from_position(around_positions['up_right'])
                if up_right != cell_letter:
                    corners += 1
                                
        match [right != cell_letter, down != cell_letter].count(True):
            case 2:
                corners += 1
            case 0:
                down_right = self.get_cell_value_from_position(around_positions['down_right'])
                if down_right != cell_letter:
                    corners += 1
                
        match [down != cell_letter, left != cell_letter].count(True):
            case 2:
                corners += 1
            case 0:
                down_left = self.get_cell_value_from_position(around_positions['down_left'])
                if down_left != cell_letter:
                    corners += 1
                
        return corners

    def __bfs(self, region: Region, cell: str):
        visited: Set[Tuple[int, int]] = set(region.cells)
        queue = collections.deque(region.search_nodes)

        while queue:
            position = queue.popleft()

            for adjacent_pos in self.get_positions_in_NSEW(position).values():
                if (adjacent_pos in visited or 
                    self.is_position_out_of_bounds(adjacent_pos) or 
                    self.get_cell_value_from_position(adjacent_pos) != cell):
                    continue

                region.cells.append(adjacent_pos)
                queue.append(adjacent_pos)
                visited.add(adjacent_pos)
                self.__region_lookup[adjacent_pos] = cell

    def __position_cell_in_regions(self, cell_pos: Tuple[int, int], cell: str):
        # Check if this position is already in a region
        if cell_pos in self.__region_lookup:
            return

        # Create a new region or find an existing one
        region_id = cell
        attempt = 0
        while True:
            if region_id not in self.__regions:
                region = Region(cell_pos)
                self.__regions[region_id] = region
                self.__region_lookup[(cell_pos)] = cell
                self.__bfs(region, cell)
                break
            
            region_id = self.__get_next_cell_id(f"{cell}_{attempt}")
            attempt += 1

    def __parse_regions(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.__position_cell_in_regions((x, y), cell)

    def __get_region_perimeter(self, region: Region) -> int:
        if len(region.cells) == 1:
            return 4
        
        cell_set = set(region.cells)
        perimeter = 0
        for cell_pos in region.cells:
            for adjacent_pos in self.get_positions_in_NSEW(cell_pos).values():
                if adjacent_pos not in cell_set:
                    perimeter += 1

        return perimeter
    
    def __get_region_corners_number(self, region: Region) -> int:
        if len(region.cells) == 1:
            return 4
        
        return sum([self.__get_corners_around_cell(cell) for cell in region.cells])
    
    def __get_region_price(self, region: Region, part: Literal[1, 2]) -> int:
        match part:
            case 1:
                return len(region.cells) * self.__get_region_perimeter(region)
            case 2:
                return len(region.cells) * self.__get_region_corners_number(region)
    
    def __map_price(self, part: Literal[1, 2]) -> int:
        return sum(self.__get_region_price(region, part) for region in self.__regions.values())
    
    def solve(self, part: Literal[1, 2]) -> int:
        return self.__map_price(part)

def run():
    file = get_input_file_from_script_file(__file__)
    map = Map(file.read())

    solution_print(1, map.solve(1))
    solution_print(2, map.solve(2))

if __name__ == '__main__':
    run()