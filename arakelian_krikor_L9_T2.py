import unittest


def f(x):
    return x**3 + 3*x - 5


def bisection(a, b, func):
    error_margin = 0.001
    while True:
        try:
            a = int(a)
            b = int(b)

            c = (a + b) / 2

            if error_margin >= f(c):
                return c

            elif func(a) * func(c) <= 0:
                b = c

            elif func(b) * func(c) <= 0:
                a = c
            else:
                raise Exception("Values must not both be positive or negative!")
        except ValueError:
            print("Values must be valid numbers(integers)")
            break


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
