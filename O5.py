from functools import reduce



from image import Image
from histogram import Histogram
from O1 import grayscale
from mappings import linear_map, non_linear_map




def contrast_correction(image, min=0, max=255):

    def correction_func(pix):
        return image.pixel_apply(lambda p: round(linear_map(p, 0, 255, min, max)), pix)

    return Image.image_map(correction_func, image)

def bright_up(image, minimum=0):

    def correction_func(pix):
        return image.pixel_apply(lambda p: min(255, p + minimum), pix)

    return Image.image_map(correction_func, image)

def bright_down(image, maximum=255):

    def correction_func(pix):
        return image.pixel_apply(lambda p: max(0, p - (255 - maximum)), pix)

    return Image.image_map(correction_func, image)

def gamma_correction(image, exponent=1.0, constant = 1.0):

    def gamma_transform(color):
        return pow(color, exponent) * constant

    def correction_func(pix):
        return image.pixel_apply(lambda p: (round(non_linear_map(p, 0, 255, 0, 255, gamma_transform))), pix)


    return Image.image_map(correction_func, image)

def equalize(image):

    histogram = Histogram(image)

    def correction_func(pix):
        return round((histogram.levels - 1) * histogram.comulative_normalized_histogram(pix))

    return Image.image_map(correction_func, image, mode="L")

def linear_image_combination_2(base, upper , x=0, y=0, cords=None):

    if cords is None:
        cords = (x,y)

    if upper.mode != "RGBA":
        return base.copy().paste(upper, cords=cords)



    def compute_function(base_pix, x0, y0):

        if (x0 - cords[0] >= upper.width or
            y0 - cords[1] >= upper.height or
            x0 - cords[0] < 0 or
            y0 - cords[1] < 0):

            return base_pix
        upper_pix = upper.get_pixel(x0 - cords[0], y0 - cords[1])
        alpha = upper_pix[3] / 255.0
        r = round(base_pix[0] * (1 - alpha) + upper_pix[0] * alpha)
        g = round(base_pix[1] * (1 - alpha) + upper_pix[1] * alpha)
        b = round(base_pix[2] * (1 - alpha) + upper_pix[2] * alpha)
        return r, g, b

    return Image.image_map(compute_function, base, mode="RGB", index=True)

def linear_image_combination(base, *images):
    """
    Images can be described three ways:
    img,
    (img, (x,y))
    (img, x, y)
    it's donne by reduction from left to right
    return: rgb picture
    """

    def reduce_function(img1, img2: (Image | tuple | list)):
        if isinstance(img1, Image):
            new_base = img1
        else:
            new_base = img1[0]

        if isinstance(img2, Image):
            upper = img2
            x=0
            y=0
        else:

            if len(img2) == 2:
                upper = img2[0]
                x = img2[1][0]
                y = img2[1][1]

            elif len(img2) == 3:
                upper = img2[0]
                x = img2[1]
                y = img2[2]

            else:
                upper = img2[0]
                x = 0
                y = 0

        return linear_image_combination_2(new_base, upper, x=x, y=y)


    reduce_list = [base] +list(images)

    return reduce(reduce_function, reduce_list )





if __name__ == '__main__':
    pass




