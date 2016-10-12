class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    if next_node is not None:
      assert isinstance(next_node, Node)
    self.next_node = next_node

  def __iter__(self):
    node = self
    while node is not None:
      yield node
      node = node.next_node

  def __str__(self):
    return ' '.join(str(node.value) for node in self)

def splice(to, front):
  for node in front:
    back = node
  back.next_node = to.next_node
  to.next_node = front

def is_sublist(list_front, sublist_front):
  from copy import deepcopy
  for list_node in list_front:
    local_iterator = deepcopy(list_node)
    matched = True
    for sublist_node in sublist_front:
      if local_iterator is None or local_iterator.value != sublist_node.value:
        matched = False
        break
      local_iterator = local_iterator.next_node
    if matched:
      return list_node
  return None

def _test():
  # splice
  original = Node(
    5,
    Node(
      7,
      Node(
        9,
        Node(1)
      )
    )
  )
  to_splice = Node(
    6,
    Node(
      3,
      Node(2)
    )
  )
  print('original linked list:', original)
  print('the linked list to splice:', to_splice)
  splice(original.next_node, to_splice)
  print('spliced linked list:', original)

  # sublist
  def test_sublist(list_front, sublist_front):
    print('the original list', list_front)
    print('the sublist to match', to_match)
    node = is_sublist(original, to_match)
    if node is not None:
      print('the returned node points to', node.value)
    else:
      print('not sublist')

  # case 0
  to_match = Node(
    6,
    Node(
      3,
      Node(
        2,
        Node(9)
      )
    )
  )
  test_sublist(original, to_match)

  # case 1
  to_match = Node(
    6,
    Node(
      2,
      Node(3)
    )
  )
  test_sublist(original, to_match)

  # case 2
  to_match = Node(
    2,
    Node(
      9,
      Node(
        1,
        Node(4)
      )
    )
  )
  test_sublist(original, to_match)

  # extra case 0
  to_match = Node(0)
  test_sublist(original, to_match)

  # extra case 1
  to_match = Node(5)
  test_sublist(original, to_match)

  # extra case 2
  to_match = Node(
    2,
    Node(
      9,
      Node(1)
    )
  )
  test_sublist(original, to_match)

if __name__ == '__main__':
  _test()
