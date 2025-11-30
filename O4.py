
from math import cos, sin, pi
from functools import reduce
from operator import add
import time
import random

from image import Image

# https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
def rotate_point(point1, origin, angle):
    x = cos(angle) * (point1[0] - origin[0]) - sin(angle) * (point1[1] - origin[1]) + origin[0]
    y = sin(angle) * (point1[0] - origin[0]) + cos(angle) * (point1[1] - origin[1]) + origin[1]
    return x, y


def sub_pixels_average(sub_pixels, count):
    return tuple(map(lambda c: round(c / count),
                     reduce(lambda x, y: map(add, x, y),
                            sub_pixels)))

def rotated_sub_pixels_from_pixel (image, x0, y0, angle, n):
    """
    n = grid nxn
    """
    sp_center = 1/(2*n)
    center = (x0+ 0.5, y0 + 0.5)
    out = []
    for x in range(n):
        for y in range(n):
            sub_x = x0 + sp_center + (1 - x) * 1 / n
            sub_y = y0 + sp_center + (1 - y) * 1 / n
            out.append(image.get_subpixel(cords=rotate_point((sub_x, sub_y), center, angle)))

    return out

def random_sub_pixels_from_pixel (image, x0, y0, seed, n):
    """
    n = grid nxn
    """
    if seed:
        random.seed(seed)
    else:
        random.seed(time.time())

    out = [image.get_subpixel(cords=(random.random() + x0, random.random() + y0)) for _ in range(n*n)]
    return out

def rotated_grid_antialiasing(image, angle=0, n=2):
    """
    angle is in radians
    """
    def map_fun(pix, x ,y):
        if image.is_edge_pixel(x,y):
            return pix
        sub_pixels = rotated_sub_pixels_from_pixel(image, x, y, angle, n)
        return sub_pixels_average(sub_pixels, n*n)


    return Image.image_map(map_fun, image, mode="RGB",index=True)

def random_grid_antialiasing(image, seed=None, n=2):

    def map_fun(pix, x ,y):
        if image.is_edge_pixel(x,y):
            return pix
        sub_pixels = random_sub_pixels_from_pixel(image, x, y, seed, n)
        return sub_pixels_average(sub_pixels, n*n)

    return Image.image_map(map_fun, image, mode="RGB",index=True)


if __name__ == "__main__":
    pass