"""

Data Structure Assignment 2
By Yu Gai (NetID: yg1246)

Command line options:
  If no argument provided, the script executes all test cases.
  Otherwise, please specify shape in the 1st argument and specify sides or coordinates in other arguments.
  For example:
    python3 hw02.py EquilateralTriangle 1
    python3 hw02.py Quadrilateral [0,0] [1,0] [1,1] [0,1]
    python3 hw02.py RegularPentagon 1
  To test similarity:
    python3 hw02.py similar Triangle [0,0] [0,1] [1,0] Triangle [1,1] [1,0] [0,1]   

Inheritance hierarchy:
  Polygon
  --Triangle
  ----IsoscelesTriangle
  ------EquilateralTriangle
  --NontriangularPolygon
  ----Quadrilateral
  ------Rectangle
  --------Square
  ----Pentagon
  ------RegularPentagon
  ----Hexagon
  ------RegularHexagon
  ----Octagon
  ------RegularOctagon

The mechanism of test cases:
  The perimeter and area of all regular n-gons are respectively calculated by the formula for arbitrary n-gons and regular n-gons.
  The areas of arbitrary n-gons are respectively calculated by formula and by recursion.
  The test cases cross-validate all these approaches of calculation.
  Therefore, distinct methods of calculation should generate approximately equal results.
  The similarity test is checked by clockwise and anticlockwise rotated triangles and n-gons.

"""

import math
import cmath
import numpy as np
import numpy.linalg as la

######################################
# HELPER CLASSES AND FUNCTIONS START #
######################################

def all_positive(*args):
  """ Test whether all numbers are positive. """
  return all(arg > 0 for arg in args)

def compatible_in_dimension(*args):
  """ Test whether all the arrays are of the same shape. """
  shape = args[0].shape
  return all(arg.shape == shape for arg in args[1:])

def cosine(a, b, c):
  """ Calculate the cosine value of an inner angle of a triangle given the length of all sides. """
  return (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)

def vector_angle(left, right, return_cosine=True):
  """ Calculate the angle of 2 vectors given the coordinates of vectors. """
  cosine = np.dot(left, right) / (la.norm(left) * la.norm(right))
  if return_cosine:
    return cosine
  else:
    return np.arccos(cosine)

class IncompatibleDimensionError(Exception):
  """ The exception to be raised if coordinates are not compatible in dimension. """
  def __str__(self, *args):
    return ('Dimensions incompatible:%s' % (' {}' * len(args))).format(*args)

def generate_coordinates(n):
  """ Generate the vertexes coordinates of a regular n-gon.
    :param int n: the number of vertexes.
  """
  step = 2.0 * math.pi / float(n)
  angles = tuple(step * i for i in range(n))
  coordinates = []
  for angle in angles:
    c = cmath.rect(1.0, angle)
    coordinates.append((c.real, c.imag))
  return coordinates

def parse_polygon(*args):
  """ Create a polygon object given command line arguments. """
  shape = args[0]
  parameters = []
  for arg in args[1:]:
    if '[' in arg and ']' in arg:
      arg = arg.replace('[', '').replace(']', '')
      parameters.append(tuple(float(value) for value in arg.split(',')))
    else:
      parameters.append(float(arg))
  polygon = getattr(__import__('hw02'), shape)(*parameters)
  return polygon

##################################
# HELP CLASSES AND FUNCTIONS END #
##################################

class Polygon:
  """ The abstract base class of polygons. """
  def __init__(self, *args):
    raise NotImplementedError()
  def perimeter(self):
    raise NotImplementedError()
  def area(self):
    raise NotImplementedError()
  def similar_to(self):
    raise NotImplementedError()

