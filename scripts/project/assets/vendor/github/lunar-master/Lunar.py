#encoding:utf-8
# by chaseey
import lunardate
import datetime
import math

# 使用lunardate模块,限制阳历日期范围为1900至2049年.超出范围出错.




JIE_QI = {
    1:u"立春",2:u"雨水",3:u"惊蛰",4:u"春分",5:u"清明",6:u"谷雨",7:u"立夏",8:u"小满",9:u"芒种",10:u"夏至",11:u"小暑",12:u"大暑",
    13:u"立秋",14:u"处暑",15:u"白露",16:u"秋分",17:u"寒露",18:u"霜降",19:u"立冬",20:u"小雪",21:u"大雪",22:u"冬至",23:u"小寒",24:u"大寒"
}

# 推算节气, 默认返回立春  OUT:阳历
# 以1899年12月31日(星期日)为基准日, 之后每一天与之差值为积日
# F = 365.242 * (y – 1900) + 6.2 + 15.22 *x - 1.9 * sin(0.262 * x)  误差 0.05天左右
# 计算第x个节气公式 x = [1,2,3,4,5,...........24]
#                   [小寒,大寒,立春..... ]
def getJieqi(year,x=3):
    # 基准日
    if x not in range(1,25):
        return None
    try:
        year  = int(year)
        x = int(x)
    except:
        return None
    if year < 1900:
        return None
    x -= 1
    startDT = datetime.datetime(1899,12,31)
    # 相差的天数
    days = 365.242*(year - 1900) + 6.2 + 15.22*x - 1.9*math.sin(0.262*x)
    delta = datetime.timedelta(days=days)
    return startDT+delta



# 取得当年全年的节气时间列表.
def getJieqiList_byYear(year,jie_only=False,qi_only=False,addNum=False):
    #  addNum 加上节气对应的序号
    try:
        year = int(year)
    except:
        return []
    res = []
    if jie_only and qi_only:    # 两者相排斥
        raise KeyError
    if jie_only:
        for i in range(1,25,2):
            if addNum:
                res.append((getJieqi(year,x=i),i))
            else:
                res.append(getJieqi(year,x=i))
    elif qi_only:
        for i in range(2,25,2):
            if addNum:
                res.append((getJieqi(year,x=i),i))
            else:
                res.append(getJieqi(year,x=i))
    else:
        for i in range(1,25):
            if addNum:
                res.append((getJieqi(year,x=i),i))
            else:
                res.append(getJieqi(year,x=i))
    return res


# 取得某年某月的节气.
def getJieqiList_byMonth(year,month,jie_only=False,qi_only=False,addNum=False):
    try:
        year = int(year)
        month = int(month)
    except:
        return []
    jieqiList = getJieqiList_byYear(year,jie_only=jie_only,qi_only=qi_only,addNum=addNum)
    res = []
    if addNum:
        for dt,num in jieqiList:
            if dt.month == month:
                res.append((dt,num))
    else:
        for dt in jieqiList:
            if dt.month == month:
                res.append(dt)
    if len(res) == 0:
        raise KeyError
    return res



# 计算以1899年12月31日(星期日)为基准日开始的第m个朔日, 即初一   OUT:阳历
# M = 1.6 + 29.5306 * m + 0.4 * sin(1 - 0.45058 * m)    误差在0.2天左右
def getShuori1900(m=1):
    try:
        m = int(m)
    except:
        return None
    startDT = datetime.datetime(1899,12,31)
    days = 1.6 + 29.5306*m +0.4*math.sin(1-0.45058*m)
    delta = datetime.timedelta(days=days)
    return startDT+delta




# 设定基准起位
TIAN_GAN = u"甲,乙,丙,丁,戊,己,庚,辛,壬,癸".split(",")
DI_ZHI   = u"子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥".split(",")
SHU_XIANG = u"猪,鼠,牛,虎,兔,龙,蛇,马,羊,猴,鸡,狗".split(",")
JIA_ZHI60 = {
        1:u"甲子", 2:u"乙丑", 3:u"丙寅", 4:u"丁卯", 5:u"戊辰", 6:u"己巳", 7:u"庚午", 8:u"辛未", 9:u"壬申", 10:u"癸酉",
        11:u"甲戌", 12:u"乙亥", 13:u"丙子", 14:u"丁丑", 15:u"戊寅", 16:u"己卯", 17:u"庚辰", 18:u"辛巳", 19:u"壬午", 20:u"癸未",
        21:u"甲申", 22:u"乙酉", 23:u"丙戌", 24:u"丁亥",25:u"戊子", 26:u"己丑", 27:u"庚寅", 28:u"辛卯", 29:u"壬辰", 30:u"癸巳",
        31:u"甲午", 32:u"乙未", 33:u"丙申", 34:u"丁酉", 35:u"戊戌", 36:u"己亥", 37:u"庚子", 38:u"辛丑", 39:u"壬寅", 40:u"癸卯",
        41:u"甲辰", 42:u"乙巳", 43:u"丙午", 44:u"丁未", 45:u"戊申", 46:u"己酉", 47:u"庚戌", 48:u"辛亥",49:u"壬子", 50:u"癸丑",
        51:u"甲寅", 52:u"乙卯", 53:u"丙辰", 54:u"丁巳", 55:u"戊午", 56:u"己未",57:u"庚申", 58:u"辛酉", 59:u"壬戌", 60:u"癸亥"
}

# 从0-23小时 对应的地支, 是固定的 23:00-0:59 子, 1:00-2:59 丑
def getHourZhi(n,num=False):
    try:
        n=int(n)
        cnt = (n+1)/2
        if cnt==12:
            cnt = 0
        if num:
            return cnt+1    # 从1开始
        return DI_ZHI[cnt]
    except:
        return ""


# 时干支    IN:datetime type ,OUT:干支
def getHourGanzhi(dt,num=False):
    #以1901年1月1日凌晨一点为基准点 此刻是乙丑时的开始
    startDT=datetime.datetime(year=1901, month=1, day=1, hour=1)
    #60干支乙丑是第二个，以0为起点，则编号为1
    startGanzhi=1
    if not isinstance(dt, datetime.datetime):
        return ""
    #计算离基准时刻过去了多少时间
    delta = dt - startDT
    if delta.seconds<0:
        return ""
    #计算时刻的干支编号
    hours = delta.days*24 + delta.seconds/3600
    ganNum  = (startGanzhi + hours/2)%10
    if num: # 返回数字形式
        return (ganNum+1,getHourZhi(dt.hour,num=True))
    return (TIAN_GAN[ganNum] , getHourZhi(dt.hour))




# 日干支   IN:datetime type ,OUT:干支
def getDayGanzhi(dt,num=False):
    #函数返回60干支编号，编号范围[1,60],1901年1月1日为基准点，当天是乙卯日。
    if not isinstance(dt, datetime.date):
        return ""
    startdate=datetime.datetime(1901,1,1)
    startganzhi=16
    delta = dt - startdate
    if delta.days + delta.seconds<0:
        return ""
    res=(startganzhi+delta.days)%60
    if res == 0:
        res=60
    ganNum = (res-1)%10
    zhiNum = (res-1)%12
    if num:
        return (ganNum+1,zhiNum+1)
    return (TIAN_GAN[ganNum],DI_ZHI[zhiNum])


