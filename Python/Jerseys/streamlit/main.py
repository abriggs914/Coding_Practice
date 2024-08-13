import streamlit as st
import pandas as pd


if __name__ == '__main__':

    excel_dfs = pd.read_excel(
        r"D:\NHL Jerseys.xlsm",
        sheet_name=list(range(7))
    )

    excel_dfs_keys = list(excel_dfs.keys())

    df_nhl_jerseys = excel_dfs[excel_dfs_keys[0]]
    df_nike_jerseys = excel_dfs[excel_dfs_keys[1]]
    df_jersey_wishlist = excel_dfs[excel_dfs_keys[2]]
    df_jersey_reporting = excel_dfs[excel_dfs_keys[3]]
    df_nhl_teams = excel_dfs[excel_dfs_keys[4]]
    df_nhl_divisions = excel_dfs[excel_dfs_keys[5]]
    df_nhl_conferences = excel_dfs[excel_dfs_keys[6]]

    print(f"{df_nhl_jerseys}")
    print(f"{df_nike_jerseys}")
    print(f"{df_jersey_wishlist}")
    print(f"{df_jersey_reporting}")
    print(f"{df_nhl_teams}")
    print(f"{df_nhl_divisions}")
    print(f"{df_nhl_conferences}")