class Triangle(Polygon):
  """ The base class of triangles. """
  def __init__(self, a, b, c):
    """ Initialize a triangle object given sides or vertexes.
      :param float / tuple / numpy.ndarray a, b, c : sides or vertexes.
    """
    if all(isinstance(vertex, tuple) for vertex in (a, b, c)):
      a = np.array(list(a), dtype=np.float32)
      b = np.array(list(b), dtype=np.float32)
      c = np.array(list(c), dtype=np.float32)
    if all(isinstance(vertex, np.ndarray) for vertex in (a, b, c)):
      vertexes = [a, b, c]
      if compatible_in_dimension(*vertexes):
        # calculate sides given vertexes
        a = la.linalg.norm(vertexes[1] - vertexes[2])
        b = la.linalg.norm(vertexes[0] - vertexes[2])
        c = la.linalg.norm(vertexes[0] - vertexes[1])
      else:
        raise IncompatibleDimensionError(a, b, c)

    self.a = float(a)
    self.b = float(b)
    self.c = float(c)
    assert all_positive(self.a, self.b, self.c), 'Sides of triangle should be positive numbers.'
    assert 2 * max(self.a, self.b, self.c) < self.a + self.b + self.c, \
      'The given sides cannot form a triangle.'

  def perimeter(self):
    return self.a + self.b + self.c

  def area(self):
    cosine_C = cosine(self.a, self.b, self.c)
    return 0.5 * self.a * self.b * ((1 - cosine_C ** 2) ** 0.5)

  def similar_to(self, triangle):
    """ Test similarity. """

    from itertools import permutations

    # Check whether the other polygon is a triangle.
    assert isinstance(triangle, Triangle), 'Both polygons must be triangles.'

    # Calculate all inner angles.
    self_angles = set([round(cosine(*p), 2) for p in permutations([self.a, self.b, self.c])])
    triangle_angles = set([round(cosine(*p), 2) for p in permutations([triangle.a, triangle.b, triangle.c])])

    # Ensure all inner angles are equal.
    return self_angles == triangle_angles

class IsoscelesTriangle(Triangle):
  def __init__(self, leg, base):
    super().__init__(leg, leg, base)

  def area(self):
    """ Base class method is overridden for efficiency. """
    return 0.5 * self.c * (self.a ** 2 - 0.25 * self.c ** 2) ** 0.5

class EquilateralTriangle(IsoscelesTriangle):
  def __init__(self, l):
    super().__init__(l, l)

  def perimeter(self):
    """ Base class method is overridden for efficiency. """
    return 3 * self.a

  def area(self):
    """ Base class method is overridden for efficiency. """
    return 0.25 * (3 ** 0.5) * (self.a ** 2)

