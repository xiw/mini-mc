# -*- coding: utf-8 -*-

# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

# ---------------------------------------------------------------
# klee
# ---------------------------------------------------------------

from mc_util import *

def sched_fork(self):
  pid = os.fork()
  if pid:
    solver.add(self)
    r = True
    mc_log("assume (%s)" % (str(self),))
  else:
    solver.add(Not(self))
    r = False
    mc_log("assume ¬(%s)" % (str(self),))
  if solver.check() != sat:
    mc_log("unreachable")
    sys.exit(0)
  return r

setattr(BoolRef, "__bool__", sched_fork)
setattr(BoolRef, "__nonzero__", sched_fork)

# ---------------------------------------------------------------
# sage
# ---------------------------------------------------------------

def sched_flip(self, trace):
  solver.push()
  solver.add(self)
  r = (solver.check() == sat)
  solver.pop()
  if r:
    cond = self
  else:
    cond = Not(self)
  trace.append(cond)
  mc_log("%s: %s" % (self, r))
  return r

def mc_fuzz(f, init_keys, init_vals, cnt = 0):
  mc_log("=" * 60)
  mc_log("#%s: %s" % (cnt, ', '.join(["%s = %s" % (k, v) for k, v in zip(init_keys, init_vals)])))

  trace = []
  setattr(BoolRef, "__bool__", lambda self: sched_flip(self, trace))
  setattr(BoolRef, "__nonzero__", getattr(BoolRef, "__bool__"))

  solver.push()
  assert len(init_keys) == len(init_vals)
  for i, k in enumerate(init_keys):
    v = init_vals[i]
    solver.add(k == v)
  try:
    f()
  except:
    typ, value, tb = sys.exc_info()
    sys.excepthook(typ, value, tb)
  solver.pop()
  # this path done
  solver.add(Not(And(*trace)))

  delattr(BoolRef, "__bool__")
  delattr(BoolRef, "__nonzero__")

  # choose a new path
  while trace:
    solver.push()
    solver.add(Not(trace[-1]))
    trace = trace[:-1]
    solver.add(*trace)
    r = solver.check()
    solver.pop()
    if r != sat:
      continue
    m = solver.model()
    new_init_vals = [m.eval(k, model_completion=True) for k in init_keys]
    cnt = mc_fuzz(f, init_keys, new_init_vals, cnt + 1)

  return cnt
