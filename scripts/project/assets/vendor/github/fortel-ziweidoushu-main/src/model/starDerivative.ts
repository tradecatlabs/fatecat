import util from 'util'
import { MajorStar } from './majorStar'
import { MinorStar } from './minorStar'
import { Sky } from './sky'

class StarDerivative {
    key: string
    displayName: string

    constructor(key: string, displayName: string) {
        this.key = key
        this.displayName = displayName
    }

    toJSON() {
        return this.displayName
    }

    toString(): string {
        return this.displayName
    }

    euqals(starDerivative: StarDerivative) {
        return this.key === starDerivative.key
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars
    [util.inspect.custom](depth: number, opts: any): string {
        return this.toString()
    }

    static WEALTHINESS = Object.freeze(new StarDerivative('WEALTHINESS', '祿'))
    static POWER = Object.freeze(new StarDerivative('POWER', '權'))
    static FAME = Object.freeze(new StarDerivative('FAME', '科'))
    static PROBLEM = Object.freeze(new StarDerivative('PROBLEM', '忌'))

    static getWealthinessStar(sky: Sky): Readonly<MajorStar> {
        return [
            MajorStar.MAJOR_STAR_FIRE,
            MajorStar.MAJOR_STAR_CHANGE,
            MajorStar.MAJOR_STAR_ENJOYMENT,
            MajorStar.MAJOR_STAR_MOON,
            MajorStar.MAJOR_STAR_GREED,
            MajorStar.MAJOR_STAR_GOLD,
            MajorStar.MAJOR_STAR_SUN,
            MajorStar.MAJOR_STAR_ARGUMENT,
            MajorStar.MAJOR_STAR_RULE,
            MajorStar.MAJOR_STAR_PIONEER,
        ][sky.index]
    }

    static getPowerStar(sky: Sky): Readonly<MajorStar> {
        return [
            MajorStar.MAJOR_STAR_PIONEER,
            MajorStar.MAJOR_STAR_RULE,
            MajorStar.MAJOR_STAR_CHANGE,
            MajorStar.MAJOR_STAR_ENJOYMENT,
            MajorStar.MAJOR_STAR_MOON,
            MajorStar.MAJOR_STAR_GREED,
            MajorStar.MAJOR_STAR_GOLD,
            MajorStar.MAJOR_STAR_SUN,
            MajorStar.MAJOR_STAR_EMPEROR,
            MajorStar.MAJOR_STAR_ARGUMENT,
        ][sky.index]
    }

    static getFameStar(sky: Sky): Readonly<MajorStar | MinorStar> {
        return [
            MajorStar.MAJOR_STAR_GOLD,
            MajorStar.MAJOR_STAR_EMPEROR,
            MinorStar.MINOR_STAR_CLEVER,
            MajorStar.MAJOR_STAR_CHANGE,
            MajorStar.MAJOR_STAR_SUN,
            MajorStar.MAJOR_STAR_RULE,
            MajorStar.MAJOR_STAR_TREASURY,
            MinorStar.MINOR_STAR_SKILL,
            MajorStar.MAJOR_STAR_TREASURY,
            MajorStar.MAJOR_STAR_MOON,
        ][sky.index]
    }

    static getProblemStar(sky: Sky): Readonly<MajorStar | MinorStar> {
        return [
            MajorStar.MAJOR_STAR_SUN,
            MajorStar.MAJOR_STAR_MOON,
            MajorStar.MAJOR_STAR_FIRE,
            MajorStar.MAJOR_STAR_ARGUMENT,
            MajorStar.MAJOR_STAR_CHANGE,
            MinorStar.MINOR_STAR_SKILL,
            MajorStar.MAJOR_STAR_ENJOYMENT,
            MinorStar.MINOR_STAR_CLEVER,
            MajorStar.MAJOR_STAR_GOLD,
            MajorStar.MAJOR_STAR_GREED,
        ][sky.index]
    }
}

export { StarDerivative }
