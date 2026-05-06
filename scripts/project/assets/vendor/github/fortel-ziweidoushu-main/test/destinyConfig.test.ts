import { DayTimeGround } from '../src/model/dayTimeGround'
import { ConfigType, Gender } from '../src/model/destinyConfig'
import { DestinyConfigBuilder } from '../src/util/destinyConfigBuilder'

describe('Test DestinyConfig', () => {
    it('Test DestinyConfigBuilder.withText', () => {
        const destinyConfig = DestinyConfigBuilder.withText('1952年12月15日寅時天盤女')

        expect(destinyConfig.year).toBe(1952)
        expect(destinyConfig.month).toBe(12)
        expect(destinyConfig.day).toBe(15)
        expect(destinyConfig.isLeapMonth).toBe(false)
        expect(destinyConfig.bornTimeGround).toBe(DayTimeGround.getByName('寅時'))
        expect(destinyConfig.configType).toBe(ConfigType.SKY)
        expect(destinyConfig.gender).toBe(Gender.F)
    })

    it('Test DestinyConfigBuilder.withText, default value', () => {
        expect(DestinyConfigBuilder.withText('1952年12月15日寅時天盤').gender).toBe(Gender.M)
        expect(DestinyConfigBuilder.withText('1952年12月15日寅時天盤').day).toBe(15) // test calendar = lunar
        expect(DestinyConfigBuilder.withText('1952年12月15日寅時').configType).toBe(ConfigType.SKY)
    })

    it('Test DestinyConfigBuilder.withlunar', () => {
        const destinyConfig = DestinyConfigBuilder.withlunar({
            year: 1952,
            month: 12,
            day: 15,
            isLeapMonth: false,
            bornTimeGround: DayTimeGround.getByName('寅時'),
            configType: ConfigType.SKY,
            gender: Gender.F,
        })

        expect(destinyConfig.year).toBe(1952)
        expect(destinyConfig.month).toBe(12)
        expect(destinyConfig.day).toBe(15)
        expect(destinyConfig.isLeapMonth).toBe(false)
        expect(destinyConfig.bornTimeGround).toBe(DayTimeGround.getByName('寅時'))
        expect(destinyConfig.configType).toBe(ConfigType.SKY)
        expect(destinyConfig.gender).toBe(Gender.F)
    })

    it('Test DestinyConfigBuilder.withSolar', () => {
        const destinyConfig = DestinyConfigBuilder.withSolar({
            year: 1953,
            month: 1,
            day: 29,
            bornTimeGround: DayTimeGround.getByName('寅時'),
            configType: ConfigType.SKY,
            gender: Gender.F,
        })

        expect(destinyConfig.year).toBe(1952)
        expect(destinyConfig.month).toBe(12)
        expect(destinyConfig.day).toBe(15)
        expect(destinyConfig.isLeapMonth).toBe(false)
        expect(destinyConfig.bornTimeGround).toBe(DayTimeGround.getByName('寅時'))
        expect(destinyConfig.configType).toBe(ConfigType.SKY)
        expect(destinyConfig.gender).toBe(Gender.F)
    })
})
