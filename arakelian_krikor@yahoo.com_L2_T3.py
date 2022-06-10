import sys


def repeated_els(target_list):
    control_list = []
    for num in target_list:
        if num in control_list:
            return True
        else:
            control_list.append(num)
    return False


print(repeated_els(sys.argv[1:]))
