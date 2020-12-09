import argparse

from ProjectRecord import ProjectRecord, LatexProjectPrinter, ShapefileProjectPrinter, write_project_record_to_yaml, \
    get_project_yaml_filename


def handle_args():
    parser = argparse.ArgumentParser(description="Process site visit directory structure")
    parser.add_argument("dir")
    parser.add_argument("texOutput")
    parser.add_argument("shapeOutput")
    return parser.parse_args()


if __name__ == "__main__":
    args = handle_args()
    p = ProjectRecord("./src/imgs/")

    lp = LatexProjectPrinter(p, args.texOutput)
    lp.write_to_file()

    sp = ShapefileProjectPrinter(p, args.shapeOutput)
    sp.write_to_file()

    write_project_record_to_yaml(p, get_project_yaml_filename(p))
