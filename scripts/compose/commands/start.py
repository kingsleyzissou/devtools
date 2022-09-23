import json
import subprocess
from tools import echo


def run(blueprint, image_type, host, port):
    output = subprocess.run([
        "ssh", "-q", host, "-p", port,
        "composer-cli", "compose", "--json",
        "start", blueprint, image_type
    ], capture_output=True, encoding="utf-8")

    if output.returncode == 0:
        c = json.loads(output.stdout)
        print(c["body"]["build_id"])
        return output.returncode

    err = json.loads(output.stdout)
    echo(err["body"]["errors"][0]["msg"], "ERROR")
    return output.returncode


def start(args):
    return run(args.blueprint, args.image_type, args.host, args.port)
