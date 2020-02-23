import json

from xbrl_parser import XBRL
from xbrl_parser.console_scripts import argument_parser


def main():
    args = argument_parser.default()
    xbrl_standard = args.xbrl_standard
    xbrl_standard = xbrl_standard.lower()
    if xbrl_standard == "ifrs":
        xbrl_standard = "ifrs"
    elif xbrl_standard not in ["gaap", "dei"]:
        raise NotImplementedError("The standard %s is not available." % xbrl_standard)

    for file in args.files:
        ifrs = XBRL(file, xbrl_standard)
        ifrs.parse()
        print(json.dumps(ifrs.financials, indent=4, sort_keys=True, default=str))


if __name__ == '__main__':
    main()
