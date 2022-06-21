class Fibs:
    def __init__(self):
        self.current = 0

    def __next__(self):
        self.current += 1
        return self.current - 1

    def __iter__(self):
        return self


fibs = Fibs()
for f in fibs:
    if f > 1000:
        print(f)
        break
