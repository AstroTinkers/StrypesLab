import sys

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
message = sys.argv[1]
key = sys.argv[2]
encoded_message = ""
decoded_message = ""
key = key * ((len(message) // len(key)) + 1)
for index, character in enumerate(message):
    splitter = alphabet.index(key[index])
    letter_pos = alphabet.index(character)
    alphabet_temp = alphabet[splitter:] + alphabet[:splitter]
    encoded_message += alphabet_temp[letter_pos]
print(encoded_message)
for index, character in enumerate(encoded_message):
    splitter = alphabet.index(key[index])
    alphabet_temp = alphabet[splitter:] + alphabet[:splitter]
    letter_pos = alphabet_temp.index(character)
    decoded_message += alphabet[letter_pos]
print(decoded_message)
