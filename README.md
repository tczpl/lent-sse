# LENT-SSE: Leveraging Executed and Near Transactions for Speculative Symbolic Execution of Smart Contracts

We choose Mythril to implement the modules and algorithms (ETSA and NTRA) of LENT-SSE. We mainly modify the modules of symbolic EVM (sym.py), SMT solver (model.py), etc.

**We also upload a copy in HotCRP as supplementary material.**

## Requirements

Python3, Z3, etc. As the same as [https://github.com/ConsenSys/mythril](https://github.com/ConsenSys/mythril).

```bash
$ pip3 install -r requirements.txt
```

## Run

```bash
$ python3 benchmark.py # or checkout the benchmark_usage.sh, then set the "dataset rlimit strategy txcount"
$ ls results/ # finding the results
```

## Resutls
The results of the SmartBugs dataset in the paper are in `results_paper/` rather than `results/`.

As for results of the the Top1K dataset, they are too large to be uploaded in the repository, but they can be reproduced by running `python3 benchmark.py top1k 500000 dfs 2`.


