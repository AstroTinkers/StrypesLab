import unittest
from math import exp
# from arakelian_krikor_L9_T1 import bisection
# from arakelian_krikor_L9_T1 import f


def f(x):
    return exp(x)-2*x-2


def bisection(a, b, func):
    error_margin = 0.001
    while True:
        try:
            a, b = int(a), int(b)
        except ValueError:
            print("Values must be valid numbers(integers)")
            break
        else:
            if a > 0 > b or a < 0 < b:
                c = (a + b) / 2
                if error_margin >= f(c):
                    return c
                elif func(a) * func(c) <= 0:
                    b = c
                elif func(b) * func(c) <= 0:
                    a = c
                else:
                    raise Exception("Unable to find an answer, both values have become positive or negative")
            else:
                raise Exception("Values must not both be positive or negative!")


class TestBisection(unittest.TestCase):
    def test_bisection_exception(self):
        # Test if function raises correct errors
        self.assertRaises(ValueError, bisection('g', 'r', f))
        self.assertRaises(ValueError, bisection('g', 5, f))
        self.assertRaises(ValueError, bisection(-7, 'r', f))
        self.assertRaises(Exception, bisection(-7, -5, f))
        self.assertRaises(Exception, bisection(15, 2, f))
        self.assertRaises(Exception, bisection(10, -3, f))

    def test_bisection_result(self):
        # Test if function performs correctly
        self.assertAlmostEqual(bisection(-3, 4, f), 0.5)
        self.assertAlmostEqual(bisection(-5, 5, f), 0)
        self.assertAlmostEqual(bisection(-1, 3, f), 1.0)


if __name__ == "__main__":
    unittest.main()
