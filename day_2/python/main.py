from io import TextIOWrapper
from itertools import combinations, pairwise
from typing import List
from utils.python import get_input_file_from_script_file

def get_reports(file: TextIOWrapper) -> List[List[int]]:
    lines = [line.replace('\n', '') for line in file.readlines()]
    reports = [[int(number) for number in line.split(' ')] for line in lines]

    return reports

def is_report_safe_part_one(report: List[int]) -> bool:
    asc, desc = False, False

    for index in range(len(report)-1):
        to_compare = (report[index], report[index + 1])
        difference = to_compare[0] - to_compare[1]
        current_creasing = 'asc' if difference < 0 else 'desc'

        if not 1 <= abs(difference) <= 3:
                return False

        if index == 0:
            if current_creasing == 'asc':
                asc = True
            else:
                desc = True
            continue

        if current_creasing == 'asc' and desc:
            return False
        if current_creasing == 'desc' and asc:
            return False
        
    return True

class Report:
    MAX_DIFFERENCE = 3
    MIN_DIFFERENCE = 1

    def __init__(self, report: List[int]):
        self.__report = report

    def __is_continuous_line(self, desc: bool = False) -> bool:
        return sorted(self.__report, reverse=desc) == self.__report

    def __is_continuous_incline(self) -> bool:
        return self.__is_continuous_line()
    
    def __is_continuous_decline(self) -> bool:
        return self.__is_continuous_line(desc=True)

    def __is_continuous(self) -> bool:
        return self.__is_continuous_incline() or self.__is_continuous_decline()

    def __respect_differences(self) -> bool:
        differences = [abs(a - b) for a, b in pairwise(self.__report)]

        return all([self.MIN_DIFFERENCE <= difference <= self.MAX_DIFFERENCE for difference in differences])

    def is_safe(self) -> bool:
        return self.__is_continuous() and self.__respect_differences()

def run ():
    file = get_input_file_from_script_file(__file__)
    reports = get_reports(file)
    safe_reports_part_one = [report for report in reports if Report(report).is_safe()]
    safe_reports_part_two = [report for report in reports if any([Report(list(comb)).is_safe() for comb in combinations(report, len(report)-1)])]

    print("Part one solution is: ", len(safe_reports_part_one))
    print("Part two solution is: ", len(safe_reports_part_two))

if __name__ == '__main__':
    run()