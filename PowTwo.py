class PowTwo:

    def __init__(self, max):
        self.n = 0
        self.max = max

    def __iter__(self):
        return self

    def __next__(self):
        if self.n > self.max:
            raise StopIteration

        result = 2**self.n
        self.n += 1
        return result