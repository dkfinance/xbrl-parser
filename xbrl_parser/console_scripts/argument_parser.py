from argparse import ArgumentParser, Namespace


def default() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("files", type=str, nargs="+", help="One or XLBR files to be parsed.")
    parser.add_argument("-o", "--output-file", dest="output_file",
                        help="Output file, if no file is specified it will be printed to stdout.")
    return parser.parse_args()
