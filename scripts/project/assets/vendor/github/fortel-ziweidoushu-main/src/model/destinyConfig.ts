import { DayTimeGround } from './dayTimeGround'
import { Ground } from './ground'
import { Sky } from './sky'

class DestinyConfig {
    year: number
    month: number
    day: number
    isLeapMonth: boolean
    yearSky: Sky
    yearGround: Ground
    monthSky: Sky
    monthGround: Ground
    daySky: Sky
    dayGround: Ground
    bornTimeGround: DayTimeGround
    configType: ConfigType
    gender: Gender

    constructor(params: {
        year: number
        month: number
        day: number
        isLeapMonth: boolean
        yearSky: Sky
        yearGround: Ground
        monthSky: Sky
        monthGround: Ground
        daySky: Sky
        dayGround: Ground
        bornTimeGround: DayTimeGround
        configType: ConfigType
        gender: Gender
    }) {
        const { year, month, day, isLeapMonth, yearSky, yearGround, monthSky, monthGround, daySky, dayGround, bornTimeGround, configType, gender } =
            params

        this.year = year
        this.month = month
        this.day = day
        this.isLeapMonth = isLeapMonth
        this.yearSky = yearSky
        this.yearGround = yearGround
        this.monthSky = monthSky
        this.monthGround = monthGround
        this.daySky = daySky
        this.dayGround = dayGround
        this.bornTimeGround = bornTimeGround
        this.configType = configType
        this.gender = gender
    }

    getLogicalMonth(): number {
        if (this.isLeapMonth && this.day > 15) {
            return this.month + 1
        } else {
            return this.month
        }
    }

    toJSON() {
        return {
            year: this.year,
            month: this.month,
            day: this.day,
            isLeapMonth: this.isLeapMonth,
            yearSky: this.yearSky,
            yearGround: this.yearGround,
            monthSky: this.monthSky,
            monthGround: this.monthGround,
            daySky: this.daySky,
            dayGround: this.dayGround,
            bornTimeGround: this.bornTimeGround,
            configType: configTypeDisplayName[this.configType],
            gender: genderDisplayName[this.gender],
        }
    }

    toString(): string {
        return JSON.stringify(this)
    }
}

enum ConfigType {
    GROUND = 'GROUND',
    SKY = 'SKY',
    HUMAN = 'HUMAN',
}

const configTypeDisplayName = {
    GROUND: '地盤',
    SKY: '天盤',
    HUMAN: '人盤',
}

enum Gender {
    M = 'M',
    F = 'F',
}

const genderDisplayName = {
    M: '男',
    F: '女',
}

export { DestinyConfig, ConfigType, Gender }
