from functools import cache
import operator

from image import Image
from O1 import grayscale


def matrix_group(m1, m2, m3, m4):
    return list(map(lambda x, y: x + y, m1, m2)) + list(map(lambda x, y: x + y, m3, m4))


def unit_matrix(n):
    return [[1] * n] * n


def scalar_mult(matrix, n):
    return [[n * i for i in j] for j in matrix]


def matrix_add(matrix1, matrix2):
    return [list(map(operator.add, i, j)) for i, j in zip(matrix1, matrix2)]


@cache
def diffusion_matrix(n):
    if n == 1:
        return [[0]]
    return matrix_group(scalar_mult(diffusion_matrix(n // 2), 4),
                        matrix_add(scalar_mult(diffusion_matrix(n // 2), 4),
                                   scalar_mult(unit_matrix(n // 2), 3)),
                        matrix_add(scalar_mult(diffusion_matrix(n // 2), 4),
                                   scalar_mult(unit_matrix(n // 2), 2)),
                        matrix_add(scalar_mult(diffusion_matrix(n // 2), 4),
                                   unit_matrix(n // 2)))

def gray_scale_to_bw(origin, size=16):

    def_matrix = diffusion_matrix(size)

    @cache
    def nth_pixel(n):
        return [[0 if x > (n * ((size * size) / 256)) else 1 for x in i] for i in def_matrix]

    out = Image.custom_new(width=origin.width * size, height=origin.height * size, mode="1")

    for x in range(origin.width):
        for y in range(origin.height):

            out.paste_list(nth_pixel(origin.get_pixel(cords=(x, y))), cords=(x * size, y * size))

    return out


if __name__ == "__main__":
    pass

