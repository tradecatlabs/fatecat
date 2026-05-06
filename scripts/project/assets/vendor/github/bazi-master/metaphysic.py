import datetime
import math
import ganzhi
import wuxingData

tiangans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
wuxingNames = ["金", "木", "水", "火", "土"]

# wuxingDicForTiangan = {
#     "甲":"阳木",
#     "乙":"阴木",
#     "丙":"阳火",
#     "丁":"阴火",
#     "戊":"阳土",
#     "己":"阴土",
#     "庚":"阳金",
#     "辛":"阴金",
#     "壬":"阳水",
#     "癸":"阴水"
# }
# wuxingDicForDizhi = {
#     "子":"阳水",
#     "丑":"阴土",
#     "寅":"阳木",
#     "卯":"阴木",
#     "辰":"阳土",
#     "巳":"阴火",
#     "午":"阳火",
#     "未":"阴土",
#     "申":"阳金",
#     "酉":"阴金",
#     "戌":"阳土",
#     "亥":"阴水"
# }

wuxingDicForTiangan = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水"
}
wuxingDicForDizhi = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水"
}


def calculateTime(tianganOfDay, time):  # tiangan%10 : 10
    tianganIndex = (2 * tianganOfDay - 1) % 10
    if time == 23 or time == 0 or time == 24:
        dizhi = dizhis[0]
        dizhiIndex = 0
    else:
        dizhiIndex = time / 2
        if dizhiIndex >= 0.5:
            dizhiIndex = math.ceil(dizhiIndex)
        else:
            dizhiIndex = round(dizhiIndex)
        dizhi = dizhis[dizhiIndex]
    return tiangans[(tianganIndex - 1 + dizhiIndex) % 10] + dizhi


def getShenChenBaZi(year, month, day, time):
    data = ganzhi.day(year, month, day)
    tianganOfDay = data[2]
    tianganOfDaySymbol = tiangans.index(tianganOfDay) + 1
    ganzhiOfTime = calculateTime(tianganOfDaySymbol, time)
    return data[0] + '-' + ganzhiOfTime


def getWuXing(bazi):
    bazilist = str(bazi).split("-")
    wuxingList = []
    countForJin = 0
    countForMu = 0
    countForShui = 0
    countForHuo = 0
    countForTu = 0
    for bazi in bazilist:
        wuxingList.append(wuxingDicForTiangan[bazi[0]])
        wuxingList.append(wuxingDicForDizhi[bazi[1]])
    for wuxing in wuxingList:
        if wuxing == "金":
            countForJin = countForJin + 1
        elif wuxing == "木":
            countForMu = countForMu + 1
        elif wuxing == "水":
            countForShui = countForShui + 1
        elif wuxing == "火":
            countForHuo = countForHuo + 1
        else:
            countForTu = countForTu + 1
    scoreForJin = round(countForJin / 8, 2)
    scoreForMu = round(countForMu / 8, 2)
    scoreForShui = round(countForShui / 8, 2)
    scoreForHuo = round(countForHuo / 8, 2)
    scoreForTu = round(countForTu / 8, 2)
    return (scoreForJin, scoreForMu, scoreForShui, scoreForHuo, scoreForTu)


def main():
    # birthYear = input("please input your birth year: ")
    # birthMonth = input("please input your birth month: ")
    # birthDay = input("please input your birth day: ")
    # birthTime = input("please input your birth time: ")
    shenchenbazi = getShenChenBaZi(1994, 5, 8, 9)
    # shenchenbazi = getShenChenBaZi(
    #     int(birthYear), int(birthMonth), int(birthDay), int(birthTime))
    print("你的生辰八字是: %s" % (shenchenbazi))
    wuxing = getWuXing(shenchenbazi)
    print("您的生辰八字五行指数为金：%.2f,木：%.2f,水：%.2f,火：%.2f,土:%.2f" % (wuxing))
    minScore = 0
    minIndexes = []
    for index, value in enumerate(wuxing):
        if value == minScore:
            minIndexes.append(index)
    lackingWuxings = []
    for minIndex in minIndexes:
        lackingWuxings.append(wuxingNames[minIndex])
    wuxingCharacters = []
    print(lackingWuxings)
    for lackingWuxing in lackingWuxings:
        lackingWuxingCharacters = wuxingData.wuxingDic.get(lackingWuxing)
        if lackingWuxingCharacters:
            wuxingCharacters.extend(wuxingData.wuxingDic.get(lackingWuxing))
    return wuxingCharacters

if __name__ == '__main__':
    main()