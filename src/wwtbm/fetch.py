"""Module to fetch imput data."""

from pathlib import Path

import pandas as pd


def read_excel_file(file_path: Path, sheet: str) -> pd.DataFrame:
    """Read Excel file and return DataFrame.

    Args:
        file_path (Path): Input file path.
        sheet (str): Sheet name.

    Returns:
        pd.DataFrame: Input df.
    """
    return pd.read_excel(file_path, sheet_name=sheet)


def get_answers_power_automate_hook(file_path: Path, sheet: str, trigger_path: Path) -> pd.DataFrame:
    """Fetches data from input excel.

    Creates a trigger for Power Automate Desktop. PWD uses this trigger to sync
    the input excel with the web.

    Note:
        See the data directory of the repository for template flows.

    Args:
        file_path (Path): Path to input file.
        sheet (str): Worksheet name.
        trigger_path (Path): Trigger path for power automate.

    Returns:
        DataFrame: Input excel file as pandas DataFrame.
    """
    # with open(trigger_path, "w"):
    #     pass

    while True:
        if not Path(trigger_path).exists():
            print("Reading Excel file...")
            return read_excel_file(file_path, sheet=sheet)

def filter_first_occurrence(df):
    """
    Returns a DataFrame that contains only the first occurrence of each (ID, Name, Question).

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: A filtered DataFrame with only the first occurrence of each (ID, Name, Question).
    """
    # Print column names for debugging
    print("Columns in DataFrame:", df.columns.tolist())

    # Ensure required columns exist
    required_columns = {"ID", "Name", "Question", "Answer", "Correct"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns in DataFrame: {missing_columns}")

    # Get only the first occurrence of each (ID, Name, Question)
    filtered_df = df.groupby(["ID", "Name", "Question"]).first().reset_index()

    return filtered_df

    
def get_answer_data():
 
    from os import environ

    file_path = Path(environ["ANSWERS_FILE"])
    trigger_path = Path(environ["TRIGGER_FILE"])
    answer_sheet = environ["ANSWER_SHEET"]

    df_answer_unfiltered = get_answers_power_automate_hook(
        file_path=file_path,
        sheet=answer_sheet,
        trigger_path=trigger_path,
    )

    df_answer = filter_first_occurrence(df_answer_unfiltered)
    
    return df_answer

def main():

    df_answer = get_answer_data()    
    return df_answer

if __name__ == "__main__":
    main()
    
    