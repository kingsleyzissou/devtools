import subprocess
from devtools import echo


def run(compose, host, port):
    prepare(host, port)
    output = subprocess.run([
        "ssh", "-q", host, "-p", port,
        "osbuild", "--store", "./store",
        "--output-directory", "./output",
        "--checkpoint", "build",
        "--export", "qcow2",
        f"{compose}.json"
    ], encoding="utf-8")

    if output.returncode != 0:
        # echo("Error inspecting compose", "ERROR")
        return output.returncode

    # print(output.stdout)
    return output.returncode


def prepare(host, port):
    subprocess.run([
        "ssh", "-q", host, "-p", port,
        "mkdir", "-p", "store", "output"
    ], encoding="utf-8")


def inspect(args):
    r = run(args.compose, args.host, args.port)
    return r
