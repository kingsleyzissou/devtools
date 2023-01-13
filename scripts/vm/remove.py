import subprocess
from devtools import echo, sanitize_output


def remove(overlay):
    echo("Deleting overlay...")
    r = subprocess.run(["rm", overlay.overlay_image], capture_output=True)

    if r.returncode == 0:
        echo("Overlay deleted successfully", "OK")
        return r.returncode

    echo(sanitize_output(r.stderr), "ERROR")
    return r.returncode
