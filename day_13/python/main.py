from typing import Literal
from utils.python import get_input_file_from_script_file

class Button:
    def __init__(self, data: str):
        x, y = data.split(',')
        self.x = int(x.split('+')[-1])
        self.y = int(y.split('+')[-1])

class Prize:
    def __init__(self, data: str):
        x, y = data.split(',')
        self.x = int(x.split('=')[-1])
        self.y = int(y.split('=')[-1])

class Claw:
    def __init__(self, data: str):
        button_a, button_b, prize = data.split('\n')
        self.__button_a = Button(button_a)
        self.__button_b = Button(button_b)
        self.__prize = Prize(prize)
        self.best: None | int = None

    def __calculate_best(self, part: Literal[1, 2]):
        max_iterations = self.__get_max_iterations(part)
        for a in range(max_iterations):
            for b in range(max_iterations):
                x = self.__button_a.x * a + self.__button_b.x * b
                y = self.__button_a.y * a + self.__button_b.y * b

                if x == self.__prize.x and y == self.__prize.y:
                    cost = 3 * a + b
                    self.best = cost if self.best is None else min(self.best, cost)

    def __get_lowest_x(self):
        return min(self.__button_a.x, self.__button_b.x)
    
    def __get_lowest_y(self):
        return min(self.__button_a.y, self.__button_b.y)
    
    def __get_max_iterations(self, part: Literal[1, 2]):
        match part:
            case 1:
                # You estimate that each button would need to be pressed no more than 100 times to win a prize.
                # How else would someone be expected to play?
                return 101
            case 2:
                return max(self.__prize.x // self.__get_lowest_x(), self.__prize.y // self.__get_lowest_y())
    
    def get_best(self, part: Literal[1, 2]):
        if part == 2:
            self.__prize.x += 10000000000000
            self.__prize.y += 10000000000000

        self.__calculate_best(part)

        return self.best if self.best is not None else 0

class Solution:
    def __init__(self, data: str):
        self.__claws = [Claw(x) for x in data.split('\n\n')]
    
    def solve(self, part: Literal[1, 2]):
        return sum([x.get_best(part) for x in self.__claws])

def run():
    file = get_input_file_from_script_file(__file__)
    solution = Solution(file.read())

    print(f'Part one solution is: {solution.solve(1)}')
    # print(f'Part two solution is: {solution.solve(2)}')

if __name__ == '__main__':
    run()