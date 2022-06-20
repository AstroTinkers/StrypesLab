import sys


def num_times(number, times):
    number = int(number)
    times = int(times)
    return number if times == 1 else number*num_times(number, times - 1)


print(num_times(sys.argv[1], sys.argv[2]))
