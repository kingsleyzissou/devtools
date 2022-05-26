import argparse

from .cancel import cancel
from .remove import remove
from .compose import compose
from .download import download

def add_compose_parser(sub_parser):
    compose_parser = sub_parser.add_parser(name="start")
    compose_parser.add_argument("blueprint", help="Composer blueprint", type=str)
    compose_parser.add_argument("-i", "--image-type", help="Image type", type=str, default="qcow2")
    compose_parser.add_argument("--host", type=str, default="localvm", help="Remote host")
    compose_parser.add_argument("-p", "--port", type=str, default="2222", help="Remote port")
    compose_parser.set_defaults(func=compose)

def add_download_parser(sub_parser):
    download_parser = sub_parser.add_parser(name="download")
    download_parser.add_argument("compose", help="Compose id", type=str)
    download_parser.add_argument("-m", "--manifest", help="Keep manifest", action="store_false", default=False)
    download_parser.add_argument("--host", type=str, default="localvm", help="Remote host")
    download_parser.add_argument("-p", "--port", type=str, default="2222", help="Remote port")
    download_parser.set_defaults(func=download)

def add_cancel_parser(sub_parser):
    cancel_parser = sub_parser.add_parser(name="cancel")
    cancel_parser.add_argument("compose", help="Compose id", type=str)
    cancel_parser.add_argument("-m", "--manifest", help="Keep manifest", action="store_false", default=False)
    cancel_parser.add_argument("--host", type=str, default="localvm", help="Remote host")
    cancel_parser.add_argument("-p", "--port", type=str, default="2222", help="Remote port")
    cancel_parser.set_defaults(func=cancel)

def add_remove_parser(sub_parser):
    remove_parser = sub_parser.add_parser(name="remove")
    remove_parser.add_argument("compose", help="Compose id", type=str)
    remove_parser.add_argument("-m", "--manifest", help="Keep manifest", action="store_false", default=False)
    remove_parser.add_argument("--host", type=str, default="localvm", help="Remote host")
    remove_parser.add_argument("-p", "--port", type=str, default="2222", help="Remote port")
    remove_parser.set_defaults(func=remove)

def parse_args():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers()
    add_compose_parser(sub_parser)
    add_download_parser(sub_parser)
    add_cancel_parser(sub_parser)
    add_remove_parser(sub_parser)
    return parser.parse_args()
