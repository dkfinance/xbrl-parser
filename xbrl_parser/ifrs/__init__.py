from lxml import etree

from xbrl_parser.utilities import convert_to_correct_type


class IFRS:
    def __init__(self, file: str, *prefixes: [str]):
        """

        :param file: path to the file.
        :param prefixes: list of extra prefixes to look for (fx. ifrs-dk).
        """
        self.financials = {}
        tree = etree.parse(file)
        for tag in tree.iter():
            if tag.prefix != "ifrs-full" and tag.prefix not in prefixes:
                continue
            name = tag.tag[tag.tag.rfind("}") + 1:]
            self.financials[name] = convert_to_correct_type(tag.text)
