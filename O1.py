from math import floor
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


if __name__ == "__main__":
    with Image.open('image/jirka.jpg') as img:
        with grayscale(img) as gr:
            gr.save('image/grayjirka.jpg')

        with desaturate(img, s=0.7, r=0, b=0.7, g=0.3) as ds:
            ds.save('image/desatjirka.jpg')
