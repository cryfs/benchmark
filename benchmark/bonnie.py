import subprocess


class Bonnie(object):
    def __init__(self, dir, name):
        self.dir = dir
        self.name = name

    def run(self, numRuns):
        output = subprocess.check_output(
            ["bonnie++", "-d", self.dir, "-m", self.name, "-x", str(numRuns), "-r", "128", "-s", "256", "-n", "256"])
            #["bonnie++", "-d", self.dir, "-m", self.name, "-x", str(numRuns), "-n", "256"])
        return self._generate_csv_from_output(output, numRuns)

    def header_line(self):
        return ("name,file_size,putc,putc_cpu,put_block,put_block_cpu,rewrite,rewrite_cpu,getc,getc_cpu,get_block,"
                "get_block_cpu,seeks,seeks_cpu,num_files,seq_create,seq_create_cpu,seq_stat,seq_stat_cpu,seq_del,"
                "seq_del_cpu,ran_create,ran_create_cpu,ran_stat,ran_stat_cpu,ran_del,ran_del_cpu")

    def _generate_csv_from_output(self, output, expectedNumLines):
        lines = output.decode().strip().splitlines()
        if lines[0] == self.header_line():
            lines = lines[1:]
        expected_num_column_separators = self.header_line().count(",")
        assert(all([line.count(",") == expected_num_column_separators for line in lines]))
        assert(len(lines) == expectedNumLines)
        return "\n".join(lines)
