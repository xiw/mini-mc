#!/usr/bin/env python

# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

"""
This resembles Figure 4 of the UC-KLEE paper (CAV'11).
"""

from mc import *

def ffs_newlib(x):
  if x == 0:
    return 0
  i = 0
  while True:
    t = (1 << i) & x
    i = i + 1
    if t != 0:
      return i

def ffs_uclibc(i):
  n = 1
  if (i & 0xffff) == 0:
    n = n + 16
    i = i >> 16
  if (i & 0xff) == 0:
    n = n + 8
    i = i >> 8
  if (i & 0x0f) == 0:
    n = n + 4
    i = i >> 4
  if (i & 0x03) == 0:
    n = n + 2
    i = i >> 2
  if i != 0:
    return n + ((i + 1) & 0x01)
  return 0

x = BitVec("x", 32)
assert ffs_newlib(x) == ffs_uclibc(x)
