from functools import cache
import random
from typing import Dict, Tuple, List
from utils.python import get_file

class Region:
    def __init__(self, first_cell: Tuple[int, int]):
        self.cells: List[Tuple[int, int]] = [first_cell]
        self.search_nodes: List[Tuple[int, int]] = [first_cell]
        self.perimeter = 0

class Map:
    def __init__(self, data: List[str]):
        self.map = [x.replace('\n', '') for x in data]
        self.__regions: Dict[str, Region] = {}
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
        while len(region.search_nodes) != 0:
            x, y = region.search_nodes.pop(0)

            for adjacent_pos in self.get_positions_adjacent_to(x, y):
                if self.is_position_out_of_bounds(*adjacent_pos):
                    continue
                if adjacent_pos not in region.cells and self.map[adjacent_pos[1]][adjacent_pos[0]] == cell:
                    region.cells.append(adjacent_pos)
                    region.search_nodes.append(adjacent_pos)

    def __position_cell_in_regions(self, x: int, y: int, cell: str):
        if not cell in self.__regions:
            region = Region((x, y))
            self.__regions[cell] = region
            self.__bfs(region, cell)
            return
        
        if (x, y) in self.__regions[cell].cells:
            return

        region_found_or_created = False
        while not region_found_or_created:
            cell_id = self.__get_next_cell_id(cell)
            if not cell_id in self.__regions:
                region = Region((x, y))
                self.__regions[cell_id] = region
                self.__bfs(region, cell)
                region_found_or_created = True
            else:
                if (x, y) in self.__regions[cell_id].cells:
                    region_found_or_created = True

    def __parse_regions(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.__position_cell_in_regions(x, y, cell)

    def __get_region_perimeter(self, region: Region):
        if len(region.cells) == 1:
            return 4
        
        perimeter = 0
        for x, y in region.cells:
            for adjacent_pos in self.get_positions_adjacent_to(x, y):
                if adjacent_pos not in region.cells:
                    perimeter += 1

        return perimeter
    
    def __get_region_price(self, region: Region) -> int:
        return len(region.cells) * self.__get_region_perimeter(region)
    
    def __map_price(self) -> int:
        return sum([self.__get_region_price(region) for region in self.__regions.values()])
    
    def solve_part_one(self) -> int:
        return self.__map_price()

def run():
    file = get_file(__file__)
    map = Map(file.readlines())

    print(f'Part one solution is: {map.solve_part_one()}')

if __name__ == '__main__':
    run()