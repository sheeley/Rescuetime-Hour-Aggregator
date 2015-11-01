from requests import get
from pprint import pprint
from datetime import date
from calendar import Calendar
from argparse import ArgumentParser

ENDPOINT = 'https://www.rescuetime.com/anapi/data'
TODAY = date.today()

def get_hours_for_month(args):
    '''given a month, determine applicable weeks and calculate hours'''
    if not args.month:
        args.month = TODAY.month
    month = int(args.month)

    if args.verbose:
        print 'Categories: {}'.format(args.categories)

    for week in Calendar(args.first_day).monthdayscalendar(TODAY.year, month):
        get_hours_for_week(year=TODAY.year,
                           month=month,
                           days=week,
                           args=args)

def get_hours_for_week(year=None, month=None, days=[], args=None):
    '''calculate hours worked in categories for a particular week'''
    start_day = min(days)
    if start_day == 0:
        start_day = 1

    end_day = max(days)

    start_date = date(year, month, start_day)
    end_date = date(year, month, end_day)

    if start_date > TODAY:
        if args.verbose:
            print 'Skipping {} as it is in the future'.format(start_date)
        return

    params = {
        'format': 'json',
        'rs':     'week',
        'rk':     'overview',
        'rb':     start_date.isoformat(),
        're':     end_date.isoformat(),
        'key':    args.key
    }

    resp = get(ENDPOINT, params)
    resp.raise_for_status()
    data = resp.json()
    rows = data.get('rows', [])
    total_seconds = 0
    for rid, seconds, _, category in rows:
        if category not in args.categories:
            continue
        total_seconds += seconds

    if not total_seconds and args.verbose:
        pprint(params)
        pprint(data)
    hours = total_seconds / 3600.0
    print 'hours from {} to {} {}'.format(start_date, end_date, hours)

if __name__ == '__main__':
    parser = ArgumentParser(description='Get hours from rescuetime.')
    parser.add_argument('-m', '--month',
                        help='Month to calculate, defaults to last month.',
                        default=TODAY.month - 1)
    parser.add_argument('-k', '--key',
                        help='Rescuetime API key')
    parser.add_argument('-c', '--categories',
                        nargs='+',
                        help='Space delimited Rescuetime categories to include in calculation',
                        default=['Software Development'])
    parser.add_argument('-f', '--first_day',
                        help='First day of the week. 0 for Monday, 6 for Sunday. Defaults to 6.',
                        default=6)
    parser.add_argument('-v', '--verbose',
                        help='Verbose - print additional logs',
                        # nargs='?',
                        action='store_const',
                        const=True)
    args = parser.parse_args()

    if not args.key:
        try:
            with open('key', 'r') as key_file:
                args.key = key_file.read().strip()
        except:
            pass

    if not args.key:
        print 'must include an api key via arguments or "key" file in this directory'
    else:
        get_hours_for_month(args)
