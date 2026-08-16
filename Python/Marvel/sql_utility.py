import re
from typing import Literal, Any

from itertools import combinations
import pandas as pd
import datetime

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General SQL Utility Functions
    Version..............1.05
    Date...........2026-08-15
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


def no_specials(text: str, r_char: str = "") -> str:
    """ Exception on '_' """
    invalid = {
        " ", "!", "@", "#", "$", "%",
        "^", "&", "*", "(", ")", "-",
        "+", "=", "'", "\"", "[", "]",
        "{", "}", "\\", "|", ":", ";",
        "<", ",", ">", ".", "?", "/",
        "~", "`"
    }
    for c in invalid:
        text = text.replace(c, r_char)
    return text


def date_first(msg: str, keyword="date") -> str:
    """
        Ensure that a column name that specifies data follows the 'date-first' noming convention
        1 pass only! If the keyword appears
        EX: date_first("Quote Date") => "DateQuote"
    """

    r_msg = msg
    l_msg = msg.lower()
    l_key = keyword.lower()
    if l_key in l_msg:
        i = l_msg.index(l_key)
        # ensure that the word isn't "update"
        if l_msg[i - 2:i] != "up":
            r_msg = f"Date{msg[:i]}{msg[i + len(keyword):]}"
    return r_msg.strip()

    # lmsg = msg.lower()
    # if keyword in msg:
    #     idx = msg.index(keyword)
    #     if msg[idx - 2 : idx].lower() != "up":
    #         msg = f"Date{msg[:idx]}{msg[idx + len(keyword):]}"
    # print(f"RETURNED MESSAGE '{msg=}'")
    # return msg


def wrap(val: Any, is_col: bool = True, sanitize: bool = True) -> str:
    """
        Add '[' prefix and ']' suffix to a string, ensuring a unique identifier in SSMS
        Used heavily in 'parse_where' and 'create_sql' functions.

        see tests below in test_create_sql_parse_where_wrap()
    """
    if not str(val).strip():
        return ""
    # print(f"wrap: {val}")
    if is_col:
        v: str = f"[{str(val).removeprefix('[').removesuffix(']')}]"
    else:
        if isinstance(val, str) and val != "NULL":
            v: str = f"'{val}'"
        elif isinstance(val, datetime.datetime):
            v: str = f"'{val:%Y-%m-%d %H:%M:%S}'"
        elif isinstance(val, datetime.date):
            v: str = f"'{val:%Y-%m-%d}'"
        elif val is None:
            v: str = "NULL"
        else:
            v: str = str(val)
    if sanitize:
        v = v.strip()
        if v:
            v_first, *v_end = v
            v = v_first + re.sub(r"[;'\\\"]", "", v[1:-1]) + "".join(v_end[-1:])
    return v


