#!/usr/bin/env python
import random

class LatinSquare(object):
  def __init__(self, size):
    self.done = False
    while not self.done:
      self.row_restrictions = []
      self.col_restrictions = []
      self.data = []
      self.size = size
      self.done = self.fill()
    print self.format()

  def format(self):
    return "\n".join([" ".join(["%2d" % x for x in self.data[x*self.size:(x+1)*self.size]]) for x in range(self.size)])

  def fill_spot(self, row, col):
    restrictions = self.row_restrictions[row] | self.col_restrictions[col]
    possible = [x for x in range(1, self.size + 1) if not (restrictions >> x) & 1]
    if possible:
      val = possible[random.randint(0, len(possible) - 1)]
      self.row_restrictions[row] |= 1 << val
      self.col_restrictions[col] |= 1 << val
      self.data[self.size * row + col] = val
      return val
    return None

  def revert_spot(self, row, col):
    self.row_restrictions[row] &= -1 ^ (1 << self.data[self.size * row + col])
    self.col_restrictions[col] &= -1 ^ (1 << self.data[self.size * row + col])
    self.data[self.size * row + col] = 0

  def fill_row(self, row, depth):
    for col in range(self.size):
      while len(self.col_restrictions) <= col:
        self.col_restrictions.append(0)
      while len(self.data) <= self.size * row + col:
        self.data.append(0)
      if not self.fill_spot(row, col):
        for xcol in range(col):
          self.revert_spot(row, xcol)
        if depth:
          return self.fill_row(row, depth - 1)
        else:
          return False
    return True

  def fill(self):
    for row in range(self.size):
      while len(self.row_restrictions) <= row:
        self.row_restrictions.append(0)
      if not self.fill_row(row, self.size):
        return False
    return True

if __name__ == '__main__':
  import sys
  size = 5
  if len(sys.argv) == 2:
    size = int(sys.argv[1])
  l = LatinSquare(size)
