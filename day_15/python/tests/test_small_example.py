import unittest
import day_15.python.main as day_15

class TestPartOne(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self):
        self.data = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<'''
        boxes_expected = {
            (5, 1): 105,
            (6, 1): 106,
            (6, 3): 306,
            (3, 4): 403,
            (4, 5): 504,
            (4, 6): 604
        }

        self.boxes_positions_at_end = boxes_expected.keys()
        self.boxes_gps_at_end = boxes_expected.items()

        return super().setUp()
    
    def test_position_of_robot(self):
        map = day_15.Map(self.data)
        map.run()
        self.assertEqual(map.robot_position, (4, 4))

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
        self.assertEqual(sum(self.boxes_gps_at_end), 2028)

    def test_solve_part_one(self):
        map = day_15.Map(self.data)

        self.assertEqual(map.solve_part_one(), 2028)