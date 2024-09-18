from time import time

from mythril.support.support_utils import Singleton

from typing import Callable
import z3
import sys


def stat_smt_query(func: Callable):
    """Measures statistics for annotated smt query check function"""
    stat_store = SolverStatistics()

    def function_wrapper(*args, **kwargs):
        if not stat_store.enabled:
            return func(*args, **kwargs)

        stat_store.query_count += 1
        begin = time()

        result = func(*args, **kwargs)

        end = time()
        stat_store.solver_time += end - begin

        return result

    return function_wrapper


class SolverStatistics(object, metaclass=Singleton):
    """Solver Statistics Class

    Keeps track of the important statistics around smt queries
    """

    def __init__(self):
        self.enabled = False
        self.query_count = 0
        self.solver_time = 0

    def __repr__(self):
        return "Query count: {} \nSolver time: {}".format(
            self.query_count, self.solver_time
        )


s = z3.Optimize()
# before_rlimit_count = 0
s.check()
# after_rlimit_count = s.statistics().get_key_value("rlimit count")
# print("run", after_rlimit_count-before_rlimit_count,  before_rlimit_count, after_rlimit_count)

def stat_rlimit(func):
    def function_wrapper(*args, **kwargs):
        f = sys._getframe()
        func_name = f.f_back.f_code.co_name
        s = z3.Optimize()
        r1 = s.statistics().get_key_value("rlimit count")
        result = func(*args, **kwargs)
        r2 = s.statistics().get_key_value("rlimit count")
        print(func_name, r1, r2)
        return result

    return function_wrapper
