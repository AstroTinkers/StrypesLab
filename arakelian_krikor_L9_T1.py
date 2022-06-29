from math import exp


def f(x):
    return x**3 + 3*x - 5


def bisection(a, b, func):
    error_margin = 0.001
    try:
        a, b = int(a), int(b)
    except ValueError:
        raise ValueError("Values must be valid numbers(integers)")
    if a > 0 > b or a < 0 < b:
        while True:
            c = (a + b) / 2
            if error_margin >= a - b:
                return c
            if func(c) * func(a) <= 0:
                b = c
            elif func(c) * func(b) <= 0:
                a = c
    else:
        raise Exception("Values must not both be positive or negative!")
