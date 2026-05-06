# -*- coding: utf-8 -*-
import traceback
import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
from lunarcalendar.festival import festivals

if __name__ == '__main__':
    # solar converts to lunar, then converts to solar
    solar = Solar(2018, 1, 1)
    print(solar)
    lunar = Converter.Solar2Lunar(solar)
    print(lunar)
    solar = Converter.Lunar2Solar(lunar)
    print(solar)
    print(solar.to_date(), type(solar.to_date()))
    print(Solar.from_date(datetime.date(2018, 1, 1)))

    print('=' * 20)

    # lunar converts to solar, then converts to solar
    lunar = Lunar(2018, 2, 30, isleap=False)
    print(lunar)
    solar = Converter.Lunar2Solar(lunar)
    print(solar)
    lunar = Converter.Solar2Lunar(solar)
    print(lunar)
    print(lunar.to_date(), type(lunar.to_date()))
    print(Lunar.from_date(datetime.date(2018, 4, 15)))

    print('=' * 20)

    # if lunar does not exist, raise DateNotExist
    try:
        lunar = Lunar(2018, 2, 15, isleap=True)
    except DateNotExist:
        print(traceback.format_exc())

    print('=' * 20)

    # print festivals, using English or Chinese
    print("contain {} festivals".format(len(festivals)))
    print("----- print all festivals on 2018 in chinese: -----")
    for fest in festivals:
        print(fest.get_lang('zh'), fest(2018))
    print("----- print all festivals on 2017 in english: -----")
    for fest in festivals:
        print(fest.get_lang('en'), fest(2017))