# 年干支 ,以每年立春时刻变换年干支.
# 立春都在阳历的2月 4或5号
def getYearGanzhi(dt,num=False):
    if not isinstance(dt,datetime.datetime):
        return ""
    if dt.year < 1900:
        return ""
    # 当年立春日期
    springDt = getJieqi(dt.year,x=3)
    # 比立春更早的是上一年的干支.
    y = dt.year
    if dt < springDt:
        y -= 1
    ganNum = (y-4)%10
    zhiNum = (y-4)%12
    if num:
        return (ganNum+1,zhiNum+1)
    return (TIAN_GAN[ganNum],DI_ZHI[zhiNum])



# 月干支 根据24节气时刻计算的,也就是每隔两个节气是一个月。不过以月初一为界的情况下认为闰月是不更换月干支的。
def getMonthGanzhi(dt,num=False):
    # 月支 按阴历正月(立春当天开始)为寅(2),二月为卯(3)...十二月为丑(1),对应气节.
    # 推算月干 =  年干x2+月支 超过10则减去10的倍数到0-9，0视做10
    #  阴历月份数字    11 12 1 2  3 4  5  6 7  8  9 10
    #                子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥
    #  对应地支索引    0  1  2 3  4  5  6  7 8 9  10 11
    # 月干列表:
    # 年　份  一月	二月	三月	四月	五月	六月	七月	八月	九月	十月	十一月	十二月
    # 甲、己	  丙寅	丁卯	戊辰	己巳	庚午	辛未	壬申	癸酉	甲戌	乙亥	丙子	     丁丑
    # 乙、庚	  戊寅	己卯	庚辰	辛巳	壬午	癸未	甲申	乙酉	丙戌	丁亥	戊子	     己丑
    # 丙、辛	  庚寅	辛卯	壬辰	癸巳	甲午	乙未	丙申	丁酉	戊戌	己亥	庚子	     辛丑
    # 丁、壬	  壬寅	癸卯	甲辰	乙巳	丙午	丁未	戊申	己酉	庚戌	辛亥	壬子	     癸丑
    # 戊、癸	  甲寅	乙卯	丙辰	丁巳	戊午	己未	庚申	辛酉	壬戌	癸亥	甲子	     乙丑
    if not isinstance(dt,datetime.datetime):
        return ""
    if dt.year < 1900:
        return ""
    # 月支变改日期表. 如     (5,     4,        6,  5,  5, 6,  7, 7,  8,  8, 7,  7)
    #　对应地支            丑(小寒)  寅(立春)   卯  辰  巳  午  未  申  酉  戌  亥  子
    # 取得当年节气变更列表,只有节那部分.
    jieqiDtList = getJieqiList_byYear(dt.year,jie_only=True)
    # 索引最开始对应 丑 1
    startzhi = 1
    zhiNum = 0  # 从小寒日期之前开始, 为子,索引0
    for jieqiDT,index in zip(jieqiDtList,range(12)):
        if dt >= jieqiDT:
            zhiNum = startzhi + index
    ganList = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 0:11,1:12}
    yg = getYearGanzhi(dt,num=True)[0]
    ganNum = (yg*2 +ganList[zhiNum])%10
    if ganNum == 0:
        ganNum = 10
    ganNum -= 1
    if num:
        return (ganNum+1,zhiNum+1)
    return (TIAN_GAN[ganNum],DI_ZHI[zhiNum])





# 属相 需要看立春前后.
def getShuxiang(dt):
    # >>> birthDate2shuXiang(1983,1,1) >>> 狗
    # >>> birthDate2shuXiang(1983,4,1) >>> 猪
    if not isinstance(dt,datetime.datetime):
        return ""
    if dt.year < 1900:
        return ""
    index = (dt.year+8)%12
    # 当年立春日期
    sprintDT = getJieqi(dt.year,x=3)
    if dt >= sprintDT:
        index = (index + 1)%12
    return SHU_XIANG[index]

#  天干地支某项转化为五行
def ganzhi2Wuxing(gz):
    A = u"子,亥,寅,卯,巳,午,申,酉,辰,戌,丑,未,甲,乙,丙,丁,戊,己,庚,辛,壬,癸".split(",")
    B = u"水,水,木,木,火,火,金,金,土,土,土,土,木,木,火,火,火,火,金,金,水,水".split(',')
    if gz in A:
        return B[A.index(gz)]
    return ""


# 天干地支一组转化为纳音
def ganzhi2Nayin(gz):
    nayinDict = {
        u"甲子,乙丑":u"海中金", u"丙寅,丁卯":u"炉中火", u"戊辰,己巳":u"大林木",
        u"庚午,辛未":u"路旁土", u"壬申,癸酉":u"剑锋金", u"甲戌,乙亥":u"山头火",
        u"丙子,丁丑":u"漳下水", u"戊寅,己卯":u"城头土", u"庚辰,辛巳":u"白腊金",
        u"壬午,癸未":u"杨柳木", u"甲申,乙酉":u"泉中水", u"丙戌,丁亥":u"屋上土",
        u"戊子,己丑":u"霹雳火", u"庚寅,辛卯":u"松柏木", u"壬辰,癸巳":u"长流水",
        u"甲午,乙未":u"砂石金", u"丙申,丁酉":u"山下火", u"戊戌,己亥":u"平地木",
        u"庚子,辛丑":u"壁上土", u"壬寅,癸卯":u"金薄金", u"甲辰,乙巳":u"覆灯火",
        u"丙午,丁未":u"天河水", u"戊申,己酉":u"大驿土", u"庚戌,辛亥":u"钗环金",
        u"壬子,癸丑":u"桑柘木", u"甲寅,乙卯":u"大溪水", u"丙辰,丁巳":u"沙中土",
        u"戊午,己未":u"天上火", u"庚申,辛酉":u"石榴木", u"壬戌,癸亥":u"大海水"
    }
    for key,val in nayinDict.iteritems():
        if gz in key:
            return val
    return ""






# 阴历月 IN:月份数字
def getLunarMonth_cn(n,postfix=True):
    monthList = u"正,二,三,四,五,六,七,八,九,十,十一,腊".split(",")
    res = ""
    try:
        n = int(n)
        res = monthList[(n-1)]
    except:pass
    if postfix:
        return res+u"月"
    return res

def getNum2cn(n):
    try:
        n = int(n)
    except:
        return None
    if n>9 or n < 0:
        return None
    str = u'零,壹,貳,叁,肆,伍,陆,染,捌,玖'.split(",")
    return str[n]


