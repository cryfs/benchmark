import os
import io
from distutils.util import strtobool


def setup():
    _checkSudo()
    _checkRandomizeVaSpace()


def _checkSudo():
    if os.geteuid() != 0:
        answer = _askYesNo("Script not started as root. This works, but might cause unstable results. Do you want to continue?")
        if not answer:
            exit(1)


def _checkRandomizeVaSpace():
    value = _readRandomizeVaSpace()
    if value != '0':
        if _askYesNo("/proc/sys/kernel/randomize_va_space is set to %s. Filebench prefers to run with it switched off to get more stable results. Do you want to switch it off?" % value):
            _disableRandomizeVaSpace()


def _readRandomizeVaSpace():
    with io.open('/proc/sys/kernel/randomize_va_space', 'r') as randomize_va_space:
        return randomize_va_space.read().strip()


def _disableRandomizeVaSpace():
    with io.open('/proc/sys/kernel/randomize_va_space', 'w') as randomize_va_space:
        randomize_va_space.write('0')


def _askYesNo(question):
    return strtobool(input(question + " [y/n]: ").lower())