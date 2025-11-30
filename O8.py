from functools import reduce

from image import Image
from O6 import put_circle, put_line
from O5 import linear_image_combination_2

def make_function():

    max_y = 0

    def fill(image, seed_x, seed_y, color):
        nonlocal max_y
        """
        pouziva prohledavani do sirky
        """
        old_color = image.get_pixel(seed_x, seed_y)
        max_y = seed_y
        if color == old_color:
            max_y = None
            return image

        new_color = image.color_to_pixel(color)
        queue = list()
        queue.append((seed_x,seed_y))


        while queue:
            x,y = queue.pop(0)
            if image.is_out_of_bounds(x,y):
                continue
            pix_color = image.get_pixel(x,y)

            if pix_color != old_color:
                continue
            max_y = max(max_y, y)
            image.put_pixel(x,y ,color=new_color)
            queue.append((x + 1,y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))
        return image

    def max_y_reached():
        return max_y

    return fill, max_y_reached



def edges(points):
    rotated =  points[1:len(points)] + (points[0],)

    return tuple(map(lambda a,b: (a,b) , points, rotated))

def non_horizontal_edges(edge_list):

    def filter_fun (edge):
        return edge[0][0] != edge[1][0]

    return tuple(filter(filter_fun, edge_list))

def opposite_edge_point(point,edge):
    if point == edge[0]:
        return edge[1]
    if point == edge[1]:
        return edge[0]
    else:
        raise Exception("point is not edge of edge")

def is_vertex_from_some_edge(point, edge_tuple):
    """
    returns False or edge where it occurs
    """
    def reduce_fun(bool, edge):
        if bool:
            return bool
        if edge[0] == point or edge[1] == point:
            return edge

    return reduce(reduce_fun, edge_tuple, False)

fill, max_y_reached = make_function()


def max_sizes(points):

    def reduce_fun(point1, point2):
        return max(point1[0], point2[0]), max(point1[1], point2[1])

    return reduce(reduce_fun, points)

def min_sizes(points):

    def reduce_fun(point1, point2):
        return min(point1[0], point2[0]), min(point1[1], point2[1])

    return reduce(reduce_fun, points)

def put_polygon_edges(image, *points, color = "black"):

    def map_fun(edge):
        v1, v2 = edge
        put_line(image,v1[0],v1[1], v2[0], v2[1], color)

    list(map(map_fun, edges(points)))

    return image

def render_filled_polygon(*points, inner : tuple | str ="red",outer : tuple | str ="black"):
    edge_list = edges(points)
    br = max_sizes(points)
    tl = min_sizes(points)

    out = Image.custom_new(width=(br[0] + 1), height=(br[1] + 1),mode="RGBA",color=(255,255,255,0))
    put_polygon_edges(out,*points,color=out.color_to_pixel(outer))
    polygon_fill(out,out.color_to_pixel(inner),
                 out.color_to_pixel(outer),
                 edge_list,
                 tl,
                 br)
    return out


def pair_list(old_list):

    out = []
    pair = list()
    even=False

    for x in old_list:
        if even:
            pair.append(x)
            out.append(pair)
            pair = list()
        else:
            pair.append(x)
        even= not even
    return out


def get_intersections(edge_list, y):
    """
    najde intersekce pro scan-line
    """
    intersections = []
    for edge in edge_list:
        (x0, y0), (x1, y1) = edge
        if (y0 <= y < y1) or (y1 <= y < y0):

            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersections.append(round(x))

    intersections.sort()
    return intersections


def polygon_fill(image, inner, outer, edge_list, tl, br,):

    non_ho = non_horizontal_edges(edge_list)
    y = tl[1]
    while y < br[1] + 1:
        # scan line fill
        interct = get_intersections(edge_list, y)
        if len(interct) == 1 or 0:
            y += 1
            continue

        lowest_max = None
        for pair in pair_list(interct):

            if (pair[0] != pair[1]) and (image.get_pixel(pair[0] + 1, y) != outer):
                fill(image,pair[0] + 1,  y, color=inner)
                max_reached = max_y_reached()
                if max_reached:
                    if lowest_max is None:
                        lowest_max = max_reached
                    lowest_max = min(lowest_max, max_reached)
        if lowest_max is None:
            y+= 1
        else:
            y= lowest_max + 1

    return image


def put_polygon(image, *points, outer: tuple | str ="black", inner: tuple | str ="red" , filled = True):
    if not filled:
        put_polygon_edges(image, *points, color=outer)
        return image

    with render_filled_polygon(*points,
                               inner=inner,
                               outer=outer) as polly:
        with linear_image_combination_2(image, polly) as comb:

            image.paste(comb, cords=(0,0))
    return image


if __name__ == '__main__':

    STAR = ((10, 42),
    (90, 90),
    (50, 10),
    (10, 90),
    (90, 42),)
    with render_filled_polygon(*STAR, inner= "red", outer="black") as polly:
        polly.show()

