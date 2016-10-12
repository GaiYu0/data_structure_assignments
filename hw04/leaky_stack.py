class Empty(LookupError):
  """ The exception raised if top or pop method is called on empty LeakyStack instances. """
  def __str__(self):
    return 'Empty Exception' 

class LeakyStack:
  def __init__(self, capacity):
    self._array = [None for i in range(capacity)]
    self._bottom = 0
    self._length = 0

  def __str__(self):
    if self._length == 0:
      return '[]' 

    string = '[' + '{} ' * (self._length - 1) + '{}' + ']' # construct a format string
    values = []
    for offset in range(self._length):
      index = (self._bottom + offset) % self._length
      values.append(self._array[index])
    return string.format(*values) # unpack values to fill the string

  def is_empty(self):
    return self._length == 0

  def push(self, element):
    if self._length == len(self._array):
      self._array[self._bottom] = element
      self._bottom = (self._bottom + 1) % len(self._array)
    else:
      top = (self._bottom + self._length) % len(self._array)
      self._array[top] = element
      self._length += 1

  def pop(self):
    if self._length == 0:
      raise Empty()
    else:
      top = (self._bottom + self._length - 1) % len(self._array)
      value = self._array[top]
      self._array[top] = None
      self._length -= 1
      return value

  def top(self):
    if self._length == 0:
      raise Empty()
    else:
      top = (self._bottom + self._length - 1) % len(self._array)
      return self._array[top]

def _test_leaky_stack():
  print('testing LeakyStack.__init__')
  stack = LeakyStack(3)
  print('testing LeakyStack.__str__')
  print(stack)
  print('testing LeakyStack.is_empty')
  print('empty:', stack.is_empty())
  print('testing LeakyStack.push')
  for i in range(8):
    stack.push(i)
    print(stack)
  print('testing LeakyStack.top and LeakyStack.pop')
  for i in range(3):
    print('top element', stack.top())
    print('popped element', stack.pop())
    print('stack', stack)
  print('empty:', stack.is_empty())
  print('testing whether LeakyStack.top and LeakyStack.pop raise exceptions properly')
  try:
    stack.top()
  except Exception as e:
    print(e)
  try:
    stack.pop()
  except Exception as e:
    print(e)

if __name__ == '__main__':
  _test_leaky_stack()
