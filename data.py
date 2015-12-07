class Data():
    def __init__(self, length):
        self.data = []
        self.length = length
    def add(self, bar):
        self.data.append(bar)
        if len(self.data) > self.length:
            self.data.pop(0)
