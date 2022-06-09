# Zadacha 1
a = [1, 2, 3, 4, 5]
b = [6, 7, 8, 9, 10]
sum_ab = 0
for i in range(len(a)):
    sum_ab += a[i] * b[i]
print(sum_ab)

# Zadacha 2
sum_ab = 0
x = -1
for index, value in enumerate(a):
    sum_ab += value * x
    x = -1 * x
print(sum_ab)

# Zadacha 3
c = [1, 4, 9, 16, 9, 7, 4, 9, 11]
d = [i for i in c[::-1]]
print(d)

# Zadacha 4
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
phrase = "THISISASAMPLEMESSAGE"
cipher = 3
coded_message = [alphabet[(alphabet.index(letter) + cipher) - len(alphabet)] for index, letter in enumerate(phrase)]
print("".join(coded_message))
decoded_message = [alphabet[alphabet.index(letter) - cipher] for index, letter in enumerate(coded_message)]
print("".join(decoded_message))

# Zadacha 5

message = 'DECODETHIS'
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
key = input("Please, input key: ")
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
