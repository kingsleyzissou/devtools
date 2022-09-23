import json, os, subprocess, sys, dotenv
from tools import echo, load_json, write_yaml, sanitize_output

dotenv.load_dotenv()
RUN_DIR = os.path.join(os.getenv("XDG_RUNTIME_DIR"), "osbuild-vm")
DATA_DIR = os.path.join(RUN_DIR, "data")
SCRATCH_DIR = os.getenv("SCRATCH_DIR")
OVERLAY_DIR = os.getenv("OVERLAY_DIR")
SSH_KEY = os.getenv("SSH_KEY")

def get_pubkey() -> None:
    pubkey_file = os.path.expanduser(f"~/.ssh/{SSH_KEY}")
    key = subprocess.check_output(["cat", pubkey_file])
    return sanitize_output(key)

class BaseImage:

    def __init__(self, arch, distro, ports, prepare=False, location=None, simple=False):
        self.iso = None
        self.arch = arch
        self.distro = distro
        self.ports = ports
        self.simple = simple or location is not None
        self.get_image_location(location)
        if prepare:
            self.prepare_image()
        basename = os.path.splitext(os.path.basename(self.overlay_image))[0]
        self.pidfile = f"/tmp/{basename}"

    def get_image_location(self, location) -> tuple:
        if location:
            self.overlay_image = location
            return
        images = load_json("./config/data/guest-images.json")
        try:
            self.guest_image = os.path.join(SCRATCH_DIR, images[self.arch][self.distro])
            image_basename = os.path.splitext(os.path.basename(self.guest_image))[0]
            self.overlay_image = os.path.join(OVERLAY_DIR, f"{image_basename}.overlay.qcow2")
        except Exception:
            echo(f"{self.distro} not available for {self.arch} arch", "ERROR")
            sys.exit(1)

    def get_repos(self) -> None:
        repos = {}

        if self.distro.startswith("rhel8") or self.distro.startswith("centos8"):
            repos = load_json("./config/data/rhel8-repos.json")
            if not self.arch == "x86_64":
                del repos["rt"]

        if self.distro.startswith("rhel9"):
            repos = load_json("./config/data/rhel9-repos.json")

        for r in repos["yum_repos"]:
            repos["yum_repos"][r]["baseurl"] = repos["yum_repos"][r]["baseurl"].replace("${arch}", self.arch)

        return repos

    def make_overlay(self) -> None:
        echo("Making overlay")
        subprocess.run(["qemu-img", "create", "-q", "-o", f"backing_file={self.guest_image},backing_fmt=qcow2", "-f", "qcow2", self.overlay_image])
        subprocess.run(["qemu-img", "resize", "-q", self.overlay_image, "100G"])

    def make_userdata(self) -> None:
        echo("Making userdata")
        subprocess.run(["mkdir", "-p", DATA_DIR])
        user_data = load_json("./config/templates/user-data.json")

        pubkey = get_pubkey()
        for u in user_data["users"]:
            if u == "default":
                continue
            u["ssh_authorized_keys"] = [pubkey]

        repos = self.get_repos()
        data = json.dumps({**user_data, **repos})
        write_yaml(os.path.join(DATA_DIR, "user-data"), data, True)

    def make_metadata(self) -> None:
        echo("Making userdata")
        subprocess.run(["mkdir", "-p", DATA_DIR])
        meta_data = load_json("./config/templates/meta-data.json")
        meta_data["local-hostname"] = meta_data["local-hostname"].replace("${image_name}", self.distro)

        data = json.dumps({**meta_data})
        write_yaml(os.path.join(DATA_DIR, "meta-data"), data, False)

    def generate_iso(self) -> None:
        echo("Generating iso")
        self.iso = os.path.join(DATA_DIR, "composer-init.iso")
        subprocess.run(["mkisofs", "-input-charset", "utf-8", "-output",
        f"{self.iso}", "-volid", "cidata", "-joliet", "-rock",
        "-quiet", f"{RUN_DIR}/data/user-data", f"{RUN_DIR}/data/meta-data"])

    def prepare_image(self) -> None:
        if not os.path.exists(self.overlay_image):
            self.make_overlay()
            self.make_userdata()
            self.make_metadata()
            self.generate_iso()
