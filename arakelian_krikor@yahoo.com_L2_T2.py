import sys


def is_anagram(phrase1, phrase2):
    phrase1 = phrase1.casefold()
    phrase2 = phrase2.casefold()
    control_phrase = list(phrase1[:])
    for letter in phrase1:
        if letter in phrase2:
            control_phrase.pop(control_phrase.index(letter))
    return len(control_phrase) == 0


print(is_anagram(sys.argv[1], sys.argv[2]))
