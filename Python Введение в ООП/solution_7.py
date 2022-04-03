class Counter:
    def __init__(self, value=0):
        self.value = value

    def inc(self, delta=1):
        new_value = self.value + delta
        return Counter(new_value)

    def dec(self, delta=1):
        if delta <= self.value:
            self.value -= delta
        else:
            self.value = 0
        return self
