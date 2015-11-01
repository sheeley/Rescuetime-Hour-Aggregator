# Rescuetime Hours by Week
This script breaks a month down into its weeks, then totals the hours spent in each category
per week.

## Usage:
```
python get-hours.py # calculates previous month, using your API key in the 'key' file in cwd

python get-hours.py -m 5 # calculates hours in May

python get-hours.py -k SOMEAPIKEY # pass your key in as an argument

python get-hours.py -c cat1 cat2 # pass in specific categories to use

python get-hours.py --help # get full list of options
```
## Example

```
$ python get-hours.py
hours from 2015-10-01 to 2015-10-03 6.16805555556
hours from 2015-10-04 to 2015-10-10 25.6455555556
hours from 2015-10-11 to 2015-10-17 18.4211111111
hours from 2015-10-18 to 2015-10-24 21.3988888889
hours from 2015-10-25 to 2015-10-31 23.2547222222
```
