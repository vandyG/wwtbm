"""Module to fetch imput data."""

from pathlib import Path

import pandas as pd


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
    with open(trigger_path, "w"):
        pass

    while True:
        if not Path(trigger_path).exists():
            print("Reading Excel file...")
            return pd.read_excel(file_path, sheet_name=sheet)


def main():
    """Entry point."""
    from os import environ

    file_path = environ["ANSWERS_FILE"]
    trigger_path = environ["TRIGGER_FILE"]
    sheet = environ["ANSWER_SHEET"]

    df = get_answers_power_automate_hook(
        file_path=file_path,
        sheet=sheet,
        trigger_path=trigger_path,
    )

    print(df.tail(10))


if __name__ == "__main__":
    main()
