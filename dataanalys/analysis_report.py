"""
Build a yearly analysis report from configurable Excel input files.

The script reads two Excel files:

1. A file containing yearly care day values.
2. A file containing contact values by date.

It then calculates:

- Total care days per year.
- Total contacts per year.
- Average care days per contact.
- Improvement between a baseline year and a comparison year.
- A text report written to disk.

All file paths, column names, filter values, report text, and analysis years
are configured in config.py.

This file is designed to be safe to publish publicly. Do not hard-code
sensitive paths, names, internal report titles, or confidential column names
in this file.
"""

from __future__ import annotations
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
import logging
import warnings
import pandas as pd
from tabulate import tabulate
import config


# Suppress openpyxl warnings that may occur when reading exported Excel files.
warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style",
)


def configure_logger() -> logging.Logger:
    """
    Configure and return the application logger.

    The logger writes:
        - DEBUG and higher messages to the log file.
        - INFO and higher messages to the console.

    Returns:
        A configured logging.Logger instance.
    """
    config.LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if config.DEBUG_MODE else logging.INFO)

    # Prevent duplicate log messages if the module is reloaded.
    logger.handlers.clear()

    file_handler = logging.FileHandler(
        config.LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | "
        "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = configure_logger()


@dataclass(frozen=True)
class YearResult:
    """
    Store calculated statistics for one year.

    Attributes:
        care_days:
            Total number of care days.
        contacts:
            Total number of contacts.
        average:
            Average number of care days per contact.
    """

    care_days: int
    contacts: int
    average: float


def load_excel_file(file_path: Path) -> pd.DataFrame:
    """
    Load an Excel file into a pandas DataFrame.

    Args:
        file_path:
            Path to the Excel file.

    Returns:
        A pandas DataFrame containing the Excel data.

    Raises:
        FileNotFoundError:
            If the file does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    logger.info("Loading Excel file: %s", file_path)

    df = pd.read_excel(file_path)

    logger.debug(
        "Loaded file=%s shape=%s columns=%s",
        file_path,
        df.shape,
        list(df.columns),
    )

    return df


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load all source data files.

    Returns:
        A tuple containing:
            - DataFrame with care day data.
            - DataFrame with contact data.
    """
    care_days_df = load_excel_file(config.CARE_DAYS_INPUT_FILE)
    contacts_df = load_excel_file(config.CONTACTS_INPUT_FILE)

    return care_days_df, contacts_df


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str],
    dataframe_name: str,
) -> None:
    """
    Validate that a DataFrame contains all required columns.

    Args:
        df:
            DataFrame to validate.
        required_columns:
            Column names that must exist in the DataFrame.
        dataframe_name:
            Human-readable name used in error messages.

    Raises:
        ValueError:
            If one or more required columns are missing.
    """
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataframe_name} is missing required columns: "
            f"{missing_columns}"
        )

    logger.debug(
        "%s contains all required columns: %s",
        dataframe_name,
        required_columns,
    )


def validate_input_data(
    care_days_df: pd.DataFrame,
    contacts_df: pd.DataFrame,
) -> None:
    """
    Validate that the input DataFrames contain required columns.

    Args:
        care_days_df:
            DataFrame with care day data.
        contacts_df:
            DataFrame with contact data.
    """
    validate_required_columns(
        df=care_days_df,
        required_columns=[
            config.COLUMN_GROUP,
            config.COLUMN_YEAR,
            config.COLUMN_CARE_DAYS,
        ],
        dataframe_name="care_days_df",
    )

    validate_required_columns(
        df=contacts_df,
        required_columns=[
            config.COLUMN_CONTACTS,
            config.COLUMN_CONTACT_DATE,
            config.COLUMN_CONTACT_STATUS,
        ],
        dataframe_name="contacts_df",
    )


