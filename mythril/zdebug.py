import z3
import sys

def stat_rlimit(func):
    def function_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
        f = sys._getframe()
        f_back_name = f.f_back.f_code.co_name
        f_back_file = f.f_back.f_code.co_filename
        s = z3.Optimize()
        r1 = s.statistics().get_key_value("rlimit count")
        result = func(*args, **kwargs)
        r2 = s.statistics().get_key_value("rlimit count")
        print(f_back_file+":"+f_back_name, r1, r2)
        tmpf = f.f_back
        for i in range(3):
            tmpf = tmpf.f_back
            tmpf_name = tmpf.f_code.co_name
            tmpf_file = tmpf.f_code.co_filename
            print(tmpf_file+":"+tmpf_name)
        return result

    return function_wrapper
