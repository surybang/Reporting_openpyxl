import pandas as pd


def write_data_to_excel(path_file: str, df: pd.DataFrame, sheet_name: str = 'DATA') -> None:
    """
    Write a DataFrame in an excel sheet (create or replace).

    Args:
        path_file (str): Path to the file.
        df (pd.DataFrame): Data.
        sheet_name (str): Name of the sheet to create or replace.
    """
    with pd.ExcelWriter(
        path_file,
        mode='a',
        engine='openpyxl',
        if_sheet_exists='replace'
    ) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