def normalize_date_columns(
    care_days_df: pd.DataFrame,
    contacts_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convert configured date columns to pandas datetime.

    Args:
        care_days_df:
            DataFrame with care day data.
        contacts_df:
            DataFrame with contact data.

    Returns:
        A tuple with normalized copies of the input DataFrames.
    """
    care_days_df = care_days_df.copy()
    contacts_df = contacts_df.copy()

    if config.CARE_DAYS_YEAR_IS_DATE:
        care_days_df[config.COLUMN_YEAR] = pd.to_datetime(
            care_days_df[config.COLUMN_YEAR],
            errors="coerce",
        )

    contacts_df[config.COLUMN_CONTACT_DATE] = pd.to_datetime(
        contacts_df[config.COLUMN_CONTACT_DATE],
        errors="coerce",
    )

    logger.debug(
        "Normalized date columns. care_days_year_dtype=%s "
        "contact_date_dtype=%s",
        care_days_df[config.COLUMN_YEAR].dtype,
        contacts_df[config.COLUMN_CONTACT_DATE].dtype,
    )

    return care_days_df, contacts_df


def filter_care_days(
    df: pd.DataFrame,
    year: str,
) -> int:
    """
    Sum care days for a specific year.

    If config.CARE_DAYS_YEAR_IS_DATE is True, the configured year column is
    expected to contain datetime values such as 2024-01-01.

    If config.CARE_DAYS_YEAR_IS_DATE is False, the configured year column is
    expected to contain values such as 2024 or "2024".

    Only rows where the configured group column is not empty are included.

    Args:
        df:
            DataFrame containing care day data.
        year:
            Year to filter on, for example "2024".

    Returns:
        Total number of care days for the selected year.
    """
    valid_group_mask = (
        df[config.COLUMN_GROUP].notna()
        & (df[config.COLUMN_GROUP].astype(str).str.strip() != "")
    )

    if config.CARE_DAYS_YEAR_IS_DATE:
        year_value = pd.Timestamp(
            year=int(year),
            month=1,
            day=1,
        )
        year_mask = df[config.COLUMN_YEAR] == year_value
    else:
        year_mask = df[config.COLUMN_YEAR].astype(str) == str(year)

    care_days = int(
        df.loc[
            valid_group_mask & year_mask,
            config.COLUMN_CARE_DAYS,
        ].sum()
    )

    logger.debug(
        "Filtered care days: year=%s care_days=%s",
        year,
        care_days,
    )

    return care_days


def filter_contacts(
    df: pd.DataFrame,
    start_date: str,
    end_date: str,
) -> int:
    """
    Sum contacts within a date interval.

    Only rows where the configured contact status column equals the configured
    included value are included.

    Args:
        df:
            DataFrame containing contact data.
        start_date:
            Start date for the period, for example "2024-01-01".
        end_date:
            End date for the period, for example "2024-12-31".

    Returns:
        Total number of contacts within the selected period.
    """
    start_timestamp = pd.Timestamp(start_date)
    end_timestamp = pd.Timestamp(end_date)

    filtered = df.loc[
        (df[config.COLUMN_CONTACT_STATUS]
         == config.CONTACT_STATUS_INCLUDED_VALUE)
        & (df[config.COLUMN_CONTACT_DATE] >= start_timestamp)
        & (df[config.COLUMN_CONTACT_DATE] <= end_timestamp)
    ]

    contacts = int(filtered[config.COLUMN_CONTACTS].sum())

    logger.debug(
        "Filtered contacts: start_date=%s end_date=%s contacts=%s",
        start_date,
        end_date,
        contacts,
    )

    return contacts


def create_year_periods(
    start_year: int,
    end_year: int,
) -> list[tuple[str, str, str]]:
    """
    Create yearly date periods between two years.

    Example:
        create_year_periods(2024, 2025)

    Returns:
        [
            ("2024", "2024-01-01", "2024-12-31"),
            ("2025", "2025-01-01", "2025-12-31"),
        ]

    Args:
        start_year:
            First year to include.
        end_year:
            Last year to include.

    Returns:
        A list of tuples with year, start date, and end date.
    """
    if end_year < start_year:
        raise ValueError("end_year must be greater than or equal to start_year.")

    year_periods = [
        (
            str(year),
            f"{year}-01-01",
            f"{year}-12-31",
        )
        for year in range(start_year, end_year + 1)
    ]

    logger.debug("Created year periods=%s", year_periods)

    return year_periods


def calculate_year_result(
    year: str,
    start_date: str,
    end_date: str,
    care_days_df: pd.DataFrame,
    contacts_df: pd.DataFrame,
) -> YearResult:
    """
    Calculate yearly statistics.

    The function calculates:
        - Total care days.
        - Total contacts.
        - Average care days per contact.

    Args:
        year:
            Year to calculate, for example "2024".
        start_date:
            First date in the calculation period.
        end_date:
            Last date in the calculation period.
        care_days_df:
            DataFrame containing care day data.
        contacts_df:
            DataFrame containing contact data.

    Returns:
        A YearResult instance with calculated values.
    """
    care_days = filter_care_days(
        df=care_days_df,
        year=year,
    )

    contacts = filter_contacts(
        df=contacts_df,
        start_date=start_date,
        end_date=end_date,
    )

    average = care_days / contacts if contacts else 0.0

    logger.debug(
        "Calculated yearly result: year=%s care_days=%s contacts=%s "
        "average=%.4f",
        year,
        care_days,
        contacts,
        average,
    )

    return YearResult(
        care_days=care_days,
        contacts=contacts,
        average=round(average, 4),
    )


def calculate_improvement(
    baseline: YearResult,
    comparison: YearResult,
) -> dict[str, float | int]:
    """
    Calculate improvement metrics between two yearly results.

    The function calculates:
        - Difference in average care days per contact.
        - Improvement percentage.
        - Estimated freed care days based on average difference.
        - Actual difference in total care days.

    Args:
        baseline:
            YearResult used as the baseline year.
        comparison:
            YearResult used as the comparison year.

    Returns:
        A dictionary containing calculated improvement values.

    Raises:
        ZeroDivisionError:
            If baseline.average is zero.
    """
    logger.info("Calculating improvement")

    if baseline.average == 0:
        raise ZeroDivisionError(
            "Cannot calculate improvement percentage because "
            "baseline average is zero."
        )

    difference = baseline.average - comparison.average
    improvement_percent = difference / baseline.average * 100
    estimated_freed_days = difference * comparison.contacts
    actual_freed_days = baseline.care_days - comparison.care_days

    result = {
        "difference": difference,
        "improvement_percent": improvement_percent,
        "estimated_freed_days": estimated_freed_days,
        "actual_freed_days": actual_freed_days,
    }

    logger.debug("Improvement result=%s", result)

    return result


def build_table(
    results: dict[str, YearResult],
) -> list[list[object]]:
    """
    Build table data for the report.

    Args:
        results:
            Dictionary where keys are years and values are YearResult objects.

    Returns:
        A list of table rows used by tabulate.
    """
    table_data = []

    for year, data in results.items():
        table_data.append(
            [
                year,
                data.care_days,
                data.contacts,
                f"{data.average:.2f}",
                "CareDays / Contacts",
            ]
