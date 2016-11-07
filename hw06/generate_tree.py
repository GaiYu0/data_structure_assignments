from itertools import permutations
from facility import *

def factorial(n):
  return n * factorial(n - 1) if n else 1

N = 9
TOTAL = factorial(N)

called = 0
def calculate_value(node):
  global called
  called += 1
  if node.value is None:
    children_value = list(calculate_value(child) for child in node.children)
    if node.depth() % 2 == 0:
      node.value = max(children_value)
    else:
      node.value = min(children_value)
  return node.value

def generate(interval=TOTAL / 10):
  root = Node()
  sequences = permutations(range(N))
  for index, sequence in enumerate(sequences):
    if (index + 1) % interval == 0:
      print('%d percent of configurations loaded'% ((index + 1) * 100 / TOTAL))
    parent = root
    for index, move in enumerate(sequence):
      children_moves = [child.move for child in parent.children]
      try:
        move_index = children_moves.index(move)
        child = parent.children[move_index]
      except:
        child = Node(children=[], move=move) # TODO
        parent.append_child(child)
      '''
      child = parent.goto(move)
      if child is None:
        child = Node(children=[], move=move) # TODO
        parent.append_child(child)
      '''
      value = judge(sequence[:index + 1])
      if value == 0 and index != len(sequence) - 1:
        parent = child
      else:
        child.value = value
        break
  calculate_value(root)
  return root

if __name__ == '__main__':
  import pickle
  root = generate()
  queue = [root]
  none_count = 0
  while queue:
    node = queue.pop()
    if node.value is None:
      none_count += 1
      iterator = node
      print('#' * 10)
      while iterator.parent is not None:
        print(iterator.move)
        iterator = iterator.parent
    queue.extend(node.children)
  print('none', none_count)

# pickle.dump(root, open('game_configurations', 'wb'))
