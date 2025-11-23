from PIL import Image as PilImage


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
        new_img = PilImage.new(image.mode, image.size, image.getpixel((0, 0)))
        return cls(new_img)

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
    def image_map(fun, first, *args):

        if args:
            images = [first] + list(args)
        else:
            images = [first]

        smallest_width = min([i.width for i in images])
        smallest_height = min([i.height for i in images])
        size = (smallest_width, smallest_height)

        new = Image(PilImage.new(first.image.mode, size, first.image.getpixel((0, 0))))

        for x in range(smallest_width):
            for y in range(smallest_height):
                pixels = [img.image.getpixel((x, y)) for img in images]
                new_pixel = fun(*pixels)
                new.image.putpixel((x, y), new_pixel)

        return new

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