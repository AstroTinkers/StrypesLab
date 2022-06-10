import sys

uniques = set()
for num in sys.argv[1:]:
    uniques.add(num)
print([int(el) for el in uniques])

