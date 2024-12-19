from io import TextIOWrapper
from typing import List, Tuple
from utils.python import get_input_file_from_script_file, deep_copy_arg, solution_print

def get_left_and_right(file: TextIOWrapper) -> Tuple[List[int], List[int]]:
    lines = [line.replace('\n', '') for line in file.readlines()]
    left = []
    right = []

    for line in lines:
        l,r = line.split('   ')
        left.append(int(l))
        right.append(int(r))

    return left, right

def pair_min_left_with_min_right(left: List[int], right: List[int]) -> List[Tuple[int, int]]:
    paired = []
    while len(left) > 0 and len(right) > 0:
        min_left = min(left)
        left.remove(min_left)

        min_right = min(right)
        right.remove(min_right)

        paired.append((min_left, min_right))

    return paired

@deep_copy_arg()
def part_one_solution(left: List[int], right: List[int]) -> int:
    paired = pair_min_left_with_min_right(left, right)

    return sum(max(pair) - min(pair) for pair in paired)

def part_two_solution(left: List[int], right: List[int]) -> int:
    return sum(number * right.count(number) for number in left)

def run():
    file = get_input_file_from_script_file(__file__)
    left, right = get_left_and_right(file)

    solution_print(1, part_one_solution(left, right))
    solution_print(2, part_two_solution(left, right))

if __name__ == "__main__":
    run()