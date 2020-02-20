from collections import OrderedDict

import xmltodict

from xbrl_parser.utilities import convert_to_correct_type, xbrli_period_convert, camel_to_snake


class XBRL:
    def __init__(self, file: str, *prefixes: str):
        with open(file) as f:
            p = xmltodict.parse(f.read())
        if "xbrli:xbrl" not in p.keys():
            raise Exception()
        xbrl = p["xbrli:xbrl"]
        context = {}
        self.financials = {}
        for key, val in xbrl.items():
            if "xbrli:context" in key:
                if isinstance(val, list):
                    for l in val:
                        id = l["@id"]
                        period = xbrli_period_convert(l["xbrli:period"])
                        context[id] = {
                            "period": period,
                        }
                continue
            elif not any(x in key for x in prefixes):
                continue
            name = camel_to_snake(key[key.rfind(":") + 1:])
            if isinstance(val, list):
                self.financials[name] = []
                for p in val:
                    if isinstance(p, OrderedDict):
                        context_ref = p["@contextRef"]
                        unit = p["@unitRef"]
                        value = convert_to_correct_type(p["#text"])
                        self.financials[name].append({
                            "context_ref": context[context_ref],
                            "unit": unit,
                            "value": value
                        })
                    else:
                        raise Exception(":-(")
            else:
                self.financials[name] = val
