# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

from __future__ import print_function
from z3 import *
from multiprocessing import Lock
import os, atexit

solver = Solver()
lock = Lock()

def mc_log(s):
  # "atomic" print; less concern about performance
  with lock:
    print("[%s] %s" % (os.getpid(), s), file=sys.stderr)

def mc_assume(b):
  return solver.add(b)

def mc_assert(b):
  solver.push()
  solver.add(Not(b))
  r = solver.check()
  solver.pop()
  if r == sat:
    raise Exception(solver.model())

def mc_model_repr(self):
  decls = sorted(self.decls(), key=str)
  return ", ".join(["%s = %s" % (k, self[k]) for k in decls])

setattr(ModelRef, "__repr__", mc_model_repr)

def mc_unsignedBitVec():
  conf = {
    "__div__"    : UDiv,
    "__rdiv__"   : lambda self, other: UDiv(other, self),
    "__mod__"    : URem,
    "__rmod__"   : lambda self, other: URem(other, self),
    "__rshift__" : LShR,
    "__rrshift__": lambda self, other: LShR(other, self),
    "__lt__"     : ULT,
    "__le__"     : ULE,
    "__gt__"     : UGT,
    "__ge__"     : UGE
  }
  for k, v in conf.items():
    setattr(BitVecRef, k, v)

def mc_excepthook(typ, value, tb):
  import traceback
  from pygments import highlight
  from pygments.lexers import get_lexer_by_name
  from pygments.formatters import get_formatter_by_name

  code = ''.join(traceback.format_exception(typ, value, tb))
  lexer = get_lexer_by_name("pytb", stripall=True)
  formatter = get_formatter_by_name("terminal256")
  mc_log(highlight(code, lexer, formatter))

if sys.stderr.isatty():
  try:
    import pygments
    sys.excepthook = mc_excepthook
  except:
    pass

def mc_exit():
  # wait until all child processes done
  try:
    while True:
      os.waitpid(0, 0)
  except:
    pass
  mc_log("exit")

atexit.register(mc_exit)
