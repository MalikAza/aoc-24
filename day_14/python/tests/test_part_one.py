import unittest
import day_14.python.main as day_14

class TestPartOne(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_first_example_position_of_robot(self):
        solution = day_14.Solution(['p=2,4 v=2,-3'], 11, 7)
        for i in range(1, 6):
            solution.move_robots()

            match i:
                case 1:
                    self.assertEqual(solution.get_robots_positions(), [(4, 1)])
                case 2:
                    self.assertEqual(solution.get_robots_positions(), [(6, 5)])
                case 3:
                    self.assertEqual(solution.get_robots_positions(), [(8, 2)])
                case 4:
                    self.assertEqual(solution.get_robots_positions(), [(10, 6)])
                case 5:
                    self.assertEqual(solution.get_robots_positions(), [(1, 3)])

    def test_robot_move_inbounds(self):
        robot = day_14.Robot('p=0,0 v=1,1')
        robot.move(11, 7)

        self.assertEqual(robot.get_position(), (1, 1))

    def test_robot_move_more_than_max_x(self):
        robot = day_14.Robot('p=10,0 v=3,0')
        robot.move(11, 7)

        self.assertEqual(robot.get_position(), (2, 0))

    def test_robot_move_more_than_max_y(self):
        robot = day_14.Robot('p=0,6 v=0,3')
        robot.move(11, 7)

        self.assertEqual(robot.get_position(), (0, 2))

    def test_robot_move_negative_x(self):
        robot = day_14.Robot('p=0,0 v=-1,0')
        robot.move(11, 7)

        self.assertEqual(robot.get_position(), (10, 0))

    def test_robot_move_negative_y(self):
        robot = day_14.Robot('p=0,0 v=0,-1')
        robot.move(11, 7)

        self.assertEqual(robot.get_position(), (0, 6))

    def test_second_example_position_of_robots(self):
        input_data = [
            'p=0,4 v=3,-3',
            'p=6,3 v=-1,-3',
            'p=10,3 v=-1,2',
            'p=2,0 v=2,-1',
            'p=0,0 v=1,3',
            'p=3,0 v=-2,-2',
            'p=7,6 v=-1,-3',
            'p=3,0 v=-1,-2',
            'p=9,3 v=2,3',
            'p=7,3 v=-1,2',
            'p=2,4 v=2,-3',
            'p=9,5 v=-3,-3'
        ]
        solution = day_14.Solution(input_data, 11, 7)
        for _ in range(100):
            solution.move_robots()

        expected_final_positions = [
            (6, 0),
            (6, 0),
            (9, 0),
            (0, 2),
            (1, 3),
            (2, 3),
            (5, 4),
            (3, 5),
            (4, 5),
            (4, 5),
            (1, 6),
            (6, 6)
        ]

        for expected_position in expected_final_positions:
            self.assertIn(expected_position, solution.get_robots_positions())

    def test_second_example_quadrant_min_max(self):
        solution = day_14.Solution([], 11, 7)

        self.assertEqual(solution.get_quadrant_min_max(1), ((0, 0), (4, 2)))
        self.assertEqual(solution.get_quadrant_min_max(2), ((6, 0), (10, 2)))
        self.assertEqual(solution.get_quadrant_min_max(3), ((0, 4), (4, 6)))
        self.assertEqual(solution.get_quadrant_min_max(4), ((6, 4), (10, 6)))

    def test_is_robot_in_quadran(self):
        solution = day_14.Solution([], 11, 7)

        self.assertTrue(solution.is_robot_in_quadrant((0, 0), 1))
        self.assertTrue(solution.is_robot_in_quadrant((4, 2), 1))

        self.assertTrue(solution.is_robot_in_quadrant((6, 0), 2))
        self.assertTrue(solution.is_robot_in_quadrant((10, 2), 2))

        self.assertTrue(solution.is_robot_in_quadrant((0, 4), 3))
        self.assertTrue(solution.is_robot_in_quadrant((4, 6), 3))

        self.assertTrue(solution.is_robot_in_quadrant((6, 4), 4))
        self.assertTrue(solution.is_robot_in_quadrant((10, 6), 4))

        self.assertTrue(solution.is_robot_in_quadrant((0, 2), 1))

    def test_second_example_how_many_robots_in_quadrants(self):
        input_data = [
            'p=0,4 v=3,-3',
            'p=6,3 v=-1,-3',
            'p=10,3 v=-1,2',
            'p=2,0 v=2,-1',
            'p=0,0 v=1,3',
            'p=3,0 v=-2,-2',
            'p=7,6 v=-1,-3',
            'p=3,0 v=-1,-2',
            'p=9,3 v=2,3',
            'p=7,3 v=-1,2',
            'p=2,4 v=2,-3',
            'p=9,5 v=-3,-3'
        ]
        solution = day_14.Solution(input_data, 11, 7)
        for _ in range(100):
            solution.move_robots()

        self.assertEqual(solution.how_many_robots_in_quadrant(1), 1)
        self.assertEqual(solution.how_many_robots_in_quadrant(2), 3)
        self.assertEqual(solution.how_many_robots_in_quadrant(3), 4)
        self.assertEqual(solution.how_many_robots_in_quadrant(4), 1)