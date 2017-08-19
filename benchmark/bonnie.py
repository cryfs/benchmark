import subprocess


class Bonnie(object):
    def __init__(self, dir, name):
        self.dir = dir
        self.name = name

    def run(self, numRuns, create_test_size=16, readwrite_test_size=None):
        options = ["bonnie++", "-d", self.dir, "-m", self.name, "-x", str(numRuns)]
        if create_test_size is not None:
            options = options + ["-n", "%d:10240:10240:10" % create_test_size]
        if readwrite_test_size is not None:
            options = options + ["-s", str(readwrite_test_size)]
        output = subprocess.check_output(options)
        return self._generate_csv_from_output(output, numRuns)

    def _generate_csv_from_output(self, output, expectedNumLines):
        lines = output.decode().strip().splitlines()
        assert(len(lines) == expectedNumLines)
        return "\n".join(lines)

    @classmethod
    def csv2html(self, csv):
        return subprocess.check_output(["bon_csv2html"], input=csv.encode(encoding="UTF-8")).decode(encoding="UTF-8")
