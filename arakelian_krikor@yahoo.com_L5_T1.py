import sys


def fibonacci(num_position):
    global sequence
    if num_position in sequence:
        pass
    else:
        sequence[num_position] = fibonacci(num_position - 1) + fibonacci(num_position - 2)
    return sequence[num_position]


sys.argv[1] = int(sys.argv[1])
sys.argv[2] = int(sys.argv[2])
sequence = {1: 0, 2: 1}
fibonacci(sys.argv[2])
range_to_print = list()
for pos in sequence:
    if sys.argv[1] <= pos <= sys.argv[2]:
        range_to_print.append(sequence[pos])
print(range_to_print)
