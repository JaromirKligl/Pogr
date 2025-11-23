from image import Image
from palette import Palette
import time


if __name__ == '__main__':

    pale = Palette(5,2,1)
    start = time.perf_counter()
    with Image.render_palette(pale) as pal:
        pal.save('image/palette.jpg')
    end = time.perf_counter()
    print(end-start)