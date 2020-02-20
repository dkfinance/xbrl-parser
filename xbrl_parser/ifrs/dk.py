from xbrl_parser.ifrs import IFRS


class IFRSDK(IFRS):
    def __init__(self, file: str):
        super().__init__(file, "ifrs-dk")
