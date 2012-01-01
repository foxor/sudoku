#!/usr/bin/env python

import random

from main import Sudoku

class Multiplayer_Sudoku(Sudoku):
  def __init__(self, players, revealed=0):
    super(Multiplayer_Sudoku, self).__init__()
    self.players = players
    self.mistakes = dict((x,0) for x in players)
    self.cur_player = 0
    self.known_data = list(False for x in range(len(self.data)))
    for reveal in sorted(range(len(self.data)), key=lambda x: random.random())[:revealed]:
      self.known_data[reveal] = True

  def format(self):
    self.data_bak = self.data
    self.data = list(self.data[x] if self.known_data[x] else "?" for x in range(len(self.data)))
    r = "Errors: %s\n\nCurrent Player: %s\n\n%s" % (self.mistakes, self.players[self.cur_player], super(Multiplayer_Sudoku, self).format())
    self.data = self.data_bak
    return r

  def done(self):
    return all(self.known_data)

  def guess(self, row, col, val):
    if val == self.data[col + row * self.size]:
      self.known_data[col + row * self.size] = True
      return True
    return False

  def unknown(self, row, col):
    return not self.known_data[col + row * self.size]

  def interactive(self):
    while not self.done():
      try:
        print self.format()
        row,col,val = (int(x) for x in raw_input("Please enter your seletion in the form 'row col val' where each is a number 1-9\n--->").split(' '))
        assert 1 <= row and row <= 9
        assert 1 <= col and col <= 9
        assert 1 <= val and val <= 9
        row -= 1
        col -= 1
      except KeyboardInterrupt:
        print "\nbye!"
        break
      except:
        raw_input("That isn't formatted like I expect.\n\n Say you want to put the number 1 in the first spot, try '1 1 1' (without quotes)\n\nPress enter to continue")
        continue
      if self.unknown(row, col):
        if not self.guess(row, col, val):
          raw_input("Wrong! <press enter to continue>")
          self.mistakes[self.players[self.cur_player]] = self.mistakes[self.players[self.cur_player]] + 1
        else:
          raw_input("Correct! <press enter to continue>")
        self.cur_player = (self.cur_player + 1) % len(self.players)
      else:
        raw_input("That square is already full. <press enter to continue")
    print "\n" * 10
    self.players.sort(key=lambda x: self.mistakes[x])
    if len(self.players) == 1:
      print "You Win!"
    elif self.mistakes[self.players[0]] == self.mistakes[self.players[1]]:
      print "Tie Game!"
    else:
      print "%s Wins!" % self.players[0]
    print "Final score (mistakes):"
    print "\n".join("%s: %d" % (x, self.mistakes[x]) for x in self.players)

if __name__ == '__main__':
  names = []
  while True:
    name = raw_input("Please enter the name of player #%d <empty if done>: " % (len(names) + 1))
    if not name:
      if not names:
        names = ["anonymous"]
      break
    names.append(name)
  Multiplayer_Sudoku(names, 10).interactive()
