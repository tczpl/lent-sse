import json
import glob
import os
import sys
import time
import multiprocessing
import csv
import signal

dataset = "smartbugs"
if len(sys.argv) > 1:
    dataset = sys.argv[1]

rlimit = 5000000
if len(sys.argv) > 2:
    rlimit = int(sys.argv[2]) # 100000000

strategy = "dfs"
if len(sys.argv) > 3:
    strategy = sys.argv[3]

tx_count = 2
if len(sys.argv) > 4:
    tx_count = int(sys.argv[4]) # 

cpu_count = int(multiprocessing.cpu_count()/2)
if len(sys.argv) > 5:
    cpu_count = int(sys.argv[5])


print(f'running benchmark with {dataset}-dataset, {rlimit}-rlimit, {strategy}-strategy, {tx_count}-tx')

benchmark_process_lock = multiprocessing.Semaphore(cpu_count)

base_dir = './results/result_'+dataset+'-cpu'+str(cpu_count)+'-tx'+str(tx_count)+'-strategy'+strategy+'/'
try:
    os.mkdir(base_dir)
except:
    pass

# lent:  ETSA
# lent9: ETSA+NTRA
# ji:    used for providing fair comparison between origin and lent
run_types = ["origin", "lent9", "ji", "ji"]

for run_type in run_types:
    result_dir = base_dir+run_type+'-rlimit'+str(rlimit)+"/"
    json_dir=result_dir+"json/"
    log_dir = result_dir+"log/"

    silence = " >/dev/null 2>&1"
    # silence = ""
    try:
        os.mkdir(result_dir)
    except:
        pass
    try:
        os.mkdir(json_dir)
    except:
        pass
    try:
        os.mkdir(log_dir)
    except:
        pass

def run_smartbugs(index, file_path, contract_name, run_type):
    ret = os.fork()
    if ret != 0:
        return ret
    else:
        benchmark_process_lock.acquire()

    start_time = time.time()

    result_dir = base_dir+run_type+'-rlimit'+str(rlimit)+"/"
    json_dir=result_dir+"json/"
    log_dir = result_dir+"log/"
    contract_cmd = ':'+contract_name if contract_name!="" else ""
    res_file = json_dir+str(index)+".json"
    silence=">" +log_dir+str(index)+".txt"

    # if os.path.exists(res_file):
    #     benchmark_process_lock.release()
    #     print(run_type, index, file_path, "exists")
    #     exit()

    use_lent = "0" 
    # if run_type == "lent":
    if "lent" in run_type:
        use_lent = "1"

    if run_type=="lent":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent2":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent2={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent3":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent3={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent4":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent4={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent5":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent5={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent6":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent5={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent7":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent7={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent8":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent8={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent9":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent9={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="origin":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="ji":
        cmd = f"./myth a {file_path}{contract_cmd} --solv=0.4.25 --strategy={strategy} --output-json={res_file}  --use-lent={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)

    end_time = time.time()
    used_time = end_time-start_time
    
    if run_type != "ji":
        print(run_type, index, file_path, used_time)

    benchmark_process_lock.release()
    exit()



def run_top1k(index, file_path, run_type):

    ret = os.fork()
    if ret != 0:
        return ret
    else:
        benchmark_process_lock.acquire()

    start_time = time.time()

    result_dir = base_dir+run_type+'-rlimit'+str(rlimit)+"/"
    json_dir=result_dir+"json/"
    log_dir = result_dir+"log/"
    bytecode = json.loads(open(file_path).read())["creationCode"]
    contract_cmd = '--code ' + bytecode
    silence=">" +log_dir+str(index)+".txt"
    res_file = json_dir+str(index)+".json"

    use_lent = "0" 
    # if run_type == "lent":
    if "lent" in run_type:
        use_lent = "1"

    if run_type=="lent":
        cmd = f"./myth4g a {contract_cmd} --strategy={strategy} --output-json={res_file}  --use-lent={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="lent9":
        cmd = f"./myth4g a {contract_cmd} --strategy={strategy} --output-json={res_file}  --use-lent9={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="origin":
        cmd = f"./myth4g a {contract_cmd} --strategy={strategy} --output-json={res_file}  --use-lent={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)
    elif run_type=="ji":
        cmd = f"./myth4g a {contract_cmd} --strategy={strategy} --output-json={res_file}  --use-lent={use_lent} --rlimit={rlimit} --transaction-count={tx_count}" +silence
        print(cmd)
        os.system(cmd)

    end_time = time.time()
    used_time = end_time-start_time
    
    if run_type != "ji":
        print(run_type, index, file_path, used_time)

    benchmark_process_lock.release()
    exit()



runtype_of_pid = {}
pidcnt_of_runtype = {}

for run_type in run_types:
    pidcnt_of_runtype[run_type] = 0

for run_type in run_types:
    if dataset == "smartbugs":
        with open("list_"+dataset+".csv") as f:
            for row in csv.reader(f, skipinitialspace=True):
                indexName=row[0]
                actualName=row[1]
                arr = actualName.strip().split(":")
                file_path = arr[0]
                contract_name = arr[1]


                # Out of memory
                if indexName in ["file39", "file92", "file112", "file115"]:
                    continue
                if tx_count >=3:
                    if indexName == "file33":
                        continue

                pid = run_smartbugs(indexName, file_path, contract_name, run_type)

                runtype_of_pid[pid] = run_type
                # print("pid", pid, "run_type", run_type)
                pidcnt_of_runtype[run_type] += 1
    

    if dataset == "top1k":
        lines  = open("list_top1k.txt").readlines()
        pid_cnt = 0
        for index in range(len(lines)):
            arr  = lines[index].strip().split(",")
            address = arr[0]
            file_path = "top1000/"+address+".json"

            # out of memory
            if run_type in ["origin", "lent9", "lent"] and index in [431, 685]:
                continue

            pid = run_top1k(index, file_path, run_type)
            print("top1k pending", pid)

            runtype_of_pid[pid] = run_type
            # print("pid", pid, "run_type", run_type)
            pidcnt_of_runtype[run_type] += 1

while True:
    pid, status = os.wait()

    run_type = runtype_of_pid[pid]
    del runtype_of_pid[pid]
    pidcnt_of_runtype[run_type] -=1

    isFinished = True
    for run_type in run_types:
        if run_type != "ji":
            if pidcnt_of_runtype[run_type] >0:
                isFinished = False
    print(pidcnt_of_runtype)
    if isFinished:
        print("finish")
        break

os.system("pkill python3")
print("all finish")