#　阴历日 IN: 天数字
def getLunarDay_cn(n):
    dayList = u'初一,初二,初三,初四,初五,初六,初七,初八,初九,初十,十一,十二,十三,十四,十五,十六,十七,' \
              u'十八,十九,二十,廿一,廿二,廿三,廿四,廿五,廿六,廿七,廿八,廿九,三十'.split(",")
    try:
        n = int(n)
        return dayList[n-1]
    except:pass
    return ""


# 起大运岁计算 OUT:dt-type
def getQiyun_Date(dt,sex=1):
    # 默认sex=1 为男  sex=0为女
    if not isinstance(dt,datetime.datetime):
        return ""
    # 出生年干. 起位 甲乙丙丁.... 1开始
    yg = getYearGanzhi(dt,num=True)[0]
    # 年干是[甲,丙,戊,庚,壬], yg%2==1 ,是阳年, 男顺向, 女逆向
    # 年干是[乙,丁,己,辛,癸], yg%2==0, 是阴年, 男逆向,  女顺向
    direction = 1     # 方向 1顺 0逆
    if yg%2==1:     # 阳年
        if not sex:
            direction=0
    else:           # 阴年
        if sex:
            direction=0

    # 求 出生的下一个月立节日期, 与上一个月立节日期
    if dt.month == 12:
        jieqiNextMonthDt = getJieqiList_byMonth(dt.year+1,1,jie_only=True)[0]
    else:
        jieqiNextMonthDt = getJieqiList_byMonth(dt.year,dt.month+1,jie_only=True)[0]
    if dt.month == 1:
        jieqiPreMonthDt  = getJieqiList_byMonth(dt.year-1,12,jie_only=True)[0]
    else:
        jieqiPreMonthDt  = getJieqiList_byMonth(dt.year,dt.month-1,jie_only=True)[0]
    # 出生上一个立节日期, 与上一个月的立节日期,可能相同,可能不同.
    jieqiList = getJieqiList_byMonth(dt.year-1,12,jie_only=True) + getJieqiList_byYear(dt.year,jie_only=True)
    jieqiPreDt = None
    i = len(jieqiList) -1
    while dt <= jieqiList[i]:
        i -= 1
    jieqiPreDt = jieqiList[i]
    if dt in jieqiList:     # 刚好出生在节气时刻, 虽然可能性很小
        jieqiPreDt = dt

    if direction:   # 顺向计算  阳男,阴女
        #  出生至下一日起,到下月立节的日,时 为止,三日折1年,一日折4月,一时辰折10天
        deltaNextMonth = jieqiNextMonthDt - dt
        deltaPre = dt - jieqiPreDt     # 求出生距上一个立节的天数
        delta_days = deltaNextMonth.days
        delta_hours = deltaNextMonth.seconds/3600 + deltaPre.days + deltaPre.seconds/3600     # 补上出生日距前一个立节的天数
        # 折算年,月,日 指出生后的第几年几月 那个月的立节后第几日
        daYun_years = delta_days/3
        daYun_months = (delta_days%3) * 4
        daYun_days = (delta_hours/2)*10

    else:           # 逆向, 阴男,阳女
        #  出生日的上一日起,到上月立节的日,时 为止,三日折1年,一日折4月,一时辰折10天
        deltaPreMonth = dt - jieqiPreMonthDt
        deltaPre = dt - jieqiPreDt
        delta_days = deltaPreMonth.days
        delta_hours = deltaPreMonth.seconds/3600 + deltaPre.days + deltaPre.seconds/3600    # 补上出生日到下一个立节的天数
        # 折算年,月,日 指出生后的第几年几月 那个月的立节后第几日
        daYun_years = delta_days/3
        daYun_months = (delta_days%3) * 4
        daYun_days = (delta_hours/2)*10

    # 返回实际起运日期
    final_y = dt.year + daYun_years
    final_m = dt.month + daYun_months
    while final_m > 12:
        final_m -= 12
        final_y += 1
    # 取得出生后 第几年几月的那个月的立节
    final_jieqiDt = getJieqiList_byMonth(final_y,final_m,jie_only=True)[0]
    final_DT = final_jieqiDt + datetime.timedelta(days=daYun_days)
    return final_DT



# 排小运 按虚岁算, 有一年算一年, 阳男阴女顺行, 阴男阳女逆行
# 由时柱排起 按60甲子顺序下去, 如1998戊寅年五月初六壬子时生男, 一岁小运是癸丑, 二岁是甲寅 如果生女,则逆顺 一岁是辛亥,二岁庚戌.
# OUT: [1岁开始对应的60甲子干支,...]
def getXiaoyun_list(dt,sex=1,ages=1):
    # 默认返回 1岁对应的60甲子
    # 默认sex=1 为男  sex=0为女
    if not isinstance(dt,datetime.datetime):
        return None
    try:
        ages = abs(int(ages))
    except:
        return None
    # 出生年干. 起位 甲乙丙丁.... 1开始
    yg = getYearGanzhi(dt,num=True)[0]
    # 年干是[甲,丙,戊,庚,壬], yg%2==1 ,是阳年, 男顺向, 女逆向
    # 年干是[乙,丁,己,辛,癸], yg%2==0, 是阴年, 男逆向,  女顺向
    direction = 1     # 方向 1顺 0逆
    tgz = "".join(getHourGanzhi(dt))
    cnt = JIA_ZHI60.values().index(tgz) +1     # 出生时干支对应60甲子的序号, 作为0岁起位,
    res = []
    if (yg%2==1 and sex) or (yg%2==0 and not sex):    # 顺向
        for i in range(1,ages+1):
            cnt += 1
            if cnt>60:  # 指针大于60,复位1
                cnt=1
            res.append(JIA_ZHI60[cnt])
    else:       #逆向
        for i in range(1,ages+1):
            cnt -= 1
            if cnt < 1:  # 指针小于1,复位60
                cnt=60
            res.append(JIA_ZHI60[cnt])
    return res



# 旬空  IN: 60甲子日对应的 天干,地支的数字  OUT:两个 地支
def getXunkong(ganNum,zhiNum,num=False):
    """
    空亡的计算方法：11-天干数+地支数。计算的结果所对应的地支数即为空亡。如果计算结果>12 减去12就是空亡。
    如甲子日空亡为11-1+1=11，11为戌，即为戌亥空。
    """
    try:
        ganNum = int(ganNum)
        zhiNum = int(zhiNum)
    except:
        return ""
    cnt = 11-ganNum+zhiNum
    if cnt>12:
        cnt -= 12
    # cnt 空亡 地支序号.
    cnt2 = cnt+1
    if cnt2 > 12:
        cnt2 = 1
    if num:
        return (cnt,cnt2)
    return (DI_ZHI[cnt-1],DI_ZHI[cnt2-1])



#　四住推命
#　





