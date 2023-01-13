import subprocess
from devtools import echo


def get_results(compose):
    echo("Fetching results...")
    r = subprocess.run(["ssh", "-q", "localvm", "composer-cli",
                       "compose", "results", compose], capture_output=True)
    return r. returncode


def dl_tar(compose, code):
    if code != 0:
        return code
    echo("Downloading image...")
    r = subprocess.run(
        ["scp", "-q", f"localvm:{compose}.tar", "./images/."], capture_output=True)
    return r.returncode


def rm_tar(compose, code, remote=False):
    if code != 0:
        return code
    if remote:
        echo("Removing remote tar...")
        r = subprocess.run(["ssh", "-q", "localvm", "rm",
                           f"{compose}.tar"], capture_output=True)
        return r.returncode
    echo("Removing tar...")
    r = subprocess.run(["rm", f"images/{compose}.tar"], capture_output=True)
    return r.returncode


def unzip(compose, code):
    if code != 0:
        return code
    echo("Unzipping tar...")
    r = subprocess.run(
        ["tar", "-xvf", f"{compose}.tar", ""], cwd="images", capture_output=True)
    return r.returncode


def mv_manifest(compose, keep, code):
    if code != 0:
        return code
    if keep:
        echo("Moving manifest...")
        r = subprocess.run(
            ["mv", f"images/{compose}.json", "manifests/."], capture_output=True)
        return r.returncode
    echo("Removing manifest...")
    r = subprocess.run(["rm", f"images/{compose}.json"], capture_output=True)
    return r.returncode


def mv(compose, name, code):
    if code != 0:
        return code
    echo("Renaming file...")
    r = subprocess.run(["mv", f"images/{compose}-disk.qcow2",
                        f"images/{name}.qcow2"], capture_output=True)
    return r.returncode


def overlay(compose, name, fmt, code):
    if code != 0:
        return code
    echo("Creating overlay")
    # image_dir = os.path.join(os.getcwd(), "images")
    # overlay_dir = os.path.join(os.getcwd(), "images", "overlays")
    r = subprocess.run(["qemu-img", "create", "-o",
                        f"backing_file=../{name}.{fmt},backing_fmt={fmt}",
                        "-f", fmt, f"./images/overlays/{name}.{fmt}"], capture_output=True)
    if r.returncode != 0:
        echo("There was an error", "ERROR")
        echo(r.stderr, "ERROR")
    return r.returncode


def run(compose, name, keep_manifest):
    r = get_results(compose)
    r = dl_tar(compose, r)
    r = rm_tar(compose, r, remote=True)
    r = unzip(compose, r)
    r = rm_tar(compose, r)
    r = mv_manifest(compose, keep_manifest, r)
    if name is not None:
        r = mv(compose, name, r)
        r = overlay(compose, name, "qcow2", r)
    return r


def download(args):
    return run(args.compose, args.name, args.manifest)
