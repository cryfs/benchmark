import argparse
from benchmark.bonnie import Bonnie
from benchmark.filesystems import PlainFs, EncFs, TrueCrypt, VeraCrypt, CryFs


def main():
    parser = argparse.ArgumentParser(description="Run filesystem benchmarks comparing cryfs to other file systems")
    parser.add_argument('--dir', required=True, help="Directory where the benchmark is run.")
    parser.add_argument('--runs', type=int, default=1, help="Number of runs.")
    parser.add_argument('--output-file', help="Name of a html file where the benchmark results should be stored")
    args = parser.parse_args()
    run_benchmark(args.dir, args.runs, args.output_file)


def run_benchmark(dir, numRuns, outputFile):
    # Setup only needed for filebench
    #setup.setup()

    truecrypt = ""
    cryfs = ""
    plain = ""
    encfs = ""
    veracrypt = ""

    for numRun in range(numRuns):
        with TrueCrypt(dir) as fs:
            output = Bonnie(name="TrueCrypt (%d)" % numRun, dir=fs.mount_dir).run(1)
            print("TrueCrypt Output: %s" % output)
            truecrypt += output + "\n"

        with CryFs(dir) as fs:
            output = Bonnie(name="CryFS (%d)" % numRun, dir=fs.mount_dir).run(1)
            print("CryFS Output: %s" % output)
            cryfs += output + "\n"

        with PlainFs(dir) as fs:
            output = Bonnie(name="plain (%d)" % numRun, dir=fs.mount_dir).run(1)
            print("Plain Output: %s" % output)
            plain += output + "\n"

        with EncFs(dir) as fs:
            output = Bonnie(name="EncFS (%d)" % numRun, dir=fs.mount_dir).run(1)
            print("EncFS Output: %s" % output)
            encfs += output + "\n"

        with VeraCrypt(dir) as fs:
            output = Bonnie(name="VeraCrypt (%d)" % numRun, dir=fs.mount_dir).run(1)
            print("VeraCrypt Output: %s" % output)
            veracrypt += output + "\n"

    output = cryfs + encfs + truecrypt + veracrypt + plain
    print("Output:\n")
    print(output)

    if outputFile is not None:
        with open(outputFile, 'w') as output_file:
            output_file.write(output)
        html = Bonnie.csv2html(output)
        with open("%s.html" % outputFile, 'w') as output_file:
            output_file.write(html)
        print("Output stored to %s and %s.html" % (outputFile, outputFile))
