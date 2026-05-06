import { Ground } from './ground'
import { MajorStar } from './majorStar'
import { MinorStar } from './minorStar'
import { Sky } from './sky'
import { StarDerivative } from './starDerivative'

class Runtime {
    static getRuntimeStars() {
        return [
            MinorStar.MINOR_STAR_EARN,
            MinorStar.MINOR_STAR_BENEFACTOR_MAN,
            MinorStar.MINOR_STAR_BENEFACTOR_WOMAN,
            MinorStar.MINOR_STAR_CLEVER,
            MinorStar.MINOR_STAR_SKILL,
            MinorStar.MINOR_STAR_COMPETITION,
            MinorStar.MINOR_STAR_HINDRANCE,
        ]
    }

    static getRuntimeStarsLocation(sky: Sky) {
        const runtimeStarsLocation = new Map<MinorStar, Ground>()
        for (const minorStar of this.getRuntimeStars()) {
            runtimeStarsLocation.set(minorStar, MinorStar.minorStarPlacers.get(minorStar)!.evalRuntimeGround(sky))
        }
        return runtimeStarsLocation
    }

    static getRuntimeLocationStars(sky: Sky) {
        const runtimeLocationStars = new Map<Ground, MinorStar[]>()
        for (const minorStar of this.getRuntimeStars()) {
            const ground = MinorStar.minorStarPlacers.get(minorStar)!.evalRuntimeGround(sky)
            if (!runtimeLocationStars.has(ground)) {
                runtimeLocationStars.set(ground, [minorStar])
            } else {
                runtimeLocationStars.get(ground)?.push(minorStar)
            }
        }
        return runtimeLocationStars
    }

    static getDerivativeMapOf(sky: Sky): Map<StarDerivative, MajorStar | MinorStar> {
        const starDerivativeMap = new Map<StarDerivative, MajorStar | MinorStar>()

        starDerivativeMap.set(StarDerivative.WEALTHINESS, StarDerivative.getWealthinessStar(sky))
        starDerivativeMap.set(StarDerivative.POWER, StarDerivative.getPowerStar(sky))
        starDerivativeMap.set(StarDerivative.FAME, StarDerivative.getFameStar(sky))
        starDerivativeMap.set(StarDerivative.PROBLEM, StarDerivative.getProblemStar(sky))

        return starDerivativeMap
    }

    static getStarToDerivativeMapOf(sky: Sky): Map<MajorStar | MinorStar, StarDerivative> {
        const starDerivativeMap = new Map<MajorStar | MinorStar, StarDerivative>()

        starDerivativeMap.set(StarDerivative.getWealthinessStar(sky), StarDerivative.WEALTHINESS)
        starDerivativeMap.set(StarDerivative.getPowerStar(sky), StarDerivative.POWER)
        starDerivativeMap.set(StarDerivative.getFameStar(sky), StarDerivative.FAME)
        starDerivativeMap.set(StarDerivative.getProblemStar(sky), StarDerivative.PROBLEM)

        return starDerivativeMap
    }

    static getDerivativeOf(starDerivative: StarDerivative, sky: Sky): MajorStar | MinorStar {
        if (StarDerivative.WEALTHINESS.euqals(starDerivative)) {
            return StarDerivative.getWealthinessStar(sky)
        } else if (StarDerivative.POWER.euqals(starDerivative)) {
            return StarDerivative.getPowerStar(sky)
        } else if (StarDerivative.FAME.euqals(starDerivative)) {
            return StarDerivative.getFameStar(sky)
        } else if (StarDerivative.PROBLEM.euqals(starDerivative)) {
            return StarDerivative.getProblemStar(sky)
        } else {
            throw new Error('Cannot find Star Derivative')
        }
    }
}

export { Runtime }
