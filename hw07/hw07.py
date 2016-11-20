class Heap:
  def __init__(self, compare):
    self._compare = compare

  def __getitem__(self, location):
    return self._array[location]
  
  def __setitem__(self, location, value):
    self._array[location] = value
    self._up(location)
    self._down(location)

  def __str__(self):
    lines = []
    def to_string(index=0, tabs=0):
      lines.append('+' * (tabs + 1) + '-' + str(self._array[index]))
      if self._leaf(index):
        return
      else:
        left_index = self._left(index)
        to_string(left_index, tabs + 1)
        right_index = self._right(index)
        if right_index < len(self._array):
          to_string(right_index, tabs + 1)
    to_string()
    return  '\n'.join(lines)

  def _parent(self, index):
    return (index - 1) // 2

  def _left(self, index):
    return index * 2 + 1

  def _right(self, index):
    return index * 2 + 2

  def _leaf(self, index):
    end = len(self._array) - 1
    return end < self._left(index) and end < self._right(index)

  def _up(self, index):
    parent_index = self._parent(index)
    if parent_index < 0:
      return
    else:
      parent_value = self._array[parent_index]
      child_value = self._array[index]
      if self._compare(child_value, parent_value):
        self._array[parent_index], self._array[index] = child_value, parent_value
        parent_value.set_location(self, index)
        child_value.set_location(self, parent_index)
        return self._up(parent_index)
      else:
        return

  def _down(self, index):
    if self._leaf(index):
      return
    parent_value = self._array[index]
    left_index = self._left(index)
    left_value = self._array[left_index]
    right_index = self._right(index)
    if right_index < len(self._array):
      right_value = self._array[right_index]
      extremum_index = index
      extremum_value = parent_value
      if self._compare(left_value, parent_value):
        extremum_index = left_index
        extremum_value = left_value
      if self._compare(right_value, extremum_value):
        extremum_index = right_index
        extremum_value = right_value
      if extremum_index == index:
        return
      self._array[index], self._array[extremum_index] = extremum_value, parent_value
      extremum_value.set_location(self, index)
      parent_value.set_location(self, extremum_index)
      return self._down(extremum_index)
    else:
      if self._compare(left_value, parent_value):
        self._array[index], self._array[left_index] = left_value, parent_value
        left_value.set_location(self, index)
        parent_value.set_location(self, left_index)
      return
    
  @property
  def root(self):
    return self._array[0]

  def heapify(self, elements):
    self._array = elements[:]
    for index, element in enumerate(self._array):
      element.set_location(self, index)
    for index in range(len(self._array) - 1, -1, -1):
      if not self._leaf(index):
        end_index = index
        break
    for index in range(end_index, -1, -1):
      self._down(index)

class Player:
  def __init__(self, p, locations):
    self._property = p
    self._locations = locations
  def __eq__(self, other):
    return self._property == other._property
  def __lt__(self, other):
    return self._property < other._property
  def __gt__(self, other):
    return self._property > other._property
  def __repr__(self):
    return self.__str__()
  def __str__(self):
    return str(self._property)
  def __sub__(self, other):
    return self._property - other._property
  def get_location(self, heap):
    return self._locations[heap]
  def set_location(self, heap, location):
    self._locations[heap] = location
  def transfer_to(self, other):
    self._property /= 2.0
    other._property += self._property
    return Player(self._property, self._locations), Player(other._property, other._locations)

def play(N_PLAYERS, THRESHOLD=1):
  import random
  from operator import lt, gt
  scale = 1E3
  minimum_heap = Heap(lt)
  maximum_heap = Heap(gt)
  players = [Player(random.random() * scale, {minimum_heap : None, maximum_heap : None}) for i in range(N_PLAYERS)]
  minimum_heap.heapify(players)
  maximum_heap.heapify(players)

  iterations = 0
  while maximum_heap.root - minimum_heap.root > THRESHOLD:
    print('Poorest', minimum_heap.root, 'Wealthiest', maximum_heap.root)
    maximum, minimum = maximum_heap.root.transfer_to(minimum_heap.root)
    print('The property of the previously poorest player increases to %s.\n' % str(minimum))
    print('The property of the previously wealthiest player reduces to %s.\n' % str(maximum))
    maximum_heap[maximum.get_location(maximum_heap)] = maximum
    maximum_heap[minimum.get_location(maximum_heap)] = minimum
    minimum_heap[maximum.get_location(minimum_heap)] = maximum
    minimum_heap[minimum.get_location(minimum_heap)] = minimum
    '''
    print('minimum_heap')
    print(minimum_heap)
    print('maximum_heap')
    print(maximum_heap)
    '''
#   input();
    iterations += 1

def to_accuracy(value, accuracy):
  return str(value)[:accuracy]

def test_play(N_PLAYERS, ITERATIONS, ACCURACY=6):
  import os
  import pickle
  import random

  if os.path.exists('./error_values'):
    initial_values = pickle.load(open('./error_values', 'rb'))
  else:
    scale = 1E3
    initial_values = [random.random() * scale for i in range(N_PLAYERS)]
# print('repeated', len(initial_values) != len(set(initial_values)))

  def heap_play():
    from operator import lt, gt
    minimum_heap = Heap(lt)
    maximum_heap = Heap(gt)
    players = [Player(value, {minimum_heap : None, maximum_heap : None}) for value in initial_values]
    minimum_heap.heapify(players)
    maximum_heap.heapify(players)
    log = [(to_accuracy(maximum_heap.root, ACCURACY), to_accuracy(minimum_heap.root, ACCURACY))]
    for i in range(ITERATIONS):
      maximum, minimum = maximum_heap.root.transfer_to(minimum_heap.root)
      log.append((to_accuracy(maximum, ACCURACY), to_accuracy(minimum, ACCURACY)))
      maximum_heap[maximum.get_location(maximum_heap)] = maximum
      maximum_heap[minimum.get_location(maximum_heap)] = minimum
      minimum_heap[maximum.get_location(minimum_heap)] = maximum
      minimum_heap[minimum.get_location(minimum_heap)] = minimum
    return log

  def array_play():
    values = initial_values[:]
    log = [(to_accuracy(max(values), ACCURACY), to_accuracy(min(values), ACCURACY))]
    for i in range(ITERATIONS):
      maximum_value = max(values)
      minimum_value = min(values)
      maximum_index = values.index(maximum_value)
      minimum_index = values.index(minimum_value)
      values[minimum_index] = minimum_value + maximum_value / 2.0
      values[maximum_index] = maximum_value / 2.0
      log.append(
        (
          to_accuracy(values[maximum_index], ACCURACY),
          to_accuracy(values[minimum_index], ACCURACY)
        )
      )
    return log

  heap_log = heap_play()
  array_log = array_play()
  matched = True
  for index, value in enumerate(zip(heap_log, array_log)):
    heap_entry, array_entry = value
    if heap_entry != array_entry:
      print('Error! Iteration %d\nHeap entry: %s\nArray entry: %s' % (index,heap_entry, array_entry)) 
      matched = False

  if not matched:
    pickle.dump(initial_values, open('./error_values', 'wb'))

  return matched
      
if __name__ == '__main__':
  import sys
  N_PLAYERS = int(sys.argv[1])
  if len(sys.argv) == 3:
    ITERATIONS = int(sys.argv[2])
    result = test_play(N_PLAYERS, ITERATIONS)
    print('Passed: {}'.format(result))
  else:
    play(N_PLAYERS)
