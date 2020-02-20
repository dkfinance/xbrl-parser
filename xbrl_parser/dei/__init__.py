from xbrl_parser import XBRL


class DEI(XBRL):
    def __init__(self, file: str):
        """

        :param file: path to the file.
        """
        super().__init__(file, "dei:")
