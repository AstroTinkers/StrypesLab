from math import exp


def f(x):
    return exp(x)-2*x-2


def bisection(a, b, func):
    error_margin = 0.001
    while True:
        try:
            a = int(a)
            b = int(b)
        except ValueError:
            raise ValueError("Values must be valid numbers(integers)")
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


lower = input("Please enter lower range: ")
upper = input("Please enter upper range: ")
print(bisection(lower, upper, f))

