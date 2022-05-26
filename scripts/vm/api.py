import argparse

###############################################################################
# Constants
###############################################################################

PORTS = "22:2222,443:10443,9090:9091,8080:8080"

###############################################################################
# Constants
###############################################################################

PORTS = "22:2222,443:10443,9090:9091,8080:8080"

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--distro", help="Distro", type=str)
    group.add_argument("-i", "--input", help="Path to local image", type=str)
    parser.add_argument("-a", "--arch", help="Architecture", default="x86_64", type=str)
    parser.add_argument("-p", "--ports", default=PORTS, help="Ports to forward to vm", type=str)
    parser.add_argument("--simple", default=False, help="Simple VM configuration", action="store_true")
    parser.add_argument("command", help="The VM command to run", type=str)
    return parser.parse_args()
