# -*- coding: utf-8 -*-
# online Lunar Calendar: https://wannianrili.51240.com/
import datetime
from lunarcalendar import solarterm


def test_solarterms():
    '''
    2012-01-06, 06:43:54.28   小寒
    2012-01-21, 00:09:49.08   大寒
    2012-02-04, 18:22:22.53   立春
    2012-02-19, 14:17:35.37   雨水
    2012-03-05, 12:21:01.56   惊蛰
    2012-03-20, 13:14:24.17   春分
    2012-04-04, 17:05:34.65   清明
    2012-04-20, 00:12:03.28   谷雨
    2012-05-05, 10:19:39.54   立夏
    2012-05-20, 23:15:30.28   小满
    2012-06-05, 14:25:52.96   芒种
    2012-06-21, 07:08:46.98   夏至
    2012-07-07, 00:40:42.66   小暑
    2012-07-22, 18:00:50.72   大暑
    2012-08-07, 10:30:31.88   立秋
    2012-08-23, 01:06:48.41   处暑
    2012-09-07, 13:28:59.41   白露
    2012-09-22, 22:48:57.14   秋分
    2012-10-08, 05:11:41.45   寒露
    2012-10-23, 08:13:32.83   霜降
    2012-11-07, 08:25:56.47   立冬
    2012-11-22, 05:50:08.09   小雪
    2012-12-07, 01:18:55.23   大雪
    2012-12-21, 19:11:35.61   冬至
    '''
    assert solarterm.XiaoHan(2012) == datetime.date(2012, 1, 6)
    assert solarterm.DaHan(2012) == datetime.date(2012, 1, 21)
    assert solarterm.LiChun(2012) == datetime.date(2012, 2, 4)
    assert solarterm.YuShui(2012) == datetime.date(2012, 2, 19)
    assert solarterm.JingZhe(2012) == datetime.date(2012, 3, 5)
    assert solarterm.ChunFen(2012) == datetime.date(2012, 3, 20)

    assert solarterm.QingMing(2012) == datetime.date(2012, 4, 4)
    assert solarterm.GuYu(2012) == datetime.date(2012, 4, 20)
    assert solarterm.LiXia(2012) == datetime.date(2012, 5, 5)
    assert solarterm.XiaoMan(2012) == datetime.date(2012, 5, 20)
    assert solarterm.MangZhong(2012) == datetime.date(2012, 6, 5)
    assert solarterm.XiaZhi(2012) == datetime.date(2012, 6, 21)

    assert solarterm.XiaoShu(2012) == datetime.date(2012, 7, 7)
    assert solarterm.DaShu(2012) == datetime.date(2012, 7, 22)
    assert solarterm.LiQiu(2012) == datetime.date(2012, 8, 7)
    assert solarterm.ChuShu(2012) == datetime.date(2012, 8, 23)
    assert solarterm.BaiLu(2012) == datetime.date(2012, 9, 7)
    assert solarterm.QiuFen(2012) == datetime.date(2012, 9, 22)

    assert solarterm.HanLu(2012) == datetime.date(2012, 10, 8)
    assert solarterm.ShuangJiang(2012) == datetime.date(2012, 10, 23)
    assert solarterm.LiDong(2012) == datetime.date(2012, 11, 7)
    assert solarterm.XiaoXue(2012) == datetime.date(2012, 11, 22)
    assert solarterm.DaXue(2012) == datetime.date(2012, 12, 7)
    assert solarterm.DongZhi(2012) == datetime.date(2012, 12, 21)

    ''' 1918, according to online Lunar Calendar: https://wannianrili.51240.com/ '''
    assert solarterm.XiaoHan(1918) == datetime.date(1918, 1, 6)
    assert solarterm.DaHan(1918) == datetime.date(1918, 1, 21)
    assert solarterm.LiChun(1918) == datetime.date(1918, 2, 4)
    assert solarterm.YuShui(1918) == datetime.date(1918, 2, 19)
    assert solarterm.JingZhe(1918) == datetime.date(1918, 3, 6)
    assert solarterm.ChunFen(1918) == datetime.date(1918, 3, 21)

    assert solarterm.QingMing(1918) == datetime.date(1918, 4, 5)
    assert solarterm.GuYu(1918) == datetime.date(1918, 4, 21)
    assert solarterm.LiXia(1918) == datetime.date(1918, 5, 6)
    assert solarterm.XiaoMan(1918) == datetime.date(1918, 5, 22)
    assert solarterm.MangZhong(1918) == datetime.date(1918, 6, 6)
    assert solarterm.XiaZhi(1918) == datetime.date(1918, 6, 22)

    assert solarterm.XiaoShu(1918) == datetime.date(1918, 7, 8)
    assert solarterm.DaShu(1918) == datetime.date(1918, 7, 24)
    assert solarterm.LiQiu(1918) == datetime.date(1918, 8, 8)
    assert solarterm.ChuShu(1918) == datetime.date(1918, 8, 24)
    assert solarterm.BaiLu(1918) == datetime.date(1918, 9, 8)
    assert solarterm.QiuFen(1918) == datetime.date(1918, 9, 24)

    assert solarterm.HanLu(1918) == datetime.date(1918, 10, 9)
    assert solarterm.ShuangJiang(1918) == datetime.date(1918, 10, 24)
    assert solarterm.LiDong(1918) == datetime.date(1918, 11, 8)
    assert solarterm.XiaoXue(1918) == datetime.date(1918, 11, 23)
    assert solarterm.DaXue(1918) == datetime.date(1918, 12, 8)
    assert solarterm.DongZhi(1918) == datetime.date(1918, 12, 22)
