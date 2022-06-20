import sys


def binary_search(number, left_stop, right_stop, search_list):
    if search_list[left_stop] <= number <= search_list[right_stop]:
        splitter = left_stop + (right_stop - left_stop) // 2
        if search_list[splitter] == number:
            return splitter
        elif search_list[splitter] > number:
            return binary_search(number, left_stop, splitter - 1, search_list)
        elif search_list[splitter] < number:
            return binary_search(number, splitter + 1, right_stop, search_list)

    else:
        return -1


numbers = [30, 40, 50, 52, 56, 62, 70, 91, 100, 131, 132, 166, 170, 195, 202, 205, 212, 248, 249, 256, 263, 272, 288,
           289, 290, 296, 332, 345, 352, 364, 380, 390, 407, 412, 429, 430, 438, 444, 486, 493, 497, 499, 510, 513,
           514, 519, 521, 521, 535, 546, 552, 554, 556, 570, 584, 638, 640, 655, 655, 657, 692, 692, 711, 713, 731,
           739, 740, 842, 858, 885, 887, 888, 893, 898, 900, 903, 908, 909, 959, 988]
sys.argv[1] = int(sys.argv[1])
result = binary_search(sys.argv[1], 0, len(numbers) - 1, numbers)
if result != -1:
    print(f"found at {result}")
else:
    print('not found')
