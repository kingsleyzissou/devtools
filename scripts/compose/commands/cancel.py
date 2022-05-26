import subprocess
from tools import echo

from .delete import delete

def run(compose, host, port):
    output = subprocess.run([
      "ssh", "-q", host, "-p", port,
      "composer-cli", "compose", "cancel", compose
    ], encoding="utf-8")

    if output.returncode == 0:
        echo("Compose cancelled", "OK")
        return output.returncode

    echo(output.stdout, "DANGER")
    return output.returncode

def cancel(args):
    r =  run(args.compose, args.host, args.port)
    if r == 0:
        return delete(args)
    return 1
