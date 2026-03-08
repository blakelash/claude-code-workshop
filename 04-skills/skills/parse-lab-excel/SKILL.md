---
name: parse-lab-excel
description: Parse messy lab Excel files (merged cells, multi-row headers, metadata in margins) into clean, standardized CSV format.
---

# Skill: Parse Lab Excel Files

## Context

Lab instruments and collaborators often provide data in messy Excel files with merged cells, multiple header rows, metadata in random locations, and inconsistent formatting. This skill standardizes the parsing of these files into clean CSV format.

## Inputs

- **Excel file path**: Path to the .xlsx file
- **Sheet name or index**: Which sheet to parse (default: first sheet)
- **Output path**: Where to save the cleaned CSV

## Procedure

### Step 1 — Inspect the file

1. Open the Excel file and list all sheet names
2. Read the target sheet WITHOUT parsing (raw read with `header=None`)
3. Display the first 20 rows to identify:
   - Where the actual data headers are (might not be row 0)
   - Whether there are merged cells or multi-row headers
   - Where the data actually starts
   - Whether there's metadata in the margins (instrument name, date, operator)
4. Report findings and proposed parsing strategy to the user

**Stop and ask if:** the structure is ambiguous or there are multiple possible interpretations.

### Step 2 — Extract metadata

1. Pull out any metadata found above/beside the data table:
   - Instrument name, date, operator, experiment ID
2. Save metadata as a comment block at the top of the output or as a separate `_metadata.json` file

### Step 3 — Parse the data table

1. Re-read the sheet with the correct `header` row and `skiprows`
2. Clean column names: strip whitespace, lowercase, replace spaces with underscores
3. Remove completely empty rows and columns
4. Convert data types appropriately (numbers as float/int, dates as datetime)
5. Handle merged cells by forward-filling

### Step 4 — Validate

1. Check for:
   - Duplicate column names (append suffix if found)
   - Columns that are entirely empty
   - Unexpected data types (e.g., text in a numeric column)
2. Report any issues found

### Step 5 — Save

1. Save cleaned data to output path as CSV
2. Print summary: number of rows, columns, any transformations applied

## Failure modes

| Issue | What to do |
|-------|-----------|
| File is .xls (old format) | Use `engine='xlrd'` |
| Password-protected | Stop, ask user |
| Multiple data tables on one sheet | Stop, ask user which table to extract |
| Encoding issues | Try UTF-8, then Latin-1, then report |

## Reference files

These are in the same directory as this skill — read them if needed:

- `column_name_mappings.json` — standard column renames for common instrument outputs (e.g., "Absorbance @ 260nm" → "abs_260")
- `expected_output.csv` — example of what a correctly parsed CSV should look like

## Dependencies

```python
import pandas as pd
import openpyxl
import json
```
