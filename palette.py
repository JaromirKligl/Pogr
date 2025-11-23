from functools import cache

class Palette:
    _r = 0
    _g = 0
    _b = 0

    def __init__(self, r, g, b):
        self._r = r
        self._g = g
        self._b = b
        self._max = pow(2, r+g+b) - 1

    def max(self):
        return self._max

    @cache
    def __getitem__(self, item):
        if item > self._max or item < 0:
            raise IndexError

        r : int = ((item >> (self._g + self._b)) * self._max) / (pow(2, self._r) - 1)
        g : int = ((item >> self._b & (pow(2, self._g) - 1)) * self._max) / (pow(2, self._g) - 1)
        b : int = (item & (pow(2, self._b) - 1)) * self._max / (pow(2, self._b) - 1)

        return int(r), int(g), int(b)

