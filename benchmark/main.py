import argparse
from benchmark.bonnie import Bonnie
from benchmark.filesystems import PlainFs, EncFs


def main():
    parser = argparse.ArgumentParser(description="Run filesystem benchmarks comparing cryfs to other file systems")
    parser.add_argument('--dir', required=True)
    parser.add_argument('--runs', type=int, default=1)
    args = parser.parse_args()
    run_benchmark(args.dir)


def run_benchmark(dir):
    # Setup only needed for filebench
    #setup.setup()

    with PlainFs(dir) as fs:
        plain = Bonnie(name="plain", dir=fs.mount_dir).run(2)

    with EncFs(dir) as fs:
        encfs = Bonnie(name="EncFS", dir=fs.mount_dir).run(2)

    print("Output plain:\n%s\n\nOutput EncFs:\n%s\n" % (plain, encfs))
