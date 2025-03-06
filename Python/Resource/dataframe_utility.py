import datetime
import random
from typing import Optional, Any

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
    Date...........2025-03-05
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
        empty_freq: float | dict[str: float] | list[float] = 0,
        defaults: Optional[dict[str: Any]] = None,
        **kwargs
) -> pd.DataFrame:
    """
    Generate random data for a DataFrame.
    Param 'defaults' will take precedence over ALL kwargs params.
    :param n_rows: Number of rows
    :param n_columns: Number of columns, or a list of column names, or a dict of columns and data types.
    :param dtypes: A tuple of primitive datatypes that will constrain the random data's data type.
    :param empty_freq: The frequency of None values in the result DataFrame.
    :param defaults: A dictionary of string column names and the availble options when choosing a cell value. Can be a single value or a list of options. 
    :param kwargs: Optional params to constrain the random data even more:
            min_random_int -- default: -5
            max_random_int -- default: 5
            min_random_float -- default: -5
            max_random_float -- default: 5
            min_random_date -- default: 100 days ago
            max_random_date -- default: 100 days from now
            min_len_random_str -- default: 1
            max_len_random_str -- default: 5
            min_sub_list_len -- default: 0
            max_sub_list_len -- default: 3
            match_sub_list_lens -- default: False
            match_sub_list_dtypes -- default: False
    :return: pandas Dataframe
    """
    min_random_int = kwargs.get("min_random_int", -5)
    max_random_int = kwargs.get("max_random_int", 5)
    min_random_float = kwargs.get("min_random_float", -5)
    max_random_float = kwargs.get("max_random_float", 5)
    min_random_date = kwargs.get("min_random_date", datetime.datetime.now().date() + datetime.timedelta(days=-100))
    max_random_date = kwargs.get("max_random_date", datetime.datetime.now().date() + datetime.timedelta(days=100))
    min_len_random_str = kwargs.get("min_len_random_str", 1)
    max_len_random_str = kwargs.get("max_len_random_str", 5)
    min_sub_list_len = kwargs.get("min_sub_list_len", 0)
    max_sub_list_len = kwargs.get("max_sub_list_len", 3)
    match_sub_list_lens = kwargs.get("match_sub_list_lens", False)
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
        "min_sub_list_len",
        "max_sub_list_len",
        "match_sub_list_lens",
        "match_sub_list_dtypes"
    ]
    for kw in list_kwargs:
        if kw in kwargs:
            kwargs.pop(kw)
    if kwargs:
        raise ValueError(f"Unexpected kwargs leftover: {kwargs=}")
    
    if (n_rows < 0) or (not isinstance(n_rows, int)):
        raise ValueError(f"'n_rows' must be an int greater than 0, got {n_rows=}, {type(n_rows)=}")
    if (not isinstance(n_columns, (list, dict, int))) or (isinstance(n_columns, int) and (n_columns < 0)):
        raise ValueError(f"'n_columns' must be an int greater than 0, or a list of strings, or a dictionary of string column names paired with the expeceted column's data type. Got {n_columns=}, {type(n_columns)=}")        
    if (not isinstance(empty_freq, (list, dict, float, int))) or (isinstance(empty_freq, (float, int)) and (not (0 <= empty_freq <= 1))) or (isinstance(empty_freq, list) and [ef for ef in empty_freq if not 0 <= ef <= 1]) or (isinstance(empty_freq, dict) and [ef for ef in empty_freq.values() if not 0 < ef < 1]):
        raise ValueError(f"'empty_freq' must be a float, or a list of floats, or a dictionary of string column names paired with floats, representing the 'empty_freq' (0 <= EF <= 1) for that column. Got {empty_freq=}, {type(empty_freq)=}")
    if (defaults is not None) and (not isinstance(defaults, dict)):
        raise ValueError(f"'defaults' must be None, or an instance of a dictionary. Got {defaults=}, {type(defaults)=}")
    
    if not isinstance(min_random_int, int):
        raise ValueError(f"'min_random_int' must be an int, got: {min_random_int=}, {type(min_random_int)}")
    if not isinstance(max_random_int, int):
        raise ValueError(f"'max_random_int' must be an int, got: {max_random_int=}, {type(max_random_int)}")
    if not isinstance(min_random_float, (float, int)):
        raise ValueError(f"'min_random_float' must be an float, got: {min_random_float=}, {type(min_random_float)}")
    if not isinstance(max_random_float, (float, int)):
        raise ValueError(f"'max_random_float' must be an float, got: {max_random_float=}, {type(max_random_float)}")
    if not isinstance(min_random_date, (datetime.datetime, datetime.date, pd.Timestamp)):
        raise ValueError(f"'min_random_date' must be an datetime.datetime, datetime.date, or pd.Timestamp, got: {min_random_date=}, {type(min_random_date)}")
    if not isinstance(max_random_date, (datetime.datetime, datetime.date, pd.Timestamp)):
        raise ValueError(f"'max_random_date' must be an datetime.datetime, datetime.date, or pd.Timestamp, got: {max_random_date=}, {type(max_random_date)}")
    if not isinstance(min_len_random_str, int):
        raise ValueError(f"'min_len_random_str' must be an int, got: {min_len_random_str=}, {type(min_len_random_str)}")
    if not isinstance(max_len_random_str, int):
        raise ValueError(f"'max_len_random_str' must be an int, got: {max_len_random_str=}, {type(max_len_random_str)}")
    if not isinstance(min_sub_list_len, int):
        raise ValueError(f"'min_sub_list_len' must be an int, got: {min_sub_list_len=}, {type(min_sub_list_len)}")
    if not isinstance(max_sub_list_len, int):
        raise ValueError(f"'max_sub_list_len' must be an int, got: {max_sub_list_len=}, {type(max_sub_list_len)}")
    if not isinstance(match_sub_list_lens, bool):
        raise ValueError(f"'match_sub_list_lens' must be an bool, got: {match_sub_list_lens=}, {type(match_sub_list_lens)}")
    if not isinstance(match_sub_list_dtypes, bool):
        raise ValueError(f"'match_sub_list_dtypes' must be an bool, got: {match_sub_list_dtypes=}, {type(match_sub_list_dtypes)}")
    
    min_random_int, max_random_int = utility.minmax(min_random_int, max_random_int)
    min_random_float, max_random_float = utility.minmax(min_random_float, max_random_float)
    min_random_date, max_random_date = utility.minmax(min_random_date, max_random_date)
    min_len_random_str, max_len_random_str = utility.minmax(min_len_random_str, max_len_random_str)
    min_sub_list_len, max_sub_list_len = utility.minmax(min_sub_list_len, max_sub_list_len)

    n_c = 5 if n_columns is None else n_columns
    n_c = len(n_c) if isinstance(n_c, (list, dict)) else n_c
    valid_cols = excel_column_name(n_c - 1)
    cn = valid_cols
    if isinstance(n_columns, (list, dict)) and all(n_columns) and (len(n_columns) == n_c):
        cn = list(n_columns)
    
    if isinstance(empty_freq, list) and (len(empty_freq) < n_c):
        raise ValueError(f"when passing a list for param 'empty_freq', it's length must be at least as long as the number of columns that will be created. (len(empty_freq) < len(n_columns)).")

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
    
    defaults = {} if defaults is None else defaults
    # defaults = {k: random.choice(v) if isinstance(v, list) else v for k, v in defaults.items()}
    defaults = {k: (lambda v_=v: random.choice(v_)) if isinstance(v, list) else v for k, v in defaults.items()}

    cn_dt = list(n_columns.values()) if isinstance(n_columns, dict) else [random.choice(dt) for _ in cn]
    matching_cn_dt = random.choice(dt2)
    matching_sub_len = random.randint(min_sub_list_len, max_sub_list_len)
    # lens_sub = [matching_sub_len if match_sub_list_lens else random.randint(min_sub_list_len, max_sub_list_len) for i in range(max_sub_list_len + 1)]
    cn_dt_sub = [matching_cn_dt if match_sub_list_dtypes else random.choice(dt2) for i in range(max_sub_list_len + 1)]
    cn_ef = [empty_freq.get(col, 0) if isinstance(empty_freq, dict) else (empty_freq[i] if isinstance(empty_freq, list) else empty_freq) for i, col in enumerate(cn)]
    cn_ef_sub = [[empty_freq.get(col, 0) if isinstance(empty_freq, dict) else (empty_freq[i] if isinstance(empty_freq, list) else empty_freq) for j in range(max_sub_list_len + 1)] for i, col in enumerate(cn)]

    # print(f"{cn=}")
    # print(f"{dt=}")
    # print(f"{cn_dt=}")
    # print(f"{cn_dt_sub=}")
    # print(f"{cn_ef=}")
    # print(f"{matching_cn_dt=}")
    # print(f"{matching_sub_len=}")

    def get_random(dtype: Optional[str] = None, col_num: int = 0, nested: bool = False):
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
            return [(defaults.get(cn[col_num])()) if callable(defaults.get(cn[col_num])) else defaults.get(cn[col_num], (get_random(cn_dt_sub[i], col_num=col_num, nested=True) if random.random() > cn_ef_sub[col_num][i] else None)) for i in range(matching_sub_len if match_sub_list_lens else random.randint(min_sub_list_len, max_sub_list_len))]
        elif nested and (dtype == "list"):
            raise ValueError("Cannot nest lists. Ensure that at least one other dtype is available to create random data with")
        if dtype == "int":
            return random.randint(min_random_int, max_random_int)
        return (defaults.get(cn[col_num])()) if callable(defaults.get(cn[col_num])) else defaults.get(cn[col_num], get_random(random.choice(dt) if dtype is None else dtype, col_num=col_num))

    data = [
        dict(zip(cn, [(defaults.get(cn[j])()) if callable(defaults.get(cn[j])) else defaults.get(cn[j], get_random(cn_dt[j], col_num=j) if random.random() > cn_ef[j] else None) for j in range(len(cn))]))
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
    print(random_df(10, 6, min_sub_list_len=4, max_sub_list_len=5, match_sub_list_lens=False))
    print(random_df(10, 6, min_sub_list_len=0, max_sub_list_len=0, match_sub_list_lens=False))
    print(random_df(1, 1))

    print(random_df(3, 3, **{
        "min_random_int": -8,
        "max_random_int": -1,
        "min_random_float": 100,
        "max_random_float": -2,
        "min_random_date": datetime.datetime(2021,1,1),
        "max_random_date": datetime.datetime(2027,12,31,23,59,59),
        "min_len_random_str": -3,
        "max_len_random_str": 7,
        "min_sub_list_len": 14,
        "max_sub_list_len": 6,
        "match_sub_list_lens": False,
        "match_sub_list_dtypes": True
    }))

    print(random_df(
        3,
        3,
        empty_freq=0.3,
        **{
        "min_random_int": -8,
        "max_random_int": -1,
        "min_random_float": 100,
        "max_random_float": -2,
        "min_random_date": datetime.datetime(2021,1,1),
        "max_random_date": datetime.datetime(2027,12,31,23,59,59),
        "min_len_random_str": -3,
        "max_len_random_str": 7,
        "min_sub_list_len": 14,
        "max_sub_list_len": 6,
        "match_sub_list_lens": False,
        "match_sub_list_dtypes": True
    }))

    print(random_df(
        10,
        3,
        empty_freq=[0, 0.98, 1],
        **{
        "min_random_int": -8,
        "max_random_int": -1,
        "min_random_float": 100,
        "max_random_float": -2,
        "min_random_date": datetime.datetime(2021,1,1),
        "max_random_date": datetime.datetime(2027,12,31,23,59,59),
        "min_len_random_str": -3,
        "max_len_random_str": 7,
        "min_sub_list_len": 14,
        "max_sub_list_len": 6,
        "match_sub_list_lens": False,
        "match_sub_list_dtypes": True
    }))

    print(random_df(
        10,
        3,
        defaults={"A":[-1, -3, -5, -7, -9, -11],"B":4,"C":6,"D":8,"E":10},
        **{
        "min_random_int": -8,
        "max_random_int": -1,
        "min_random_float": 100,
        "max_random_float": -2,
        "min_random_date": datetime.datetime(2021,1,1),
        "max_random_date": datetime.datetime(2027,12,31,23,59,59),
        "min_len_random_str": -3,
        "max_len_random_str": 7,
        "min_sub_list_len": 14,
        "max_sub_list_len": 6,
        "match_sub_list_lens": False,
        "match_sub_list_dtypes": True
    }))

    print(random_df(
        10,
        n_columns={"Name": "str", "Cust": "int", "CustType": "str", "Active": "bool"},
        defaults={"CustType":["A", "B", "C"], "Active":1},
        **{
        "min_random_int": 16,
        "max_random_int": 1,
        "min_random_float": 100,
        "max_random_float": -2,
        "min_random_date": datetime.datetime(2021,1,1),
        "max_random_date": datetime.datetime(2027,12,31,23,59,59),
        "min_len_random_str": 3,
        "max_len_random_str": 7,
        "min_sub_list_len": 14,
        "max_sub_list_len": 6,
        "match_sub_list_lens": False,
        "match_sub_list_dtypes": True
    }))