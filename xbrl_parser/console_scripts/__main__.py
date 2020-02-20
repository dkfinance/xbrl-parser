from pprint import pprint

from xbrl_parser.console_scripts import argument_parser
from xbrl_parser.dei import DEI
from xbrl_parser.gaap import GAAP
from xbrl_parser.ifrs import IFRS


def parse_ifrs():
    args = argument_parser.default()
    for file in args.files:
        ifrs = IFRS(file=file)
        pprint(ifrs.financials)


def parse_gaap():
    args = argument_parser.default()
    for file in args.files:
        gaap = GAAP(file=file)
        pprint(gaap.financials)


def parse_dei():
    args = argument_parser.default()
    for file in args.files:
        dei = DEI(file=file)
        pprint(dei.financials)


if __name__ == '__main__':
    parse_ifrs()
