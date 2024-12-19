from copy import deepcopy
from functools import reduce
from itertools import count
from operator import mul
from typing import List, Literal, Tuple
from utils.python import get_input_file_from_script_file, solution_print
import numpy as np

class Robot:
    __slots__ = ['__x', '__y', '__vx', '__vy']

    def __init__(self, data: str):
        positions, velocity = data.split(' v=')
        x, y = tuple(map(int, positions.replace('p=', '').split(',')))
        vx, vy = tuple(map(int, velocity.split(',')))

        self.__x = x
        self.__y = y
        self.__vx = vx
        self.__vy = vy

    def __move_x(self, max_x: int):
        self.__x = (self.__x + self.__vx) % max_x

    def __move_y(self, max_y: int):
        self.__y = (self.__y + self.__vy) % max_y

    def move(self, max_x: int, max_y: int):
        self.__move_x(max_x)
        self.__move_y(max_y)

    def get_position(self):
        return (self.__x, self.__y)

class Solution:
    def __init__(self, data: List[str], max_x: int, max_y: int):
        self.__robots = [Robot(line) for line in data]
        self.__max_x = max_x
        self.__max_y = max_y
        self.__middle_x = (max_x // 2) - 1
        self.__middle_y = (max_y // 2) - 1

    def move_robots(self):
        for robot in self.__robots:
            robot.move(self.__max_x, self.__max_y)

    def get_robots_positions(self):
        return tuple(robot.get_position() for robot in self.__robots)

    def get_quadrant_min_max(self, quadrant: Literal[1, 2, 3, 4]) -> Tuple[Tuple[int, int]]:         
        match quadrant:
            case 1:
                return (
                    (0, 0), 
                    (self.__middle_x, self.__middle_y)
                )
            case 2:
                return (
                    (
                        self.__middle_x + 1 if self.__max_x % 2 == 0 else self.__middle_x + 2, 
                        0
                    ),
                    (self.__max_x - 1, self.__middle_y)
                )
            case 3:
                return (
                    (
                        0,
                        self.__middle_y + 1 if self.__max_y % 2 == 0 else self.__middle_y + 2
                    ),
                    (self.__middle_x, self.__max_y - 1)
                )
            case 4:
                return (
                    (
                        self.__middle_x + 1 if self.__max_x % 2 == 0 else self.__middle_x + 2,
                        self.__middle_y + 1 if self.__max_y % 2 == 0 else self.__middle_y + 2
                    ),
                    (self.__max_x - 1, self.__max_y - 1)
                )

    def is_robot_in_quadrant(self, robot: Tuple[int, int], quadrant: Literal[1, 2, 3, 4]):
        min_pos, max_pos = self.get_quadrant_min_max(quadrant)

        return all(min_p <= r <= max_p for r, min_p, max_p in zip(robot, min_pos, max_pos))

    def how_many_robots_in_quadrant(self, quadrant: Literal[1, 2, 3, 4]):
        robots_positions = self.get_robots_positions()

        return len(tuple(robot for robot in robots_positions if self.is_robot_in_quadrant(robot, quadrant)))

    def move_robots_x_times(self, times: int):
        for _ in range(times):
            self.move_robots()

    def display(self):
        robot_positions = self.get_robots_positions()
        grid = np.full((self.__max_y, self.__max_x), ' ', dtype=str)

        for x, y in robot_positions:
            grid[y, x] = '#'

        return tuple(''.join(row) for row in grid)
    
    def solve(self, part: Literal[1, 2]):
        match part:
            case 1:
                self.move_robots_x_times(100)

                return reduce(mul, [self.how_many_robots_in_quadrant(quadrant) for quadrant in [1, 2, 3, 4]])
            case 2:
                print('Searching xmas tree for part two...\nIterations:')
                for i in count(1):
                    self.move_robots()
                    display = self.display()
                    print(i, end='\r')

                    if any('########' in row for row in display):
                        print('\n'.join(display))

                        if input('Is xmas tree found? (y/n) ').lower() == 'y':
                            return i

def run():
    file = get_input_file_from_script_file(__file__)
    solution_part_one = Solution(file.readlines(), 101, 103)
    solution_part_two = deepcopy(solution_part_one)

    solution_print(1, solution_part_one.solve(1))
    solution_print(2, solution_part_two.solve(2))

if __name__ == '__main__':
    run()