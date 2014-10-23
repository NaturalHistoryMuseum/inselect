import collections

from inselect.lib.inselect_error import InselectError


# Simple representations of Points and rectangles
Point = collections.namedtuple('Point', ['x', 'y'])
Coordinates = collections.namedtuple('Coordinates', ['x0', 'y0', 'x1', 'y1'])


class Rect(object):
    def __init__(self, left, top, width, height):
        if left<0 or top<0 or width<=0 or height<=0:
            raise InselectError('Bad rectangle')
        self.left, self.top, self.width, self.height = left, top, width, height

    def __repr__(self):
        return 'Rect({0}, {1}, {2}, {3})'.format(self.left,
                                                 self.top,
                                                 self.width,
                                                 self.height)

    def __str__(self):
        return '{0}, {1}, {2}, {3} (Area {4})'.format(self.left,
                                                      self.top,
                                                      self.width,
                                                      self.height,
                                                      self.area)

    def __iter__(self):
        return iter( (self.left, self.top, self.width, self.height) )

    @property
    def area(self):
        return self.width*self.height

    @property
    def coordinates(self):
        return Coordinates(self.left, self.top, self.left+self.width,
                           self.top+self.height)

    @property
    def centre(self):
        return Point(self.left+self.width/2, self.top+self.height/2)

    def __eq__(self, other):
        if isinstance(other, Rect):
            return (self.left==other.left and
                    self.top==other.top and
                    self.width==other.width and
                    self.height==other.height)
        else:
            raise NotImplementedError()

    def __neq__(self, other):
      return not self==other
