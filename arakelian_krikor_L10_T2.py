import sys
with open(sys.argv[1], 'r') as file:
    stem_dict = {}
    for line in file.readlines():
        key, value = line.split(":")
        value = value.strip("\n")
        stem_dict[key] = value
if sys.argv[2] in stem_dict:
    print(stem_dict[sys.argv[2]])
else:
    print("Not found.")
