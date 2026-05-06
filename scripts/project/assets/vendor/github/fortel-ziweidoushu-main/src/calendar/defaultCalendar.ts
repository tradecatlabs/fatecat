import { calendar } from './jjonline/js-calendar-converter/calendar.js'
import { Ground } from '../model/ground'
import { Sky } from '../model/sky'
import type { Calendar } from './calender'

const defaultCalendar: Calendar = {
    solar2lunar: function (
        solarYear: number,
        solarMonth: number,
        solarDay: number,
    ): {
        lunarYear: number
        lunarMonth: number
        lunarDay: number
        isLeapMonth: boolean
        yearSky: Sky
        yearGround: Ground
        monthSky: Sky
        monthGround: Ground
        daySky: Sky
        dayGround: Ground
    } {
        const result = calendar.solar2lunar(solarYear, solarMonth, solarDay)
        if (this.solarMonthDays(solarYear, solarMonth) < solarDay) {
            throw new Error('Invalid date')
        }
        if (result !== -1) {
            return {
                lunarYear: result.lYear,
                lunarMonth: result.lMonth,
                lunarDay: result.lDay,
                isLeapMonth: result.isLeap,
                yearSky: Sky.getByName(result.gzYear[0]),
                yearGround: Ground.getByName(result.gzYear[1]),
                monthSky: Sky.getByName(result.gzMonth[0]),
                monthGround: Ground.getByName(result.gzMonth[1]),
                daySky: Sky.getByName(result.gzDay[0]),
                dayGround: Ground.getByName(result.gzDay[1]),
            }
        }
        throw new Error('Invalid date')
    },
    lunar2solar: function (
        lunarYear: number,
        lunarMonth: number,
        lunarDay: number,
        isLeapMonth: boolean,
    ): { solarYear: number; solarMonth: number; solarDay: number } {
        if (this.lunarMonthDays(lunarYear, lunarMonth, isLeapMonth) < lunarDay) {
            throw new Error('Invalid date')
        }
        const result = calendar.lunar2solar(lunarYear, lunarMonth, lunarDay, isLeapMonth)
        if (result !== -1) {
            return {
                solarYear: result.cYear,
                solarMonth: result.cMonth,
                solarDay: result.cDay,
            }
        }
        throw new Error('Invalid date')
    },
    lunarSkyGround: function (
        lunarYear: number,
        lunarMonth: number,
        lunarDay: number,
        isLeapMonth: boolean,
    ): { yearSky: Sky; yearGround: Ground; monthSky: Sky; monthGround: Ground; daySky: Sky; dayGround: Ground } {
        const result = calendar.lunar2solar(lunarYear, lunarMonth, lunarDay, isLeapMonth)
        if (result !== -1) {
            return {
                yearSky: Sky.getByName(result.gzYear[0]),
                yearGround: Ground.getByName(result.gzYear[1]),
                monthSky: Sky.getByName(result.gzMonth[0]),
                monthGround: Ground.getByName(result.gzMonth[1]),
                daySky: Sky.getByName(result.gzDay[0]),
                dayGround: Ground.getByName(result.gzDay[1]),
            }
        }
        throw new Error('Invalid date')
    },
    lunarMonthDays: function (year: number, month: number, leap: boolean): number {
        if (!leap) {
            return calendar.monthDays(year, month)
        } else {
            if (calendar.leapMonth(year) != month) {
                throw new Error('Invalid date')
            }
            return calendar.leapDays(year)
        }
    },
    solarMonthDays: function (year: number, month: number): number {
        return calendar.solarDays(year, month)
    },
}

export { defaultCalendar }
