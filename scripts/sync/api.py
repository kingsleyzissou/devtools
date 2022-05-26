import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Choose at least one of [composer|osbuild|cockpit]")
    parser.add_argument("--composer", help="Install composer dev on VM", default=False, action="store_true")
    parser.add_argument("--osbuild", help="Install osbuild dev on VM", default=False, action="store_true")
    parser.add_argument("--cockpit", help="Install cockpit on VM", default=False, action="store_true")
    parser.add_argument("--koji", help="Install koji on VM", default=False, action="store_true")
    parser.add_argument("--blueprints", help="Update blueprints on VM", default=False, action="store_true")
    parser.add_argument("-d", "--distro", help="[rhel | fedora]", type=str)
    parser.add_argument("--host", type=str, default="localvm", help="Remote host")
    parser.add_argument("-p", "--port", type=str, default="2222", help="Remote port")
    return parser.parse_args()
