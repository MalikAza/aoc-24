from functools import cache
import random
from typing import Dict, Tuple, List, Set
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
    def is_position_out_of_bounds(self, x, y):
        return y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[y])

    @cache
    def get_positions_adjacent_to(self, x, y) -> List[Tuple[int, int]]:
        """
        Down, Right, Up, Left
        """
        return [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
    
    def __bfs(self, region: Region, cell: str):
        visited: Set[Tuple[int, int]] = set(region.cells)
        queue = collections.deque(region.search_nodes)

        while queue:
            x, y = queue.popleft()

            for adjacent_pos in self.get_positions_adjacent_to(x, y):
                if (adjacent_pos in visited or 
                    self.is_position_out_of_bounds(*adjacent_pos) or 
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
            for adjacent_pos in self.get_positions_adjacent_to(x, y):
                if adjacent_pos not in cell_set:
                    perimeter += 1

        return perimeter
    
    def __get_region_price(self, region: Region) -> int:
        return len(region.cells) * self.__get_region_perimeter(region)
    
    def __map_price(self) -> int:
        return sum(self.__get_region_price(region) for region in self.__regions.values())
    
    def solve_part_one(self) -> int:
        return self.__map_price()

def run():
    file = get_file(__file__)
    map = Map(file.readlines())

    print(f'Part one solution is: {map.solve_part_one()}')

if __name__ == '__main__':
    run()