class NontriangularPolygon:
  """ The base class for all n-gons. (n > 3) """
  def __init__(self, *args):
    """ Initialize a NontriangularPolygon object given sides or vertexes. 
      :param float / tuple / numpy.array: sides or vertexes. 
    """
    if all(isinstance(arg, (tuple, np.ndarray)) for arg in args):
      self._cartesian = True
      if isinstance(args[0], tuple):
        self._vertexes = tuple(np.array(list(arg), dtype=np.float32) for arg in args)
      else:
        self._vertexes = tuple(args)
      if compatible_in_dimension(*self._vertexes):
        self._sides = []
        for i, vertex in enumerate(self._vertexes):
          next_vertex = self._vertexes[(i + 1) % len(self._vertexes)]
          self._sides.append(la.norm(self._vertexes[i] - next_vertex))
    else:
      self._cartesian = False
      self._sides = [float(arg) for arg in args]

    # Check whether the sides can form a polygon.
    assert all(side > 0 for side in self._sides)
    if not self._cartesian:
      assert 2 * max(self._sides) < math.fsum(self._sides)

  def perimeter(self):
    return math.fsum(self._sides)

  def area(self, mode='formula'):
    """ Calculate area.
      :param str mode: 'recursive' or 'formula
    """
    if self._cartesian:
      if mode == 'recursive':
        '''
          The algorithm recursively partition the n-gon to smaller polygon and triangles.
        '''
        triangles = []
        inner_polygon_vertexes = []
        # Figure out the vertexes of sub-triangles and sub-polygon.
        for i in range(0, len(self._vertexes), 2):
          inner_polygon_vertexes.append(self._vertexes[i])
          if len(self._vertexes) - 3 < i:
            if i == len(self._vertexes) - 2:
              triangles.append(Triangle(self._vertexes[-2], self._vertexes[-1], self._vertexes[0]))
          else:
            triangles.append(Triangle(self._vertexes[i], self._vertexes[i + 1], self._vertexes[i + 2]))

        # Calculate the area of sub-polygon
        polygon_area = 0 if len(inner_polygon_vertexes) == 2 else \
          Triangle(*inner_polygon_vertexes).area() if len(inner_polygon_vertexes) == 3 else\
          NontriangularPolygon(*inner_polygon_vertexes).area()

        # Sum the areas of sub-triangles and sub-polygon.
        return math.fsum(triangle.area() for triangle in triangles) + polygon_area

      if mode == 'formula':
        '''
          The formula is described in
            http://mathworld.wolfram.com/PolygonArea.html
        '''
        return 0.5 * abs(
          math.fsum(
            np.cross(
              self._vertexes[i],
              self._vertexes[(i + 1) % len(self._vertexes)]
            ) for i in range(len(self._vertexes))
          )
        )
      
      raise Exception('Unsupported mode of area calculation.')

    else:
      raise Exception(
        "A polygon's area cannot be calculated if the polygon is not specified by vertex coordinate."
      )

  def similar_to(self, polygon):
    # check the equality of vertex numbers
    if len(self._vertexes) != len(polygon._vertexes):
      return False

    # compute inner angles (modular operation is used to calculate the last angle)
    total_vertexes = len(self._vertexes)
    self_angles = [
      round(vector_angle(vertex - self._vertexes[i - 1], vertex - self._vertexes[(i + 1) % total_vertexes]), 2) \
        for i, vertex in enumerate(self._vertexes)
    ]
    polygon_angles = [
      round(vector_angle(vertex - self._vertexes[i - 1], vertex - self._vertexes[(i + 1) % total_vertexes]), 2) \
        for i, vertex in enumerate(self._vertexes)
    ]

    # check similarity
    offsets = [i for i, angle in enumerate(polygon_angles) if self_angles[0] == angle]
    for offset in offsets:
      # determine the sequences of angles and sides should be matched clockwise, anticlockwise
      # exit loop if the sequences cannot be matched

      # check the equality of angles
      clockwise = True
      for i, angle in enumerate(self_angles):
        if angle != polygon_angles[(i + offset) % total_vertexes]:
          clockwise = False
          break
      anticlockwise = True
      for i, angle in enumerate(self_angles):
        if angle != polygon_angles[(offset - i) % total_vertexes]:
          anticlockwise = False
          break
      if not (clockwise or anticlockwise):
        break
      
      # check the proportionality of sides only if angles are equal
      # check the proportionality of sides and return True if sides are proportional
      ratio = self._sides[0] / polygon._sides[offset]
      if clockwise:
        if all(
          self_side / polygon._sides[(i + offset) % total_vertexes] == ratio \
            for i, self_side in enumerate(self._sides)
        ):
          return True
      if anticlockwise:
        print(self._sides, polygon._sides)
        if all(
          self_side / polygon._sides[(offset - i) % total_vertexes] == ratio \
            for i, self_side in enumerate(self._sides)
        ):
          return True

    return False

class Quadrilateral(NontriangularPolygon):
  def __init__(self, a, b, c, d):
    super().__init__(a, b, c, d)

class Rectangle(Quadrilateral):
  def __init__(self, a, b):
    super().__init__(a, b, a, b)

  def perimeter(self):
    """ Base class method is overridden for efficiency. """
    return 2 * (self._sides[0] + self._sides[1])

  def area(self):
    """ Base class method is overridden for efficiency. """
    return self._sides[0] * self._sides[1]

