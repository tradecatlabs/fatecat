/* eslint-disable @typescript-eslint/no-explicit-any */
import { defaultCalendar } from '../src/calendar/defaultCalendar'

describe('Test calendar', () => {
    it('Test lunar 1990-1-30 is invalid date', () => {
        let e = null
        try {
            defaultCalendar.lunar2solar(1990, 1, 30, false)
        } catch (error: any) {
            e = error
        }
        expect(e).toBeInstanceOf(Error)
    })

    it('Test lunar 1990-4-1 leap is invalid date', () => {
        let e = null
        try {
            defaultCalendar.lunar2solar(1990, 4, 1, true)
        } catch (error: any) {
            e = error
        }
        expect(e).toBeInstanceOf(Error)
    })

    it('Test solar 1996-07-15 convert to lunar 1996-05-30', () => {
        const result = defaultCalendar.solar2lunar(1996, 7, 15)
        expect(result.lunarYear).toBe(1996)
        expect(result.lunarMonth).toBe(5)
        expect(result.lunarDay).toBe(30)
        expect(result.isLeapMonth).toBe(false)
    })

    it('Test solar 1996-08-14 convert to lunar 1996-07-01', () => {
        const result = defaultCalendar.solar2lunar(1996, 8, 14)
        expect(result.lunarYear).toBe(1996)
        expect(result.lunarMonth).toBe(7)
        expect(result.lunarDay).toBe(1)
        expect(result.isLeapMonth).toBe(false)
    })

    it('Test lunar 2017-06-30 leap convert to solar 2017-08-21', () => {
        const result = defaultCalendar.lunar2solar(2017, 6, 30, true)
        expect(result.solarYear).toBe(2017)
        expect(result.solarMonth).toBe(8)
        expect(result.solarDay).toBe(21)
    })

    it('Test solar 2017-08-15 convert to lunar 2017-06-24 leap', () => {
        const result = defaultCalendar.solar2lunar(2017, 8, 15)
        expect(result.lunarYear).toBe(2017)
        expect(result.lunarMonth).toBe(6)
        expect(result.lunarDay).toBe(24)
        expect(result.isLeapMonth).toBe(true)
    })

    it('Test solar 2033-08-25 convert to lunar 2033-08-01', () => {
        const result = defaultCalendar.solar2lunar(2033, 8, 25)
        expect(result.lunarYear).toBe(2033)
        expect(result.lunarMonth).toBe(8)
        expect(result.lunarDay).toBe(1)
        expect(result.isLeapMonth).toBe(false)
    })

    it('Test solar 2033-12-22 convert to lunar 2033-11-01 leap', () => {
        const result = defaultCalendar.solar2lunar(2033, 12, 22)
        expect(result.lunarYear).toBe(2033)
        expect(result.lunarMonth).toBe(11)
        expect(result.lunarDay).toBe(1)
        expect(result.isLeapMonth).toBe(true)
    })

    it('Test solar 2033-09-23 convert to lunar 2033-09-01', () => {
        const result = defaultCalendar.solar2lunar(2033, 9, 23)
        expect(result.lunarYear).toBe(2033)
        expect(result.lunarMonth).toBe(9)
        expect(result.lunarDay).toBe(1)
        expect(result.isLeapMonth).toBe(false)
    })
})
