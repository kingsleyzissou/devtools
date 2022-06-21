import subprocess
from tools import echo

def run(compose, host, port):
    output = subprocess.run([
      "ssh", "-q", host, "-p", port,
      "composer-cli", "compose", "delete", compose
    ], encoding="utf-8")

    if output.returncode == 0:
        echo("Compose deleted", "OK")
        return output.returncode

    echo(output.stdout, "ERROR")
    return output.returncode

def delete(args):
    return run(args.compose, args.host, args.port)