class Square(Rectangle):
  def __init__(self, l):
    super().__init__(l, l)

  def perimeter(self):
    """ Base class method is overridden for efficiency. """
    return 4 * self._sides[0]

  def area(self):
    """ Base class method is overridden for efficiency. """
    return self._sides[0] ** 2

class Pentagon(NontriangularPolygon):
  def __init__(self, a, b, c, d, e):
    super().__init__(a, b, c, d, e)

class Hexagon(NontriangularPolygon):
  def __init__(self, a, b, c, d, e, f):
    super().__init__(a, b, c, d, e, f)

class Octagon(NontriangularPolygon):
  def __init__(self, a, b, c, d, e, f, g, h):
    super().__init__(a, b, c, d, e, f, g, h)

class RegularPentagon(NontriangularPolygon):
  def __init__(self, l):
    super().__init__(*((l,) * 5))
  def perimeter(self):
    """ Base class method is overridden for efficiency. """
    return 5 * self._sides[0]
  def area(self):
    """ Base class method is overridden for efficiency. """
    return 0.25 * (25 + 10 * 5 ** 0.5) ** 0.5 * self._sides[0] ** 2

class RegularHexagon(NontriangularPolygon):
  def __init__(self, l):
    super().__init__(*((l,) * 6))
  def perimeter(self):
    """ Base class method is overridden for efficiency. """
    return 6 * self._sides[0]
  def area(self):
    """ Base class method is overridden for efficiency. """
    return 1.5 * 3 ** 0.5 * self._sides[0] ** 2

class RegularOctagon(NontriangularPolygon):
  def __init__(self, l):
    super().__init__(*((l,) * 8))
  def perimeter(self):
    """ Base class method is overridden for efficiency. """
    return 8 * self._sides[0]
  def area(self):
    """ Base class method is overridden for efficiency. """
    return 2 * (1 + 2 ** 0.5) * self._sides[0] ** 2

