import ast
import re
from collections import OrderedDict
from datetime import datetime


def convert_to_correct_type(val: str):
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except ValueError:
        try:
            return ast.literal_eval(val)
        except Exception:
            return val
    except Exception:
        return val


def xbrli_convert_period(period: OrderedDict):
    p = {}
    for key, val in period.items():
        c = key[key.rfind(":") + 1:]
        name = camel_to_snake(c)
        p[name] = convert_to_correct_type(val)
    return p


def xbrli_convert_entity(val):
    identifier = val["xbrli:identifier"]
    return {
        "cvr": identifier["#text"],
        "scheme": identifier["@scheme"]
    }


def xbrli_parse_scenario(scenario: OrderedDict):
    p = {}
    for key, val in scenario.items():
        c = key[key.rfind(":") + 1:]
        name = camel_to_snake(c)
        p[name] = dict(val)
    return p


def camel_to_snake(name: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def snake_to_camel(name: str):
    first, *rest = name.split('_')
    return first + ''.join(word.capitalize() for word in rest)
