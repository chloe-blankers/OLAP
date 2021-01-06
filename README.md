# OLAP
This program allows you to create queries in Python to calculate the minimum, maximum, mean, sum, and count of numeric columns on a data set and perform group-by along with top-k for categorical columns.

### Aggregates

--top <k> <categorical-field-name>
compute the ​top k ​most common values of categorical-field-name
a string listing the top values with their counts, in descending order, e.g. “red: 456, green: 345, blue: 234”
If the values contain double quote or newline characters, they should be escaped using the usual printf syntax, e.g. “\n” for newlines, \” for double quotes
--min <numeric-field-name>
compute the ​minimum​value of numeric-field-name
a floating point number, or “NaN” if there were no numeric values in the column
--max <numeric-field-name>
compute the ​maximum​value of numeric-field-name
a floating point number, or “NaN” if there were no numeric values in the column
--mean <numeric-field-name>
compute the ​mean​(average) of numeric-field-name
a floating point number, or “NaN” if there were no numeric values in the column
--sum <numeric-field-name>
compute the ​sum​of numeric-field-name
a floating point number, or “NaN” if there were no numeric values in the column
--count count​the number of records
Group By
Add optional named argument for a ​group-by --group-by categorical-field-name
an integer, or zero if there were no records

### Example Input File

Sector,Ticker,Date,Open,High,Low,Close,Volume,OpenInt
Technology,intc,6/20/72,0.01592,0.01592,0.01592,0.01592,7878523,0
Financial Services,axp,6/21/72,1.4866,1.4957,1.4866,1.4866,1057078,0
Consumer Cyclical,dis,6/21/72,1.506,1.5244,1.506,1.5151,1220068,0
Technology,ibm,6/21/72,16.501,16.658,16.484,16.524,579628,0
Technology,intc,6/21/72,0.01592,0.01592,0.01592,0.01592,16363089,0
Financial Services,axp,6/22/72,1.514,1.5228,1.514,1.514,835584,0
Technology,intc,6/20/72,0.01592,0.01592,0.01592,0.01592,7878523,0
Financial Services,axp,6/21/72,1.4866,1.4957,1.4866,1.4866,1057078,0
....

Command: `python OLAP.py --input input.csv --group-by ticker --count --min open --max open --mean open --min high --max high --mean high --min low --max low --mean close --min close --max close --mean close`
