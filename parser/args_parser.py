import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-cl', help='Diactivate console logging', type=int, default=1)

def parse_args() -> list[argparse.Namespace]:
    args = parser.parse_args()
    return args._get_kwargs()