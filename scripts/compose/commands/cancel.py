import subprocess
from devtools import echo


def run(compose, host, port):
    output = subprocess.run([
        "ssh", "-q", host, "-p", port,
        "composer-cli", "compose", "cancel", compose
    ], encoding="utf-8")

    if output.returncode == 0:
        echo("Compose cancelled", "OK")
        subprocess.run([
            "compose", "delete",
            "--compose", compose,
        ], encoding="utf-8")
        return output.returncode

    echo(output.stdout, "ERROR")
    return output.returncode


def cancel(args):
    r = run(args.compose, args.host, args.port)
    return r
