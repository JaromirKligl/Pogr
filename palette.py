from functools import cache
from math import floor


class Palette:
    _r = 0
    _g = 0
    _b = 0

    def __init__(self, r, g, b):
        self._r = r
        self._g = g
        self._b = b
        self._max = pow(2, r+g+b) - 1

    @property
    def max(self):
        return self._max

    @cache
    def __getitem__(self, item):
        if item > self._max or item < 0:
            raise IndexError
        if self._r != 0:
            r: int = ((item >> (self._g + self._b)) * self.max) // (pow(2, self._r) - 1)
        else:
            r: int = 0

        if self._g != 0:
            g: int = ((item >> self._b & (pow(2, self._g) - 1)) * self.max) // (pow(2, self._g) - 1)
        else:
            g: int = 0
        if self._b != 0:
            b: int = (item & (pow(2, self._b) - 1)) * self.max // (pow(2, self._b) - 1)
        else:
            b: int = 0

        return r, g, b

    @cache
    def convert_pixel(self, pixel):
        r, g, b = pixel
        new_r = round((r * (pow(2, self._r) - 1)) / self.max) << (self._g + self._b)
        new_g = round(g * (pow(2, self._g) - 1) / self.max) << self._b
        new_b = round(b * (pow(2, self._b) - 1) / self.max)
        return self[new_r | new_g | new_b]