def parse_where(clauses: Any, in_line: bool = True) -> str | list[str]:
    """
        Function to read a data structure of clauses and column names to output appropriate SQL WHERE clause

        see tests below in test_create_sql_parse_where_wrap()
    """
    trace: bool = False
    where_clause = ""

    print(f"PW type={type(clauses)}, {clauses=}")

    def op_process(var, ops_dict: dict[str: Any]) -> str:

        print(f"{var=}, {ops_dict=}")

        ops_clause = []
        for op, value_s in ops_dict.items():
            # op_s = "="
            op = op.lower()
            match op:
                case "!=":
                    op = "<>"
                case "<" | ">" | "<=" | ">=":
                    op = op
                case "in" | "not in" | "between":
                    op = op.upper()
                case "like":
                    op = "LIKE"
                case _:
                    op = "="
            # op = op_s
            test = ""
            # if not isinstance(value_s, (list, tuple)):
            value_s = [value_s]
            for i, val in enumerate(value_s):
                if op == "BETWEEN":
                    v0, v1 = val
                    ops_clause.append(f"{var} {op} {wrap(v0, is_col=False)} AND {wrap(v1, is_col=False)}")
                else:
                    if isinstance(val, (list, tuple)):
                        if op in ("IN", "NOT IN"):
                            in_mem = []
                            for j, val_ in enumerate(val):
                                in_mem.append(wrap(val_, is_col=False))
                            ops_clause.append(f"{var} {op} ({', '.join(in_mem)})")
                        else:
                            for j, val_ in enumerate(val):
                                ops_clause.append(f"{var} {op} {wrap(val_, is_col=False)}")
                    else:
                        ops_clause.append(f"{var} {op} {wrap(val, is_col=False)}")
            # test = []
            # print(f"OP {op=}, {value_s=}")
            # if not isinstance(value_s, (list, tuple)):
            #     value_s = [value_s]
            # for i, val in enumerate(value_s):
            #     if isinstance(val, (list, tuple)):
            #         if op_s == "between":
            #             v0, v1 = val
            #             test.append(f"{v0} AND {v1}")
            #         else:
            #             for j, val
            #     else:
            #
            #         test.append(f" {val}")
            #     # test = value_s
            #     print(f"OP {test=}")

            # ops_clause.append(f"{var} {op_s} {test}")
        ops_clause = "(" + (") AND (".join(ops_clause)) + ")"
        print(f"OP type={type(ops_clause)}, {ops_clause=}")
        return ops_clause

    def help_parse(clause_stmt, logic="OR", nest_level: int = 1) -> str:  # list[str]:

        if not clause_stmt:
            return ""

        # ts = ("####" * nest_level)
        ologic: str = "OR" if logic == "AND" else "AND"
        nl = "" if in_line else "\n"
        ts = "\t"
        ts1 = ("\t" * (nest_level + 0))
        # a = ts + ("(" if in_line else f"A(")
        a = ("(" if in_line else f"(")
        # b = ts + (f" {logic} " if in_line else f"\n{ts1}{logic}Z")
        b = (f" {logic} " if in_line else f"\n{ts1}{logic} ")
        c = ")" if in_line else f")"

        if trace:
            print(f"HP, LG={logic}, type={type(clause_stmt)}, {clause_stmt=}")

        if isinstance(clause_stmt, str):
            return ("=0=" if trace else "") + nl + ts + a + (
                b.join([clause_stmt]).removesuffix(logic).removeprefix("(").removesuffix(")")) + c
            # if in_line:
            #     return "(" + (f" {logic} ".join([clause_stmt]).strip().removesuffix(logic).strip()) + ")"
            # else:
            #     return "\t(" + (f" {logic} ".join([clause_stmt]).strip().removesuffix(logic).strip()) + ")"

        if isinstance(clause_stmt, (list, tuple)) and (len(clause_stmt) == 2) and isinstance(clause_stmt[1], dict):
            var, stmt_data_s = clause_stmt
            if (isinstance(var, str) and isinstance(stmt_data_s, dict)):
                d = (f" {ologic} " if in_line else f"\n{ts1}{ologic}Z")
                return ("=1=" if trace else "") + nl + ts + a + (
                    d.join([op_process(var, stmt_data_s)]).removesuffix(logic).removeprefix("(").removesuffix(")")) + c
                # return "=1=" + ts + a + (b.join([op_process(var, stmt_data_s)]).removesuffix(logic).removeprefix("(").removesuffix(")")) + c
                # return a + (b.join([op_process(var, stmt_data_s)]).strip().removesuffix(logic)) + c

            # # else:
            #     if in_line:
            #         return "(" + (f" {logic} ".join([op_process(var, stmt_data_s)]).strip().removesuffix(logic).strip()) + ")"
            #     else:
            #         return "\t(" + (f"\n\t{logic} ".join([op_process(var, stmt_data_s)]).strip().removesuffix(logic).strip()) + ")"
            # # else:
            # #     for
        if isinstance(clause_stmt, dict):
            return ("=2=" if trace else "") + nl + ts + a + (
                b.join([op_process(k, v).removeprefix("(").removesuffix(")") for k, v in clause_stmt.items()])) + c
            # if in_line:
            #     return "(" + (f" {logic} ".join([op_process(k, v) for k, v in clause_stmt.items()])) + ")"
            # else:
            #     return "\t(" + (f"\n\t{logic} ".join([op_process(k, v) for k, v in clause_stmt.items()])) + ")"

        res_clauses = []
        for i, clause_data in enumerate(clause_stmt):
            if trace:
                print(f"HP LOOP {i=}, type={type(clause_data)}, {clause_data=}")
            if isinstance(clause_stmt, dict):
                var = clause_data
                clause_data = clause_stmt[clause_data]
                if not isinstance(clause_data, dict):
                    res_clauses.extend(
                        [("=4=" if trace else "") + help_parse(cd, nest_level=nest_level + 1) for cd in clause_data])
                    # res_clauses += ["A"]
                else:
                    res_clauses.append(("=5=" if trace else "") + op_process(var, clause_data))
                    # res_clauses += ["B"]
            else:
                if isinstance(clause_data, (list, tuple)):
                    ret_val = help_parse(
                        clause_data,
                        logic=ologic,
                        nest_level=0
                    ).strip().removeprefix("(").removesuffix(")").strip()

                    res_clauses.append(
                        ("=6=" if trace else "") + "(" + ret_val + ")"
                    )
                    # res_clauses.append(op_process(var, clause_data))
                    # res_clauses += ["C"]
                elif isinstance(clause_data, str):
                    res_clauses.append(("7" if trace else "") + clause_data)
                else:
                    if isinstance(clause_data, dict):
                        res_clauses.extend([("=8=" if trace else "") + help_parse(clause_data, logic=ologic,
                                                                                  nest_level=nest_level + 1)])
                        # res_clauses += ["D"]
                    else:
                        res_clauses += [f"INVESTIGATE THIS CLAUSE_DATA {type(clause_data)=}"]
        if res_clauses:
            res_clauses[0] = f"({res_clauses[0]}"
            res_clauses[-1] = f"{res_clauses[-1]})"
        # return a + (b.join(res_clauses)) + c
        # return b.join(res_clauses)
        return f"{nl}\t" + f"{nl}\t{logic} ".join(res_clauses)
        # if in_line:
        #     return "(" + (f" {logic} ".join(res_clauses).strip().removesuffix(logic).strip()) + ")"
        # else:
        #     return "\t(" + (f"\n\t{logic} ".join(res_clauses).strip().removesuffix(logic).strip()) + ")"

    return help_parse(clauses)


