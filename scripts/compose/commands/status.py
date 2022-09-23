import subprocess
from tools import echo


def run(host, port, json):
    args = [
        "ssh", "-q", host, "-p", port,
        "composer-cli", "compose", "status"
    ]

    if json:
        args.append("--json")

    output = subprocess.run(args, encoding="utf-8")

    if output.returncode == 0:
        # echo("Compose cancelled", "OK")
        return output.returncode

    echo(output.stdout, "ERROR")
    return output.returncode


def status(args):
    return run(args.host, args.port, args.json)
