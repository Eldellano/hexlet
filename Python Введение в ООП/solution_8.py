class HourClock:
    def __init__(self, value=0):
        self.value = value

    @property
    def hours(self):
        return self.value

    @hours.setter
    def hours(self, new):
        self.value = new
        if self.value > 11:
            self.value %= 12
        if self.value < 0:
            self.value = self.value + 12
