import operator

class Matrix:
  def __init__(self, matrix):
    """ Initializer.
      :param list matrix: A nested list.
    """
    assert isinstance(matrix, (list, tuple)), 'Matrix initializer only accepts nested list.'
    assert all(isinstance(row, (list, tuple)) for row in matrix), \
      'Matrix initializer only accepts nested list.'

    self._row_count = len(matrix)
    self._column_count = len(matrix[0])
    assert all(len(row) == self._column_count for row in matrix), \
      'Every list in the nested list must contain identical number of values.'
    assert all(isinstance(value, (int, float)) for row in matrix for value in row), \
      'Matrix only accepts integer or float values.'

    self._matrix = [[] for i in range(len(matrix))]
    for index, row in enumerate(self._matrix):
      row.extend(matrix[index])

  def __str__(self):
    """ Convert Matrix instance to string. """
    string = ''
    for row in self._matrix:
      for value in row:
        string += '{} '.format(value)
      string += '\n'
    return string
  
  def __add__(self, matrix):
    """ Override + operator. """
    return self._elementwise(matrix, operator.add)

  def __sub__(self, matrix):
    """ Override - operator. """
    return self._elementwise(matrix, operator.sub)

  def __mul__(self, matrix):
    """ Override * operator. """
    return self._elementwise(matrix, operator.mul)

  def __truediv__(self, matrix):
    """ Override / operator. """
    return self._elementwise(matrix, operator.truediv)

  def det(self):
    """ Compute the determinant. """
    if self.shape == (1, 1):
      return self._matrix[0][0]
    assert self._row_count == self._column_count, 'Determinant is only available for square matrix.'
    if self._row_count == 2:
      return self._matrix[0][0] * self._matrix[1][1] - self._matrix[0][1] * self._matrix[1][0]
    result = 0
    for index, value in enumerate(self._matrix[0]):
      coefficient = (-1) ** index * value
      minor = Matrix([row[:index] + row[index + 1:] for row in self._matrix[1:]]) # find the minor matrix
      result += coefficient * minor.det()
    return result

  def dot(self, matrix):
    """ Compute the dot product of matrixes.
      :param Matrix matrix
    """
    assert isinstance(matrix, Matrix), 'Operands must be Matrix instances.'
    assert len(self._matrix[0]) == len(matrix._matrix), 'The shapes of operands are not compatible.'
    result = [[] for i in range(self._row_count)]
    for row_index, row in enumerate(result):
      for column in matrix.transpose()._matrix:
        dot_product = _dot_product(self._matrix[row_index], column) # the dot product of row and column
        row.append(dot_product)
    return Matrix(result)
  
  def _elementwise(self, matrix, operator):
    """ Implementation of elementwise operations. Users should not call _elementwise.
      :param Matrix matrix
      :param callable operator: operator(left, right)
    """
    assert isinstance(matrix, Matrix), 'Operands must be Matrix instances.'
    assert self.shape == matrix.shape, 'Incompatible shapes.'
    result = [[] for i in range(len(self._matrix))]
    for row_index, row in enumerate(self._matrix):
      for column_index, value in enumerate(row):
        value = operator(value, matrix._matrix[row_index][column_index])
        result[row_index].append(value)
    return Matrix(result)

  @property
  def shape(self):
    """ Return the shape of matrix in the form of (row, column). """
    return self._row_count, self._column_count

  def to_list(self):
    """ Convert the matrix to a (nested) list. """
    matrix = [[] for i in range(self._row_count)]
    for index, row in enumerate(matrix):
      row.extend(self._matrix[index])
    return matrix

  def transpose(self):
    """ Return a transposed matrix. """
    return Matrix(list(zip(*self._matrix)))

def _dot_product(left, right):
  """ Compute the dot product of vectors. Helper function for Matrix.dot.
    :param iterable left: Vector.
    :param iterable right: Vector.
    Users should not call _dot_product.
  """
  return sum(l * r for l, r in zip(left, right))

def _test_equal(array, matrix, accuracy=1E-4):
  """ Test the equality of numpy.ndarray instance and Matrix instance. Only for the purpose of unit test. Users should not call _test_equal.
    :param numpy.ndarray array
    :param Matrix matrix
    :param float accuracy: Tolerance of numerical instability.
  """
  import numpy as np
  error = np.abs(array - np.array(matrix.to_list()))
  return error.max() < accuracy

def _test():
  """
    Unit test.
    Users should not call _test.
  """
  # initialization
  matrix_list = [[1] * 3, [2] * 3, [3] * 3]
  matrix = Matrix(matrix_list)
  print('matrix')
  print(matrix) # __str__
  # modification of matrix_list cannot affect matrix
  matrix_list.append([1024] * 3)
  print('modified matrix_list', matrix_list)
  print('matrix')
  print(matrix)

  import numpy as np

  # elementwise operation
  shape = (16, 64)
  left_array = np.random.random(shape)
  right_array = np.random.random(shape)
  left_matrix = Matrix(left_array.tolist())
  right_matrix = Matrix(right_array.tolist())
  print('Test + operation', _test_equal(left_array + right_array, left_matrix + right_matrix))
  print('Test - operation', _test_equal(left_array - right_array, left_matrix - right_matrix))
  print('Test * operation', _test_equal(left_array * right_array, left_matrix * right_matrix))
  print('Test / operation', _test_equal(left_array / right_array, left_matrix / right_matrix))

  # dot product
  left_shape = (4, 2)
  right_shape = (2, 4)
  left_array = np.random.random(left_shape)
  right_array = np.random.random(right_shape)
  result_array = np.dot(left_array, right_array)

  left_matrix = Matrix(left_array.tolist())
  right_matrix = Matrix(right_array.tolist())
  result_matrix = left_matrix.dot(right_matrix)
  
  print('Test dot product', _test_equal(result_array, result_matrix))

  # determinant
  import numpy.linalg as la
  accuracy = 4 # tolerate Python's numerical instability
  N = 4
  array = np.random.random((N, N))
  array_det = round(la.det(array), accuracy)
  matrix = Matrix(array.tolist())
  matrix_det = round(matrix.det(), accuracy)
  print('Test determinant', array_det == matrix_det)

if __name__ == '__main__':
  _test() 
