# Yearly Statistics Report

A generic Python project for:

- Reading Excel files
- Calculating annual statistics
- Comparing multiple years
- Generating text-based reports
- Writing debug logs

The project contains no domain-specific logic and can be adapted to almost any yearly KPI analysis.

---

## Features

- Read Excel files using pandas
- Configurable column names
- Configurable file paths
- Annual calculations
- Year-over-year comparison
- Text report generation
- Debug logging

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

or on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install pandas openpyxl tabulate
```

---

## Configuration

Open:

```text
src/config.py
```

and modify:

### Input files

```python
INPUT_FILE_1
INPUT_FILE_2
```

### Output files

```python
REPORT_FILE
LOG_FILE
```

### Dataset columns

```python
COL_YEAR
COL_METRIC_1
COL_METRIC_2
COL_FLAG
COL_DATE
```

### Analysis years

```python
START_YEAR
END_YEAR

BASELINE_YEAR
COMPARISON_YEAR
```

---

## Run

```bash
python src/main.py
```

---

## Example Output

```text
Annual KPI Comparison Report

| Year | Metric 1 | Metric 2 | Average |
|------|----------|----------|---------|
| 2024 | 1000     | 500      | 2.00    |
| 2025 | 900      | 600      | 1.50    |

Difference: 0.50
Improvement: 25.00%
```

---

## Logging

Debug logs are written to:

```text
data/logs/debug.log
```

Console output shows INFO-level messages and above.

---

## Project Structure

```text
project/
│
├── README.md
├── src/
│   ├── config.py
│   └── main.py
│
├── data/
│   ├── input/
│   ├── output/
│   └── logs/
│
└── requirements.txt
```
