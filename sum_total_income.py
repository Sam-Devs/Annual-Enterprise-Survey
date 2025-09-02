#!/usr/bin/env python3
"""
Task:
    Using the dataset annual-enterprise-survey-2021-financial-year-provisional-csv.csv, write a Python program that calculates the total “Total income” (Variable_name) for each Industry_name_NZSIOC. 
    Your code should group rows by industry, sum the Value column (converting it from string to numeric), and print the results sorted from highest to lowest.
"""

import argparse
import pandas as pd
import re
import sys
from typing import Optional

def value_to_float(s: Optional[str]) -> Optional[float]:
    """Convert the 'Value' string to a float.
       And handles commas (thousands separators), parentheses for negatives, and blanks.
    """
    if s is None:
        return None
    s = str(s).strip()
    if s == "" or s in {"-", ".."}:
        return None
    # Incase parentheses indicate negative numbers like "(1,234)"
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg = True
        s = s[1:-1]
    # To remove commas and whitespace
    s = re.sub(r"[,\s]", "", s)
    try:
        val = float(s)
        return -val if neg else val
    except Exception:
        return None

def main(argv=None):
    parser = argparse.ArgumentParser(description="Sum 'Total income' by industry.")
    parser.add_argument("--path", required=True, help="Path to CSV file")
    parser.add_argument("--year", type=int, default=None, help="If provided, filter to this Year (e.g. 2021)")
    parser.add_argument("--level", type=str, default=None, help="If provided, filter Industry_aggregation_NZSIOC (e.g. 'Level 1')")
    parser.add_argument("--top", type=int, default=None, help="Print top N industries (by total income)")
    parser.add_argument("--output", type=str, default=None, help="Optional CSV output path")
    parser.add_argument("--chunksize", type=int, default=0, help="Use chunked reading if file is large (rows per chunk), 0 means read all")
    args = parser.parse_args(argv)

    # Read CSV in chunks
    if args.chunksize and args.chunksize > 0:
        # chunked reading (For memory friendliness)
        reader = pd.read_csv(args.path, dtype=str, chunksize=args.chunksize)
    else:
        reader = [pd.read_csv(args.path, dtype=str)]

    agg = {}  # industry_name -> running sum

    for chunk in reader:
        # filters early (year/level)
        if args.year is not None:
            chunk = chunk[chunk["Year"].astype(str) == str(args.year)]
        if args.level is not None:
            chunk = chunk[chunk["Industry_aggregation_NZSIOC"] == args.level]

        # Filter for Total income
        chunk = chunk[chunk["Variable_name"] == "Total income"].copy()
        if chunk.empty:
            continue

        # Create numeric column
        chunk["Value_num"] = chunk["Value"].map(value_to_float)

        # Group within chunk
        grouped = chunk.groupby("Industry_name_NZSIOC")["Value_num"].sum(min_count=1)
        for industry, value in grouped.items():
            if pd.isna(value):
                continue
            agg[industry] = agg.get(industry, 0.0) + float(value)

    # Convert to list and sort
    result = sorted(agg.items(), key=lambda x: x[1], reverse=True)

    # Print
    print("\nTotal Total income by Industry (sorting high -> low)\n")
    print(f"{'Rank':>4}  {'Industry':<60} {'Total income':>20}")
    print("-" * 90)
    for i, (industry, total) in enumerate(result, start=1):
        if args.top and i > args.top:
            break
        # Formatted with thousands separators, two decimals
        print(f"{i:4d}.  {industry:<60} {total:20,.2f}")

if __name__ == "__main__":
    main()