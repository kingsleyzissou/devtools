import argparse

from .commands.start import start
from .commands.cancel import cancel
from .commands.delete import delete
from .commands.status import status
from .commands.download import download


def add_start_parser(sub_parser):
    start_parser = sub_parser.add_parser(name="start")
    start_parser.add_argument("blueprint", help="Composer blueprint", type=str)
    start_parser.add_argument("-i", "--image-type",
                              help="Image type", type=str, default="qcow2")
    start_parser.add_argument(
        "--host", type=str, default="localvm", help="Remote host")
    start_parser.add_argument("-p", "--port", type=str,
                              default="2222", help="Remote port")
    start_parser.set_defaults(func=start)


def add_download_parser(sub_parser):
    download_parser = sub_parser.add_parser(name="download")
    download_parser.add_argument("compose", help="Compose id", type=str)
    download_parser.add_argument(
        "-n", "--name", help="New file name", type=str)
    download_parser.add_argument(
        "-m", "--manifest", help="Keep manifest", action="store_false", default=False)
    download_parser.add_argument(
        "--host", type=str, default="localvm", help="Remote host")
    download_parser.add_argument(
        "-p", "--port", type=str, default="2222", help="Remote port")
    download_parser.set_defaults(func=download)


def add_status_parser(sub_parser):
    status_parser = sub_parser.add_parser(name="status")
    status_parser.add_argument(
        "--host", type=str, default="localvm", help="Remote host")
    status_parser.add_argument(
        "-p", "--port", type=str, default="2222", help="Remote port")
    status_parser.add_argument(
        "--json", help="Json output", action="store_true", default=False)
    status_parser.set_defaults(func=status)


def add_cancel_parser(sub_parser):
    cancel_parser = sub_parser.add_parser(name="cancel")
    cancel_parser.add_argument("compose", help="Compose id", type=str)
    cancel_parser.add_argument(
        "--host", type=str, default="localvm", help="Remote host")
    cancel_parser.add_argument(
        "-p", "--port", type=str, default="2222", help="Remote port")
    cancel_parser.set_defaults(func=cancel)


def add_delete_parser(sub_parser):
    delete_parser = sub_parser.add_parser(name="delete")
    group = delete_parser.add_mutually_exclusive_group()
    group.add_argument("--compose", help="Compose id", type=str)
    group.add_argument(
        "--finished", help="Delete finished", action="store_true", default=False)
    group.add_argument(
        "--failed", help="Delete failed", action="store_true", default=False)
    delete_parser.add_argument(
        "--host", type=str, default="localvm", help="Remote host")
    delete_parser.add_argument(
        "-p", "--port", type=str, default="2222", help="Remote port")
    delete_parser.set_defaults(func=delete)


def parse_args():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers()
    add_start_parser(sub_parser)
    add_download_parser(sub_parser)
    add_status_parser(sub_parser)
    add_cancel_parser(sub_parser)
    add_delete_parser(sub_parser)
    return parser.parse_args()
