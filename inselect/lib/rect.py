import collections


# Simple representations of Points and rectangles
Point = collections.namedtuple('Point', ['x', 'y'])
Coordinates = collections.namedtuple('Coordinates', ['x0', 'y0', 'x1', 'y1'])


class Rect(collections.namedtuple('Rect', ['left', 'top', 'width', 'height'])):
    @property
    def area(self):
        "The product of width and height"
        return self.width*self.height

    @property
    def coordinates(self):
        "Coordinates(left, top, right, bottom)"
        return Coordinates(self.left, self.top, self.left+self.width,
                           self.top+self.height)

    @property
    def topleft(self):
        "Point(x, y)"
        return Point(self.left, self.top)

    @property
    def bottomright(self):
        "Point(x, y)"
        return Point(self.left+self.width, self.top+self.height)

    @property
    def centre(self):
        "Point(x, y)"
        return Point(self.left+self.width/2, self.top+self.height/2)

    def __eq__(self, other):
        if isinstance(other, Rect):
            return (self.left==other.left and
                    self.top==other.top and
                    self.width==other.width and
                    self.height==other.height)
        else:
            raise NotImplementedError()

    def __ne__(self, other):
      return not self==other
