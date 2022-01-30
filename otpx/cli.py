import sys
import argparse

from os.path import join
from pathlib import Path

from otpx.app import Otpx
from otpx.exceptions import otpxException

home = str(Path.home())
keyspath = join(home, ".otpx", "keys")

parser = argparse.ArgumentParser()
parser.add_argument("command", nargs="?", default="showall")
parser.add_argument("--keys", default=keyspath)


def main():
    args, unknownargs = parser.parse_known_args()
    command = args.command
    if command.startswith("_"):
        print("Invalid command")
        sys.exit(1)

    app = Otpx(parser, args)
    try:
        getattr(app, command)(*unknownargs)
    except otpxException as e:
        print(e)
        sys.exit(1)
