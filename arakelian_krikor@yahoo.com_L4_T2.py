import sys
my_dict = dict.fromkeys(sys.argv[1], 0)
for letter in sys.argv[1]:
    my_dict[letter] += 1
print(list(my_dict.items()))
