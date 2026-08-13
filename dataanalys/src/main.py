"""
Example script for yearly KPI analysis.

Workflow:

1. Load source data.
2. Calculate yearly statistics.
3. Compare years.
4. Generate a report.
5. Write report and logs.
"""

from dataclasses import dataclass
from io import StringIO
from pathlib import Path
import logging
import warnings

import pandas as pd
from tabulate import tabulate

from config import (
    INPUT_FILE_1,
    INPUT_FILE_2,
    REPORT_FILE,
    LOG_FILE,
    COL_YEAR,
    COL_METRIC_1,
    COL_METRIC_2,
    COL_FLAG,
    COL_DATE,
    FLAG_VALUE,
    REPORT_TITLE,
    REPORT_SOURCE_INFORMATION,
    START_YEAR,
    END_YEAR,
    BASELINE_YEAR,
    COMPARISON_YEAR,
    DEBUG_MODE,
)

warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style",
)


def configure_logger() -> logging.Logger:
    """
    Configure application logging.

    Returns:
        Configured logger instance.
    """

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger(__name__)

    logger.setLevel(
        logging.DEBUG if DEBUG_MODE else logging.INFO
    )

    logger.handlers.clear()

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | "
        "%(funcName)s | %(message)s"
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
    Statistics for one year.

    Attributes:
        metric_1:
            First calculated metric.

        metric_2:
            Second calculated metric.

        average:
            Calculated average value.
    """

    metric_1: int
    metric_2: int
    average: float


def load_dataframe(path: Path) -> pd.DataFrame:
    """
    Load an Excel file into a DataFrame.

    Args:
        path:
            Path to Excel file.

    Returns:
        Loaded DataFrame.
    """
    return pd.read_excel(path)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load source datasets.

    Returns:
        Two pandas DataFrames.
    """

    logger.info("Loading data")

    return (
        load_dataframe(INPUT_FILE_1),
        load_dataframe(INPUT_FILE_2),
    )


def create_year_periods(
    start_year: int,
    end_year: int,
) -> list[tuple[str, str, str]]:
    """
    Generate yearly periods.

    Args:
        start_year:
            First year.

        end_year:
            Last year.

    Returns:
        List of yearly date ranges.
    """

    return [
        (
            str(year),
            f"{year}-01-01",
            f"{year}-12-31",
        )
        for year in range(
            start_year,
            end_year + 1,
        )
    ]


def calculate_metric_1(
    df: pd.DataFrame,
    year: str,
) -> int:
    """
    Calculate metric 1 for a year.
    """

    year_date = pd.Timestamp(
        year=int(year),
        month=1,
        day=1,
    )

    return int(
        df.loc[
            df[COL_YEAR] == year_date,
            COL_METRIC_1,
        ].sum()
    )


def calculate_metric_2(
    df: pd.DataFrame,
    start_date: str,
    end_date: str,
) -> int:
    """
    Calculate metric 2 for a date interval.
    """

    filtered = df.loc[
        (df[COL_FLAG] == FLAG_VALUE)
        & (df[COL_DATE] >= start_date)
        & (df[COL_DATE] <= end_date)
    ]

    return int(filtered[COL_METRIC_2].sum())


def calculate_year_result(
    year: str,
    start_date: str,
    end_date: str,
    df_1: pd.DataFrame,
    df_2: pd.DataFrame,
) -> YearResult:
    """
    Calculate annual statistics.
    """

    metric_1 = calculate_metric_1(
        df_1,
        year,
    )

    metric_2 = calculate_metric_2(
        df_2,
        start_date,
        end_date,
    )

    average = metric_1 / metric_2 if metric_2 else 0

    return YearResult(
        metric_1=metric_1,
        metric_2=metric_2,
        average=average,
    )


def calculate_improvement(
    baseline: YearResult,
    comparison: YearResult,
) -> dict[str, float]:
    """
    Calculate improvement between two years.
    """

    difference = (
        baseline.average -
        comparison.average
    )

    improvement_percent = (
        difference /
        baseline.average *
        100
    )

    return {
        "difference": difference,
        "improvement_percent": improvement_percent,
    }


def build_report(
    results: dict[str, YearResult],
) -> str:
    """
    Build a text report.

    Returns:
        Complete report text.
    """

    report = StringIO()

    headers = [
        "Year",
        "Metric 1",
        "Metric 2",
        "Average",
    ]

    table = [
        [
            year,
            result.metric_1,
            result.metric_2,
            round(result.average, 2),
        ]
        for year, result in results.items()
    ]

    report.write(
        f"{REPORT_TITLE}\n\n"
    )

    report.write(
        tabulate(
            table,
            headers=headers,
            tablefmt="github",
        )
    )

    report.write("\n\n")

    improvement = calculate_improvement(
        results[BASELINE_YEAR],
        results[COMPARISON_YEAR],
    )

    report.write(
        f"Difference: "
        f"{improvement['difference']:.2f}\n"
    )

    report.write(
        f"Improvement: "
        f"{improvement['improvement_percent']:.2f}%\n"
    )

    report.write(
        f"\n{REPORT_SOURCE_INFORMATION}"
    )

    return report.getvalue()


def write_report(
    report: str,
    output_file: Path,
) -> None:
    """
    Write report to disk.
    """

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_text(
        report,
        encoding="utf-8",
    )


def main() -> None:
    """
    Execute application workflow.
    """

    logger.info("Starting application")

    df_1, df_2 = load_data()

    periods = create_year_periods(
        START_YEAR,
        END_YEAR,
    )

    results: dict[str, YearResult] = {}

    for year, start_date, end_date in periods:
        results[year] = calculate_year_result(
            year,
            start_date,
            end_date,
            df_1,
            df_2,
        )

    report = build_report(results)

    write_report(
        report,
        REPORT_FILE,
    )

    logger.info("Finished application")


if __name__ == "__main__":
    main()
