import collections


# Simple representations of Points and rectangles
Point = collections.namedtuple('Point', ['x', 'y'])
Coordinates = collections.namedtuple('Coordinates', ['x0', 'y0', 'x1', 'y1'])


class Rect(collections.namedtuple('Rect', ['left', 'top', 'width', 'height'])):
    @property
    def area(self):
        "The product of width and height"
        return self.width * self.height

    @property
    def coordinates(self):
        "Coordinates(left, top, right, bottom)"
        return Coordinates(self.left, self.top, self.left + self.width,
                           self.top + self.height)

    @property
    def topleft(self):
        "Point(x, y)"
        return Point(self.left, self.top)

    @property
    def bottomright(self):
        "Point(x, y)"
        return Point(self.left + self.width, self.top + self.height)

    @property
    def centre(self):
        "Point(x, y)"
        return Point(self.left + self.width / 2, self.top + self.height / 2)

    def padded(self, percent):
        "Returns self with percentage padding applied"
        x_offset = self.width * float(percent) / 100.0
        y_offset = self.height * float(percent) / 100.0
        return Rect(self.left - x_offset, self.top - y_offset,
                    self.width + 2 * x_offset, self.height + 2 * y_offset)

    def intersect(self, other):
        "Returns self intersected to be within other"
        if isinstance(other, Rect):
            left, top, right, bottom = self.coordinates
            other_left, other_top, other_right, other_bottom = other.coordinates
            left = max(other_left, left)
            top = max(other_top, top)
            width = min(other_right, right) - left
            height = min(other_bottom, bottom) - top
            return Rect(left, top, width, height)
        else:
            raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, Rect):
            return (self.left == other.left and
                    self.top == other.top and
                    self.width == other.width and
                    self.height == other.height)
        else:
            raise NotImplementedError()

    def __ne__(self, other):
        return not self == other
