import sys

from .api import parse_args

def main():
    args = parse_args()
    sys.exit(args.func(args))
