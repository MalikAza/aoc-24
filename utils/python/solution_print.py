def solution_print(part: int, solution: int) -> None:
    part_string = ''

    match part:
        case 1:
            part_string = 'one'
        case 2:
            part_string = 'two'
    
    print(f"Part {part} solution is: {solution}")