from itertools import permutations
from facility import *

def factorial(n):
  return n * factorial(n - 1) if n else 1

N = 9
TOTAL = factorial(N)

def calculate_value(node):
  # calculate the value of a node
  if node.value is None:
    children_value = list(calculate_value(child) for child in node.children)
    if node.depth() % 2 == 0:
      node.value = max(children_value)
    else:
      node.value = min(children_value)
  return node.value

def generate(interval=TOTAL / 10):
  # generate a tree
  root = Node()
  sequences = permutations(range(N))

  # record sequences in a tree
  for index, sequence in enumerate(sequences):
    # logging
    if (index + 1) % interval == 0:
      print('%d percent of configurations loaded'% ((index + 1) * 100 / TOTAL))
    parent = root
    for index, move in enumerate(sequence):
      children_moves = [child.move for child in parent.children]
      try:
        move_index = children_moves.index(move)
        child = parent.children[move_index]
      except:
        child = Node(move=move)
        parent.append_child(child)
      value = judge(sequence[:index + 1])
      if value == 0 and index != len(sequence) - 1:
        parent = child
      else:
        child.value = value
        break
  calculate_value(root)
  return root
