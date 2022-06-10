import sys

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
message = sys.argv[1]
cipher = int(sys.argv[2])
coded_message = [alphabet[(alphabet.index(letter) + cipher) - len(alphabet)] for letter in message]
print("".join(coded_message))
decoded_message = [alphabet[alphabet.index(letter) - cipher] for letter in coded_message]
print("".join(decoded_message))
