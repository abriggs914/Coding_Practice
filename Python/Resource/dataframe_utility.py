import datetime
import numpy as np
import pandas as pd


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


VERSION = \
    """	
    General Utility file for Dataframe operations
    Version..............1.01
    Date...........2023-03-20
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