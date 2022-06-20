import sys

d={1:'a',2:'b',3:'c',4:'a',5:'d',6:'e',7:'a',8:'b'}
my_value = sys.argv[1]
found_keys = [key for key in d if d[key] == my_value]

print(found_keys)





my_dict = dict.fromkeys('brontosaurus', 0)
for letter in 'brontosaurus':
    my_dict[letter] += 1
print(my_dict)

sequence = {0: 0, 1: 1}


def fibonacci(num_position):
    global sequence
    if num_position in sequence:
        pass
    else:
        sequence[num_position] = fibonacci(num_position - 1) + fibonacci(num_position - 2)
    return sequence[num_position]


print(fibonacci(10))

def num_times(number, times):
    return number if times == 1 else number*num_times(number, times - 1)


print(num_times(int(input()), int(input())))