def f(x):
    return x ** 3 + 3 * x - 5


def bisection_func(func, a, b, error_margin):
    while True:
        c = (a + b) / 2

        if error_margin >= f(c):
            return c

        elif func(a) * func(c) <= 0:
            b = c

        elif func(b) * func(c) <= 0:
            a = c


while True:
    try:
        lower = int(input("Please enter lower range: "))
        upper = int(input("Please enter upper range: "))
        print(bisection_func(f, lower, upper, 0.001))
        break
    except ValueError:
        print("Please enter valid numbers(integers)")
        continue
    except:
        print("Values must not be both positive or negative!")
        continue




with open('new_file.txt', 'x+') as file:
    file.write('a_new_line\n')
    file.write('c_new_line\n')
    file.write('g_new_line\n')
    file.write('w_new_line\n')
    file.write('b_new_line\n')
    file.write('j_new_line\n')
    file.write('o_new_line\n')
    file.write('h_new_line\n')
with open('new_file.txt', 'r') as file:
    lines_to_sort = [file.readlines()]
    lines_to_sort.sort()
with open('new_file2.txt', 'x+') as file2:
    file2.writelines(lines_to_sort)


