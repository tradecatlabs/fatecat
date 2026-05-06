# -*- coding: utf-8 -*-
# online Lunar-Solar-Converter: https://wannianrili.51240.com/
import datetime
import pytest
from lunarcalendar.converter import Solar, Lunar, DateNotExist, Converter


def test_solar():
    Solar(2016, 1, 31)
    Solar(2016, 2, 29)
    Solar(2000, 2, 29)
    with pytest.raises(DateNotExist):
        Solar(2018, 2, 29)
    with pytest.raises(DateNotExist):
        Solar(2100, 2, 29)
    with pytest.raises(DateNotExist):
        Solar(2016, 4, 31)
    with pytest.raises(DateNotExist):
        Solar(2016, 6, 31)
    with pytest.raises(DateNotExist):
        Solar(2016, 9, 31)
    with pytest.raises(DateNotExist):
        Solar(2016, 11, 31)


def test_lunar():
    Lunar(2012, 4, 4)  # date(2012, 4, 24)
    Lunar(2012, 4, 4, True)  # date(2012, 5, 24)
    Lunar(2018, 2, 30)  # date(2018, 4, 14)
    with pytest.raises(DateNotExist):
        Lunar(2018, 2, 2, True)
    with pytest.raises(DateNotExist):
        Lunar(2018, 3, 30)


def test_solar_converter():
    solar = Solar(2018, 4, 1)
    expect_solar = Converter.Lunar2Solar(Converter.Solar2Lunar(solar))
    assert solar == expect_solar

    solar = Solar(2016, 2, 29)
    expect_solar = Converter.Lunar2Solar(Converter.Solar2Lunar(solar))
    assert solar == expect_solar


def test_lunar_converter():
    lunar = Lunar(1990, 1, 29)  # date(1990, 2, 24)
    expect_lunar = Converter.Solar2Lunar(Converter.Lunar2Solar(lunar))
    assert lunar == expect_lunar

    lunar = Lunar(2018, 2, 30)  # date(2018, 4, 14)
    expect_lunar = Converter.Solar2Lunar(Converter.Lunar2Solar(lunar))
    assert lunar == expect_lunar

    lunar = Lunar(2012, 4, 4)  # date(2012, 4, 24)
    expect_lunar = Converter.Solar2Lunar(Converter.Lunar2Solar(lunar))
    assert lunar == expect_lunar

    lunar = Lunar(2012, 4, 4, True)  # date(2012, 5, 24)
    expect_lunar = Converter.Solar2Lunar(Converter.Lunar2Solar(lunar))
    assert lunar == expect_lunar


def test_converter():
    that = datetime.date(2018, 1, 1)
    solar = Solar.from_date(that)
    lunar = Lunar.from_date(that)
    assert solar == lunar
    assert solar == Converter.Lunar2Solar(lunar)
    assert lunar == Converter.Solar2Lunar(solar)
    assert solar.to_date() == lunar.to_date()
    assert that == solar.to_date()
    assert that == lunar.to_date()
