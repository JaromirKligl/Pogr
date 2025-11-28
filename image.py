from PIL import Image as PilImage
from math import floor

from palette import Palette


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

        img = PilImage.new("RGB", size, (0, 0, 0))
        for x in range(size[0]):
            for y in range(size[1]):
                new_pixel = palette[floor(x/w_block) + (16 * floor(y/h_block))]
                img.putpixel((x, y), new_pixel)

        return cls(img)

    @classmethod
    def custom_new(cls, width=1024, height=1024, size=None, mode="RGB"):
        if size is None:
            size = (width, height)

        return cls(PilImage.new(mode, (width, height), "white"))

    @property
    def size(self):
        return self.image.size

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @staticmethod
    def image_map(fun, first, *args, mode=None):

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
                new_pixel = fun(*pixels)
                new.image.putpixel((x, y), new_pixel)

        return new

    def get_pixel(self, x=0, y=0, cords=None):
        if cords is None:
            cords = (x, y)
        return self.image.getpixel(cords)

    def paste(self, img, x=0, y=0, cords=None):
        if cords is None:
            cords = (x, y)

        self.image.paste(img, cords)
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

    def save(self, link):
        """saves the image and returns it"""
        self.image.save(link)
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