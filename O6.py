from image import Image

from O4 import rotated_grid_antialiasing

def put_line(image, x0, y0, x1, y1, color="black"):
    dx = x1 - x0
    dy = y1 - y0
    if dx == 0:
        return image

    prediction = 2*(dy - dx)
    y = y0

    for x in range(x0, x1 + 1):
        image.put_pixel(x=x, y=y, color=color)
        if prediction >= 0:
            y+= 1
            prediction += 2*(dy - dx)

        prediction += 2*dy
    return image

def put_circle(image, xc, yc, radius=10, color="black"):
    x = 0
    y = radius
    prediction = 1-radius
    while x < y+1:
        image.put_pixel(x=xc + x, y= yc + y, color=color)
        image.put_pixel(x=xc + x, y=yc - y, color=color)
        image.put_pixel(x=xc + y, y=yc + x, color=color)
        image.put_pixel(x=xc + y, y=yc - x, color=color)

        image.put_pixel(x=xc - x, y=yc + y, color=color)
        image.put_pixel(x=xc - x, y=yc - y, color=color)
        image.put_pixel(x=xc - y, y=yc + x, color=color)
        image.put_pixel(x=xc - y, y=yc - x, color=color)

        if prediction > 0:
            prediction -= (2 * y) - 2
            y -= 1

        prediction += (2 * x) + 3
        x+= 1
    return image





if __name__ == '__main__':

    with Image.custom_new(size=(100,100), color="aliceblue") as blank:
        put_circle(blank, 50, 50, 30, color="red")
        blank.show()
        with rotated_grid_antialiasing(blank, n=16) as fixed:
            fixed.show()
