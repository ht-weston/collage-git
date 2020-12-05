import sys
from DirProcess import DirProcessor

if __name__ == "__main__":
    processor = DirProcessor(sys.argv[1])

    print(processor.do_process())
