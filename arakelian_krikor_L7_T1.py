class Fibs:
    def __init__(self):
        self.a = 0
        self.b = 1
        self.c = 1

    def __next__(self):
        self.c = self.a + self.b
        self.a = self.b
        self.b = self.c
        return self.b - self.a

    def __iter__(self):
        return self