#  真太阳时间换算, IN:平太阳时间 dt类型
def getTrueSunDatetime(dt=None):
    if not isinstance(dt,datetime.datetime):
        return ""
    try:
        dateStr = dt.strftime('%m-%d')
    except:
        return ""
    dateList = {
        "01-01":datetime.timedelta(minutes=-3,seconds=-9), "01-02":datetime.timedelta(minutes=-3,seconds=-38),
        "01-03":datetime.timedelta(minutes=-4,seconds=-6), "01-04":datetime.timedelta(minutes=-4,seconds=-33),
        "01-05":datetime.timedelta(minutes=-5,seconds=-1), "01-06":datetime.timedelta(minutes=-5,seconds=-27),
        "01-07":datetime.timedelta(minutes=-5,seconds=-54), "01-08":datetime.timedelta(minutes=-6,seconds=-20),
        "01-09":datetime.timedelta(minutes=-6,seconds=-45), "01-10":datetime.timedelta(minutes=-7,seconds=-10),
        "01-11":datetime.timedelta(minutes=-7,seconds=-35), "01-12":datetime.timedelta(minutes=-7,seconds=-59),
        "01-13":datetime.timedelta(minutes=-8,seconds=-22), "01-14":datetime.timedelta(minutes=-8,seconds=-45),
        "01-15":datetime.timedelta(minutes=-9,seconds=-7), "01-16":datetime.timedelta(minutes=-9,seconds=-28),
        "01-17":datetime.timedelta(minutes=-9,seconds=-49), "01-18":datetime.timedelta(minutes=-10,seconds=-9),
        "01-19":datetime.timedelta(minutes=-10,seconds=-28), "01-20":datetime.timedelta(minutes=-10,seconds=-47),
        "01-21":datetime.timedelta(minutes=-11,seconds=-5), "01-22":datetime.timedelta(minutes=-11,seconds=-22),
        "01-23":datetime.timedelta(minutes=-11,seconds=-38), "01-24":datetime.timedelta(minutes=-11,seconds=-54),
        "01-25":datetime.timedelta(minutes=-12,seconds=-8), "01-26":datetime.timedelta(minutes=-12,seconds=-22),
        "01-27":datetime.timedelta(minutes=-12,seconds=-35), "01-28":datetime.timedelta(minutes=-12,seconds=-59),
        "01-29":datetime.timedelta(minutes=-13,seconds=-10), "01-30":datetime.timedelta(minutes=-13,seconds=-19),
        "01-31":datetime.timedelta(minutes=-13,seconds=-37), "02-01":datetime.timedelta(minutes=-13,seconds=-44),
        "02-02":datetime.timedelta(minutes=-13,seconds=-50), "02-03":datetime.timedelta(minutes=-13,seconds=-56),
        "02-04":datetime.timedelta(minutes=-14,seconds=-1), "02-05":datetime.timedelta(minutes=-14,seconds=-5),
        "02-06":datetime.timedelta(minutes=-14,seconds=-9), "02-07":datetime.timedelta(minutes=-14,seconds=-11),
        "02-08":datetime.timedelta(minutes=-14,seconds=-13), "02-09":datetime.timedelta(minutes=-14,seconds=-14),
        "02-10":datetime.timedelta(minutes=-14,seconds=-15), "02-11":datetime.timedelta(minutes=-14,seconds=-14),
        "02-12":datetime.timedelta(minutes=-14,seconds=-13), "02-13":datetime.timedelta(minutes=-14,seconds=-11),
        "02-14":datetime.timedelta(minutes=-14,seconds=-8), "02-15":datetime.timedelta(minutes=-14,seconds=-5),
        "02-16":datetime.timedelta(minutes=-14,seconds=-1), "02-17":datetime.timedelta(minutes=-13,seconds=-56),
        "02-18":datetime.timedelta(minutes=-13,seconds=-51), "02-19":datetime.timedelta(minutes=-13,seconds=-44),
        "02-20":datetime.timedelta(minutes=-13,seconds=-38), "02-21":datetime.timedelta(minutes=-13,seconds=-30),
        "02-22":datetime.timedelta(minutes=-13,seconds=-22), "02-23":datetime.timedelta(minutes=-13,seconds=-13),
        "02-24":datetime.timedelta(minutes=-11,seconds=-4), "02-25":datetime.timedelta(minutes=-12,seconds=-54),
        "02-26":datetime.timedelta(minutes=-12,seconds=-43), "02-27":datetime.timedelta(minutes=-12,seconds=-32),
        "02-28":datetime.timedelta(minutes=-12,seconds=-21), "02-29":datetime.timedelta(minutes=-12,seconds=-8),
        "03-01":datetime.timedelta(minutes=-11,seconds=-56), "03-02":datetime.timedelta(minutes=-11,seconds=-43),
        "03-03":datetime.timedelta(minutes=-11,seconds=-29), "03-04":datetime.timedelta(minutes=-11,seconds=-15),
        "03-05":datetime.timedelta(minutes=-11,seconds=-1), "03-06":datetime.timedelta(minutes=-10,seconds=-47),
        "03-07":datetime.timedelta(minutes=-10,seconds=-32), "03-08":datetime.timedelta(minutes=-10,seconds=-16),
        "03-09":datetime.timedelta(minutes=-10,seconds=-1), "03-10":datetime.timedelta(minutes=-9,seconds=-45),
        "03-11":datetime.timedelta(minutes=-9,seconds=-28), "03-12":datetime.timedelta(minutes=-9,seconds=-12),
        "03-13":datetime.timedelta(minutes=-8,seconds=-55), "03-14":datetime.timedelta(minutes=-8,seconds=-38),
        "03-15":datetime.timedelta(minutes=-8,seconds=-21), "03-16":datetime.timedelta(minutes=-8,seconds=-4),
        "03-17":datetime.timedelta(minutes=-7,seconds=-46), "03-18":datetime.timedelta(minutes=-7,seconds=-29),
        "03-19":datetime.timedelta(minutes=-7,seconds=-11), "03-20":datetime.timedelta(minutes=-6,seconds=-53),
        "03-21":datetime.timedelta(minutes=-6,seconds=-35), "03-22":datetime.timedelta(minutes=-6,seconds=-17),
        "03-23":datetime.timedelta(minutes=-5,seconds=-58), "03-24":datetime.timedelta(minutes=-5,seconds=-40),
        "03-25":datetime.timedelta(minutes=-5,seconds=-22), "03-26":datetime.timedelta(minutes=-5,seconds=-4),
        "03-27":datetime.timedelta(minutes=-4,seconds=-45), "03-28":datetime.timedelta(minutes=-4,seconds=-27),
        "03-29":datetime.timedelta(minutes=-4,seconds=-9), "03-30":datetime.timedelta(minutes=-3,seconds=-51),
        "03-31":datetime.timedelta(minutes=-3,seconds=-33), "04-01":datetime.timedelta(minutes=-3,seconds=-16),
        "04-02":datetime.timedelta(minutes=-2,seconds=-58), "04-03":datetime.timedelta(minutes=-2,seconds=-41),
        "04-04":datetime.timedelta(minutes=-2,seconds=-24), "04-05":datetime.timedelta(minutes=-2,seconds=-7),
        "04-06":datetime.timedelta(minutes=-1,seconds=-50), "04-07":datetime.timedelta(minutes=-1,seconds=-33),
        "04-08":datetime.timedelta(minutes=-1,seconds=-17), "04-09":datetime.timedelta(minutes=-1,seconds=-1),
        "04-10":datetime.timedelta(minutes=+0,seconds=+46), "04-11":datetime.timedelta(minutes=+0,seconds=+30),
        "04-12":datetime.timedelta(minutes=+0,seconds=+16), "04-13":datetime.timedelta(minutes=+0,seconds=+1),
        "04-14":datetime.timedelta(minutes=+0,seconds=+13), "04-15":datetime.timedelta(minutes=+0,seconds=+27),
        "04-16":datetime.timedelta(minutes=+0,seconds=+41), "04-17":datetime.timedelta(minutes=+0,seconds=+54),
        "04-18":datetime.timedelta(minutes=+1,seconds=+6), "04-19":datetime.timedelta(minutes=+1,seconds=+19),
        "04-20":datetime.timedelta(minutes=+1,seconds=+31), "04-21":datetime.timedelta(minutes=+1,seconds=+42),
        "04-22":datetime.timedelta(minutes=+1,seconds=+53), "04-23":datetime.timedelta(minutes=+2,seconds=+4),
        "04-24":datetime.timedelta(minutes=+2,seconds=+14), "04-25":datetime.timedelta(minutes=+2,seconds=+23),
        "04-26":datetime.timedelta(minutes=+2,seconds=+33), "04-27":datetime.timedelta(minutes=+2,seconds=+41),
        "04-28":datetime.timedelta(minutes=+2,seconds=+49), "04-29":datetime.timedelta(minutes=+2,seconds=+57),
        "04-30":datetime.timedelta(minutes=+3,seconds=+4), "05-01":datetime.timedelta(minutes=+1,seconds=+10),
        "05-02":datetime.timedelta(minutes=+3,seconds=+16), "05-03":datetime.timedelta(minutes=+3,seconds=+21),
        "05-04":datetime.timedelta(minutes=+3,seconds=+26), "05-05":datetime.timedelta(minutes=+3,seconds=+30),
        "05-06":datetime.timedelta(minutes=+3,seconds=+37), "05-07":datetime.timedelta(minutes=+3,seconds=+36),
        "05-08":datetime.timedelta(minutes=+3,seconds=+39), "05-09":datetime.timedelta(minutes=+3,seconds=+40),
        "05-10":datetime.timedelta(minutes=+3,seconds=+42), "05-11":datetime.timedelta(minutes=+3,seconds=+42),
        "05-12":datetime.timedelta(minutes=+3,seconds=+42), "05-13":datetime.timedelta(minutes=+3,seconds=+42),
        "05-14":datetime.timedelta(minutes=+3,seconds=+41), "05-15":datetime.timedelta(minutes=+3,seconds=+39),
        "05-16":datetime.timedelta(minutes=+3,seconds=+37), "05-17":datetime.timedelta(minutes=+3,seconds=+34),
        "05-18":datetime.timedelta(minutes=+3,seconds=+31), "05-19":datetime.timedelta(minutes=+3,seconds=+27),
        "05-20":datetime.timedelta(minutes=+3,seconds=+23), "05-21":datetime.timedelta(minutes=+3,seconds=+18),
        "05-22":datetime.timedelta(minutes=+3,seconds=+13), "05-23":datetime.timedelta(minutes=+3,seconds=+7),
        "05-24":datetime.timedelta(minutes=+3,seconds=+1), "05-25":datetime.timedelta(minutes=+2,seconds=+54),
        "05-26":datetime.timedelta(minutes=+2,seconds=+47), "05-27":datetime.timedelta(minutes=+2,seconds=+39),
        "05-28":datetime.timedelta(minutes=+2,seconds=+31), "05-29":datetime.timedelta(minutes=+2,seconds=+22),
        "05-30":datetime.timedelta(minutes=+2,seconds=+13), "05-31":datetime.timedelta(minutes=+2,seconds=+4),
        "06-01":datetime.timedelta(minutes=+1,seconds=+54), "06-02":datetime.timedelta(minutes=+1,seconds=+44),
        "06-03":datetime.timedelta(minutes=+1,seconds=+34), "06-04":datetime.timedelta(minutes=+1,seconds=+23),
        "06-05":datetime.timedelta(minutes=+1,seconds=+12), "06-06":datetime.timedelta(minutes=+1,seconds=+0),
        "06-07":datetime.timedelta(minutes=+0,seconds=+48), "06-08":datetime.timedelta(minutes=+0,seconds=+36),
        "06-09":datetime.timedelta(minutes=+0,seconds=+24), "06-10":datetime.timedelta(minutes=+0,seconds=+12),
        "06-11":datetime.timedelta(minutes=+0,seconds=+1), "06-12":datetime.timedelta(minutes=+0,seconds=+14),
        "06-13":datetime.timedelta(minutes=+0,seconds=+39), "06-14":datetime.timedelta(minutes=+0,seconds=+52),
        "06-15":datetime.timedelta(minutes=-1,seconds=-5), "06-16":datetime.timedelta(minutes=-1,seconds=-18),
        "06-17":datetime.timedelta(minutes=-1,seconds=-31), "06-18":datetime.timedelta(minutes=-1,seconds=-45),
        "06-19":datetime.timedelta(minutes=-1,seconds=-57), "06-20":datetime.timedelta(minutes=-2,seconds=-10),
        "06-21":datetime.timedelta(minutes=-2,seconds=-23), "06-22":datetime.timedelta(minutes=-2,seconds=-36),
        "06-23":datetime.timedelta(minutes=-2,seconds=-48), "06-24":datetime.timedelta(minutes=-3,seconds=-1),
        "06-25":datetime.timedelta(minutes=-3,seconds=-13), "06-26":datetime.timedelta(minutes=-3,seconds=-25),
        "06-27":datetime.timedelta(minutes=-3,seconds=-37), "06-28":datetime.timedelta(minutes=-3,seconds=-49),
        "06-29":datetime.timedelta(minutes=-4,seconds=-0), "06-30":datetime.timedelta(minutes=-4,seconds=-11),
        "07-01":datetime.timedelta(minutes=-4,seconds=-22), "07-02":datetime.timedelta(minutes=-4,seconds=-33),
        "07-03":datetime.timedelta(minutes=-4,seconds=-43), "07-04":datetime.timedelta(minutes=-4,seconds=-53),
        "07-05":datetime.timedelta(minutes=-5,seconds=-2), "07-06":datetime.timedelta(minutes=-5,seconds=-11),
        "07-07":datetime.timedelta(minutes=-5,seconds=-20), "07-08":datetime.timedelta(minutes=-5,seconds=-28),
        "07-09":datetime.timedelta(minutes=-5,seconds=-36), "07-10":datetime.timedelta(minutes=-5,seconds=-43),
        "07-11":datetime.timedelta(minutes=-5,seconds=-50), "07-12":datetime.timedelta(minutes=-5,seconds=-56),
        "07-13":datetime.timedelta(minutes=-6,seconds=-2), "07-14":datetime.timedelta(minutes=-6,seconds=-8),
        "07-15":datetime.timedelta(minutes=-6,seconds=-12), "07-16":datetime.timedelta(minutes=-6,seconds=-16),
        "07-17":datetime.timedelta(minutes=-6,seconds=-20), "07-18":datetime.timedelta(minutes=-6,seconds=-23),
        "07-19":datetime.timedelta(minutes=-6,seconds=-25), "07-20":datetime.timedelta(minutes=-6,seconds=-27),
        "07-21":datetime.timedelta(minutes=-6,seconds=-29), "07-22":datetime.timedelta(minutes=-6,seconds=-29),
        "07-23":datetime.timedelta(minutes=-6,seconds=-29), "07-24":datetime.timedelta(minutes=-6,seconds=-29),
        "07-25":datetime.timedelta(minutes=-6,seconds=-28), "07-26":datetime.timedelta(minutes=-6,seconds=-26),
        "07-27":datetime.timedelta(minutes=-6,seconds=-24), "07-28":datetime.timedelta(minutes=-6,seconds=-21),
        "07-29":datetime.timedelta(minutes=-6,seconds=-17), "07-30":datetime.timedelta(minutes=-6,seconds=-13),
        "07-31":datetime.timedelta(minutes=-6,seconds=-8), "08-01":datetime.timedelta(minutes=-6,seconds=-3),
        "08-02":datetime.timedelta(minutes=-5,seconds=-57), "08-03":datetime.timedelta(minutes=-5,seconds=-51),
        "08-04":datetime.timedelta(minutes=-5,seconds=-44), "08-05":datetime.timedelta(minutes=-5,seconds=-36),
        "08-06":datetime.timedelta(minutes=-5,seconds=-28), "08-07":datetime.timedelta(minutes=-5,seconds=-19),
        "08-08":datetime.timedelta(minutes=-5,seconds=-10), "08-09":datetime.timedelta(minutes=-5,seconds=-0),
        "08-10":datetime.timedelta(minutes=-4,seconds=-50), "08-11":datetime.timedelta(minutes=-4,seconds=-39),
        "08-12":datetime.timedelta(minutes=-4,seconds=-27), "08-13":datetime.timedelta(minutes=-4,seconds=-15),
        "08-14":datetime.timedelta(minutes=-4,seconds=-2), "08-15":datetime.timedelta(minutes=-3,seconds=-49),
        "08-16":datetime.timedelta(minutes=-3,seconds=-36), "08-17":datetime.timedelta(minutes=-3,seconds=-21),
        "08-18":datetime.timedelta(minutes=-3,seconds=-7), "08-19":datetime.timedelta(minutes=-2,seconds=-51),
        "08-20":datetime.timedelta(minutes=-2,seconds=-36), "08-21":datetime.timedelta(minutes=-2,seconds=-20),
        "08-22":datetime.timedelta(minutes=-2,seconds=-3), "08-23":datetime.timedelta(minutes=-1,seconds=-47),
        "08-24":datetime.timedelta(minutes=-1,seconds=-29), "08-25":datetime.timedelta(minutes=-1,seconds=-12),
        "08-26":datetime.timedelta(minutes=+0,seconds=+54), "08-27":datetime.timedelta(minutes=+0,seconds=+35),
        "08-28":datetime.timedelta(minutes=+0,seconds=+17), "08-29":datetime.timedelta(minutes=+0,seconds=+2),
        "08-30":datetime.timedelta(minutes=+0,seconds=+21), "08-31":datetime.timedelta(minutes=+0,seconds=+41),
        "09-01":datetime.timedelta(minutes=+1,seconds=+0), "09-02":datetime.timedelta(minutes=+1,seconds=+20),
        "09-03":datetime.timedelta(minutes=+1,seconds=+40), "09-04":datetime.timedelta(minutes=+2,seconds=+1),
        "09-05":datetime.timedelta(minutes=+2,seconds=+21), "09-06":datetime.timedelta(minutes=+2,seconds=+42),
        "09-07":datetime.timedelta(minutes=+3,seconds=+3), "09-08":datetime.timedelta(minutes=+3,seconds=+3),
        "09-09":datetime.timedelta(minutes=+3,seconds=+24), "09-10":datetime.timedelta(minutes=+3,seconds=+45),
        "09-11":datetime.timedelta(minutes=+4,seconds=+6), "09-12":datetime.timedelta(minutes=+4,seconds=+27),
        "09-13":datetime.timedelta(minutes=+4,seconds=+48), "09-14":datetime.timedelta(minutes=+5,seconds=+10),
        "09-15":datetime.timedelta(minutes=+5,seconds=+31), "09-16":datetime.timedelta(minutes=+5,seconds=+53),
        "09-17":datetime.timedelta(minutes=+6,seconds=+14), "09-18":datetime.timedelta(minutes=+6,seconds=+35),
        "09-19":datetime.timedelta(minutes=+6,seconds=+57), "09-20":datetime.timedelta(minutes=+7,seconds=+18),
        "09-21":datetime.timedelta(minutes=+7,seconds=+39), "09-22":datetime.timedelta(minutes=+8,seconds=+0),
        "09-23":datetime.timedelta(minutes=+8,seconds=+21), "09-24":datetime.timedelta(minutes=+8,seconds=+42),
        "09-25":datetime.timedelta(minutes=+9,seconds=+2), "09-26":datetime.timedelta(minutes=+9,seconds=+22),
        "09-27":datetime.timedelta(minutes=+9,seconds=+42), "09-28":datetime.timedelta(minutes=+10,seconds=+2),
        "09-29":datetime.timedelta(minutes=+10,seconds=+21), "09-30":datetime.timedelta(minutes=+10,seconds=+40),
        "10-01":datetime.timedelta(minutes=+10,seconds=+59), "10-02":datetime.timedelta(minutes=+11,seconds=+18),
        "10-03":datetime.timedelta(minutes=+11,seconds=+36), "10-04":datetime.timedelta(minutes=+11,seconds=+36),
        "10-05":datetime.timedelta(minutes=+11,seconds=+53), "10-06":datetime.timedelta(minutes=+12,seconds=+11),
        "10-07":datetime.timedelta(minutes=+12,seconds=+28), "10-08":datetime.timedelta(minutes=+12,seconds=+44),
        "10-09":datetime.timedelta(minutes=+12,seconds=+60), "10-10":datetime.timedelta(minutes=+13,seconds=+16),
        "10-11":datetime.timedelta(minutes=+13,seconds=+16), "10-12":datetime.timedelta(minutes=+13,seconds=+31),
        "10-13":datetime.timedelta(minutes=+13,seconds=+45), "10-14":datetime.timedelta(minutes=+13,seconds=+59),
        "10-15":datetime.timedelta(minutes=+14,seconds=+13), "10-16":datetime.timedelta(minutes=+14,seconds=+26),
        "10-17":datetime.timedelta(minutes=+14,seconds=+38), "10-18":datetime.timedelta(minutes=+14,seconds=+50),
        "10-19":datetime.timedelta(minutes=+15,seconds=+1), "10-20":datetime.timedelta(minutes=+15,seconds=+12),
        "10-21":datetime.timedelta(minutes=+11,seconds=+21), "10-22":datetime.timedelta(minutes=+15,seconds=+31),
        "10-23":datetime.timedelta(minutes=+15,seconds=+40), "10-24":datetime.timedelta(minutes=+15,seconds=+48),
        "10-25":datetime.timedelta(minutes=+15,seconds=+55), "10-26":datetime.timedelta(minutes=+16,seconds=+1),
        "10-27":datetime.timedelta(minutes=+16,seconds=+7), "10-28":datetime.timedelta(minutes=+16,seconds=+12),
        "10-29":datetime.timedelta(minutes=+16,seconds=+16), "10-30":datetime.timedelta(minutes=+16,seconds=+20),
        "10-31":datetime.timedelta(minutes=+16,seconds=+22), "11-01":datetime.timedelta(minutes=+16,seconds=+24),
        "11-02":datetime.timedelta(minutes=+16,seconds=+25), "11-03":datetime.timedelta(minutes=+16,seconds=+25),
        "11-04":datetime.timedelta(minutes=+16,seconds=+24), "11-05":datetime.timedelta(minutes=+16,seconds=+23),
        "11-06":datetime.timedelta(minutes=+16,seconds=+21), "11-07":datetime.timedelta(minutes=+16,seconds=+17),
        "11-08":datetime.timedelta(minutes=+16,seconds=+13), "11-09":datetime.timedelta(minutes=+16,seconds=+9),
        "11-10":datetime.timedelta(minutes=+16,seconds=+3), "11-11":datetime.timedelta(minutes=+15,seconds=+56),
        "11-12":datetime.timedelta(minutes=+15,seconds=+49), "11-13":datetime.timedelta(minutes=+15,seconds=+41),
        "11-14":datetime.timedelta(minutes=+15,seconds=+32), "11-15":datetime.timedelta(minutes=+15,seconds=+22),
        "11-16":datetime.timedelta(minutes=+15,seconds=+11), "11-17":datetime.timedelta(minutes=+14,seconds=+60),
        "11-18":datetime.timedelta(minutes=+14,seconds=+47), "11-19":datetime.timedelta(minutes=+14,seconds=+34),
        "11-20":datetime.timedelta(minutes=+14,seconds=+20), "11-21":datetime.timedelta(minutes=+14,seconds=+6),
        "11-22":datetime.timedelta(minutes=+13,seconds=+50), "11-23":datetime.timedelta(minutes=+13,seconds=+34),
        "11-24":datetime.timedelta(minutes=+13,seconds=+17), "11-25":datetime.timedelta(minutes=+12,seconds=+59),
        "11-26":datetime.timedelta(minutes=+12,seconds=+40), "11-27":datetime.timedelta(minutes=+12,seconds=+21),
        "11-28":datetime.timedelta(minutes=+12,seconds=+1), "11-29":datetime.timedelta(minutes=+11,seconds=+40),
        "11-30":datetime.timedelta(minutes=+11,seconds=+18), "12-01":datetime.timedelta(minutes=+10,seconds=+56),
        "12-02":datetime.timedelta(minutes=+10,seconds=+33), "12-03":datetime.timedelta(minutes=+10,seconds=+9),
        "12-04":datetime.timedelta(minutes=+9,seconds=+45), "12-05":datetime.timedelta(minutes=+9,seconds=+21),
        "12-06":datetime.timedelta(minutes=+8,seconds=+55), "12-07":datetime.timedelta(minutes=+8,seconds=+29),
        "12-08":datetime.timedelta(minutes=+8,seconds=+3), "12-09":datetime.timedelta(minutes=+7,seconds=+36),
        "12-10":datetime.timedelta(minutes=+7,seconds=+9), "12-11":datetime.timedelta(minutes=+6,seconds=+42),
        "12-12":datetime.timedelta(minutes=+6,seconds=+14), "12-13":datetime.timedelta(minutes=+5,seconds=+46),
        "12-14":datetime.timedelta(minutes=+5,seconds=+17), "12-15":datetime.timedelta(minutes=+4,seconds=+48),
        "12-16":datetime.timedelta(minutes=+4,seconds=+19), "12-17":datetime.timedelta(minutes=+3,seconds=+50),
        "12-18":datetime.timedelta(minutes=+3,seconds=+21), "12-19":datetime.timedelta(minutes=+2,seconds=+51),
        "12-20":datetime.timedelta(minutes=+2,seconds=+22), "12-21":datetime.timedelta(minutes=+1,seconds=+52),
        "12-22":datetime.timedelta(minutes=+1,seconds=+22), "12-23":datetime.timedelta(minutes=+0,seconds=+52),
        "12-24":datetime.timedelta(minutes=+0,seconds=+23), "12-25":datetime.timedelta(minutes=+0,seconds=+7),
        "12-26":datetime.timedelta(minutes=+0,seconds=+37), "12-27":datetime.timedelta(minutes=-1,seconds=-6),
        "12-28":datetime.timedelta(minutes=-1,seconds=-36), "12-29":datetime.timedelta(minutes=-2,seconds=-5),
        "12-30":datetime.timedelta(minutes=-2,seconds=-34), "12-31":datetime.timedelta(minutes=-3,seconds=-3),
    }
    return dt+dateList[dateStr]


