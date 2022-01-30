import threading
import signal
import pyperclip
import pyotp
import time

from os import makedirs
from os.path import dirname

from otpx.screen import CliScreen
from otpx.helpers import validate_totp_secret
from otpx.exceptions import otpxKeyIgnored, otpxError

exitevent = threading.Event()


class Secret:
    def __init__(self, confline):
        if ":" not in confline:
            raise otpxKeyIgnored

        k, v = confline.split(":")
        k, v = k.strip(), v.strip()

        values = v.split()
        if len(values) > 1:
            # HOTP
            self.secret = values[0]
            self.algo = pyotp.HOTP(values[0])
            self.algoname = "hotp"
            self.counter = int(values[1])

        else:
            # TOTP
            if not validate_totp_secret(v):
                print("ERROR: Invalid secret `%s`" % k)
                raise otpxKeyIgnored

            self.secret = v
            self.algo = pyotp.TOTP(v)
            self.algoname = "totp"
            self.counter = None

        self.name = k
        self.key = k.lower()

    @property
    def remains(self):
        if self.algoname != "totp":
            return -1

        return self.algo.interval - time.time() % self.algo.interval

    @property
    def code(self):
        if self.algoname == "hotp":
            return self.algo.at(self.counter)

        return self.algo.now()

    def __str__(self):
        if self.algoname == "hotp":
            return "%s: %s %s\n" % (self.name, self.secret, self.counter)

        return "%s: %s\n" % (self.name, self.secret)


class Otpx:
    def __init__(self, parser, args):
        self.keyspath = args.keys
        self.cargs = args
        self.outgap = 0.5
        self.out = CliScreen()
        self.keys = dict()

        makedirs(dirname(self.keyspath), exist_ok=True)
        with open(self.keyspath, "a+") as f:
            f.seek(0)
            for line in f.readlines():
                try:
                    secret = Secret(line)
                    self.keys[secret.key] = secret
                except otpxKeyIgnored:
                    continue

    def _kill_signal_handler(self, signal_number, *args, **kwargs):
        self.out.end()
        exitevent.set()

    def showall(self):
        if not self.keys:
            raise otpxError("No keys")

        signal.signal(signal.SIGINT, self._kill_signal_handler)
        signal.signal(signal.SIGTERM, self._kill_signal_handler)
        out = self.out
        out.start()
        maxcolwidth = max(map(len, self.keys.keys()))
        colwidths = (maxcolwidth + 2, 10, 10)

        def presenter():
            while not exitevent.is_set():
                out.refresh()
                out.addrow(("name", "code", "remains"), colwidths=colwidths)
                for k, v in self.keys.items():
                    out.addrow(
                        (k, v.code, int(v.remains)), colwidths=colwidths
                    )

                exitevent.wait(self.outgap)

        for w in (self.worker1, self.worker2, self.worker3):
            t = threading.Thread(target=presenter, daemon=True)
            t.start()

        signal.pause()

    def _find_item(self, k):
        v = self.keys.get(k.lower())
        if not v:
            raise otpxError("Key not found `%s`" % k)
        return v

    def _update_keys(self):
        with open(self.keyspath, "w+") as f:
            for k, v in self.keys.items():
                f.write(str(v))

    def show(self, k):
        print(k, self._find_item(k).code)

    def copy(self, k):
        code = self._find_item(k).code
        pyperclip.copy(code)
        print(k, code, "Copied!")

    def inc(self, k):
        item = self._find_item(k)
        if item.algoname != "hotp":
            print("Its not HOTP key `%s`" % k)
            return

        item.counter += 1
        self._update_keys()
        print(k, item.code)

    def version(self):
        import otpx

        print("otpx", otpx.__version__)

    def __getattr__(self, k):
        return lambda: self.show(k)
