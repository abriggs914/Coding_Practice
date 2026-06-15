import datetime
import tkinter
from typing import Any

import pandas

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General JSON Centered Utility Functions
    Version..............1.05
    Date...........2026-05-05
    Author(s)....Avery Briggs
    """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(),
                                      "%Y-%m-%dictionary")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if
            w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def jsonify(value: Any, in_line: bool = True, t_depth: int = 0) -> str:
    """
        Convert objects and common data types to serializable json.
        Use a file object to write the string result to a json file.
        Read the json file using a file object then evaluate the results.
        
        ex:
            import json            
            
            path: str = "PATH_TO_JSON_FILE"
            data: dict | list = {...}
            
            ## Writing
            data: str = jsonify(data)
            with open(path) as f:
                f.write(data)
            
            ## Reading
            with open(path) as f:
                data: dict | list = eval(json.load(f))
                # OR
                data: dict | list = eval(f.read())
    """
    # print(f"t={type(value)}, {value=}")

    s_ = " " * 4 * t_depth
    s1_ = s_ + (" " * 4)

    if value is None:
        return "null"

    elif isinstance(value, dict):
        if in_line:
            return "{" + ", ".join([f"\"{jsonify(k).removeprefix(chr(34)).removesuffix(chr(34))}\": {jsonify(v, True, 0)}" for k, v in value.items()]) + "}"
        else:
            return f"{s_ if t_depth == 0 else ''}{{\n{s1_}" + f"\n{s1_}".join(
                [f"\"{jsonify(k, False, t_depth + 1).removeprefix(chr(34)).removesuffix(chr(34))}\": {jsonify(v, False, t_depth + 1)}," for k, v in value.items()])[
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
            return f"{p1}" + ", ".join([f"{jsonify(v, True, 0)}" for v in value]) + f"{p2}"
        else:
            return f"{s_ if t_depth == 0 else ''}{p1}\n{s1_}" + f"\n{s1_}".join(
                [f"{jsonify(v, False, t_depth + 1)}," for v in value])[:-1] + f"\n{s_}{p2}"
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, pandas.DataFrame):
        return value.to_json()

    elif isinstance(value, datetime.datetime):
        y, n, d, h, m, s = value.year, value.month, value.day, value.hour, value.minute, value.second
        return f"\"datetime.datetime({', '.join(map(str, [y, n, d, h, m, s]))})\""

    if isinstance(value, tkinter.Variable):
        if isinstance(value, tkinter.BooleanVar):
            return f"\"tkinter.BooleanVar(value={jsonify(value.get())})\""
        elif isinstance(value, tkinter.IntVar):
            return f"\"tkinter.IntVar(value={jsonify(value.get())})\""
        elif isinstance(value, tkinter.DoubleVar):
            return f"\"tkinter.DoubleVar(value={jsonify(value.get())})\""
        elif isinstance(value, tkinter.StringVar):
            return f"\"tkinter.StringVar(value={jsonify(value.get())})\""
        else:
            return f"\"tkinter.Variable(value={jsonify(value.get())})\""

    elif isinstance(value, str):
        return f"\"{value}\"".replace("\\", "\\\\")
    elif hasattr(value, "__repr__"):
        rpr = repr(value).replace("\\", "\\\\")
        if all([
            "__main__" in rpr[:50],
            "object at" in rpr[:100],
            "<" in rpr[:5],
            ">" in rpr[-5:]
            ]):
            print(f"Object appears to have returned a generic repr string. This may not be json serializable.")
        return rpr
    elif hasattr(value, "__str__"):
        str_ = str(value).replace("\\", "\\\\")
        if all([
            "__main__" in str_[:50],
            "object at" in str_[:100],
            "<" in str_[:5],
            ">" in str_[-5:]
            ]):
            print(f"Object appears to have returned a generic str string. This may not be json serializable.")
        return str_
    else:
        return str(value).replace("\\", "\\\\")
    
    
    
    ##    def jsonify(value: Any, in_line: bool = True, t_depth: int = 0, smart_len: int = 40) -> str:
    
    # s_ = " " * 4 * t_depth
    # s1_ = s_ + (" " * 4)

    # def clean_key(k: Any) -> str:
    #     return jsonify(k, True, 0, smart_len).removeprefix('"').removesuffix('"')

    # def should_inline(text: str) -> bool:
    #     return len(text) <= smart_len and "\n" not in text

    # if value is None:
    #     return "null"

    # elif isinstance(value, dict):
    #     inline = "{" + ", ".join(
	# 		f"\"{clean_key(k)}\": {jsonify(v, True, 0, smart_len)}"
	# 		for k, v in value.items()
	# 	) + "}"

    #     if in_line or should_inline(inline):
    #         return inline

    #     if not value:
    #         return "{}"

    #     items = []
    #     for k, v in value.items():
    #         v_inline = jsonify(v, True, t_depth + 1, smart_len)
    #         if should_inline(v_inline):
    #             v_text = v_inline
    #         else:
    #             v_text = jsonify(v, False, t_depth + 1, smart_len)

    #         items.append(f"{s1_}\"{clean_key(k)}\": {v_text}")

    #     return (
	# 		f"{s_ if t_depth == 0 else ''}{{\n"
	# 		+ ",\n".join(items)
	# 		+ f"\n{s_}}}"
	# 	)

    # elif isinstance(value, (list, tuple, set)):
    #     p1, p2 = "[", "]"

    #     values = list(value)
    #     inline = f"{p1}" + ", ".join(
	# 		jsonify(v, True, 0, smart_len)
	# 		for v in values
	# 	) + f"{p2}"

    #     if in_line or should_inline(inline):
    #         return inline

    #     if not values:
    #         return f"{p1}{p2}"

    #     items = []
    #     for v in values:
    #         v_inline = jsonify(v, True, t_depth + 1, smart_len)
    #         if should_inline(v_inline):
    #             v_text = v_inline
    #         else:
    #             v_text = jsonify(v, False, t_depth + 1, smart_len)

    #         items.append(f"{s1_}{v_text}")

    #     return (
	# 		f"{s_ if t_depth == 0 else ''}{p1}\n"
	# 		+ ",\n".join(items)
	# 		+ f"\n{s_}{p2}"
	# 	)

    # elif isinstance(value, bool):
    #     return str(value).lower()

    # elif isinstance(value, pandas.DataFrame):
    #     return value.to_json()

    # elif isinstance(value, datetime.datetime):
    #     y, n, d, h, m, s = (
	# 		value.year,
	# 		value.month,
	# 		value.day,
	# 		value.hour,
	# 		value.minute,
	# 		value.second,
	# 	)
    #     return f"\"datetime.datetime({', '.join(map(str, [y, n, d, h, m, s]))})\""

    # if isinstance(value, tkinter.Variable):
    #     if isinstance(value, tkinter.BooleanVar):
    #         return f"\"tkinter.BooleanVar(value={jsonify(value.get(), True, 0, smart_len)})\""
    #     elif isinstance(value, tkinter.IntVar):
    #         return f"\"tkinter.IntVar(value={jsonify(value.get(), True, 0, smart_len)})\""
    #     elif isinstance(value, tkinter.DoubleVar):
    #         return f"\"tkinter.DoubleVar(value={jsonify(value.get(), True, 0, smart_len)})\""
    #     elif isinstance(value, tkinter.StringVar):
    #         return f"\"tkinter.StringVar(value={jsonify(value.get(), True, 0, smart_len)})\""
    #     else:
    #         return f"\"tkinter.Variable(value={jsonify(value.get(), True, 0, smart_len)})\""

    # elif isinstance(value, str):
    #     return f"\"{value}\""

    # elif hasattr(value, "__repr__"):
    #     rpr = repr(value)
    #     if all([
	# 		"__main__" in rpr[:50],
	# 		"object at" in rpr[:100],
	# 		"<" in rpr[:5],
	# 		">" in rpr[-5:]
	# 	]):
    #         print("Object appears to have returned a generic repr string. This may not be json serializable.")
    #     return rpr

    # elif hasattr(value, "__str__"):
    #     str_ = str(value)
    #     if all([
	# 		"__main__" in str_[:50],
	# 		"object at" in str_[:100],
	# 		"<" in str_[:5],
	# 		">" in str_[-5:]
	# 	]):
    #         print("Object appears to have returned a generic str string. This may not be json serializable.")
    #     return str_

    # else:
    #     return str(value)


    # def de_jsonify(value):
    #     if isinstance(value, str):
    #         if value.startswith("datetime.datetime(") and value.endswith(")") and value.count(",") == 5:
    #             # datetime


def peek_json(result, depth: int = 20):
    """
    Function takes a json object and attempts to gather all keys into a tree structure for viewing.
    If a list is found, assumes ALL list items are the same format as the first element, does not sample the rest.
    """
    def helper(data, d):
        if d > depth:
            return "..."

        if isinstance(data, dict):
            return {
                k: helper(v, d + 1)
                for k, v in data.items()
            }

        elif isinstance(data, list):
            if not data:
                return ["empty_list"]
            return [helper(data[0], d + 1)]

        elif isinstance(data, tuple):
            if not data:
                return ["empty_tuple"]
            return [helper(data[0], d + 1)]

        else:
            return type(data).__name__

    return helper(result, 0)


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

    print(jsonify(tests))
    print(peek_json(tests))
    
    import os
    import json
    
    p = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Data\data.json"
    
    with open(p) as f:
        data = json.load(f)
    
    with open(p) as f:
        data = json.load(f)
    
    dn, bn = os.path.dirname(p), os.path.basename(p)
    pn = os.path.join(dn, f"{bn}")
    data = jsonify(data, False)
    with open(pn, "w") as f:
        f.write(data)