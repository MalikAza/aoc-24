import sys
from day_1.python.main import run as day_1
from day_2.python.main import run as day_2
from day_3.python.main import run as day_3
from day_4.python.main import run as day_4
from day_5.python.main import run as day_5
from day_6.python.main import run as day_6
from day_7.python.main import run as day_7
from day_9.python.main import run as day_9
from day_11.python.main import run as day_11
from day_12.python.main import run as day_12
from day_13.python.main import run as day_13
from day_14.python.main import run as day_14
from day_15.python.main import run as day_15
from day_19.python.main import run as day_19

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python runner.py <day_number>')
        sys.exit(1)

    day = sys.argv[1]

    match day:
        case '1':
            day_1()
        case '2':
            day_2()
        case '3':
            day_3()
        case '4':
            day_4()
        case '5':
            day_5()
        case '6':
            day_6()
        case '7':
            day_7()
        case '9':
            day_9()
        case '11':
            day_11()
        case '12':
            day_12()
        case '13':
            day_13()
        case '14':
            day_14()
        case '15':
            day_15()
        case '19':
            day_19()
        case _:
            print('No solution for this day.')