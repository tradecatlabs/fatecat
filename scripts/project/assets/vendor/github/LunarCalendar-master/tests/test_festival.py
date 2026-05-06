# -*- coding: utf-8 -*-
# online Lunar Calendar: https://wannianrili.51240.com/
import datetime
from lunarcalendar import festival


def test_festivals():
    assert festival.NewYear(2018) == datetime.date(2018, 1, 1)
    assert festival.Valentine(2018) == datetime.date(2018, 2, 14)
    assert festival.WomenDay(2018) == datetime.date(2018, 3, 8)
    assert festival.ArborDay(2018) == datetime.date(2018, 3, 12)
    assert festival.ChingMing(2018) == datetime.date(2018, 4, 5)
    assert festival.ChingMing(2012) == datetime.date(2012, 4, 4)
    assert festival.ChingMing(2088) == datetime.date(2088, 4, 4)

    assert festival.LabourDay(2018) == datetime.date(2018, 5, 1)
    assert festival.YouthDay(2018) == datetime.date(2018, 5, 4)
    assert festival.NurseDay(2018) == datetime.date(2018, 5, 12)
    assert festival.MotherDay(2018) == datetime.date(2018, 5, 13)  # 2th sunday in May
    assert festival.ChildrenDay(2018) == datetime.date(2018, 6, 1)

    assert festival.FatherDay(2018) == datetime.date(2018, 6, 17)  # 3th sunday in June
    assert festival.TeacherDay(2018) == datetime.date(2018, 9, 10)
    assert festival.NationDay(2018) == datetime.date(2018, 10, 1)
    assert festival.Halloween(2018) == datetime.date(2018, 10, 31)
    assert festival.Thanksgiving(2018) == datetime.date(2018, 11, 22)

    assert festival.ChristmasEve(2018) == datetime.date(2018, 12, 24)
    assert festival.ChristmasDay(2018) == datetime.date(2018, 12, 25)
    assert festival.Easter(2019) == datetime.date(2019, 4, 21)

    assert festival.LaBa(2018) == datetime.date(2018, 1, 24)
    assert festival.XiaoNian(2018) == datetime.date(2018, 2, 8)
    assert festival.NewYearEve(2018) == datetime.date(2018, 2, 15)
    assert festival.ChineseNewYear(2018) == datetime.date(2018, 2, 16)
    assert festival.PoWu(2018) == datetime.date(2018, 2, 20)
    assert festival.Lantern(2018) == datetime.date(2018, 3, 2)
    assert festival.DragonHead(2018) == datetime.date(2018, 3, 18)

    assert festival.DragonBoat(2018) == datetime.date(2018, 6, 18)
    assert festival.Qixi(2018) == datetime.date(2018, 8, 17)
    assert festival.Ghost(2018) == datetime.date(2018, 8, 25)
    assert festival.MidAutumn(2018) == datetime.date(2018, 9, 24)
    assert festival.ChongYang(2018) == datetime.date(2018, 10, 17)

    assert festival.Hanyi(2018) == datetime.date(2018, 11, 8)
    assert festival.DongJie(2018) == datetime.date(2018, 12, 22)
