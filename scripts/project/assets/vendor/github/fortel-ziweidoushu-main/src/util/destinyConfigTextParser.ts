import { Calendar, CalendarType } from '../calendar/calender'
import { defaultCalendar } from '../calendar/defaultCalendar'
import { DayTimeGround } from '../model/dayTimeGround'
import { ConfigType, Gender } from '../model/destinyConfig'
import { str2Uni } from '../utils'

const CHINESE_NUMBER_CHARACTERS = '零一二三四五六七八九十廿'
const CHINESE_NUMBER_CHARACTERS_UNICODE = str2Uni(CHINESE_NUMBER_CHARACTERS)
const ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS = '零一二三四五六七八九'
const ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE = str2Uni(ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS)
// const CHINESE_ONE_TO_TWELVE = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
const TEN_UNICODE = str2Uni('十')
const GROUND_CHAR = '子丑寅卯辰巳午未申酉戌亥'
const GROUND_CHAR_UNICODE = str2Uni(GROUND_CHAR)

function chineseNumToDecimal(input: string): number | null {
    if (input.match(/[0-9]+/)) {
        return parseInt(input)
    }
    const matches = input.match(new RegExp(`[${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]+`, 'u'))
    if (matches) {
        let value = 0
        for (let i = 0; i < input.length; i++) {
            value *= 10
            if (ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS.includes(input.charAt(i))) {
                value += ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS.indexOf(input.charAt(i))
            }
            if (input.charAt(i) === '兩') {
                value += 2
            }
        }
        return value
    } else {
        return null
    }
}

