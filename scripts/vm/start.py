import os, string, subprocess
from tools import echo, read_file, write_file

ARCH_ARGS = {
  "x86_64": [
    "-enable-kvm",
    "-cpu host"
  ],
  "aarch": [],
  "ppc": [],
  "s390x": []
}

def build_cmd(overlay) -> str:
    def split_ports(forwards):
        l,r = forwards.split(':')
        return f"hostfwd=tcp::{r}-:{l}"

    if overlay.simple:
        overlay.ports = "22:2223"

    tmplt = string.Template(read_file("./config/templates/qemu-template"))
    t = tmplt.safe_substitute({
        "arch": overlay.arch,
        "image": overlay.overlay_image,
        "mac": "FE:0B:6E:22:3D:00",
        "fwds": ",".join([split_ports(p) for p in overlay.ports.split(",")]),
        "pidfile": overlay.pidfile
    })

    if overlay.iso:
        t += " \\\n" + f"--cdrom {overlay.iso}"

    if not overlay.simple:
        t += " \\\n" + "-nographic"

    arch_args = ARCH_ARGS[overlay.arch]
    if len(arch_args) > 0:
        t += " \\\n" + " \\\n".join(arch_args)

    return t

def create_script(cmd) -> None:
    tmplt = string.Template(read_file("./config/templates/expect-template"))
    t = tmplt.safe_substitute({
        "qemu": cmd
    })
    write_file("/tmp/qemu", t)
    os.chmod("/tmp/qemu", 0o775)

def launch() -> int:
    echo("Starting VM...", "OK")
    try:
        subprocess.run(["expect", "/tmp/qemu"])
        return 0
    except KeyboardInterrupt:
        echo("Keyboard interrupt, aborting", "OK")
        return 0
    except Exception:
        echo("Some weird error", "ERROR")
        return 1

def start(overlay):
    create_script(build_cmd(overlay))
    return launch()
