# BEGIN (write your solution here)
class Counter:
    value = 0

    def inc(self, delta=1):
        self.value += delta

    def dec(self, delta=1):
        if delta <= self.value:
            self.value -= delta
        else:
            self.value = 0
# END
