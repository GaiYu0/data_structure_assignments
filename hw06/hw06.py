import os
import pickle

from facility import *
from generate_tree import *

def print_board(moves):
  print('#########')
  print('# BOARD #')
  print('#########')
  print(to_string(moves))

def main(symbol='XO'):
  print('initializing')
  root = generate()

  choice = input('Would you like to use X or O?\n')
  if choice == 'X':
    human_player = 0
  elif choice == 'O':
    human_player = 1

  moves = []
  print_board(moves)
  for i in range(9):
    if i % 2 == human_player:
      move = int(input('How would you like to move?\n'))
      if move in moves:
        print('Invalid move!')
    else:
      move = choose_move(root, moves)
      print('Computer moves to %d.' % move)
    moves.append(move)
    print_board(moves)
    result = judge(moves)
    if result == 1:
      print('Winner: X')
      return
    elif result == -1:
      print('Winner: O')
      return
  print('Draw')
  return

if __name__ == '__main__':
  main()
