from itertools import combinations
import random

class Node:
  def __init__(self, parent=None, children=[], move=None, value=None):
    self.parent = parent
    self.children = children
    self.move = move
    self.value = value
  def append_child(self, child):
    child.parent = self
    self.children.append(child)
  def depth(self):
    result = 0
    node = self
    while node.parent is not None:
      node = node.parent
      result += 1
    return result
  def goto(self, move):
    for child in self.children:
      if child.move == move:
        return child
    return None

def choose_move(root, moves):
  # TODO random choice
  node = root
  for move in moves:
    children_moves = [child.move for child in node.children]
    index = children_moves.index(move)
    node = node.children[index]
  values = [child.value for child in node.children]
  player = len(moves) % 2
  if player == 0:
    metric = max
  else:
    metric = min
  optimal = metric(values)
  index = random.choice([index for index, value in enumerate(values) if value == optimal])
  optimal_move = node.children[index].move
  return optimal_move

def to_coordinate(n):
  X = n % 3
  Y = int(n / 3)
  return X, Y

def AP(s):
  # whether a sequence is an arithmetic progression
  s = [left + right for left, right in zip(s, s[::-1])]
  return min(s) == max(s)

def judge(moves):
  if len(moves) < 5:
    return 0
  player = (len(moves) - 1) % 2
  player_moves = [move for index, move in enumerate(moves) if index % 2 == player]
  player_moves.sort()
  for sequence in combinations(player_moves, 3):
    coordinates = map(to_coordinate, sequence)
    X, Y = zip(*coordinates)
    if AP(X) and AP(Y):
      return 1 if player == 0 else -1
  return 0

def to_string(moves, symbol='XO', line_delimiter='-', column_delimiter='|'):
  string = []
  for i in range(9):
    try:
      index = moves.index(i) % 2
      string.append(symbol[index])
    except:
      string.append(str(i))
    if i % 3 == 2:
      string.append('\n')
  return ''.join(string)

if __name__ == '__main__':
# print(judge([0, 1, 3, 6, 4, 5, 8]))
  '''
  for i in range(9):
    print(to_coordinate(i))
  '''
  print(judge([0, 1, 4, 8, 3, 5, 6]))
