from argparse import ArgumentParser, Namespace


def default() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("files", type=str, nargs="+", help="One or XLBR files to be parsed.")
    parser.add_argument("-s", "--xbrl-standard", dest="xbrl_standard",
                        help="Which standard do you want to parse? available options: 'IFRS', 'DEI', 'GAAP'.",
                        default="IFRS")
    return parser.parse_args()
