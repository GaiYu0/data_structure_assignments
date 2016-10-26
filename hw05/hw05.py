class Node:
  __slots__ = 'data', 'next_node'

  def __init__(self, data, next_node=None):
    self.data = data
    self.next_node = next_node

  def __iter__(self):
    node = self
    while node is not None:
      yield node
      node = node.next_node
  
  def __len__(self):
    return sum(1 for node in self)

  def __str__(self):
    elements = []
    node = self
    while node is not None:
      elements.append(str(node.data))
      node = node.next_node
    return ' '.join(elements)

def reverse_list(node):
  if node.next_node:
    head = reverse_list(node.next_node)
    node.next_node.next_node = node
    node.next_node = None
    return head
  else:
    return node

def bubble_sort(head):
  total = len(head) - 1
  for node in head:
    count = 0
    for iterator in head:
      if count == total:
        break
      if iterator.data > iterator.next_node.data:
        iterator.data, iterator.next_node.data = \
          iterator.next_node.data, iterator.data
      count += 1
    total -= 1

def shuffle_list(head):
  length = len(head)
  count = 0
  for node in head:
    count += 1
    if count == int(length / 2):
      head0 = node.next_node
      node.next_node = None
      break
  iterator = head
  for i in range(length // 2):
    to_insert = head0
    head0 = head0.next_node
    to_insert.next_node = iterator.next_node
    iterator.next_node = to_insert
    iterator = to_insert.next_node
  to_insert.next_node = head0
  
if __name__ == '__main__':
  linked_list = Node(
    34, Node(
      1, Node(
        8, Node(
          3, Node(
            55, Node(
              21, Node(
                13, Node(
                  2, Node(
                    1
  )))))))))
  print('{:<12}'.format('linked list'), linked_list)
  linked_list = reverse_list(linked_list)
  print('{:<12}'.format('reverse'), linked_list)
  bubble_sort(linked_list)
  print('{:<12}'.format('bubble sort'), linked_list)
  shuffle_list(linked_list)
  print('{:<12}'.format('shuffle'), linked_list)
