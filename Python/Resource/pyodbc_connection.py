import datetime

import pandas as pd
import pyodbc


VERSION = \
    """
    General Pyodbc connection handler.
    Geared towards BWS connections.
    Version...............1.7
    Date...........2024-02-29
    Author(s)....Avery Briggs
    """


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(), "%Y-%m-%dictionary")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def connect(sql, driver="{SQL Server}",
            server="server3", database="BWSdb", uid="user5", pwd="M@gic456", do_print=False, do_show=False):
    template = "DRIVER={dri};SERVER={svr};DATABASE={db};UID={uid};PWD={pwd}"
    # params = [driver, server, database, uid, pwd]
    if pwd and uid is None:
        raise ValueError("Error you must pass both a username and a password. Got only a password.")
    if uid and pwd is None:
        raise ValueError("Error you must pass both a username and a password. Got only a username.")
    # print(f"before {template=}")
    cstr = template.format(dri=driver, svr=server, db=database, uid=uid, pwd=pwd)

    has_insert = all([(stmt in sql.upper()) for stmt in ["INSERT INTO", "VALUES"]])
    has_update = all([(stmt in sql.upper()) for stmt in ["UPDATE", "SET"]])

    # print(f"after {template=}")
    df = None
    # print(f"\tRES\t{cstr=}, {template=}")
    try:
        # sql_opt = "SELECT [IT Requests].*, [dept].[Dept] AS [DeptName], [IT Personnel].[Name] AS [ITPersonnelAssignedName] FROM [IT Requests] LEFT JOIN [Dept] ON [IT Requests].[Department] = [Dept].[DeptID] LEFT JOIN [IT Personnel] ON [IT Requests].[ITPersonAssignedID] = [IT Personnel].[ITPersonID#]"
        if do_print:
            print("connecting...")
        if do_show:
            print(f"cstr: '{cstr}'")
        conn = pyodbc.connect(cstr)
        crsr = conn.cursor()
        if do_print:
            print("querying...")
        if do_show:
            print(sql)

        if has_insert or has_update:
            # no return value
            crsr.execute(sql)
            conn.commit()
        else:
            df = pd.DataFrame(pd.read_sql_query(sql, conn))

        if do_print:
            print("closing...")
        conn.close()
    except pyodbc.DatabaseError as de:
        print(f"DatabaseError\n{de}")
    # except TypeError as te:
    #     print(f"TypeError\n{te}")
    finally:
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame()
    return df


if __name__ == "__main__":
    print(connect("SELECT * FROM [IT Requests]"))
    # print(connect("SELECT * FROM [IT Requests]", uid="user5"))  # error this out
    print(connect("SELECT * FROM [IT Requests]", uid="user5", pwd="M@gic456"))
    print(connect("SELECT * FROM [ClkTransaction]", database="SysproCompmanyA", uid="SRS", pwd=""))
