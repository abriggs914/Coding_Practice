import datetime
import random
from typing import Optional

import numpy as np
import pandas as pd

import utility
from utility import excel_column_name

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


VERSION = \
    """	
    General Utility file for Dataframe operations
    Version..............1.02
    Date...........2025-03-04
    Author(s)....Avery Briggs
    """


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


def is_date_dtype(df, col_name):
    """
    Check if the data type of a column in a Pandas DataFrame is a date or time data type.
    Args:
        df (pandas.DataFrame): The DataFrame containing the column to check.
        col_name (str): The name of the column to check.
    Returns:
        bool: True if the column data type is a date or time data type, False otherwise.
    """
    dtype = df.dtypes[col_name]
    return np.issubdtype(dtype, np.datetime64) or np.issubdtype(dtype, np.timedelta64)


def is_numeric_dtype(df, col_name):
    """
    Check if the values in a column of a Pandas DataFrame are numerical.
    Args:
        df (pandas.DataFrame): The DataFrame containing the column to check.
        col_name (str): The name of the column to check.
    Returns:
        bool: True if the values in the column are numerical, False otherwise.
    """
    dtype = df.dtypes[col_name]
    return np.issubdtype(dtype, np.number)


def random_df(
        n_rows: int = 5,
        n_columns: Optional[list[str] | dict[str: str] | int] = None,
        dtypes: tuple[str] | str = ('int', 'float', 'str', 'datetime', 'bool', 'list'),
        **kwargs
) -> pd.DataFrame:
    """
    Generate random data for a DataFrame.
    :param n_rows: Number of rows
    :param n_columns: Number of columns, or a list of column names, or a dict of columns and data types.
    :param dtypes: A tuple of primitive datatypes that will constrain the random data's data type.
    :param kwargs: Optional params to constrain the random data even more:
            min_random_int -- default: -5
            max_random_int -- default: 5
            min_random_float -- default: -5
            max_random_float -- default: 5
            min_random_date -- default: 100 days ago
            max_random_date -- default: 100 days from now
            min_len_random_str -- default: 0
            max_len_random_str -- default: 5
            max_sub_list_len -- default: 3
            match_sub_list_dtypes -- default: False
    :return: pandas Dataframe
    """
    min_random_int = kwargs.get("min_random_int", -5)
    max_random_int = kwargs.get("max_random_int", 5)
    min_random_float = kwargs.get("min_random_float", -5)
    max_random_float = kwargs.get("max_random_float", 5)
    min_random_date = kwargs.get("min_random_date", datetime.datetime.now().date() + datetime.timedelta(days=-100))
    max_random_date = kwargs.get("max_random_date", datetime.datetime.now().date() + datetime.timedelta(days=100))
    min_len_random_str = kwargs.get("min_len_random_str", 0)
    max_len_random_str = kwargs.get("max_len_random_str", 5)
    max_sub_list_len = kwargs.get("max_sub_list_len", 3)
    match_sub_list_dtypes = kwargs.get("match_sub_list_dtypes", False)
    list_kwargs = [
        "min_random_int",
        "max_random_int",
        "min_random_float",
        "max_random_float",
        "min_random_date",
        "max_random_date",
        "min_len_random_str",
        "max_len_random_str",
        "max_sub_list_len",
        "match_sub_list_dtypes"
    ]
    for kw in list_kwargs:
        if kw in kwargs:
            kwargs.pop(kw)
    if kwargs:
        raise ValueError(f"Unexpected kwargs leftover: {kwargs=}")

    n_c = 5 if n_columns is None else n_columns
    n_c = len(n_c) if isinstance(n_c, (list, dict)) else n_c
    valid_cols = excel_column_name(n_c - 1)
    cn = valid_cols
    if isinstance(n_columns, (list, dict)) and all(n_columns) and (len(n_columns) == n_c):
        cn = list(n_columns)

    if not isinstance(dtypes, (list, tuple)):
        dtypes = [dtypes]

    if isinstance(n_columns, dict):
        dtypes = [d_t for d_t in dtypes if d_t in n_columns.values()]
    valid_dtypes = ('int', 'float', 'str', 'datetime', 'bool', 'list')
    valid_dtypes2 = ('int', 'float', 'str', 'datetime', 'bool')
    dt = [d_t for d_t in dtypes if d_t in valid_dtypes]
    dt2 = [d_t for d_t in dtypes if d_t in valid_dtypes2]
    if not dt:
        dt = valid_dtypes
    if not dt2:
        dt2 = valid_dtypes2
        if (len(dt) == 1) and (dt[0] == "list"):
            dt = valid_dtypes

    cn_dt = list(n_columns.values()) if isinstance(n_columns, dict) else [random.choice(dt) for _ in cn]
    matching_cn_dt = random.choice(dt2)
    cn_dt_sub = [matching_cn_dt if match_sub_list_dtypes else random.choice(dt2) for i in range(max_sub_list_len)]

    # print(f"{cn=}")
    # print(f"{dt=}")
    # print(f"{cn_dt=}")
    # print(f"{cn_dt_sub=}")
    # print(f"{matching_cn_dt=}")

    def get_random(dtype: Optional[str] = None, nested: bool = False):
        # print(f"{dtype=}, {nested=}")
        if dtype == "bool":
            return random.choice([True, False])
        if dtype == "float":
            return utility.random_in_range(min_random_float, max_random_float)
        if dtype == "datetime":
            return min_random_date + datetime.timedelta(days=random.randint(0, (max_random_date - min_random_date).days))
        if dtype == "str":
            return "".join([chr(random.randint(ord("A"), ord("Z"))) for i in range(random.randint(max(0, min_len_random_str), max_len_random_str))])
        if not nested and (dtype == "list"):
            return [get_random(cn_dt_sub[i], nested=True) for i in range(max_sub_list_len)]
        elif nested and (dtype == "list"):
            raise ValueError("Cannot nest lists. Ensure that at least one other dtype is available to create random data with")
        if dtype == "int":
            return random.randint(min_random_int, max_random_int)
        return get_random(random.choice(dt) if dtype is None else dtype)

    data = [
        dict(zip(cn, [get_random(cn_dt[j]) for j in range(len(cn))]))
        for i in range(n_rows)
    ]
    return pd.DataFrame(data)


if __name__ == '__main__':

    df = random_df(5, 3, match_sub_list_dtypes=True, dtypes=("list", "int"))
    print(df)
    print(random_df(n_columns=["Name", "Date", "Price", "Cust"]))
    print(random_df(n_columns={"Name": "str", "Date": "datetime", "Price": "float", "Cust": "list"}, min_len_random_str=4, max_len_random_str=4))
    print(random_df(n_columns={"Name": "str", "Date": "datetime", "Price": "float", "Cust": "list", "US": "bool"}, min_len_random_str=4, max_len_random_str=4))
    print(random_df(n_columns={"Name": "list", "Cust": "list"}, max_sub_list_len=6))
    print(random_df(10, 6, dtypes="bool"))
