from image import Image

from O4 import rotated_grid_antialiasing


def _plot_line_low(image, x0,y0,x1,y1, color):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    prediction = (2 * dy) - dx
    y = y0

    for x in range(x0, x1 + 1):
        image.put_pixel(x,y)
        if prediction > 0:
            y += yi
            prediction += 2* (dy-dx)
        else:
            prediction += 2*dy

def _plot_line_high(image, x0,y0,x1,y1, color):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    prediction = (2 * dx) - dy
    x = x0

    for y in range(y0, y1 + 1):
        image.put_pixel(x,y)
        if prediction > 0:
            x += xi
            prediction += 2* (dx-dy)
        else:
            prediction += 2*dx


def put_line(image, x0, y0, x1, y1, color):
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            _plot_line_low(image, x1,y1,x0,y0, color)
            return image
        _plot_line_low(image, x0,y0,x1,y1, color)
        return image
    if y0 > y1:
        _plot_line_high(image, x1,y1,x0,y0, color)
        return image

    _plot_line_high(image, x0,y0,x1,y1, color)
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
        with rotated_grid_antialiasing(blank, n=8) as fixed:
            fixed.show()
