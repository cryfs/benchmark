import argparse
from benchmark.bonnie import Bonnie
from benchmark.filesystems import PlainFs, EncFs, TrueCrypt, VeraCrypt, CryFs


def main():
    parser = argparse.ArgumentParser(description="Run filesystem benchmarks comparing cryfs to other file systems")
    parser.add_argument('--dir', required=True, help="Directory where the benchmark is run.")
    parser.add_argument('--runs', type=int, default=1, help="Number of runs.")
    args = parser.parse_args()
    run_benchmark(args.dir, args.runs)


def run_benchmark(dir, numRuns):
    # Setup only needed for filebench
    #setup.setup()

    truecrypt = ""
    with TrueCrypt(dir) as fs:
      truecrypt = truecrypt + Bonnie(name="TrueCrypt", dir=fs.mount_dir).run(numRuns)
    print("TrueCrypt Output: %s" % truecrypt)

    cryfs = ""
    with CryFs(dir) as fs:
      cryfs = cryfs + Bonnie(name="CryFS", dir=fs.mount_dir).run(numRuns)
    print("CryFS Output: %s" % cryfs)

    plain=""
    with PlainFs(dir) as fs:
        plain = Bonnie(name="plain", dir=fs.mount_dir).run(numRuns)
    print("Plain Output: %s" % plain)

    encfs = ""
    with EncFs(dir) as fs:
        encfs = Bonnie(name="EncFS", dir=fs.mount_dir).run(numRuns)
    print("EncFS Output: %s" % encfs)

    veracrypt=""
    with VeraCrypt(dir) as fs:
        veracrypt = Bonnie(name="VeraCrypt", dir=fs.mount_dir).run(numRuns)
    print("VeraCrypt Output: %s" % veracrypt)

    output = "\n".join([plain, encfs, truecrypt, veracrypt, cryfs])
    print("Output:\n")
    print(output)
