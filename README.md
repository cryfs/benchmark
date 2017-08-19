# benchmark
Benchmark tools for measuring the performance of CryFS

Run with

    $ python3 -m benchmark --dir [testdir] --runs [numRuns] --output-file [output-file]

The tool will then run the benchmark and in the end, it will output CSV lines.
These lines can be imported into the results.ods spreadsheet.

Hints for getting meaningful results:
- switch off swap
- don't overclock system
- run on not otherwise encrypted partition (no dmcrypt or similar)
- stop other processes (Dropbox, ...)
- make sure no CPU-heavy system processes are currently taking a lot of CPU (e.g. tracker-miner)
