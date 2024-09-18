from functools import lru_cache
from z3 import sat, unknown, unsat
from pathlib import Path
from mythril.zdebug import stat_rlimit

from mythril.support.support_args import args
from mythril.laser.smt import Optimize, Solver
from mythril.laser.ethereum.time_handler import time_handler
from mythril.exceptions import UnsatError, SolverTimeOutException
import logging
from datetime import datetime
import os
import z3


log = logging.getLogger(__name__)
# LRU cache works great when used in powers of 2

caller2cnt = {}
caller2time = {}

def get_total_info():
    return {
        "caller2cnt": caller2cnt,
        "caller2time": caller2time
    }

def get_model_info(result, get_model_start_time, constraints, minimize, maximize, caller, rlimit, before_rlimit_count, after_rlimit_count, global_path, thistx_path):
    global last_rlimit_count
    constraint_hash_input = tuple(
        list(constraints)
        + list(minimize)
        + list(maximize)
        + [len(constraints), len(minimize), len(maximize)]
    )
    get_model_end_time = datetime.now()
    duration = get_model_end_time-get_model_start_time
    duration = duration.total_seconds()
    # print("get_model_info", result, abs(hash(constraint_hash_input)), caller, rlimit, before_rlimit_count, after_rlimit_count, global_path, thistx_path)
    print("get_model_info", result, caller, global_path, thistx_path, rlimit, duration)# , flush=True)
    
    if caller not in caller2cnt:
        caller2cnt[caller] = 0
        caller2time[caller] = 0
    caller2cnt[caller] += 1
    caller2time[caller] += duration

    # with open(
    #    f"BEC_rlimit-5000000/{abs(hash(constraint_hash_input))}.smt2", "w"
    # ) as f:
    #     f.write(s.sexpr())

def get_model_wrapper(
    constraints,
    minimize=(),
    maximize=(),
    enforce_execution_time=True,
    solver_timeout=None,
    caller=str("UNKNOWN"),
    global_path=None, thistx_path=None
):
    args.z3_uc = None
    get_model_start_time = datetime.now()
    solve_with_uc = ((args.use_ucc == "1" or args.use_ucx == "1") and caller == "is_possible")
    result, before_rlimit_count, after_rlimit_count, modelOrUc = get_model(constraints, minimize, maximize, enforce_execution_time, solver_timeout, want_uc=solve_with_uc)
    rlimit = after_rlimit_count - before_rlimit_count
    if result == sat:
        get_model_info("SAT", get_model_start_time, constraints, minimize, maximize, caller, rlimit, before_rlimit_count, after_rlimit_count, global_path, thistx_path)
        return modelOrUc
    elif result == unknown:
        log.debug("Timeout/Error encountered while solving expression using z3")
        get_model_info("UNKNOWN", get_model_start_time, constraints, minimize, maximize, caller, rlimit, before_rlimit_count, after_rlimit_count, global_path, thistx_path)
        
        if args.use_lent9=="1":
            if thistx_path != None:
                print("lent9 unknown", thistx_path)
                thistx_path_arr = thistx_path.split("-")
                if len(thistx_path_arr) > 2:
                    for i in range(len(thistx_path_arr)-1, 1, -1):
                        temp = "-".join(thistx_path_arr[0:i])
                        print("lent9 remove", temp) # aka. add NTRA
                        args.recalled_near_paths.add(temp)
        raise SolverTimeOutException
    # unsat
    if solve_with_uc:
        args.z3_uc = modelOrUc
    
    get_model_info("UNSAT2", get_model_start_time, constraints, minimize, maximize, caller, rlimit, before_rlimit_count, after_rlimit_count, global_path, thistx_path)
    raise UnsatError


# @stat_rlimit
@lru_cache(maxsize=2**23)
def get_model(
    constraints,
    minimize=(),
    maximize=(),
    enforce_execution_time=True,
    solver_timeout=None,
    want_uc = False
):
    """
    Returns a model based on given constraints as a tuple
    :param constraints: Tuple of constraints
    :param minimize: Tuple of minimization conditions
    :param maximize: Tuple of maximization conditions
    :param enforce_execution_time: Bool variable which enforces --execution-timeout's time
    :return:
    """

    # if args.use_ucc == "1":
    #     s = Solver()
    # else:
    s = Optimize()
    timeout = solver_timeout or args.solver_timeout

    # timeout or rlimit
    s.raw.set("rlimit", args.rlimit)
    # s.raw.set("timeout", timeout)

    # if args.use_ucc == "1":
    #     s.raw.set(unsat_core=True)

    for constraint in constraints:
        if type(constraint) == bool and not constraint:
            get_model_info("UNSAT1", get_model_start_time, constraints, minimize, maximize, caller, s, 0, 0, 0, global_path, thistx_path)
            raise UnsatError
    if type(constraints) != tuple:
        constraints = constraints.get_all_constraints()
    constraints = [constraint for constraint in constraints if type(constraint) != bool]

    # tmp_rlimit_count = s.raw.statistics().get_key_value("rlimit count")
    # print(tmp_rlimit_count)

    if want_uc:
        for i in range(len(constraints)):
            s.assert_and_track(constraints[i], path_index_str=str(i))
    else:
        for constraint in constraints:
            s.add(constraint)
        for e in minimize:
            s.minimize(e)
        for e in maximize:
            s.maximize(e)

    if args.solver_log:
        Path(args.solver_log).mkdir(parents=True, exist_ok=True)
        constraint_hash_input = tuple(
            list(constraints)
            + list(minimize)
            + list(maximize)
            + [len(constraints), len(minimize), len(maximize)]
        )
        with open(
            args.solver_log + f"/{abs(hash(constraint_hash_input))}.smt2", "w"
        ) as f:
            f.write(s.sexpr())

    modelOrUc = None
    before_rlimit_count = s.raw.statistics().get_key_value("rlimit count")
    result = s.check()
    if result == sat: #
        modelOrUc = s.model()
    elif result == unsat and want_uc:
        modelOrUc = s.raw.unsat_core()
        print("want_uc unsat_core", modelOrUc)

    after_rlimit_count = s.raw.statistics().get_key_value("rlimit count")

    return result, before_rlimit_count, after_rlimit_count, modelOrUc

