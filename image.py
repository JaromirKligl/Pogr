from PIL import Image as PilImage
from PIL import ImageColor as PilImageColor

from math import floor
from mappings import linear_map
import matplotlib.pyplot as plt

from palette import Palette
from histogram import Histogram

class Image:

    image = None

    def __init__(self, image):
        self.image = image

    @classmethod
    def open(cls, link):
        """Opens from link as an img"""
        return cls(PilImage.open(link))

    @classmethod
    def new_with_img_params(cls, image):
        """Create new image with params of image"""

        new_img = PilImage.new(image.mode, image.size, "white")
        return cls(new_img)

    @classmethod
    def render_palette(cls, palette, width=1024, height=1024, size=None):

        assert (palette.max == 255)
        w_block = width / 16
        h_block = height / 16

        if not size:
            size = (width, height)

        img = PilImage.new("RGB", size, "white")
        for x in range(size[0]):
            for y in range(size[1]):
                new_pixel = palette[floor(x/w_block) + (16 * floor(y/h_block))]
                img.putpixel((x, y), new_pixel)

        return cls(img)

    @classmethod
    def render_histogram(cls, histogram, width=10, height=10, size=None, gap=10):
        """
        width , height declares size of one unit of histogram
        total_width, total_height = (width + gap) * 256, height * 256
        """
        if not size:
            size = (width , height)

        picture_size = ((size[0] + gap) * 256, size[1] * 256)

        out = cls(PilImage.new("L", picture_size, "white"))
        for x in range(256):
            top = linear_map(histogram.histogram[x], 0, histogram.max,0, 255)
            col_height = size[1] * round(top)
            if col_height != 0:
                with Image.custom_new(size=(size[0], col_height), mode="L", color="black") as coll:
                    out.paste(coll, x=x* (size[0] + gap), y=(256 * size[1]) - 1 - col_height)

        return out


    @classmethod
    def custom_new(cls, width=1024, height=1024, size=None, mode="RGB", color="white"):
        if size is None:
            size = (width, height)
        return cls(PilImage.new(mode, size, color))


    @property
    def size(self):
        return self.image.size

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def mode(self):
        return self.image.mode

    @staticmethod
    def image_map(fun, first, *args, mode=None, index=False):

        if mode is None:
            mode = first.image.mode
        if args:
            images = [first] + list(args)
        else:
            images = [first]

        smallest_width = min([i.width for i in images])
        smallest_height = min([i.height for i in images])
        size = (smallest_width, smallest_height)

        new = Image(PilImage.new(mode, size, "white"))

        for x in range(smallest_width):
            for y in range(smallest_height):
                pixels = [img.image.getpixel((x, y)) for img in images]
                if index:
                    new_pixel = fun(*pixels, x ,y)
                else:
                    new_pixel = fun(*pixels)
                new.image.putpixel((x, y), new_pixel)

        return new

    def pixel_apply(self, func, pixel):
        """
        Works for RGB. RGBA. GRAYSCALE, BLACK AND WHITE
        """
        if self.image.mode == "L" or self.image.mode == "1":
            return func(pixel)
        else:
            return tuple(map(func, pixel))




    def get_pixel(self, x=0, y=0, cords=None):
        if cords is None:
            cords = (x, y)
        return self.image.getpixel(cords)


    def get_subpixel(self, x=0, y=0, cords=None):
        if cords:
            x = cords[0]
            y = cords[1]
        """
        works only in rgb mode
        returns subpixel using bilinear interpolation
        """
        assert(self.image.mode == "RGB")

        x0 = int(x)
        y0 = int(y)
        x1 = x0 + 1
        y1 = y0 + 1

        #figujeme pokud pretece
        if x0 < 0:
            x0 = 0
        if y0 < 0:
            y0 = 0

        if x1 > self.width - 1:
            x1 = self.width - 1
        if y1 > self.height -1:
            y1 = self.height - 1


        c_tl = self.get_pixel(x=x0, y=y0)
        c_tr = self.get_pixel(x=x1, y=y0)
        c_bl = self.get_pixel(x=x0, y=y1)
        c_br = self.get_pixel(x=x1, y=y1)

        dx = x - x0
        dy = y - y0

        def interpol_fun(tl, tr, bl, br):
            xtop = tr * dx + tl * (1-dx)
            xbot = br * dx + bl * (1-dx)
            return xtop * dy + xbot * (1-dy)

        return tuple(map(interpol_fun, c_tl, c_tr, c_bl, c_br))

    def is_edge_pixel(self, x, y):
        return x == 0 or y==0 or x == (self.width - 1) or y== (self.height - 1)

    def is_out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def color_to_pixel(self,color):

        if isinstance(color, str):
            return PilImageColor.getcolor(color, self.mode)
        else:
            return color

    def put_pixel(self, x=0, y=0, cords=None, color="black"):
        if cords is None:
            cords = (x, y)
        self.image.putpixel(cords, self.color_to_pixel(color))

    def paste(self, img, x=0, y=0, cords=None):
        if cords is None:
            cords = (x, y)

        self.image.paste(img.image, cords)
        return self

    def paste_list(self, list, x=0, y=0, cords=None):
        if cords is None:
            cords = (x, y)

        height = len(list)
        width = len(list[0])
        flat = [i for s in list for i in s]
        with PilImage.new(self.image.mode, (width, height)) as section:
            section.putdata(flat)
            self.paste(section, x, y, cords)

        return self

    def copy(self):
        return Image(self.image.copy())

    def save(self, link):
        """saves the image and returns it"""
        self.image.save(link)
        return self

    def show(self):
        dpi = 50
        fig = plt.figure(figsize=(self.height/dpi,self.width/dpi), dpi=dpi)
        ax = fig.add_axes((0,0,1,1))
        ax.imshow(self.image)
        ax.axis('off')
        plt.show()
        return self

    def close(self):
        self.image.close()
        self.image = None
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __del__(self):
        """Zavreni puvodni Pil Img"""
        if self.image:
            self.image.close()