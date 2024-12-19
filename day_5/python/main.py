from functools import cmp_to_key
from typing import List, Tuple
from utils.python import get_input_file_from_script_file, solution_print

class RulesStore:
    def __init__(self, data: str):
        rules_data = data.split('\n')
        self.__rules = {}

        for rule in rules_data:
            key, value = rule.split('|')

            if key not in self.__rules:
                self.__rules[key] = []

            self.__rules[key].append(value)

    def get_all(self):
        return self.__rules

class Printing:
    def __init__(self, data: str):
        self.__order = [x for x in data.split(',')]

    def get_order(self):
        return self.__order

class PrintingsStore:
    def __init__(self, data: str):
        self.__printings = [Printing(x) for x in data.split('\n')]

    def get_all(self):
        return [x.get_order() for x in self.__printings]

class Solution:
    __correct_printings: List[Tuple[str]] = []
    __incorrect_printings: List[List[str]] = []

    def __init__(self, rules: str, printings: str):
        self.__rules = RulesStore(rules).get_all()
        self.__printings = PrintingsStore(printings).get_all()
        self.__filter_printings()

    def __is_printing_correct(self, printing: List[str]):
        for index, page in enumerate(printing):
            if page not in self.__rules:
                continue

            page_rules = self.__rules[page]
            before_page = printing[:index]
            is_incorrect = any([x in page_rules for x in before_page])

            if is_incorrect:
                return False

        return True

    def __filter_printings(self):
        for printing in self.__printings:
            if self.__is_printing_correct(printing):
                self.__correct_printings.append(printing)
            else:
                self.__incorrect_printings.append(printing)

    def __get_middle_page(self, printing: Tuple[str]):
        return int(printing[len(printing) // 2])

    def __fix_incorrect_printings(self):
        def compare_printings(a, b):
                if a in self.__rules and b in self.__rules[a]:
                    return -1
                elif b in self.__rules and a in self.__rules[b]:
                    return 1
                
                return 0
        
        for printing in self.__incorrect_printings:
            printing.sort(key=cmp_to_key(compare_printings))

    def solve_part_two(self):
        self.__fix_incorrect_printings()
        return sum([self.__get_middle_page(x) for x in self.__incorrect_printings])

    def solve_part_one(self):
        return sum([self.__get_middle_page(x) for x in self.__correct_printings])

def run():
    file = get_input_file_from_script_file(__file__)
    r, p = file.read().split('\n\n')
    solution = Solution(r, p)

    solution_print(1, solution.solve_part_one())
    solution_print(2, solution.solve_part_two())

if __name__ == '__main__':
    run()