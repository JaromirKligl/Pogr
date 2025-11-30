from math import floor,sqrt

from image import Image


def get_color_mean(pix, r, g, b):
    """Zpocita prumer barev v pixelu"""
    return sum([color * coeff for color, coeff in zip(list(pix), [r, g, b])])


def grayscale(img, r=0.299, g=0.587, b=0.114):
    """Creates a grayscale image, can configure r,g,b"""
    def gray_pix_fun(pix):
        return floor(get_color_mean(pix, r, g, b))

    return Image.image_map(gray_pix_fun, img, mode='L')


def desaturate(img, s=0.5, r=0.299, g=0.587, b=0.114):
    """Creates a desaturated image, can configure r,g,b
    and saturation parameter s"""

    def des_pix_fun(gs, origin):
        return tuple([floor(gs + (s*(color - gs))) for color in origin])

    with grayscale(img, r, g, b) as gs:
        new = Image.image_map(des_pix_fun, gs, img, mode="RGB")

    return new

def desaturate_equalization(img, c = 25):
    """
    equalize saturation of all pixels by length c
    """
    def eql_fun(gs, origin):
        r,g,b = origin
        length = sqrt((r-gs)*(r-gs) + (g-gs)*(g-gs) + (b-gs)*(b-gs))
        if length == 0:
            return origin
        norm =  tuple([round((pix - gs)/length) for pix in origin])
        return tuple([gs + nr * c for nr in norm] )

    with grayscale(img) as gs:
        new = Image.image_map(eql_fun, gs, img, mode="RGB")

    return new


if __name__ == "__main__":
    pass



