import datetime


def jsonify(value, t_depth=0, in_line=True):
    s_ = " " * 4 * t_depth
    s1_ = s_ + (" " * 4)
    if isinstance(value, dict):
        if in_line:
            return "{" + "".join([f"{jsonify(k)}: {jsonify(v, 0, True)}" for k, v in value.items()]) + "}"
        else:
            return f"{s_}{{" + f"\n{s1_}"
    elif isinstance(value, datetime.datetime):
        return f"{s_}datetime.datetime({value.strftime('yyyy, mm, dd, HH, MM, SS')})"
    else:
        return str(value)
