import sys

with open(sys.argv[1], 'r') as file:
    lines_to_sort = file.readlines()
    lines_to_sort.sort()
with open(sys.argv[2], 'x+') as file2:
    for line in lines_to_sort:
        file2.write(line)
