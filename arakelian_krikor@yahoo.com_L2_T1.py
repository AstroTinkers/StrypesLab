import sys


def is_sorted(target_list):
    control_list = sorted(target_list)
    return 'sorted' if control_list == target_list else 'unsorted'


print(is_sorted(sys.argv[1:]))
