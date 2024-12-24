from functools import cache
from typing import Literal
from utils.python import get_input_file_from_script_file, solution_print

class Solution:
    def __init__(self, data: str):
        patterns, designs = data.split('\n\n')
        self.__patterns = patterns.split(', ')
        self.__designs = designs.split('\n')

    @cache
    def how_many_patterns_can_craft_design(self, design: str) -> int:
        if len(design) == 0:
            return 1
        
        solutions = 0
        for pattern in self.__patterns:
            if design.startswith(pattern):
                solutions += self.how_many_patterns_can_craft_design(design[len(pattern):])

        return solutions
    
    def solve(self, part: Literal[1, 2]) -> int:
        match part:
            case 1:
                return sum(1 for design in self.__designs if self.how_many_patterns_can_craft_design(design) > 0)
            case 2:
                return sum(self.how_many_patterns_can_craft_design(design) for design in self.__designs)

def run():
    file = get_input_file_from_script_file(__file__)
    solution = Solution(file.read())

    solution_print(1, solution.solve(1))
    solution_print(2, solution.solve(2))

if __name__ == '__main__':
    run()