function text2DestinyConfig(input: string, calendar: Calendar = defaultCalendar) {
    try {
        let calendarType: CalendarType | null = null
        let year: number | null = null
        let month: number | null = null
        let day: number | null = null
        let isLeapMonth = false
        let bornTimeGround: DayTimeGround | null = null
        let hour: number | null = null
        let minute: number | null = null
        let gender: Gender | null = null
        let configType: ConfigType | null = null

        if (['農曆', '農歷', '舊曆', '舊歷'].find((keyword) => input.includes(keyword))) {
            calendarType = CalendarType.LUNAR
        } else if (['西曆', '西歷', '公曆', '公歷', '新曆', '新歷'].find((keyword) => input.includes(keyword))) {
            calendarType = CalendarType.SOLAR
        }

        {
            const matches = input.match(/([0-9]{2,4})-([0-9]{1,2})-([0-9]{1,2})/)
            if (matches) {
                calendarType = CalendarType.SOLAR
                year = parseInt(matches[1])
                month = parseInt(matches[2])
                day = parseInt(matches[3])
            }
        }

        if (input.includes('年')) {
            const regex = new RegExp(`([0-9]{2,4})?([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]{2,4})?${str2Uni('年')}`, 'u')
            const matches = input.match(regex)
            if (matches) {
                if (matches[1]) {
                    year = parseInt(matches[1])
                } else if (matches[2]) {
                    year = chineseNumToDecimal(matches[2])
                }
            }
        }

        if (year !== null && year < 100) {
            const thisYear = new Date().getFullYear()
            const thisYearFirstTwoDigit = thisYear - (thisYear % 100)
            const thisYearLastTwoDigit = thisYear % 100
            if (year < thisYearLastTwoDigit + 1) {
                year = thisYearFirstTwoDigit + year
            } else {
                year = thisYearFirstTwoDigit + year - 100
            }
        }

        if (input.match(new RegExp(`[${str2Uni('閏閠潤')}][0-9${CHINESE_NUMBER_CHARACTERS_UNICODE}]+${str2Uni('月')}`, 'u'))) {
            isLeapMonth = true
            calendarType = CalendarType.LUNAR
        }

        if (input.includes('月')) {
            let monthDetermined = false
            if (input.includes('正月')) {
                month = 1
                monthDetermined = true
            } else if (input.includes('十月')) {
                month = 10
                monthDetermined = true
            }

            if (!monthDetermined) {
                //十?月
                const matches = input.match(new RegExp(`[${TEN_UNICODE}]([${CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${str2Uni('月')}`, 'u'))
                if (matches && matches[1]) {
                    const digit = chineseNumToDecimal(matches[1])
                    if (digit) {
                        month = 10 + digit
                        monthDetermined = true
                    }
                }
            }

            if (!monthDetermined) {
                //?月
                const matches = input.match(new RegExp(`([${CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${str2Uni('月')}`, 'u'))
                if (matches && matches[1]) {
                    month = chineseNumToDecimal(matches[1])
                    monthDetermined = true
                }
            }

            if (!monthDetermined) {
                const matches = input.match(new RegExp(`([0-9]{1,2})${str2Uni('月')}`, 'u'))
                if (matches && matches[1]) {
                    month = parseInt(matches[1])
                    monthDetermined = true
                }
            }
        }

        let dayDetermined = false
        if (input.includes('初')) {
            {
                const matches = input.match(new RegExp(`${str2Uni('初')}([0-9]{1,2})`, 'u'))
                if (matches && matches[1]) {
                    calendarType = CalendarType.LUNAR

                    day = parseInt(matches[1])
                    dayDetermined = true
                }
            }

            if (!dayDetermined) {
                const matches = input.match(
                    new RegExp(`${str2Uni('初')}(${str2Uni('十')}?)([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)`, 'u'),
                )
                if (matches) {
                    calendarType = CalendarType.LUNAR

                    if (matches[1] && !matches[2]) {
                        day = 10
                        dayDetermined = true
                    } else if (matches[1] && matches[2]) {
                        const digit = chineseNumToDecimal(matches[2])
                        if (digit) {
                            day = 10 + digit
                            dayDetermined = true
                        }
                    } else if (!matches[1] && matches[2]) {
                        const digit = chineseNumToDecimal(matches[2])
                        if (digit) {
                            day = digit
                            dayDetermined = true
                        }
                    }
                }
            }
        } else if (input.includes('日') || input.includes('號')) {
            const dayCharPattern = `[${str2Uni('日號')}]`

            if (!dayDetermined) {
                const matches = input.match(new RegExp(`([0-9]{1,2})?${dayCharPattern}`, 'u'))
                if (matches && matches[1]) {
                    day = parseInt(matches[1])
                    dayDetermined = true
                }
            }

            if (!dayDetermined) {
                if (input.includes('三十日') || input.includes('三十號')) {
                    day = 30
                    dayDetermined = true
                } else if (input.includes('三十一日') || input.includes('三十一號')) {
                    day = 31
                    dayDetermined = true
                }
            }

            if (!dayDetermined) {
                const matches = input.match(
                    new RegExp(`(${str2Uni('廿')}|${str2Uni('二十')})([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${dayCharPattern}`, 'u'),
                )
                if (matches && matches[1]) {
                    const digit = chineseNumToDecimal(matches[2])
                    if (digit) {
                        day = matches[2] ? 20 + digit : 20
                    }
                    dayDetermined = true
                }
            }

            if (!dayDetermined) {
                const matches = input.match(
                    new RegExp(`${str2Uni('十')}([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${dayCharPattern}`, 'u'),
                )
                if (matches && matches[1]) {
                    const digit = chineseNumToDecimal(matches[1])
                    if (digit) {
                        day = matches[1] ? 10 + digit : 10
                        dayDetermined = true
                    }
                }
            }

            if (!dayDetermined) {
                const matches = input.match(new RegExp(`([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${dayCharPattern}`, 'u'))
                if (matches && matches[1]) {
                    day = chineseNumToDecimal(matches[1])
                    dayDetermined = true
                }
            }
        }

        let hourDetermined = false
        let minuteDetermined = false

        //hour:minute
        {
            const matches = input.match(new RegExp(`([0-9]{1,2}):([0-9]{2})`))
            if (matches && matches[1] && matches[2]) {
                hour = parseInt(matches[1])
                minute = parseInt(matches[2])
                hourDetermined = true
                minuteDetermined = true
            }
        }

        //hour
        const hourCharPattern = `[${str2Uni('時點')}]`

        if (!hourDetermined) {
            if (input.includes('兩點')) {
                hour = 2
                hourDetermined = true
            }
        }

        if (!hourDetermined) {
            const matches = input.match(
                new RegExp(`(${str2Uni('廿')}|(?!${str2Uni('二十')}))([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${hourCharPattern}`, 'u'),
            )
            if (matches && matches[1] && matches[2]) {
                const digit = chineseNumToDecimal(matches[2])
                if (digit) {
                    hour = matches[2] ? 20 + digit : 20
                    hourDetermined = true
                }
            }
        }

        if (!hourDetermined) {
            const matches = input.match(
                new RegExp(
                    `([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${str2Uni(
                        '十',
                    )}([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${hourCharPattern}`,
                    'u',
                ),
            )
            if (matches) {
                const digit1 = chineseNumToDecimal(matches[1])
                const digit2 = chineseNumToDecimal(matches[2])
                hour = 10
                if (digit1) {
                    hour = digit1 * 10
                }
                if (digit2) {
                    hour += digit2
                }
                hourDetermined = true
            }
        }

        if (!hourDetermined) {
            const matches = input.match(new RegExp(`([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${hourCharPattern}`, 'u'))
            if (matches && matches[1]) {
                hour = chineseNumToDecimal(matches[1])
                hourDetermined = true
            }
        }

        if (!hourDetermined) {
            const matches = input.match(new RegExp(`([0-9]{1,2})${hourCharPattern}`, 'u'))
            if (matches && matches[1]) {
                hour = parseInt(matches[1])
                hourDetermined = true
            }
        }

        if (!hourDetermined) {
            const matches = input.match(new RegExp(`([${GROUND_CHAR_UNICODE}])${hourCharPattern}`, 'u'))
            if (matches && matches[1] && GROUND_CHAR.indexOf(matches[1]) >= 0) {
                if (matches[1] === '子') {
                    hour = 0
                    hourDetermined = true
                } else {
                    hour = GROUND_CHAR.indexOf(matches[1]) * 2 - 1
                    hourDetermined = true
                }
            }
        }

        if (
            input.includes('下午') ||
            input.includes('下晝') ||
            input.includes('黃昏') ||
            input.includes('夜') ||
            input.includes('晚') ||
            input.includes('PM') ||
            input.includes('pm') ||
            input.includes('P.M.') ||
            input.includes('p.m.')
        ) {
            if (hour !== null && hour < 12) {
                hour += 12
            }
        }

        if (hour != null && (input.includes('晚上') || input.includes('半夜') || input.includes('凌晨'))) {
            if (hour >= 6 && hour < 12) {
                hour += 12
            } else if (hour > 12 && hour <= 17) {
                hour -= 12
            } else if (hour === 12) {
                hour = 0
            }
        }

        //minute

        const minuteCharPattern = `[${str2Uni('分')}]`

        if (!minuteDetermined) {
            if (input.includes('時半') || input.includes('點半')) {
                minute = 30
                minuteDetermined = true
            }
        }

        if (!minuteDetermined) {
            const matches = input.match(
                new RegExp(
                    `([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}])[${TEN_UNICODE}]([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${minuteCharPattern}`,
                    'u',
                ),
            )
            if (matches && matches[1]) {
                const digit1 = chineseNumToDecimal(matches[1])
                const digit2 = chineseNumToDecimal(matches[2])
                if (digit1) {
                    minute = digit1 * 10 + (digit2 ?? 0)
                    minuteDetermined = true
                }
            }
        }

        if (!minuteDetermined) {
            const matches = input.match(
                new RegExp(
                    `(${str2Uni('廿')}|(?!${str2Uni('二十')}))([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${minuteCharPattern}`,
                    'u',
                ),
            )
            if (matches && matches[1]) {
                const digit = chineseNumToDecimal(matches[2])
                if (digit) {
                    minute = matches[2] ? 20 + digit : 20
                    minuteDetermined = true
                }
            }
        }

        if (!minuteDetermined) {
            const matches = input.match(
                new RegExp(
                    `([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${str2Uni(
                        '十',
                    )}([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${minuteCharPattern}`,
                    'u',
                ),
            )
            if (matches) {
                const digit1 = chineseNumToDecimal(matches[1])
                const digit2 = chineseNumToDecimal(matches[2])
                minute = 10
                if (digit1) {
                    minute = digit1 * 10
                }
                if (digit2) {
                    minute += digit2
                }
                minuteDetermined = true
            }
        }

        if (!minuteDetermined) {
            const matches = input.match(new RegExp(`([${ZERO_TO_NINE_CHINESE_NUMBER_CHARACTERS_UNICODE}]?)${minuteCharPattern}`, 'u'))
            if (matches && matches[1]) {
                minute = chineseNumToDecimal(matches[1])
                minuteDetermined = true
            }
        }

        if (!minuteDetermined) {
            const matches = input.match(new RegExp(`([0-9]{1,2})${minuteCharPattern}`, 'u'))
            if (matches && matches[1]) {
                minute = parseInt(matches[1])
                minuteDetermined = true
            }
        }

        if (typeof hour === 'number') {
            bornTimeGround = DayTimeGround.getByHour(hour)
        }

        //盤
        let configTypeDetermined = false

        {
            const matches = input.match(new RegExp(`([${str2Uni('地天人')}])${str2Uni('盤')}`, 'u'))
            if (matches && matches[1]) {
                if (matches[1] === '地') {
                    configType = ConfigType.GROUND
                } else if (matches[1] === '人') {
                    configType = ConfigType.HUMAN
                } else {
                    configType = ConfigType.SKY
                }
                configTypeDetermined = true
            }
        }

        if (!configTypeDetermined) {
            if (typeof minute === 'number') {
                if (bornTimeGround) {
                    if (hour && hour >= 1 && hour < 23) {
                        if (hour === bornTimeGround.hourStart && minute <= 15) {
                            configType = ConfigType.GROUND
                        } else if (hour === bornTimeGround.hourStart + 1 && minute >= 45) {
                            configType = ConfigType.HUMAN
                        } else {
                            configType = ConfigType.SKY
                        }
                    } else if (hour) {
                        if (hour === 23 && minute <= 15) {
                            configType = ConfigType.GROUND
                        } else if (hour === 0 && minute >= 45) {
                            configType = ConfigType.HUMAN
                        } else {
                            configType = ConfigType.SKY
                        }
                    }
                }
            }
        }

        if (input.includes('男') || input.includes('先生')) {
            gender = Gender.M
        } else if (input.includes('女') || input.includes('小姐') || input.includes('太太')) {
            gender = Gender.F
        }

        if (calendarType === null) {
            if (year && year >= 1900 && year <= 2100 && month && day) {
                let lunarError: unknown = null
                try {
                    calendar.lunar2solar(year, month, day, isLeapMonth)
                } catch (e) {
                    lunarError = e
                }
                let solarError: unknown = null
                try {
                    calendar.solar2lunar(year, month, day)
                } catch (e) {
                    solarError = e
                }

                if (solarError && !lunarError) {
                    calendarType = CalendarType.LUNAR
                } else if (!solarError && lunarError) {
                    calendarType = CalendarType.SOLAR
                }
            }
        }

        return {
            calendarType,
            year,
            month,
            day,
            isLeapMonth,
            bornTimeGround,
            hour,
            minute,
            gender,
            configType,
        }
    } catch (e) {
        console.error(e)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        throw new Error('Invalid input', e as any)
    }
}

const destinyConfigTextParser = {
    parse: text2DestinyConfig,
}

export { destinyConfigTextParser }
