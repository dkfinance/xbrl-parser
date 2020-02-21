from collections import OrderedDict

import xmltodict
from xbrl_parser.utilities import convert_to_correct_type, xbrli_convert_period, camel_to_snake, xbrli_parse_scenario, \
    xbrli_convert_entity


class XBRL:
    def __init__(self, file: str, *prefixes: str):
        with open(file) as f:
            p = xmltodict.parse(f.read())
        if "xbrli:xbrl" not in p.keys():
            raise Exception()
        self.xbrli = p["xbrli:xbrl"]
        self.context = {}
        self.financials = {}
        self.prefixes = prefixes
        self.period_from = None
        self.period_to = None

    def parse(self):
        for key, val in self.xbrli.items():
            if "xbrli:context" in key:
                # If the key matches a xbrli:context, then parse it and add it to the context dict.
                self._parse_context_list(val)
                continue

            if not any((x in key) for x in self.prefixes):
                # If the key doesn't match any of our prefixes, then skip it.
                continue

            name = camel_to_snake(key[key.rfind(":") + 1:])  # rename CamelCase to snake_case.
            self._parse_statement(val, name)  # parse prefix statement.

    def _parse_context_list(self, context_list):
        if isinstance(context_list, list):
            for context_obj in context_list:
                id = context_obj["@id"]
                self.context[id] = self._parse_single_context(context_obj)

    def _parse_single_context(self, xbrli_context):
        ctx = {}
        for key, val in xbrli_context.items():
            if "xbrli:scenario" == key:
                ctx["scenario"] = xbrli_parse_scenario(val)
            elif "xbrli:period" == key:
                ctx["period"] = xbrli_convert_period(val)
            elif key == "@id":
                ctx["id"] = val
            elif key == "xbrli:entity":
                ctx["entity"] = xbrli_convert_entity(val)
            else:
                raise NotImplementedError(":-(")
        return ctx

    def _parse_statement(self, val, name):
        if isinstance(val, list):
            self.financials[name] = []
            for p in val:
                if isinstance(p, OrderedDict):
                    self.financials[name].append(self._parse_single_statement(p))
                else:
                    raise Exception(":-(")
        elif name == "ifrs-full":
            return
        elif name == "ifrs-dk":
            return
        else:
            raise NotImplementedError(name)

    def _parse_single_statement(self, p):
        context_ref = p["@contextRef"]
        unit = p["@unitRef"]
        value = convert_to_correct_type(p["#text"])
        return {
            "context_ref": self.context[context_ref],
            "unit": unit,
            "value": value
        }
