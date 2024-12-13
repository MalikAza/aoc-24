from functools import cache
import random
from typing import Dict, Literal, Tuple, List, Set
from utils.python import get_file
import collections

class Region:
    __slots__ = ['cells', 'search_nodes']
    def __init__(self, first_cell: Tuple[int, int]):
        self.cells: List[Tuple[int, int]] = [first_cell]
        self.search_nodes: List[Tuple[int, int]] = [first_cell]

class Map:
    def __init__(self, data: List[str]):
        self.map = [x.replace('\n', '') for x in data]
        self.__regions: Dict[str, Region] = {}
        self.__region_lookup: Dict[Tuple[int, int], str] = {}
        self.__parse_regions()

    @cache
    def __get_next_cell_id(self, cell_id: str) -> str:
        random.seed(cell_id)
        return f"{cell_id}{random.randint(0, 9)}"

    @cache
    def __is_position_out_of_bounds(self, position: Tuple[int, int]):
        x, y = position
        return y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[y])

    @cache
    def __get_positions_to_down(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (position[0], position[1] + 1)

    @cache
    def __get_positions_to_right(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (position[0] + 1, position[1])

    @cache
    def __get_positions_to_up(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (position[0], position[1] - 1)

    @cache
    def __get_positions_to_left(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (position[0] - 1, position[1])

    @cache
    def __get_positions_adjacent_to(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Down, Right, Up, Left
        """
        return [
            self.__get_positions_to_down(position),
            self.__get_positions_to_right(position),
            self.__get_positions_to_up(position),
            self.__get_positions_to_left(position),
        ]
    
    def __get_cell_letter_from_position(self, cell: Tuple[int, int]):
        if self.__is_position_out_of_bounds(cell):
            return None
        
        return self.map[cell[1]][cell[0]]

    def __get_corners_around_cell(self, cell: Tuple[int, int]):
        cell_letter = self.__get_cell_letter_from_position(cell)
        down, right, up, left = (self.__get_cell_letter_from_position(position) for position in self.__get_positions_adjacent_to(cell))
        corners = 0

        match [left != cell_letter, up != cell_letter].count(True):
            case 2: # convex
                corners += 1
            case 0:
                up_left = self.__get_cell_letter_from_position((cell[0] - 1, cell[1] - 1))
                if up_left != cell_letter: # concave
                    corners += 1
                
        match [up != cell_letter, right != cell_letter].count(True):
            case 2:
                corners += 1
            case 0:
                up_right = self.__get_cell_letter_from_position((cell[0] + 1, cell[1] - 1))
                if up_right != cell_letter:
                    corners += 1
                                
        match [right != cell_letter, down != cell_letter].count(True):
            case 2:
                corners += 1
            case 0:
                right_down = self.__get_cell_letter_from_position((cell[0] + 1, cell[1] + 1))
                if right_down != cell_letter:
                    corners += 1
                
        match [down != cell_letter, left != cell_letter].count(True):
            case 2:
                corners += 1
            case 0:
                down_left = self.__get_cell_letter_from_position((cell[0] - 1, cell[1] + 1))
                if down_left != cell_letter:
                    corners += 1
                
        return corners

    def __bfs(self, region: Region, cell: str):
        visited: Set[Tuple[int, int]] = set(region.cells)
        queue = collections.deque(region.search_nodes)

        while queue:
            x, y = queue.popleft()

            for adjacent_pos in self.__get_positions_adjacent_to((x, y)):
                if (adjacent_pos in visited or 
                    self.__is_position_out_of_bounds(adjacent_pos) or 
                    self.map[adjacent_pos[1]][adjacent_pos[0]] != cell):
                    continue

                region.cells.append(adjacent_pos)
                queue.append(adjacent_pos)
                visited.add(adjacent_pos)
                self.__region_lookup[adjacent_pos] = cell

    def __position_cell_in_regions(self, x: int, y: int, cell: str):
        # Check if this position is already in a region
        if (x, y) in self.__region_lookup:
            return

        # Create a new region or find an existing one
        region_id = cell
        attempt = 0
        while True:
            if region_id not in self.__regions:
                region = Region((x, y))
                self.__regions[region_id] = region
                self.__region_lookup[((x, y))] = cell
                self.__bfs(region, cell)
                break
            
            region_id = self.__get_next_cell_id(f"{cell}_{attempt}")
            attempt += 1

    def __parse_regions(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.__position_cell_in_regions(x, y, cell)

    def __get_region_perimeter(self, region: Region) -> int:
        if len(region.cells) == 1:
            return 4
        
        cell_set = set(region.cells)
        perimeter = 0
        for x, y in region.cells:
            for adjacent_pos in self.__get_positions_adjacent_to((x, y)):
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
    file = get_file(__file__)
    map = Map(file.readlines())

    print(f'Part one solution is: {map.solve(1)}')
    print(f'Part two solution is: {map.solve(2)}')

if __name__ == '__main__':
    run()