def test():
  """ Test cases
  """
  # ensure that test cases appear in an interpretable order
  test_case_labels = [
    'triangle',
    'triangle by coordinate',
    'isosceles triangle',
    'equilateral triangle',
    'quadrilateral by coordinate',
    'rectangle',
    'square',
    'pentagon',
    'pentagon by coordinate',
    'hexagon',
    'hexagon by coordinate',
    'octagon',
    'octagon by coordinate',
  ]

  test_cases = {}

  # triangles
  test_cases['triangle'] = Triangle(*([3 ** 0.5] * 3))
  test_cases['triangle by coordinate'] = \
    Triangle(*generate_coordinates(3))
  test_cases['isosceles triangle'] = IsoscelesTriangle(3 ** 0.5, 3 ** 0.5)
  test_cases['equilateral triangle'] = EquilateralTriangle(3 ** 0.5)
  
  # quadrilaterals
  test_cases['rectangle'] = Rectangle(2 ** 0.5, 2 ** 0.5)
  test_cases['square'] = Square(2 ** 0.5)
  test_cases['quadrilateral by coordinate'] = \
    Quadrilateral(*generate_coordinates(4))

  # pentagons
  test_cases['pentagon'] = RegularPentagon((0.5 * (5 - 5 ** 0.5)) ** 0.5)
  test_cases['pentagon by coordinate'] = \
    Pentagon(*generate_coordinates(5))

  # hexagons
  test_cases['hexagon'] = RegularHexagon(1.0)
  test_cases['hexagon by coordinate'] = Hexagon(*generate_coordinates(6))

  # octagons
  test_cases['octagon'] = RegularOctagon(2 / (4 + 2 * 2 ** 0.5) ** 0.5)
  test_cases['octagon by coordinate'] = \
    Octagon(*generate_coordinates(8))

  print('##############################')
  print('Checking perimeter calculation')
  print('##############################')
  for key in test_case_labels:
    value = test_cases[key]
    print('{:<32}'.format(key), value.perimeter())

  print()

  print('#########################')
  print('Checking area calculation')
  print('#########################')
  for key in test_case_labels:
    value = test_cases[key]
    print('{:<56}\t'.format('%s (area calculated by formula)' % key), value.area())
    if 'coordinate' in key and not isinstance(value, Triangle):
      print('{:<56}\t'.format('%s (area calculated by recursion)' % key), value.area(mode='recursive'))

  print()

  print('########################')
  print('Checking similarity test')
  print('########################')
  VERTEXES = 3
  # generate the original shape
  radiuses = tuple(0.1 * i for i in range(VERTEXES))
  angles = tuple(0.1 * i for i in range(VERTEXES))
  coordinates = []
  for r, phi in zip(radiuses, angles):
    c = cmath.rect(r, phi)
    coordinates.append((c.real, c.imag))
  original_polygon = NontriangularPolygon(*coordinates)
  original_triangle = Triangle(*coordinates)

  # generate the clockwise rotated shape
  clockwise_rotated_angles = tuple(0.1 * i - 0.05 for i in range(VERTEXES))
  clockwise_rotated_coordinates = []
  for r, phi in zip(radiuses, clockwise_rotated_angles):
    c = cmath.rect(r, phi)
    clockwise_rotated_coordinates.append((c.real, c.imag))
  clockwise_rotated_polygon = NontriangularPolygon(*clockwise_rotated_coordinates)
  clockwise_rotated_triangle = Triangle(*clockwise_rotated_coordinates)

  # generate the anticlockwise rotated shape
  anticlockwise_rotated_angles = tuple(math.pi - 0.1 * i for i in range(VERTEXES))
  anticlockwise_rotated_coordinates = []
  for r, phi in zip(radiuses, anticlockwise_rotated_angles):
    c = cmath.rect(r, phi)
    anticlockwise_rotated_coordinates.append((c.real, c.imag))
  anticlockwise_rotated_polygon = NontriangularPolygon(*anticlockwise_rotated_coordinates)
  anticlockwise_rotated_triangle = Triangle(*anticlockwise_rotated_coordinates)

  # check the similarity test of triangle
  triangle_clockwise_test = original_triangle.similar_to(clockwise_rotated_triangle)
  triangle_anticlockwise_test = original_triangle.similar_to(anticlockwise_rotated_triangle)

  # check the similarity test of polygon
  polygon_clockwise_test = original_polygon.similar_to(clockwise_rotated_polygon)
  polygon_anticlockwise_test = original_polygon.similar_to(anticlockwise_rotated_polygon)
  
  print('clockwise rotated triangle test', triangle_clockwise_test)
  print('anticlockwise rotated triangle test', triangle_anticlockwise_test)
  print('clockwise rotated polygon test', polygon_clockwise_test)
  print('anticlockwise rotated polygon test', polygon_anticlockwise_test)

  print('similarity test passed', 
    triangle_clockwise_test and \
    triangle_anticlockwise_test and \
    polygon_clockwise_test and \
    polygon_anticlockwise_test
  )

def main():
  """ Handles command line options. """
  import sys
  if len(sys.argv) == 1:
    test()

  else:
    if sys.argv[1] == 'similar':
      # argv[1] must be a string specifying the shape
      index = 0
      for i, arg in enumerate(sys.argv[3:]):
        if arg.isalpha():
          i += 3
          left_shape = parse_polygon(*sys.argv[2 : i])
          index = i
          break
      right_shape = parse_polygon(*sys.argv[index:])
      print(left_shape.similar_to(right_shape))

    else:
      polygon = parse_polygon(*sys.argv[1:])
      print('perimeter', polygon.perimeter())
      try:
        print('area', polygon.area())
      except Exception as e:
        print(e)

if __name__ == '__main__':
  main()
