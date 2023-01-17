import json
import subprocess
from devtools import echo


def run(compose, host, port, finished=False, failed=False):
    if finished:
        composes = status(host, port, finished, False)
        return delete_multi(host, port, composes)

    if failed:
        composes = status(host, port, False, failed)
        return delete_multi(host, port, composes)

    output = subprocess.run([
        "ssh", "-q", host, "-p", port,
        "composer-cli", "compose", "delete", compose
    ], encoding="utf-8")

    if output.returncode == 0:
        echo(f"Compose {compose} deleted", "OK")
        return output.returncode

    echo(output.stdout, "ERROR")
    return output.returncode


def status(host, port, finished, failed):
    if finished:
        output = subprocess.run([
            f"ssh -q {host} -p {port} composer-cli compose status --json | jq '.[] | select(.path == \"/compose/finished\") | .body.finished[].id'"
        ], encoding="utf-8", stdout=subprocess.PIPE, shell=True)

    if failed:
        output = subprocess.run([
            f"ssh -q {host} -p {port} composer-cli compose status --json | jq '.[] | select(.path == \"/compose/failed\") | .body.failed[].id'"
        ], encoding="utf-8", stdout=subprocess.PIPE, shell=True)

    if output.returncode == 0:
        composes = list(filter(None, output.stdout.split("\n")))
        return composes

    echo(output.stdout, "ERROR")
    return output.returncode


def delete_multi(host, port, composes):
    if len(composes) == 0:
        echo("No composes to delete")
        return len(composes)

    for c in composes:
        r = run(c, host, port)

    if r != 0:
        echo("Error deleting composes", "ERROR")
        return r

    return r


def delete(args):
    return run(args.compose, args.host, args.port, args.finished, args.failed)
