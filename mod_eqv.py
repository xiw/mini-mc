#!/usr/bin/env python

# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

"""
This resembles Figure 11 of the KLEE paper (OSDI'08).
"""

from mc import *

def mod_opt(x, y):
  if y & (-y) == y:
    return x & (y - 1)
  else:
    return x % y

def mod(x, y):
  return x % y

# Z3 is not very happy with n = 32
n = 16
mc_unsignedBitVec()
x = BitVec("x", n)
y = BitVec("y", n)
# seems okay without mc_assume(y != 0)
mc_assert(mod(x, y) == mod_opt(x, y))
