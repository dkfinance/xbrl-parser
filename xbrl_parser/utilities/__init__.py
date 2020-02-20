import ast


def convert_to_correct_type(val: str):
    try:
        return ast.literal_eval(val)
    except ValueError:
        return val
