from lxml import etree


class IFRS:
    def __init__(self, file: str):
        """

        :param file:
        """
        self.financials = {}
        tree = etree.parse(file)
        for tag in tree.iter():
            if tag.prefix != "ifrs-full":
                continue
            name = tag.tag[tag.tag.rfind("}") + 1:]
            value = tag.text
            try:
                value = float(value)
            except ValueError:
                pass
            finally:
                self.financials[name] = value
