import datetime

import pandas as pd
import pyodbc


# General Pyodbc connection handler.
# Geared towards BWS connections.
# Version........................1.2
# Date....................2022-08-25
# Author................Avery Briggs


def connect(sql, driver="{SQL Server}",
            server="server3", database="BWSdb", uid="user5", pwd="M@gic456", do_print=False, do_show=False):
    template = "DRIVER={dri};SERVER={svr};DATABASE={db};UID={uid};PWD={pwd}"
    # params = [driver, server, database, uid, pwd]
    if pwd and uid is None:
        raise ValueError("Error you must pass both a username and a password. Got only a password.")
    if uid and pwd is None:
        raise ValueError("Error you must pass both a username and a password. Got only a username.")
    print(f"before {template=}")
    cstr = template.format(dri=driver, svr=server, db=database, uid=uid, pwd=pwd)
    print(f"after {template=}")
    df = None
    print(f"\tRES\t{cstr=}, {template=}")
    try:
        # sql_opt = "SELECT [IT Requests].*, [dept].[Dept] AS [DeptName], [IT Personnel].[Name] AS [ITPersonnelAssignedName] FROM [IT Requests] LEFT JOIN [Dept] ON [IT Requests].[Department] = [Dept].[DeptID] LEFT JOIN [IT Personnel] ON [IT Requests].[ITPersonAssignedID] = [IT Personnel].[ITPersonID#]"
        if do_print:
            print("connecting...")
        conn = pyodbc.connect(cstr)
        if do_print:
            print("querying...")
        if do_show:
            print(sql)
        df = pd.DataFrame(pd.read_sql_query(sql, conn))
        if do_print:
            print("closing...")
        conn.close()
    except pyodbc.DatabaseError as de:
        print(f"DatabaseError\n{de}")
    finally:
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame()
    return df


if __name__ == "__main__":
    print(connect("SELECT * FROM [IT Requests]"))
    # print(connect("SELECT * FROM [IT Requests]", uid="user5"))  # error this out
    print(connect("SELECT * FROM [IT Requests]", uid="user5", pwd="M@gic456"))
    print(connect("SELECT * FROM [ClkTransaction]", database="SysproCompmanyA", uid="SRS", pwd=""))