"""
Application configuration.

Update this file to match your own datasets,
column names and analysis requirements.
"""

from pathlib import Path


# ============================================================================
# FILES
# ============================================================================

INPUT_FILE_1 = Path(
    "data/input/dataset_1.xlsx"
)

INPUT_FILE_2 = Path(
    "data/input/dataset_2.xlsx"
)

REPORT_FILE = Path(
    "data/output/report.txt"
)

LOG_FILE = Path(
    "data/logs/debug.log"
)


# ============================================================================
# DATASET CONFIGURATION
# ============================================================================

COL_YEAR = "Year"

COL_METRIC_1 = "Metric1"

COL_METRIC_2 = "Metric2"

COL_FLAG = "Flag"

COL_DATE = "Date"

FLAG_VALUE = "Yes"


# ============================================================================
# REPORT CONFIGURATION
# ============================================================================

REPORT_TITLE = "Annual KPI Comparison Report"

REPORT_SOURCE_INFORMATION = """
Replace this text with information about your data sources.
"""


# ============================================================================
# ANALYSIS PERIOD
# ============================================================================

START_YEAR = 2024
END_YEAR = 2025

BASELINE_YEAR = "2024"
COMPARISON_YEAR = "2025"


# ============================================================================
# LOGGING
# ============================================================================

DEBUG_MODE = True
