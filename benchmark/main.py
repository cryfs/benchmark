import argparse
from benchmark.bonnie import Bonnie
from benchmark.filesystems import PlainFs, EncFs, CryFs


def main():
    parser = argparse.ArgumentParser(description="Run filesystem benchmarks comparing cryfs to other file systems")
    parser.add_argument('--dir', required=True, help="Directory where the benchmark is run.")
    parser.add_argument('--runs', type=int, default=1, help="Number of runs.")
    args = parser.parse_args()
    run_benchmark(args.dir, args.runs)


def run_benchmark(dir, numRuns):
    # Setup only needed for filebench
    #setup.setup()

    with CryFs(dir) as fs:
        cryfs = Bonnie(name="CryFS", dir=fs.mount_dir).run(numRuns)

    with PlainFs(dir) as fs:
        plain = Bonnie(name="plain", dir=fs.mount_dir).run(numRuns)

    with EncFs(dir) as fs:
        encfs = Bonnie(name="EncFS", dir=fs.mount_dir).run(numRuns)

    output = "\n".join([plain, encfs, cryfs])
    print("Output:\n")
    print(output)
