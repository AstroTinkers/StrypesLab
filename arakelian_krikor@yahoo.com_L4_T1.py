import sys

d = {1:'a',2:'b',3:'c',4:'a',5:'d',6:'e',7:'a',8:'b'}
my_value = sys.argv[1]
found_keys = [key for key in d if d[key] == my_value]
print(found_keys)
