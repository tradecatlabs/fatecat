import { DayTimeGround } from '../src/model/dayTimeGround'
import { ConfigType, Gender } from '../src/model/destinyConfig'
import { destinyConfigTextParser } from '../src/util/destinyConfigTextParser'
import { CalendarType } from '../src/calendar/calender'

describe('Test DestinyConfig', () => {
    it('Test destinyConfigTextParser', () => {
        const destinyConfig = destinyConfigTextParser.parse('1952年12月15日寅時天盤女')

        expect(destinyConfig.year).toBe(1952)
        expect(destinyConfig.month).toBe(12)
        expect(destinyConfig.day).toBe(15)
        expect(destinyConfig.isLeapMonth).toBe(false)
        expect(destinyConfig.bornTimeGround).toBe(DayTimeGround.getByName('寅時'))
        expect(destinyConfig.configType).toBe(ConfigType.SKY)
        expect(destinyConfig.gender).toBe(Gender.F)
    })

    it('Test calendar type', () => {
        expect(destinyConfigTextParser.parse('農曆1990年3月1日 9時十分男').calendarType).toBe(CalendarType.LUNAR)
        expect(destinyConfigTextParser.parse('農歷1990年3月1日 9時十分男').calendarType).toBe(CalendarType.LUNAR)
        expect(destinyConfigTextParser.parse('舊曆1990年3月1日 9時十分男').calendarType).toBe(CalendarType.LUNAR)
        expect(destinyConfigTextParser.parse('舊歷1990年3月1日 9時十分男').calendarType).toBe(CalendarType.LUNAR)
        expect(destinyConfigTextParser.parse('西曆1990年3月1日 9時十分男').calendarType).toBe(CalendarType.SOLAR)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 9時十分男').calendarType).toBe(CalendarType.SOLAR)
        expect(destinyConfigTextParser.parse('公曆1990年3月1日 9時十分男').calendarType).toBe(CalendarType.SOLAR)
        expect(destinyConfigTextParser.parse('公歷1990年3月1日 9時十分男').calendarType).toBe(CalendarType.SOLAR)
        expect(destinyConfigTextParser.parse('新曆1990年3月1日 9時十分男').calendarType).toBe(CalendarType.SOLAR)
        expect(destinyConfigTextParser.parse('新歷1990年3月1日 9時十分男').calendarType).toBe(CalendarType.SOLAR)

        expect(destinyConfigTextParser.parse('1990年3月初一 9時十分男').calendarType).toBe(CalendarType.LUNAR)

        expect(destinyConfigTextParser.parse('2017年閏6月24日 9時十分男').calendarType).toBe(CalendarType.LUNAR)
        expect(destinyConfigTextParser.parse('2017年閠6月24日 9時十分男').calendarType).toBe(CalendarType.LUNAR)
        expect(destinyConfigTextParser.parse('2017年潤6月24日 9時十分男').calendarType).toBe(CalendarType.LUNAR)

        expect(destinyConfigTextParser.parse('1990-3-1 9時十分男').calendarType).toBe(CalendarType.SOLAR)
        expect(destinyConfigTextParser.parse('1990-03-01 9時十分男').calendarType).toBe(CalendarType.SOLAR)

        expect(destinyConfigTextParser.parse('1990年3月一日 9時十分男').calendarType).toBe(null)
    })

    it('Test year', () => {
        expect(destinyConfigTextParser.parse('一九九零年3月1日 9時十分男').year).toBe(1990)
        expect(destinyConfigTextParser.parse('1990年3月1日 9時十分男').year).toBe(1990)
    })

    it('Test month', () => {
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 9時十分男').month).toBe(3)
        expect(destinyConfigTextParser.parse('西歷1990年三月1日 9時十分男').month).toBe(3)
        expect(destinyConfigTextParser.parse('西歷1990年11月1日 9時十分男').month).toBe(11)
        expect(destinyConfigTextParser.parse('西歷1990年十一月1日 9時十分男').month).toBe(11)
    })

    it('Test day', () => {
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 9時十分男').day).toBe(1)
        expect(destinyConfigTextParser.parse('1990年3月初一 9時十分男').day).toBe(1)
        expect(destinyConfigTextParser.parse('1990年3月廿一日 9時十分男').day).toBe(21)
        expect(destinyConfigTextParser.parse('1990年3月廿一號 9時十分男').day).toBe(21)
        expect(destinyConfigTextParser.parse('1990年3月十三號 9時十分男').day).toBe(13)
        expect(destinyConfigTextParser.parse('1990年3月13號 9時十分男').day).toBe(13)
        expect(destinyConfigTextParser.parse('1990年3月二十一號 9時十分男').day).toBe(21)
        expect(destinyConfigTextParser.parse('1990年3月二十一日 9時十分男').day).toBe(21)
        expect(destinyConfigTextParser.parse('1990年3月三十日 9時十分男').day).toBe(30)
        expect(destinyConfigTextParser.parse('1990年3月三十一日 9時十分男').day).toBe(31)
        expect(destinyConfigTextParser.parse('1990年3月21號 9時十分男').day).toBe(21)
        expect(destinyConfigTextParser.parse('1990年3月30號 9時十分男').day).toBe(30)
        expect(destinyConfigTextParser.parse('1990年3月31號 9時十分男').day).toBe(31)
    })

    it('Test hour', () => {
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 9時十分男').hour).toBe(9)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 9點十分男').hour).toBe(9)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 23時十分男').hour).toBe(23)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 11時十分男').hour).toBe(11)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八點十分男').hour).toBe(8)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時十分男').hour).toBe(8)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 十時十分男').hour).toBe(10)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 十一時十分男').hour).toBe(11)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 早上五時十分男').hour).toBe(5)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 上午五時十分男').hour).toBe(5)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 下午五時十分男').hour).toBe(17)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 下午5時十分男').hour).toBe(17)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 下午5時十分男').hour).toBe(17)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 下晝5時十分男').hour).toBe(17)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 黃昏6時十分男').hour).toBe(18)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 傍晚6時十分男').hour).toBe(18)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 PM 6時十分男').hour).toBe(18)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 pm 6時十分男').hour).toBe(18)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 P.M. 6時十分男').hour).toBe(18)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 p.m. 6時十分男').hour).toBe(18)

        expect(destinyConfigTextParser.parse('西歷1990年3月1日 晚上十一時十分男').hour).toBe(23)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 晚上一時十分男').hour).toBe(1)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 半夜11時十分男').hour).toBe(23)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 半夜1時十分男').hour).toBe(1)

        expect(destinyConfigTextParser.parse('西歷1990年3月1日 7:30男').hour).toBe(7)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 07:30男').hour).toBe(7)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 20:15男').hour).toBe(20)

        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時半男').hour).toBe(8)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八點半男').hour).toBe(8)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 十時半男').hour).toBe(10)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 十點半男').hour).toBe(10)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 十二時半男').hour).toBe(12)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 十二點半男').hour).toBe(12)

        expect(destinyConfigTextParser.parse('西歷1990年3月1日 8時半男').hour).toBe(8)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 8點半男').hour).toBe(8)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 10時半男').hour).toBe(10)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 10點半男').hour).toBe(10)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 12時半男').hour).toBe(12)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 12點半男').hour).toBe(12)

        expect(destinyConfigTextParser.parse('西歷1990年3月1日 零時十分男').hour).toBe(0)
    })

    it('Test minute', () => {
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 20:15男').minute).toBe(15)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時五分男').minute).toBe(5)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時5分男').minute).toBe(5)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時十分男').minute).toBe(10)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時10分男').minute).toBe(10)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時十四分男').minute).toBe(14)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時14分男').minute).toBe(14)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時二十分男').minute).toBe(20)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時20分男').minute).toBe(20)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時三十五分男').minute).toBe(35)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時35分男').minute).toBe(35)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時半男').minute).toBe(30)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八點半男').minute).toBe(30)
    })

    it('Test config type', () => {
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時男').configType).toBe(null)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時五分男 天盤').configType).toBe(ConfigType.SKY)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時五分男 地盤').configType).toBe(ConfigType.GROUND)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時五分男 人盤').configType).toBe(ConfigType.HUMAN)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 一時五分男').configType).toBe(ConfigType.GROUND)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 二時半男').configType).toBe(ConfigType.SKY)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 二時50分男').configType).toBe(ConfigType.HUMAN)
    })

    it('Test gender', () => {
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時男').gender).toBe(Gender.M)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時先生').gender).toBe(Gender.M)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時女').gender).toBe(Gender.F)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時小姐').gender).toBe(Gender.F)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時太太').gender).toBe(Gender.F)
        expect(destinyConfigTextParser.parse('西歷1990年3月1日 八時').gender).toBe(null)
    })
})
