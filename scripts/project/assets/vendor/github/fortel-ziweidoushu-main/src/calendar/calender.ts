import { Ground } from '../model/ground'
import { Sky } from '../model/sky'

export enum CalendarType {
    LUNAR = 'LUNAR',
    SOLAR = 'SOLAR',
}

export declare type Calendar = {
    solar2lunar: (
        solarYear: number,
        solarMonth: number,
        solarDay: number,
    ) => {
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
    }

    lunar2solar: (
        lunarYear: number,
        lunarMonth: number,
        lunarDay: number,
        isLeapMonth: boolean,
    ) => {
        solarYear: number
        solarMonth: number
        solarDay: number
    }

    lunarSkyGround: (
        lunarYear: number,
        lunarMonth: number,
        lunarDay: number,
        isLeapMonth: boolean,
    ) => {
        yearSky: Sky
        yearGround: Ground
        monthSky: Sky
        monthGround: Ground
        daySky: Sky
        dayGround: Ground
    }

    lunarMonthDays: (year: number, month: number, leap: boolean) => number
    solarMonthDays: (year: number, month: number) => number
}
