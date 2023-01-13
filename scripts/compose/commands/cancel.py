import subprocess
from devtools import echo

from .delete import delete


def run(compose, host, port):
    output = subprocess.run([
        "ssh", "-q", host, "-p", port,
        "composer-cli", "compose", "cancel", compose
    ], encoding="utf-8")

    if output.returncode == 0:
        echo("Compose cancelled", "OK")
        return output.returncode

    echo(output.stdout, "ERROR")
    return output.returncode


def cancel(args):
    r = run(args.compose, args.host, args.port)
    return r
