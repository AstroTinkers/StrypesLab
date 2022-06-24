import sys
with open(sys.argv[1], 'r') as file:
    stem_dict = {}
    for line in file.readlines():
        key, value = line.split(":")
        value = value.strip("\n")
        stem_dict[key] = value
for value in stem_dict.values():
    if value.lower() in sys.argv[2]:
        print(value)
