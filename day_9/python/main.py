from copy import deepcopy
import re
from utils.python import get_input_file_from_script_file

class DiskMap:

    def __init__(self, data: str):
        self.__representation = []
        self.__data = [int(x) for x in data]
        self.__parse_data()

    def __parse_data(self):
        index = 0
        for i, number in enumerate(self.__data):
            if i % 2 == 0:
                self.__representation.extend([str(index) for _ in range(number)])
                index += 1
            else:
                self.__representation.extend(['.' for _ in range(number)])

    def __how_many_space(self):
       return self.__representation.count('.')

    def __is_digit(self, value: str):
        pattern = r'\d'
        matches = re.findall(pattern, value)

        return len(matches) > 0

    def __defrag_file_by_file(self):
        breaking_point = self.__how_many_space()

        for index, number in enumerate(self.__representation[::-1]):
            if index == breaking_point:
                break

            pos = self.__representation.index('.')

            self.__representation[pos] = number
            self.__representation[-index -1] = '.'

    def solve_part_one(self):
        self.__defrag_file_by_file()

        return sum([int(x) * index for index, x in enumerate(self.__representation) if self.__is_digit(x)])

def run():
    file = get_input_file_from_script_file(__file__)
    disk_map = DiskMap(file.read())

    print("Part one solution is: ", disk_map.solve_part_one())

if __name__ == '__main__':
    run()