from typing import List, Literal, Tuple
from utils.python import get_input_file_from_script_file
import re

class Memory:
    def __init__(self, memory: str):
        self.__memory = memory

    def __extract_muls(self) -> List[Tuple[int, int]]:
        pattern = re.compile(r'mul\((\d{1,3}),\s*(\d{1,3})\)')
        matches: List[Tuple[str, str]] = pattern.findall(self.__memory)

        return [(int(match[0]), int(match[1])) for match in matches]
    
    def __extract_muls_with_instructions(self) -> List[Tuple[int, int]]:
        pattern = re.compile(r"(don't\(\)|do\(\))|mul\((\d{1,3}),\s*(\d{1,3})\)")
        matches: List[Tuple[str] | Tuple[str, str]] = pattern.findall(self.__memory)

        correct_matches = []
        do = True
        for match in matches:
            if match[0] in ("don't()", "do()"):
                do = match[0] == 'do()'
            elif do:
                correct_matches.append((int(match[1]), int(match[2])))

        return correct_matches
    
    def solve(self, part: Literal[1, 2]) -> int:
        match part:
            case 1:
                muls = self.__extract_muls()
            case 2:
                muls = self.__extract_muls_with_instructions()

        return sum([mul[0] * mul[1] for mul in muls])

def run():
    file = get_input_file_from_script_file(__file__)
    memory = Memory(file.read())

    print("Part one solution is: ", memory.solve(1))
    print("Part two solution is: ", memory.solve(2))

if __name__ == '__main__':
    run()