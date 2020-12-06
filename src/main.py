import argparse
from DirProcess import DirProcessor


def handle_args():
    parser = argparse.ArgumentParser(description="Process site visit directory structure")
    parser.add_argument("dir")
    parser.add_argument("texOutput")
    parser.add_argument("shapeOutput")
    return parser.parse_args()


if __name__ == "__main__":
    args = handle_args()

    processor = DirProcessor(args.dir)

    processor.do_process(args.texOutput, args.shapeOutput)
