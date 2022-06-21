import subprocess
from tools import echo

def run(host, port):
    output = subprocess.run([
      "ssh", "-q", host, "-p", port,
      "composer-cli", "compose", "status"
    ], encoding="utf-8")

    if output.returncode == 0:
        # echo("Compose cancelled", "OK")
        return output.returncode

    echo(output.stdout, "ERROR")
    return output.returncode

def status(args):
    return run(args.host, args.port)
