import sys
import os
import shutil
import time
import subprocess
import signal
from benchmark.utils import random_string


class PlainFs(object):
    def __init__(self, dir):
        self.root_dir = dir
        random_id = random_string(5)
        self.mount_dir = os.path.join(self.root_dir, "plain-%s" % random_id)

    def __enter__(self):
        os.mkdir(self.mount_dir)
        return self

    def __exit__(self, type, value, tb):
        shutil.rmtree(self.mount_dir)


class EncFs(object):
    # Select paranoia mode
    _ENCFS_INPUT = "p\n".encode()

    def __init__(self, dir):
        self.root_dir = dir
        random_id = random_string(5)
        self.base_dir = os.path.join(self.root_dir, "encfs-base-%s" % random_id)
        self.mount_dir = os.path.join(self.root_dir, "encfs-mount-%s" % random_id)

    def __enter__(self):
        os.mkdir(self.base_dir)
        os.mkdir(self.mount_dir)
        self.process = subprocess.Popen(
            ["encfs", "-f", "--extpass=echo mycoolpassword", self.base_dir, self.mount_dir],
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=sys.stderr)
        self.process.stdin.write(self._ENCFS_INPUT)
        self.process.stdin.close()
        print("EncFS started. Waiting 10sec to give it some bootup time.")
        time.sleep(10)
        return self

    def __exit__(self, type, value, tb):
        self.process.send_signal(signal.SIGINT)
        self.process.wait()
        os.rmdir(self.mount_dir)
        shutil.rmtree(self.base_dir)


class CryFs(object):
    # Choose aes256-gcm
    _CRYFS_INPUT = "1\r\n".encode()

    def __init__(self, dir):
        self.root_dir = dir
        random_id = random_string(5)
        self.config_file = os.path.join(self.root_dir, "cryfs-config-%s.json" % random_id)
        self.base_dir = os.path.join(self.root_dir, "cryfs-base-%s" % random_id)
        self.mount_dir = os.path.join(self.root_dir, "cryfs-mount-%s" % random_id)

    def __enter__(self):
        os.mkdir(self.base_dir)
        os.mkdir(self.mount_dir)
        self.process = subprocess.Popen(
            ["./cryfs", "--config", self.config_file, self.base_dir, self.mount_dir, "--", "-f"],
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=sys.stderr)
        self.process.stdin.write(self._CRYFS_INPUT)
        self.process.stdin.close()
        print("CryFS started. Waiting 10sec to give it some bootup time.")
        time.sleep(10)
        return self

    def __exit__(self, type, value, tb):
        self.process.send_signal(signal.SIGINT)
        self.process.wait()
        os.unlink(self.config_file)
        os.rmdir(self.mount_dir)
        shutil.rmtree(self.base_dir)
