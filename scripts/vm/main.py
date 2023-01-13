import sys
import pkg_resources
from devtools import echo

from .api import parse_args
from .overlay import BaseImage

###############################################################################
# STUFF
###############################################################################


def run(overlay, command):
    for entry_point in pkg_resources.iter_entry_points('vm_commands'):
        if entry_point.name == command:
            return entry_point.load()(overlay)
    echo("Unknown command", "ERROR")
    return 1


def main():
    args = parse_args()
    overlay = BaseImage(args.arch, args.distro, args.ports,
                        not args.input, args.input, args.simple)
    sys.exit(run(overlay, args.command))
