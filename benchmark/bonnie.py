import subprocess


class Bonnie(object):
    def __init__(self, dir, name):
        self.dir = dir
        self.name = name

    def run(self, numRuns):
        output = subprocess.check_output(
            #["bonnie++", "-d", self.dir, "-m", self.name, "-x", str(numRuns), "-r", "128", "-s", "256"])
            ["bonnie++", "-d", self.dir, "-m", self.name, "-x", str(numRuns)])
        return self._generate_csv_from_output(output)

    def _generate_csv_from_output(self, output):
        header_line = ("name,file_size,putc,putc_cpu,put_block,put_block_cpu,rewrite,rewrite_cpu,getc,getc_cpu,"
                       "get_block,get_block_cpu,seeks,seeks_cpu,num_files,seq_create,seq_create_cpu,seq_stat,"
                       "seq_stat_cpu,seq_del,seq_del_cpu,ran_create,ran_create_cpu,ran_stat,ran_stat_cpu,ran_del,"
                       "ran_del_cpu")
        lines = output.decode().strip().splitlines()
        if len(lines) == 1:
            return [header_line] + lines
        else:
            assert (lines[0] == header_line)
            return lines