# 最得西方星座
def getConstellation(dt):
    """
    通过cookie.date值,返回星座名,如果都为空,返回今天的星座
    """
    if not isinstance(dt,datetime.datetime):
        return None
    conStr=""
    y = dt.year
    Fdt = datetime.datetime
    if dt>=Fdt(y,1,20) and dt<=Fdt(y,2,18):     conStr = u'水瓶座'
    elif dt>=Fdt(y,2,19) and dt<=Fdt(y,3,20):   conStr = u'双鱼座'
    elif dt>=Fdt(y,3,21) and dt<=Fdt(y,4,19):   conStr = u'白羊座'
    elif dt>=Fdt(y,4,20) and dt<= Fdt(y,5,20):  conStr = u'金牛座'
    elif dt>=Fdt(y,5,21) and dt<=Fdt(y,6,21):   conStr = u'双子座'
    elif dt>=Fdt(y,6,22) and dt<=Fdt(y,7,22):   conStr = u'巨蟹座'
    elif dt>=Fdt(y,7,23) and dt<=Fdt(y,8,22):   conStr = u'狮子座'
    elif dt>=Fdt(y,8,23) and dt<=Fdt(y,9,22):   conStr = u'处女座'
    elif dt>=Fdt(y,9,23) and dt<=Fdt(y,10,23):  conStr = u'天秤座'
    elif dt>=Fdt(y,10,24) and dt<=Fdt(y,11,21): conStr = u'摩羯座'
    elif dt>=Fdt(y,11,22) and dt<=Fdt(y,12,21): conStr = u'射手座'
    else:
        conStr = u'摩竭座'
    return conStr


