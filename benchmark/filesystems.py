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


class VeraCrypt(object):
    _SIZE = 35 * 1024 * 1024 * 1024  # 35GB

    def __init__(self, dir):
        self.root_dir = dir
        random_id = random_string(5)
        self.key_file = os.path.join(self.root_dir, "veracrypt-keyfile-%s" % random_id)
        self.volume_file = os.path.join(self.root_dir, "veracrypt-volume-%s" % random_id)
        self.mount_dir = os.path.join(self.root_dir, "veracrypt-mount-%s" % random_id)
        self.password = random_string(20)

    def __enter__(self):
        os.mkdir(self.mount_dir)
        self._createVolume()
        self._mountVolume()
        print("VeraCrypt started. Waiting 10sec to give it some bootup time.")
        time.sleep(10)
        return self

    def __exit__(self, type, value, tb):
        self._unmountVolume()
        os.unlink(self.key_file)
        os.unlink(self.volume_file)
        os.rmdir(self.mount_dir)

    def _createVolume(self):
        # Create key file
        subprocess.check_call(["veracrypt", "--create-keyfile", "--random-source=/dev/urandom", self.key_file])
        # Create volume
        subprocess.check_call(["veracrypt", "-c", "--volume-type=normal", "--random-source=/dev/urandom",
                               "--size=%d" % self._SIZE, "--encryption=AES", "--hash=SHA-512", "--filesystem=FAT",
                               "--password", self.password, "--pim=1", "--keyfiles=%s" % self.key_file,
                               self.volume_file])

    def _mountVolume(self):
        subprocess.check_call(["veracrypt", "--password", self.password, "--pim=1", "--keyfiles=%s" % self.key_file,
                       "--protect-hidden=no", self.volume_file, self.mount_dir])

    def _unmountVolume(self):
        subprocess.check_call(["veracrypt", "-d", self.volume_file])


class TrueCrypt(object):
    _SIZE = 35 * 1024 * 1024 * 1024  # 35GB

    def __init__(self, dir):
        self.root_dir = dir
        random_id = random_string(5)
        self.key_file = os.path.join(self.root_dir, "truecrypt-keyfile-%s" % random_id)
        self.volume_file = os.path.join(self.root_dir, "truecrypt-volume-%s" % random_id)
        self.mount_dir = os.path.join(self.root_dir, "truecrypt-mount-%s" % random_id)
        self.password = random_string(20)

    def __enter__(self):
        os.mkdir(self.mount_dir)
        self._createVolume()
        self._mountVolume()
        print("TrueCrypt started. Waiting 10sec to give it some bootup time.")
        time.sleep(10)
        return self

    def __exit__(self, type, value, tb):
        self._unmountVolume()
        os.unlink(self.key_file)
        os.unlink(self.volume_file)
        os.rmdir(self.mount_dir)

    def _createVolume(self):
        # Create key file
        subprocess.check_call(["truecrypt", "--create-keyfile", "--random-source=/dev/urandom", self.key_file])
        # Create volume
        subprocess.check_call(["truecrypt", "-c", "--random-source=/dev/urandom", "--volume-type=normal",
                               "--size=%d" % self._SIZE, "--encryption=AES", "--hash=SHA-512", "--filesystem=FAT",
                               "--password=%s" % self.password, "--keyfiles=%s" % self.key_file,
                               self.volume_file])

    def _mountVolume(self):
        subprocess.check_call(["truecrypt", "--password=%s" % self.password, "--keyfiles=%s" % self.key_file,
                       "--protect-hidden=no", self.volume_file, self.mount_dir])

    def _unmountVolume(self):
        subprocess.check_call(["truecrypt", "-d", self.volume_file])
