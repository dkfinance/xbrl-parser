from xbrl_parser import XBRL


class IFRS(XBRL):
    def __init__(self, file: str):
        """

        :param file: path to the file.
        """
        super().__init__(file, "ifrs-full")
