import datetime

import pandas as pd

from pyodbc_connection import connect


def wp(val) -> str:
    if pd.isna(val):
        return "NULL"
    if isinstance(val, str):
        return f"'{val}'"
    if isinstance(val, datetime.date):
        return f"'{val:%Y-%m-%d}'"
    if isinstance(val, datetime.datetime):
        return f"'{val:%Y-%m-%d %H:%M:%S}'"
    return val


if __name__ == '__main__':

    # # sql = "SELECT * FROM [Games]"
    # sql = "SELECT * FROM [Teams]"
    # server = r"DESKTOP-47DUBI9\SQLEXPRESS"
    # database = "NHLdb"
    # # user = "avery"
    # # password = "calgary"
    # user = ""
    # password = ""
    #
    # print(f"{connect(sql=sql, server=server, database=database, uid=user, pwd=password, do_print=True, do_show=True)}")

    ####################################################################################################################
    ####################################################################################################################

    # df = pd.read_excel(r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\nhlapi_teams_output.xlsx")
    # print(df)
    # print(df.columns)
    #
    # print(f"INSERT INTO [NHLdb].[dbo].[Teams] ([FullName], [ShortName], [CommonName], [Abbrev], [NHLAPI_TeamID], [NHLAPI_FranchiseID])")
    # print("VALUES")
    # stmts = []
    # for i, row in df.iterrows():
    #     fn = wp(row["fullName"])
    #     sn = wp(row["ShortName"])
    #     cn = wp(row["CommonName"])
    #     tc = wp(row["rawTricode"])
    #     ii = wp(row["id"])
    #     fi = wp(row["franchiseId"])
    #     stmts.append(f"({fn}, {sn}, {cn}, {tc}, {ii}, {fi})")
    #
    # print(",\n".join(stmts))

    ####################################################################################################################
    ####################################################################################################################

    # df = pd.read_excel(r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\LeagueYearsOutput.xlsx")
    # print(df)
    # print(df.columns)
    #
    # print(f"INSERT INTO [NHLdb].[dbo].[LeagueYears] ([YearStr], [StartDate], [ChampYear], [SeasonPlayed], [Comments])")
    # print("VALUES")
    # stmts = []
    # for i, row in df.iterrows():
    #     ys = wp(row["YearStr"])
    #     sd = wp(row["StartDate"])
    #     cy = wp(row["ChampYear"])
    #     sp = wp(row["SeasonPlayed"])
    #     cm = wp(row["Comments"])
    #     cy = cy if (pd.isna(cy) or (str(cy).lower() == "null")) else int(cy)
    #     stmts.append(f"({ys}, {sd}, {cy}, {sp}, {cm})")
    #
    # print(",\n".join(stmts))


    ####################################################################################################################
    ####################################################################################################################

    df = pd.read_excel(
        r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions.xlsx",
        sheet_name="DataRegularSeason20242025",
        skiprows=1
    )
    print(df)
    print(df.columns)
    sel_cols = [col for col in df.columns if "unnamed: " not in str(col).lower()]
    print(df[sel_cols])


    # print(f"INSERT INTO [NHLdb].[dbo].[LeagueYears] ([YearStr], [StartDate], [ChampYear], [SeasonPlayed], [Comments])")
    # print("VALUES")
    # stmts = []
    # for i, row in df.iterrows():
    #     ys = wp(row["YearStr"])
    #     sd = wp(row["StartDate"])
    #     cy = wp(row["ChampYear"])
    #     sp = wp(row["SeasonPlayed"])
    #     cm = wp(row["Comments"])
    #     cy = cy if (pd.isna(cy) or (str(cy).lower() == "null")) else int(cy)
    #     stmts.append(f"({ys}, {sd}, {cy}, {sp}, {cm})")
    #
    # print(",\n".join(stmts))