import subprocess
from devtools import echo


def run(compose, host, port):
    output = subprocess.run([
        "ssh", "-q", host, "-p", port,
        "composer-cli", "compose", "metadata", compose
    ], encoding="utf-8")

    if output.returncode != 0:
        echo("Error downloading metadata", "ERROR")
        return output.returncode

    tar = f"{compose}-metadata.tar"
    echo("Successfully downloaded metadata", "OK")
    return extract(tar, host, port)


def extract(tar, host, port):
    output = subprocess.run([
        "ssh", "-q", host, "-p", port,
        "tar", "-xvf", tar
    ], encoding="utf-8")

    if output.returncode != 0:
        echo("Error extracting tar", "ERROR")
        return output.returncode

    echo("Successfully extracted tar", "OK")
    return remove(tar, host, port)


def remove(tar, host, port):
    output = subprocess.run([
        "ssh", "-q", host, "-p", port,
        "rm", tar
    ], encoding="utf-8")

    if output.returncode != 0:
        echo("Error removing tar", "ERROR")
        return output.returncode

    echo("Successfully removed tar", "OK")
    return output.returncode


def metadata(args):
    r = run(args.compose, args.host, args.port)
    return r