class BazhiDate():
    """
    输入阳历年月日时分,返回天干地支等.# 性别默认为男 , 使用为女: BazhiDate(dt,sex=0) 或 sex=False
    """
    def __init__(self,year,month,day,hour=0,minute=0,sex=1):
        try:
            dt = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute))
        except KeyError:
            raise KeyError
        if sex:
            self.sex = 1
        else:
            self.sex = 0
        self.yg,self.yz = getYearGanzhi(dt)
        self.mg,self.mz = getMonthGanzhi(dt)
        self.dg,self.dz = getDayGanzhi(dt)
        self.tg,self.tz = getHourGanzhi(dt)
        self.ygNum,self.yzNum = getYearGanzhi(dt,num=True)
        self.mgNum,self.mzNum = getMonthGanzhi(dt,num=True)
        self.dgNum,self.dzNum = getDayGanzhi(dt,num=True)
        self.tgNum,self.tzNum = getHourGanzhi(dt,num=True)
        self.dt = dt

    @property
    def trueSunDatetime(self):
        """出生真太阳时间"""
        return  getTrueSunDatetime(self.dt)

    @property
    def shuXiang(self):
        return getShuxiang(self.dt)

    # 农历日期
    def lunarDate_cn(self,sx=False):
        lunarDT = lunardate.LunarDate.fromSolarDate(self.dt.year,self.dt.month,self.dt.day)
        lunarM = getLunarMonth_cn(lunarDT.month)
        lunarD = getLunarDay_cn(lunarDT.day)
        lunarY = self.yg+self.yz
        if sx:
            return lunarY+"("+self.shuXiang+")"+lunarM+lunarD
        return lunarY+u"年"+lunarM+lunarD


    def ganzhiList(self,num=False):
        if num:
            return (self.ygNum,self.yzNum,self.mgNum,self.mzNum,self.dgNum,self.dzNum,self.tgNum,self.tzNum)
        return (self.yg,self.yz,self.mg,self.mz,self.dg,self.dz,self.tg,self.tz)


    @property
    def wuXing(self):
        """天干地支转化五行属性
        """
        res = {u'金':0, u'木':0, u'水':0, u'火':0, u'土':0}
        tgdz = "".join(self.ganzhi)
        for i in tgdz:
            a = ganzhi2Wuxing(i)
            if a in res:
                res[a] += 1
        return res.items()

    @property
    def naYinList(self):
        """返回八字纳音"""
        res = []
        for gz in [self.yg+self.yz, self.mg+self.mz, self.dg+self.dz, self.tg+self.tz]:
            res.append(ganzhi2Nayin(gz))
        return res


    #  胎元 IN:出生月的天干,地支 unicode, intro:人之生月后紧接着这个月的天干与生日后的第三个月的地支
    def taiYuan(self,num=False):
        mg=self.mg
        mz=self.mz
        try:
            ganInt = TIAN_GAN.index(mg)
            zhiInt = DI_ZHI.index(mz)
            ganNewInt = (ganInt+1)%10
            zhiNewInt = (zhiInt+3)%12
            if num:
                return (ganNewInt,zhiNewInt)
            return (TIAN_GAN[ganNewInt]+DI_ZHI[zhiNewInt])
        except:pass
        return ""


    # OUT:命宫 天干,地支  IN:年干,月支,时支 intro:把生时落在生月支上，顺数至卯，卯就为命宫。
    def mingGong(self,num=False):
        TG = u'甲,己,乙,庚,丙,辛,壬,丁,戊,癸'.split(',')        # 甲己丙作首,乙庚戊为初,丙辛寻耿起,丁壬壬顺流,戊癸甲上求.
        DZ = u'寅,卯,辰,巳,午,未,申,酉,戌,亥,子,丑'.split(",")   # 命宫地支 起位 1开始
        # DZ = u'*,子,亥,戌,酉,申,未,午,巳,辰,卯,寅,丑'.split(",") # 地支起位以子1,亥2,....丑12
        # 以DZ所算的 时支+月支. = 命宫地支
        try:
            # 求月支,如果已过当月中气(气节序号双数),月支加1
            mzInt = DZ.index(self.mz) + 1       # 月支序号
            jieqiMiddleDt = getJieqiList_byMonth(self.dt.year,self.dt.month,qi_only=True)[0]
            if self.dt >= jieqiMiddleDt:
                mzInt += 1
            # 时支序号
            tzInt = DZ.index(self.tz) + 1
            mingGong_zhi_int = (12+mzInt+tzInt - 10)%12
            if mingGong_zhi_int == 0:
                mingGong_zhi_int == 12
            # sumAll = mzInt + tzInt
            # if sumAll >=14:
            #     mingGong_zhi_int = 26 - sumAll
            # else:
            #     mingGong_zhi_int = 14 - sumAll
            # 命宫地支序号出来了,不过这个序号是对应DZ
            mingGong_zhi = DZ[mingGong_zhi_int-1]
            # 求命宫天干 与年上起月法相同.
            zhiNum = DI_ZHI.index(mingGong_zhi) + 1

            # 求天干与年上求月法一样.先转为标准起位的序号.
            ganList = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 0:11,1:12}
            yg = self.ygNum
            ganNum = (yg*2 +ganList[zhiNum])%10
            if ganNum == 0:
                ganNum = 10
            ganNum -= 1

            # yzInt = TG.index(self.yg)
            # mingGong_gan_int = (int(yzInt/2)*2+1 + mingGong_zhi_int)%10
            # mingGong_gan = TG2[mingGong_gan_int]
            # 对应TIAN_GAN ,DI_ZHI的序号
            if num:
                return (ganNum,zhiNum)
            return (TIAN_GAN[ganNum],DI_ZHI[zhiNum])
        except:
            return ""

    # 旬空
    @property
    def xunKong_list(self):
        res = []
        for i,j in [(self.ygNum,self.yzNum),(self.mgNum,self.mzNum),(self.dgNum,self.dzNum),(self.tgNum,self.tzNum)]:
            res.append("".join(getXunkong(i,j)))
        return res

    # 起运日期 需要用到节气数据具体到时辰.
    @property
    def daYun_date(self):
        return getQiyun_Date(self.dt,sex=self.sex)

    # 出年后几年几月起运 大约数
    @property
    def daYunAfterBirth(self):
        newDt = self.daYun_date
        deltaY = newDt.year - self.dt.year
        deltaM = newDt.month - self.dt.month
        if deltaM < 0:
            deltaM += 12
            deltaY -= 1
        return (deltaY,deltaM)



    # OUT:小运列表
    def xiaoYun_list(self,ages=1):
        return getXiaoyun_list(self.dt,sex=self.sex,ages=ages)

    # 星座
    @property
    def constellation(self):
        return getConstellation(self.dt)






