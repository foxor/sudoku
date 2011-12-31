#!/usr/bin/env python
import random

class LatinSquare(object):
  def __init__(self, size):
    done = False
    while not done:
      self.size = size
      self.setup_data()
      done = self.fill()

  def setup_data(self):
    self.row_restrictions = [0 for x in xrange(self.size)]
    self.col_restrictions = [0 for x in xrange(self.size)]
    self.data = [0 for x in range(self.size * self.size)]

  def format(self):
    return "\n".join([" ".join(["%2d" % x for x in self.data[x*self.size:(x+1)*self.size]]) for x in range(self.size)])

  def get_restrictions(self, row, col):
    return self.row_restrictions[row] | self.col_restrictions[col]

  def find_possible(self, row, col):
    restrictions = self.get_restrictions(row, col)
    possible = list(x for x in range(1, self.size + 1) if not (restrictions >> x) & 1)
    if possible:
      val = possible[random.randint(0, len(possible) - 1)]
      self.fill_spot(row, col, val)
      return val
    return None

  def fill_spot(self, row, col, val):
    self.row_restrictions[row] |= 1 << val
    self.col_restrictions[col] |= 1 << val
    self.data[self.size * row + col] = val

  def revert_spot(self, row, col):
    self.row_restrictions[row] &= -1 ^ (1 << self.data[self.size * row + col])
    self.col_restrictions[col] &= -1 ^ (1 << self.data[self.size * row + col])
    self.data[self.size * row + col] = 0

  def fill_row(self, row, depth):
    for col in range(self.size):
      if not self.find_possible(row, col):
        for xcol in range(col):
          self.revert_spot(row, xcol)
        if depth:
          return self.fill_row(row, depth - 1)
        else:
          return False
    return True

  def fill(self):
    for row in range(self.size):
      if not self.fill_row(row, self.size):
        return False
    return True

class Sudoku(LatinSquare):
  def __init__(self):
    super(Sudoku, self).__init__(9)

  def setup_data(self):
    self.box_restrictions = [0 for x in range(9)]
    super(Sudoku, self).setup_data()

  def get_restrictions(self, row, col):
    return self.box_restrictions[col / 3 + 3 * (row / 3)] | super(Sudoku, self).get_restrictions(row, col)

  def revert_spot(self, row, col):
    self.box_restrictions[col / 3 + 3 * (row / 3)] &= -1 ^ (1 << self.data[self.size * row + col])
    super(Sudoku, self).revert_spot(row, col)

  def fill_spot(self, row, col, val):
    self.box_restrictions[col / 3 + 3 * (row / 3)] |= 1 << val
    super(Sudoku, self).fill_spot(row, col, val)

  def format(self):
    return ("\n" + '-' * 3 * 11 + "\n").join(['\n'.join(['  | '.join([' '.join(['%2s' % x for x in self.data[9*z+y:9*z+y+3]]) for y in range(0, 8, 3)]) for z in range(a,a+3)]) for a in range(0, 8, 3)]) + "\n\n"

if __name__ == '__main__':
  print Sudoku().format()
