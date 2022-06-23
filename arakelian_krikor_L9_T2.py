import unittest
from arakelian_krikor_L9_T1 import bisection
from arakelian_krikor_L9_T1 import f


class TestBisection(unittest.TestCase):
    def test_bisection_exception(self):
        # Test if function raises correct errors
        self.assertRaises(ValueError, bisection('g', 'r', f))
        self.assertRaises(ValueError, bisection('g', 5, f))
        self.assertRaises(ValueError, bisection(-7, 'r', f))
        self.assertRaises(Exception, bisection(-7, -5, f))
        self.assertRaises(Exception, bisection(15, 2, f))

    def test_bisection_result(self):
        # Test if function performs correctly
        self.assertAlmostEqual(bisection(-3, 4, f), 0.5)
        self.assertAlmostEqual(bisection(-5, 5, f), 0)
        self.assertAlmostEqual(bisection(-1, 3, f), 1.0)
