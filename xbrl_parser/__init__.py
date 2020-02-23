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
            for p in val:
                self._append_financials(name=name, val=p)
        elif name == "ifrs-full":
            return
        elif name == "ifrs-dk":
            return
        elif isinstance(val, OrderedDict):
            self._append_financials(name=name, val=val)
        elif "http://" in val:
            return
        else:
            raise NotImplementedError(name)

    def _append_financials(self, name, val):
        if isinstance(val, OrderedDict):
            if name not in self.financials:
                self.financials[name] = []
            self.financials[name].append(self._parse_single_statement(val))
        else:
            raise Exception(":-(")

    def _parse_single_statement(self, p):
        context_ref = p["@contextRef"]
        unit = p["@unitRef"] if "@unitRef" in p else None
        value = convert_to_correct_type(p["#text"])
        ok = self.context[context_ref]
        result = {
            "unit": unit,
            "value": value,
            "period": ok["period"]
        }
        result.update()
        return result

    def get_list_asset(self, name: str):
        f = self.financials[name]
        result = {}
        for ob in f:
            year = next(iter(ob["period"].values())).year
            if year not in result:
                result[year] = 0
            result[year] += ob["value"]
        return result

    def get_nwc(self, newest_year=True):
        data = self.get_list_asset(name="current_assets")
        year = self.get_newest_year(data) if newest_year else self.get_oldest_year(data)
        return (self.get_list_asset(name="current_assets")[year] -
                self.get_list_asset(name="current_liabilities")[year])

    def get_ebit(self, newest_year=True):
        data = self.get_list_asset("profit_loss_from_operating_activities")
        year = self.get_newest_year(data) if newest_year else self.get_oldest_year(data)
        return data[year]

    def get_ppe(self, newest_year=True):
        data = self.get_list_asset("property_plant_and_equipment")
        year = self.get_newest_year(data) if newest_year else self.get_oldest_year(data)
        return data[year]

    def get_current_assets(self, newest_year=True):
        data = self.get_list_asset("current_assets")
        year = self.get_newest_year(data) if newest_year else self.get_oldest_year(data)
        return data[year]

    def get_current_liabilities(self, newest_year=True):
        data = self.get_list_asset("current_liabilities")
        year = self.get_newest_year(data) if newest_year else self.get_oldest_year(data)
        return data[year]

    def get_current_ratio(self, newest_year=True):
        current_assets = self.get_current_assets(newest_year)
        current_liabilities = self.get_current_liabilities(newest_year)
        return current_assets / current_liabilities

    @staticmethod
    def get_newest_year(data: {}):
        year = 0
        for key, val in data.items():
            if key < year:
                continue
            year = key

        return year

    @staticmethod
    def get_oldest_year(data: {}):
        year = None
        for key, val in data.items():
            if year is None or key < year:
                year = key

        return year
