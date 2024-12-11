from itertools import product
from typing import List, Literal
from utils.python import get_file


class Solution:
    def __init__(self, data: List[str]):
        self.__data = [(int(value), [int(x) for x in operators_string.split(' ')]) for value, operators_string in (line.split(': ') for line in data)]

    def __evaluate_expression(self, numbers: List[int], operators: List[str]):
        result = numbers[0]

        for i in range(1, len(numbers)):
            match operators[i - 1]:
                case '+':
                    result += numbers[i]
                case '*':
                    result *= numbers[i]
                case '||':
                    result = int(str(result) + str(numbers[i]))

        return result

    def __is_equation_possible(self, final_value: int, numbers: List[int], operators: List[str]):
        operators = product(operators, repeat=len(numbers) - 1)

        for operator in operators:
            if self.__evaluate_expression(numbers, operator) == final_value:
                return True
            
        return False
    
    def solve(self, part: Literal[1, 2]):
        operators = ['+', '*']
        if part == 2: operators.append('||')

        return sum(final_value for final_value, numbers in self.__data if self.__is_equation_possible(final_value, numbers, operators))

def run():
    file = get_file(__file__)
    solution = Solution(file.read().split('\n'))
    
    print("Part one solution is: ", solution.solve(1))
    print("Part two solution is: ", solution.solve(2))

if __name__ == '__main__':
    run()