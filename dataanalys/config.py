"""
Configuration for the yearly analysis report.

Update the values in this file to match your own data sources,
column names, filter values, report text, and analysis period.

This file is intended to be safe to publish as an example configuration.
Do not add sensitive file paths, internal report names, personal names,
or confidential column names before publishing publicly.
"""

from pathlib import Path


# -----------------------------------------------------------------------------
# File paths
# -----------------------------------------------------------------------------
# Replace these paths with your own local or project-relative paths.
# For public repositories, keep these generic and document how users should
# provide their own files.

CARE_DAYS_INPUT_FILE: Path = Path("data/input/care_days.xlsx")
CONTACTS_INPUT_FILE: Path = Path("data/input/contacts.xlsx")

REPORT_OUTPUT_FILE: Path = Path("data/output/yearly_report.txt")
LOG_FILE: Path = Path("data/logs/debug.log")


# -----------------------------------------------------------------------------
# Column names
# -----------------------------------------------------------------------------
# Replace these values with the column names used in your own Excel files.

COLUMN_GROUP: str = "Group"
COLUMN_YEAR: str = "Year"
COLUMN_CARE_DAYS: str = "CareDays"

COLUMN_CONTACTS: str = "Contacts"
COLUMN_CONTACT_DATE: str = "ContactDate"
COLUMN_CONTACT_STATUS: str = "ContactStatus"


# -----------------------------------------------------------------------------
# Filter values
# -----------------------------------------------------------------------------
# Replace this with the value that identifies the rows you want to include.

CONTACT_STATUS_INCLUDED_VALUE: str = "Included"


# -----------------------------------------------------------------------------
# Report metadata
# -----------------------------------------------------------------------------

REPORT_TITLE: str = "Yearly Care Days Analysis"

REPORT_DESCRIPTION: str = (
    "This report calculates yearly totals, averages, and improvement metrics "
    "based on configurable input data."
)

REPORT_SOURCE_NOTE: str = (
    "Data sources are configured by the user. Replace this text with a "
    "non-sensitive description of your own data sources if needed."
)


# -----------------------------------------------------------------------------
# Analysis period
# -----------------------------------------------------------------------------
# START_YEAR and END_YEAR control which years are calculated.
# BASELINE_YEAR and COMPARISON_YEAR control which years are compared.

START_YEAR: int = 2024
END_YEAR: int = 2025

BASELINE_YEAR: str = "2024"
COMPARISON_YEAR: str = "2025"


# -----------------------------------------------------------------------------
# Date handling
# -----------------------------------------------------------------------------
# If the year column in the care days file contains real dates such as
# 2024-01-01, keep CARE_DAYS_YEAR_IS_DATE = True.
#
# If the year column contains plain years such as 2024 or "2024",
# set CARE_DAYS_YEAR_IS_DATE = False.

CARE_DAYS_YEAR_IS_DATE: bool = True


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

DEBUG_MODE: bool = True
