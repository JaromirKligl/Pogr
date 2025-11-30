from image import Image
from palette import Palette
import time


def convert_to_palette(img, palette):

    def convert_fun(pix):
        return palette.convert_pixel(pix)

    return Image.image_map(convert_fun, img)


if __name__ == '__main__':

    pale = Palette(6, 0, 2)

    with Image.render_palette(pale) as pal:
        pal.save('image/palette.jpg')

    with Image.open('image/wolf.jpg') as jirka:
        start = time.perf_counter()
        new = convert_to_palette(jirka, pale)
        end = time.perf_counter()
        new.save('image/wolf_new.jpg')

    print(end - start)