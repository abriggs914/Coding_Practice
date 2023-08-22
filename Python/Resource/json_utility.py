import datetime
from typing import Any


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General JSON Centered Utility Functions
    Version..............1.01
    Date...........2023-08-17
    Author(s)....Avery Briggs
    """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(),
                                      "%Y-%m-%d")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if
            w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def jsonify(value: Any, t_depth: int = 0, in_line: bool = True) -> str:
    # print(f"t={type(value)}, {value=}")

    s_ = " " * 4 * t_depth
    s1_ = s_ + (" " * 4)

    if value is None:
        return "null"

    elif isinstance(value, dict):
        if in_line:
            return "{" + ", ".join([f"{jsonify(k)}: {jsonify(v, 0, True)}" for k, v in value.items()]) + "}"
        else:
            return f"{s_ if t_depth == 0 else ''}{{\n{s1_}" + f"\n{s1_}".join(
                [f"{jsonify(k, t_depth + 1, False)}: {jsonify(v, t_depth + 1, False)}," for k, v in value.items()])[
                                                              :-1] + f"\n{s_}}}"
    elif typ := isinstance(value, (list, tuple, set)):
        # if typ == set:
        #     p1, p2 = "{", "}"
        # elif typ == list:
        #     p1, p2 = "[", "]"
        # else:
        #     p1, p2 = "(", ")"
        p1, p2 = "[", "]"

        if in_line:
            return f"{p1}" + ", ".join([f"{jsonify(v, 0, True)}" for v in value]) + f"{p2}"
        else:
            return f"{s_ if t_depth == 0 else ''}{p1}\n{s1_}" + f"\n{s1_}".join(
                [f"{jsonify(v, t_depth + 1, False)}," for v in value])[:-1] + f"\n{s_}{p2}"

    elif isinstance(value, datetime.datetime):
        y, n, d, h, m, s = value.year, value.month, value.day, value.hour, value.minute, value.second
        return f"\"datetime.datetime({', '.join(map(str, [y, n, d, h, m, s]))})\""
    elif isinstance(value, str):
        return f"\"{value}\""
    elif hasattr(value, "__repr__"):
        return repr(value)
    elif hasattr(value, "__str__"):
        return str(value)
    else:
        return str(value)


    # def de_jsonify(value):
    #     if isinstance(value, str):
    #         if value.startswith("datetime.datetime(") and value.endswith(")") and value.count(",") == 5:
    #             # datetime



if __name__ == '__main__':
    tests = [
        1,
        -1,
        1.0,
        1e4,
        "None_",
        None,
        [],
        ["a", "b"],
        {"aa": 1, "b": 7},
        {"aa": 1, "b": {"1": [1, 3, 6]}},
        {"aa": datetime.datetime.now(), "b": {"1": [1, 3, {"a": 0, "b": [0, False, 0, {1: 3, 2: 4}]}]}, "c": "a"}
    ]

    for t in tests:
        print(f"\nv: '{t}'\n{jsonify(t, in_line=False)}")
