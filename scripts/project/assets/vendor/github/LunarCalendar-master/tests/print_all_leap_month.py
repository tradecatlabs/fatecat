# -*- coding: utf-8 -*-
import traceback
import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist

''' How leap month occur in years?
May leap month occur on Jan. or Dec.?
'''

def main():
    results = {}
    for year in range(1900, 2100 + 1):
        for month in range(1, 12 + 1):
            try:
                lunar = Lunar(year, month, 1, isleap=True)
                print(lunar)
                results[lunar.month] = results.setdefault(lunar.month, 0) + 1
            except DateNotExist:
                pass
    print("results:")
    for month in sorted(results.keys()):
        print("leap month is %3s, count: %3s" % (month, results[month]))


main()
