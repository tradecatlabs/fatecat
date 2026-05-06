import { DayTimeGround } from '../model/dayTimeGround'
import { ConfigType, DestinyConfig, Gender } from '../model/destinyConfig'
import { defaultCalendar } from '../calendar/defaultCalendar'
import { Calendar, CalendarType } from '../calendar/calender'
import { destinyConfigTextParser } from './destinyConfigTextParser'

export class DestinyConfigBuilder {
    static withSolar(params: {
        year: number
        month: number
        day: number
        bornTimeHour?: number
        bornTimeGround?: DayTimeGround
        configType: ConfigType
        gender: Gender
        calendar?: Calendar
    }) {
        const { year, month, day, bornTimeHour, configType = ConfigType.SKY, gender } = params
        let { bornTimeGround, calendar } = params
        calendar ??= defaultCalendar

        const lunarDate = calendar.solar2lunar(year, month, day)
        const { yearSky, yearGround, monthSky, monthGround, daySky, dayGround } = lunarDate

        if (bornTimeHour !== undefined) {
            bornTimeGround = DayTimeGround.getByHour(bornTimeHour)
        } else if (bornTimeGround === undefined) {
            throw new Error('Cannot find born time ground')
        }

        return new DestinyConfig({
            year: lunarDate.lunarYear,
            month: lunarDate.lunarMonth,
            day: lunarDate.lunarDay,
            isLeapMonth: lunarDate.isLeapMonth,
            yearSky,
            yearGround,
            monthSky,
            monthGround,
            daySky,
            dayGround,
            bornTimeGround,
            configType,
            gender,
        })
    }

    static withlunar(params: {
        year: number
        month: number
        day: number
        isLeapMonth?: boolean
        bornTimeHour?: number
        bornTimeGround?: DayTimeGround
        configType: ConfigType
        gender: Gender
        calendar?: Calendar
    }) {
        const { year, month, day, isLeapMonth = false, bornTimeHour, configType = ConfigType.SKY, gender } = params
        let { bornTimeGround, calendar } = params
        calendar ??= defaultCalendar
        const calendarResult = calendar.lunarSkyGround(year, month, day, isLeapMonth)
        const { yearSky, yearGround, monthSky, monthGround, daySky, dayGround } = calendarResult

        if (bornTimeHour !== undefined && !bornTimeGround) {
            bornTimeGround = DayTimeGround.getByHour(bornTimeHour)
        }
        if (bornTimeGround === undefined) {
            throw new Error('Cannot find born time ground')
        }

        return new DestinyConfig({
            year,
            month,
            day,
            isLeapMonth,
            yearSky,
            yearGround,
            monthSky,
            monthGround,
            daySky,
            dayGround,
            bornTimeGround,
            configType,
            gender,
        })
    }

    static withText(input: string, calendar: Calendar = defaultCalendar) {
        input = input.trim().replaceAll('/s+', ' ')

        const parseResult = destinyConfigTextParser.parse(input, calendar)

        const { year, month, day, isLeapMonth, bornTimeGround, hour } = parseResult
        let { calendarType, gender, configType } = parseResult

        if (calendarType === null) {
            calendarType = CalendarType.LUNAR
        }
        if (gender === null) {
            gender = Gender.M
        }
        if (configType === null) {
            configType = ConfigType.SKY
        }

        if (!year || !month || !day || !bornTimeGround) {
            throw new Error('Invalid input')
        }

        if (calendarType === CalendarType.LUNAR) {
            return DestinyConfigBuilder.withlunar({
                year,
                month,
                day,
                isLeapMonth,
                bornTimeHour: hour ?? undefined,
                bornTimeGround: bornTimeGround ?? undefined,
                configType,
                gender,
                calendar,
            })
        } else {
            return DestinyConfigBuilder.withSolar({
                year,
                month,
                day,
                bornTimeHour: hour ?? undefined,
                bornTimeGround: bornTimeGround ?? undefined,
                configType,
                gender,
                calendar,
            })
        }
    }
}
