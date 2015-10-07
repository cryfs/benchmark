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

    with TrueCrypt(dir) as fs:
        truecrypt = Bonnie(name="TrueCrypt", dir=fs.mount_dir).run(numRuns, create_test_size=16)
    print("TrueCrypt Output: %s" % truecrypt)
    with TrueCrypt(dir) as fs:
        truecrypt_1m = Bonnie(name="TrueCrypt-1M", dir=fs.mount_dir).run(numRuns, create_test_size=16, readwrite_test_size="32g:1024k")
    print("TrueCrypt-1M Output: %s" % truecrypt_1m)

    with VeraCrypt(dir) as fs:
        veracrypt = Bonnie(name="VeraCrypt", dir=fs.mount_dir).run(numRuns, create_test_size=16)
    print("VeraCrypt Output: %s" % veracrypt)
    with VeraCrypt(dir) as fs:
        veracrypt_1m = Bonnie(name="VeraCrypt-!M", dir=fs.mount_dir).run(numRuns, create_test_size=16, readwrite_test_size="32g:1024k")
    print("VeraCrypt-1M Output: %s" % veracrypt_1m)

    with PlainFs(dir) as fs:
        plain = Bonnie(name="plain", dir=fs.mount_dir).run(numRuns, create_test_size=64)
    print("Plain Output: %s" % plain)
    with PlainFs(dir) as fs:
        plain_1m = Bonnie(name="plain-1M", dir=fs.mount_dir).run(numRuns, create_test_size=64, readwrite_test_size="32g:1024k")
    print("Plain-1M Output: %s" % plain_1m)

    with EncFs(dir) as fs:
        encfs = Bonnie(name="EncFS", dir=fs.mount_dir).run(numRuns, create_test_size=16)
    print("EncFS Output: %s" % encfs)
    with EncFs(dir) as fs:
        encfs_1m = Bonnie(name="EncFS-1M", dir=fs.mount_dir).run(numRuns, create_test_size=16, readwrite_test_size="32g:1024k")
    print("EncFS-1M Output: %s" % encfs_1m)

    with CryFs(dir) as fs:
        cryfs = Bonnie(name="CryFS", dir=fs.mount_dir).run(numRuns, create_test_size=16)
    print("CryFS Output: %s" % cryfs)
    with CryFs(dir) as fs:
        cryfs_1m = Bonnie(name="CryFS-1M", dir=fs.mount_dir).run(numRuns, create_test_size=16, readwrite_test_size="32g:1024k")
    print("CryFS-1M Output: %s" % cryfs_1m)

    output = "\n".join([plain, plain_1m, encfs, encfs_1m, truecrypt, truecrypt_1m, veracrypt, veracrypt_1m, cryfs, cryfs_1m])
    print("Output:\n")
    print(output)
