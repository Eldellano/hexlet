class Counter(object):
    """A simple integral counter."""

    def __init__(self):
        """Initialize a new counter with zero as starting value."""
        self.value = 0

    def inc(self, amount=1):
        """Increment counter's value."""
        self.value = max(self.value + amount, 0)

    def dec(self, amount=1):
        """Decrement counter's value."""
        self.inc(-amount)


# BEGIN (write your solution here)
class LimitedCounter(Counter):
    def __init__(self, limit):
        self.value = 0
        self.limit = limit

    def inc(self, amount=1):
        self.value = max(self.value + amount, 0)
        if self.value > self.limit:
            self.value = self.limit

    def dec(self, amount=1):
        self.inc(-amount)
        if self.value < 0:
            self.value = 0
