import unittest
import day_15.python.main as day_15

class TestPartOne(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self):
        self.data = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''
        boxes_expected = {
            (2, 1): 102,
            (4, 1): 104,
            (6, 1): 106,
            (7, 1): 107,
            (8, 1): 108,
            (1, 3): 301,
            (2, 3): 302,
            (1, 4): 401,
            (2, 4): 402,
            (1, 5): 501,
            (8, 5): 508,
            (1, 6): 601,
            (7, 6): 607,
            (8, 6): 608,
            (1, 7): 701,
            (7, 7): 707,
            (8, 7): 708,
            (1, 8): 801,
            (2, 8): 802,
            (7, 8): 807,
            (8, 8): 808
        }

        self.boxes_positions_at_end = boxes_expected.keys()
        self.boxes_gps_at_end = boxes_expected.items()

        return super().setUp()
    
    def test_position_of_robot(self):
        map = day_15.Map(self.data)
        map.run()
        self.assertEqual(map.robot_position, (3, 4))

    def test_position_of_boxes(self):
        map = day_15.Map(self.data)
        map.run()

        for box in map.get_boxes():
            self.assertIn(box, self.boxes_positions_at_end)

    def test_same_number_of_boxes(self):
        map = day_15.Map(self.data)
        map.run()

        self.assertEqual(len(map.get_boxes()), len(self.boxes_positions_at_end))

    def test_gps_coordinates_from_example(self):
        map = day_15.Map(self.data)
        self.assertEqual(map.get_gps_coordinates_from_position((4, 1)), 104)

    def test_boxes_gps_coordinates(self):
        map = day_15.Map(self.data)

        for position, value in self.boxes_gps_at_end:
            self.assertEqual(map.get_gps_coordinates_from_position(position), value)

    def text_solve_part_one_expected(self):
        self.assertEqual(sum(self.boxes_gps_at_end), 10092)

    def test_same_boxes(self):
        map = day_15.Map(self.data)
        map.run()

        self.assertEqual(map.get_boxes(), tuple(self.boxes_positions_at_end))

    def test_solve_part_one(self):
        map = day_15.Map(self.data)
        map.run()

        self.assertEqual(sum(map.get_gps_coordinates_from_position(position) for position in map.get_boxes()), 10092)

    def test_solve_part_one_return(self):
        map = day_15.Map(self.data)
        self.assertEqual(map.solve_part_one(), 10092)