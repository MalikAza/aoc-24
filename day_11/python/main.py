from copy import deepcopy
from functools import cache
from typing import List, Literal
from utils.python import get_input_file_from_script_file

class Solution:
    def __init__(self, data: str):
        self.__stones = data.split(' ')

    @cache
    def __transform_stone(self, stone: str) -> List[str]:
        if stone == '0':
            return ['1']
        elif (len_stone := len(stone)) % 2 == 0:  # even number of digits
            midpoint = len_stone // 2

            stone_1 = str(int(stone[:midpoint]))
            stone_2 = str(int(stone[midpoint:]))
            
            return [stone_1, stone_2]
        else:
            return [str(int(stone) * 2024)]

    @cache
    def __how_many_stones_produce_one_stone(self, stone: str, n_iterations: int) -> int:
        if n_iterations == 0:
            return 1
        
        return sum(self.__how_many_stones_produce_one_stone(new_stones, n_iterations - 1) for new_stones in self.__transform_stone(stone))
    
    def solve(self, part: Literal[1, 2]):
        match part:
            case 1:
                n_iterations = 25
            case 2:
                n_iterations = 75

        return sum(self.__how_many_stones_produce_one_stone(stone, n_iterations) for stone in self.__stones)

    
def run():
    from time import time
    import tracemalloc

    tracemalloc.start()
    file = get_input_file_from_script_file(__file__)

    solution_part_one = Solution(file.read())
    solution_part_two = deepcopy(solution_part_one)

    start = time()
    part_one_result = solution_part_one.solve(1)
    part_one_time = time() - start
    part_one_memory = tracemalloc.get_traced_memory()[1]
    print(f"Part one solution is: {part_one_result} (time: {part_one_time:.2f}s, memory: {part_one_memory/1024:.2f} KB)")

    # Reset memory tracing for part two
    tracemalloc.reset_peak()

    start = time()
    part_two_result = solution_part_two.solve(2)
    part_two_time = time() - start
    part_two_memory = tracemalloc.get_traced_memory()[1]
    print(f"Part two solution is: {part_two_result} (time: {part_two_time:.2f}s, memory: {part_two_memory/1024:.2f} KB)")

    tracemalloc.stop()
if __name__ == '__main__':
    run()