from pprint import pprint

from xbrl_parser.console_scripts import argument_parser
from xbrl_parser.ifrs import IFRS


def main():
    args = argument_parser.default()
    for file in args.files:
        ifrs = IFRS(file=file)
        pprint(ifrs.financials)


if __name__ == '__main__':
    main()
