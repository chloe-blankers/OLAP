# OLAP
This program allows you to create queries in Python to calculate the minimum, maximum, mean, sum, and count of numeric columns on a data set of 129,046 rows and perform group-by along with top-k for categorical columns.

## Aggregates

| Argument | Description | Output Format |
|-------|-------|-------|
| --top <k> [categorical-field-name] | compute the top k most common values of categorical-field-name | a string listing the top values with their counts, in descending order, e.g. “red: 456, green: 345, blue: 234” If the values contain double quote or newline characters, they should be escaped using the usual printf syntax, e.g. “\n” for newlines, \” for double quotes |
| --min [numeric-field-name] | compute the minimum value of numeric-field-name | a floating point number, or “NaN” if there were no numeric values in the column |
| --max [numeric-field-name] | compute the maximum value of numeric-field-name | a floating point number, or “NaN” if there were no numeric values in the column |
| --mean [numeric-field-name] | compute the mean (average) of numeric-field-name | a floating point number, or “NaN” if there were no numeric values in the column |
| --sum [numeric-field-name] | compute the sum of numeric-field-name | a floating point number, or “NaN” if there were no numeric values in the column |
| --count | count the number of records | an integer, or zero if there were no records |


## Group By
--group-by [categorical-field-name] </br> </br>
If it’s a valid categorical field, produce an output CSV file with one row of output per distinct value in that field, with:
- the value of the group-by field in the first column
- the values of any computed aggregates in subsequent columns, in the order they were specified at the command line (or just a count column, if no aggregates were requested at the command line)

## Command

`python OLAP.py --input <input-file-name> [aggregate args] [--group-by <fieldname>]`

## Input File [input.csv](https://github.com/chloe-blankers/OLAP/blob/master/input.csv) (129,046 lines)

Sector,Ticker,Date,Open,High,Low,Close,Volume,OpenInt</br>
Technology,intc,6/20/72,0.01592,0.01592,0.01592,0.01592,7878523,0</br>
Financial Services,axp,6/21/72,1.4866,1.4957,1.4866,1.4866,1057078,0</br>
Consumer Cyclical,dis,6/21/72,1.506,1.5244,1.506,1.5151,1220068,0</br>
Technology,ibm,6/21/72,16.501,16.658,16.484,16.524,579628,0</br>
Technology,intc,6/21/72,0.01592,0.01592,0.01592,0.01592,16363089,0</br>
Financial Services,axp,6/22/72,1.514,1.5228,1.514,1.514,835584,0</br>
Technology,intc,6/20/72,0.01592,0.01592,0.01592,0.01592,7878523,0</br>
Financial Services,axp,6/21/72,1.4866,1.4957,1.4866,1.4866,1057078,0</br>
....</br>

## Output File

Command:</br>
`python OLAP.py --input input.csv --group-by ticker --count --min open --max open --mean open --min high --max high --mean high --min low --max low --mean close --min close --max close --mean close`

The resulting output from this command:

![IMG](https://github.com/chloe-blankers/OLAP/blob/master/chart.PNG)
