import os
import subprocess
import sys

from .api import parse_args

PROJECTS_DIR = os.path.join("projects", "osbuild")
COMPONENTS = {
    "composer": os.path.join(os.getcwd(), "..", "osbuild-composer"),
    "osbuild": os.path.join(os.getcwd(), "..", "osbuild"),
    "blueprints": os.path.join(os.getcwd(), "blueprints")
}


def rsync(host, component, distro=None) -> None:
    src = COMPONENTS[component]
    dest = f"{host}:{PROJECTS_DIR}"

    subprocess.run(["ssh", "-q", host, "mkdir", "-p",
                   f"{PROJECTS_DIR}/{component}"])

    if component == "blueprints":
        dest = f"{host}:{PROJECTS_DIR}/{component}"
        subprocess.run(["rsync", "-aP", f"{src}/common/.", dest])
        if distro:
            subprocess.run(["rsync", "-aP", f"{src}/{distro}/.", dest])
        return

    exclude = ["--exclude", "bin", "--exclude",
               "build", "--exclude", "rpmbuild"]
    subprocess.run(["rsync", "-aP", *exclude,
                   "--delete-excluded", "--delete", src, dest])


def run(args):
    def ssh_cmd(cmd):
        ssh_cmd = ["ssh", "-q", args.host, "-p",
                   args.port, "'python3 -s -'", "<"]
        return " ".join([*ssh_cmd, *cmd])

    if args.composer:
        rsync(args.host, "composer")
        cmd = ssh_cmd(["./scripts/install/composer"])
        subprocess.run(cmd, shell=True)

    if args.osbuild:
        rsync(args.host, "osbuild")
        cmd = ssh_cmd(["./scripts/install/osbuild"])
        subprocess.run(cmd, shell=True)

    if args.cockpit:
        cmd = ssh_cmd(["./scripts/install/cockpit"])
        subprocess.run(cmd, shell=True)

    if args.koji:
        cmd = ssh_cmd(["./scripts/install/koji"])
        subprocess.run(cmd, shell=True)

    if args.blueprints:
        rsync(args.host, "blueprints", args.distro)
        cmd = ssh_cmd(["./scripts/install/blueprints"])
        subprocess.run(cmd, shell=True)

    return 0


def main():
    sys.exit(run(parse_args()))
