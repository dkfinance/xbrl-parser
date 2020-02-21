import json
from collections import OrderedDict
from importlib import import_module

from xbrl_parser.utilities import snake_to_camel


def custom(obj: object):
    if isinstance(obj, OrderedDict):
        # Convert recursively to dict
        dct = json.loads(json.dumps(obj))
        p = convert_dict(dct)
        return p


def convert_dict(d: dict, path: str = "xbrl_parser.schemas"):
    for key, val in d.items():
        x = key[key.rfind(":") + 1:]
        class_name = snake_to_camel(x)
        new_base_path = f"{path}.{x}"
        if import_string(f"{new_base_path}.{class_name}"):
            print("pog")
        elif isinstance(val, dict):
            convert_dict(val, path=new_base_path)
        else:
            print("naay")


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
                          ) from err
