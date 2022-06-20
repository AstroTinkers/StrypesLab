import sys


def is_palindrome(string):
    if len(string) <= 1:
        return True
    elif len(string) == 2:
        return string[0] == string[-1]
    else:
        if string[0] == string[-1]:
            return is_palindrome(string[1:-1])
    return False


print(is_palindrome(sys.argv[1]))
