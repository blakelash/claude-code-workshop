# Example: Running the Parse Lab Excel Skill

## Prompt

```
Parse the plate reader output in data/raw/plate_reader_2025-03-01.xlsx
- Use the "Results" sheet
- Save cleaned data to data/processed/plate_reader_cleaned.csv
```

## What Claude does

1. Opens the Excel file, lists all sheets
2. Reads raw data from "Results" sheet, shows first 20 rows
3. Identifies header row (often row 3-5 in instrument output), metadata block, and data range
4. Extracts metadata, cleans column names, parses data
5. Validates and saves clean CSV
