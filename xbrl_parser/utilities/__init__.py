import ast
import re
from collections import OrderedDict
from datetime import datetime


def convert_to_correct_type(val: str):
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except ValueError:
        return ast.literal_eval(val)
    except Exception:
        return val


def xbrli_period_convert(period: OrderedDict):
    p = {}
    for key, val in period.items():
        c = key[key.rfind(":") + 1:]
        name = camel_to_snake(c)
        p[name] = convert_to_correct_type(val)
    return p


def camel_to_snake(name: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
