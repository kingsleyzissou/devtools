import subprocess
from tools import echo, sanitize_output

def get_pid(pidfile="pidfile"):
    r = subprocess.run(["cat", pidfile], capture_output=True)
    return sanitize_output(r.stdout)

def stop(overlay):
    echo("Shutting down VM...")
    r = subprocess.run(["kill", "-9", get_pid(overlay.pidfile)], capture_output=True)

    if  r.returncode == 0:
        echo("VM shutdown successfully", "OK")
        return r.returncode

    echo(sanitize_output(r.stderr), "ERROR")
    return r.returncode
