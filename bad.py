#!/usr/bin/env python

# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

"""
Resembles Figure 1 of the SAGE paper (NDSS'08).
Will genereate five inputs.
"""

from mc import *

def top(s):
  cnt = 0 ;
  if s[0] == ord('b'):
    cnt = cnt + 1
  if s[1] == ord('a'):
    cnt = cnt + 1
  if s[2] == ord('d'):
    cnt = cnt + 1
  if s[3] == ord('!'):
    cnt = cnt + 1
  if cnt >= 3:
    assert False

n = 4
names = " ".join(["s[%s]" % (i,) for i in range(n)])
s = BitVecs(names, 8)
#top(s)
mc_fuzz(lambda: top(s), s, [0] * n)
