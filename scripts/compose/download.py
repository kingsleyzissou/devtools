import subprocess
from tools import echo

def get_results(compose):
    echo("Fetching results...")
    r = subprocess.run(["ssh", "-q", "localvm", "composer-cli", "compose", "results", compose], capture_output=True)
    return r. returncode

def dl_tar(compose, code):
    if  code != 0:
        return code
    echo("Downloading image...")
    r = subprocess.run(["scp", "-q", f"localvm:{compose}.tar", "./data/images/."], capture_output=True)
    return r.returncode

def rm_tar(compose, code, remote = False):
    if code != 0:
        return code
    if remote:
        echo("Removing remote tar...")
        r = subprocess.run(["ssh", "-q", "localvm", "rm", f"{compose}.tar"], capture_output=True)
        return r.returncode
    echo("Removing tar...")
    r = subprocess.run(["rm", f"data/images/{compose}.tar"], capture_output=True)
    return r.returncode

def unzip(compose, code):
    if code != 0:
        return code
    echo("Unzipping tar...")
    r = subprocess.run(["tar", "-xvf", f"{compose}.tar", ""], cwd="data/images", capture_output=True)
    return r.returncode

def mv_manifest(compose, keep, code):
    if code != 0:
        return code
    if keep:
        echo("Moving manifest...")
        r = subprocess.run(["mv", f"data/images/{compose}.json", "data/manifests/."], capture_output=True)
        return r.returncode
    echo("Removing manifest...")
    r = subprocess.run(["rm", f"data/images/{compose}.json"], capture_output=True)
    return r.returncode

def run(compose, keep_manifest):
    r = get_results(compose)
    r = dl_tar(compose, r)
    r = rm_tar(compose, r, remote = True)
    r = unzip(compose, r)
    r = rm_tar(compose, r)
    r = mv_manifest(compose, keep_manifest, r)
    return r

def download(args):
    return run(args.compose, args.manifest)