def schema_parse(table: str, wrapped: bool = False) -> tuple[str, str]:
    t_og = table
    table = table.lower()
    r = "0"
    spl = "", ""
    if table.lower().count(".dbo.") == 1:
        r = "1"
        spl = table.split(".dbo.")
        table = spl[-1]
        db = spl[0]
    elif (table.lower().count("dbo.") == 1) and (table.lstrip()[0] == ""):
        r = "2"
        spl = table.split(".dbo.")
        table = spl[-1]
        db = spl[0]
    elif table.lower().count("[dbo].") == 1:
        r = "3"
        spl = table.split("[dbo].")
        table = spl[-1]
        db = spl[0].removesuffix("]").removesuffix(".")
    elif table:
        r = "4"
        db = ""
        table = table.removeprefix(".").removeprefix("dbo").removeprefix("]").removeprefix(".").removeprefix("[")
    else:
        r = "5"
        db, table = spl

    t_idx = t_og.lower().index(table)
    d_idx = t_og.lower().index(db)
    table = t_og[t_idx: t_idx + len(table)]
    db = t_og[d_idx: d_idx + len(db)]

    # if is_title:
    #     r += "a"
    #     f = str.title
    # elif is_lower:
    #     r += "b"
    #     f = str.lower
    # elif is_upper:
    #     r += "e"
    #     f = str.upper
    # else:
    #     r += "d"
    #     f = lambda x: x
    #
    # table = f(table)
    # database = f(database)

    if not wrapped:
        r += "x"
        table = table.removeprefix("[").removesuffix("]")
        db = db.removeprefix("[").removesuffix("]")
    else:
        r += "y"
        table = wrap(table)
        db = wrap(db)
    # return t_og, r, database, table
    return db, table


if __name__ == '__main__':


    pass
