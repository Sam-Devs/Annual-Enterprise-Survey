# Annual Enterprise Survey

The script groups rows by `Industry_name_NZSIOC`, sums the numeric values from the `Value` column, and prints the results sorted from highest to lowest.

## Project Structure

```
─ annual-enterprise-survey-2021-financial-year-provisional-csv.csv   # CSV
─ sum_total_income.py                                                # Main script
─ requirements.txt                                                   # Dependencies
─ README.md                                                          # Documentation
```

## Requirements

- Python 3.8
- Pandas library  

Install dependencies:
```bash
pip install -r requirements.txt
```

Or simply:
```bash
pip install pandas
```

## Usage

Run the script with:

```bash
python sum_total_income.py --path ./annual-enterprise-survey-2021-financial-year-provisional-csv.csv
```

## Terminal Output

```
Total 'Total income' by Industry (sorted high -> low)

Rank  Industry                                                     Total income
-------------------------------------------------------------------------------------------
   1.  All industries                                                         757,504.00
   2.  Manufacturing                                                          117,404.00
   3.  Wholesale Trade                                                        117,396.00
   4.  Retail Trade and Accommodation                                          99,926.00
   5.  Financial and Insurance Services                                        77,676.00
   6.  Construction                                                            75,961.00
   7.  Professional, Scientific, Technical, Administrative and Support Services            58,903.00
   8.  Agriculture, Forestry and Fishing                                       48,731.00
   9.  Rental, Hiring and Real Estate Services                                 40,096.00
  10.  Transport, Postal and Warehousing                                       25,392.00
  11.  Electricity, Gas, Water and Waste Services                              24,936.00
  12.  Health Care and Social Assistance                                       22,801.00
  13.  Arts, Recreation and Other Services                                     22,640.00
  14.  Information Media and Telecommunications                                14,118.00
  15.  Education and Training                                                   5,042.00
  16.  Mining                                                                   4,687.00
  17.  Public Order, Safety and Regulatory Services                             1,796.00
```

## How It Works

1. Reads the CSV file.  
2. Cleans the `Value` column:  
   - Removes commas (`757,504 → 757504`)  
   - Handles negatives in parentheses (`(1,234) → -1234`)  
   - Converts to numeric (`float`)  
3. Filters rows where `Variable_name == "Total income"`.  
4. Groups by `Industry_name_NZSIOC` and sums `Value_num`.  
5. Prints results sorted from highest to lowest.  
