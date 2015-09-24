from subprocess import Popen, PIPE, STDOUT
from sys import stdout


class Filebench(object):
    def __init__(self, dir):
        self.dir = dir

    def run(self, workload, duration):
        process = Popen(['filebench'], stdout=stdout, stdin=PIPE, stderr=STDOUT)
        settings = "load %s\nset $dir=\"%s\"\nrun %d\n" % (workload, self.dir, duration)
        process.communicate(input=settings.encode())
