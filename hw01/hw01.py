'''
Data Structure HW01
By Yu Gai (NetID: yg1246)

This is a script simulating Conway's Game of Life.
The comments of functions is written in a format recognizable for documentation generators. 
The format is 
    """ general description
        :param <parameter type> <parameter name>: parameter description
        ...
    """
This script accepts command line arguments, as described in NYUClasses.
'''

from copy import deepcopy

def input_grid(name, columns, rows):
  """ Read the initial state from an input file.
    :param str name: input file name.
    :param int columns: the number of columns.
    :param int rows: the number of rows.
  """
  with open(name, 'r') as input_file:
    file_content = input_file.read()
    file_content = file_content.split('\n')

  maximum_length = max(len(row) for row in file_content)
  if columns:
    assert columns >= maximum_length
  else:
    columns = maximum_length

  if rows:
    assert rows >= len(file_content)
  else:
    rows = len(file_content)

  grid = [[False for column in range(columns)] for row in range(rows)]

  for row_index, row in enumerate(file_content):
    for column_index, cell in enumerate(row):
      if cell == '*':
        grid[row_index][column_index] = True

  return grid

def output_grid(grid):
  """ Generate a string representation for the grid.
    :param list grid: the grid from which a string is generated.
  """
  converted_grid = '\n'.join(
    tuple(
      ''.join('*' if cell else '-' for cell in row) for row in grid
    )
  )
  converted_grid += '\n'
  return converted_grid

def output(grids, boundary_length=32):
  """ Return a string about the history of evolution.
    :param list grids: a list containing history of grids.
    :param int boundary_length: the length of the lines composed of '=' between grids.
  """
  output = []
  for index, grid in enumerate(grids):
    output.append('Generation %d:\n' % index)
    output += grid
    output.append('=' * boundary_length + '\n')
  return ''.join(output)
 
def is_living(grid, row_index, column_index):
  """ Helper function to handle the case that index is out of range.
    :param list grid: the grid to index.
    :param int row_index: row index.
    :param int column_index: column index.
  """
  if row_index in range(len(grid)) and column_index in range(len(grid[0])):
    return grid[row_index][column_index]
  else:
    return 0

def evolve(grid):
  """ Evolve a grid.
    :param list grid: the grid to evolve.
  """
  resulted_grid = deepcopy(grid)
  for row_index, row in enumerate(grid):
    for column_index, cell in enumerate(row):
      life_count = 0
      life_count += is_living(grid, row_index + 1, column_index)
      life_count += is_living(grid, row_index - 1, column_index)
      life_count += is_living(grid, row_index, column_index - 1)
      life_count += is_living(grid, row_index, column_index + 1)
      life_count += is_living(grid, row_index - 1, column_index - 1)
      life_count += is_living(grid, row_index + 1, column_index + 1)
      life_count += is_living(grid, row_index - 1, column_index + 1)
      life_count += is_living(grid, row_index + 1, column_index - 1)
      if cell:
        if life_count < 2 or life_count > 3:
          resulted_grid[row_index][column_index] = False
      else:
        if life_count == 3:
          resulted_grid[row_index][column_index] = True
  return resulted_grid

def main():
  """ Main program.
  """
  import sys

  args = dict(enumerate(sys.argv[1:]))
  generations = int(args.pop(0, 10))
  input_file  = args.pop(1, 'life.txt')
  rows        = int(args.pop(2, 10))
  columns     = int(args.pop(3, 10))

  grid = input_grid(input_file, columns, rows)

  history = [] # the history of evolution
  history.append(grid)
  current_grid = grid

  for g in range(generations):
    current_grid = evolve(current_grid)
    history.append(current_grid)

  with open('output.txt', 'w') as output_file:
    output_file.write(
      output(
        [output_grid(h) for h in history]
      )
    )

if __name__ == '__main__':
  main()
