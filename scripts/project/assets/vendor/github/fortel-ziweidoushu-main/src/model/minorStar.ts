import { DestinyBoard } from './destinyBoard'
import { Ground } from './ground'
import { Luckiness } from './miscEnums'
import { Sky } from './sky'
import util from 'util'
import { Star } from './star'

class MinorStar implements Star {
    key: string
    displayName: string
    luck: Luckiness

    constructor(key: string, displayName: string, luck: Luckiness) {
        this.key = key
        this.displayName = displayName
        this.luck = luck
    }

    toJSON() {
        return this.displayName
    }

    toString(): string {
        return this.displayName
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars
    [util.inspect.custom](depth: number, opts: any): string {
        return this.toString()
    }

    static MINOR_STAR_EARN = Object.freeze(new MinorStar('MINOR_STAR_EARN', '祿存', Luckiness.LUCK))
    static MINOR_STAR_BENEFACTOR_MAN = Object.freeze(new MinorStar('MINOR_STAR_BENEFACTOR_MAN', '天魁', Luckiness.LUCK))
    static MINOR_STAR_BENEFACTOR_WOMAN = Object.freeze(new MinorStar('MINOR_STAR_BENEFACTOR_WOMAN', '天鉞', Luckiness.LUCK))
    static MINOR_STAR_CLEVER = Object.freeze(new MinorStar('MINOR_STAR_CLEVER', '文昌', Luckiness.LUCK))
    static MINOR_STAR_SKILL = Object.freeze(new MinorStar('MINOR_STAR_SKILL', '文曲', Luckiness.LUCK))
    static MINOR_STAR_SUPPORT_LEFT = Object.freeze(new MinorStar('MINOR_STAR_SUPPORT_LEFT', '左輔', Luckiness.LUCK))
    static MINOR_STAR_SUPPORT_RIGHT = Object.freeze(new MinorStar('MINOR_STAR_SUPPORT_RIGHT', '右弼', Luckiness.LUCK))
    static MINOR_STAR_VOID_GROUND = Object.freeze(new MinorStar('MINOR_STAR_VOID_GROUND', '地空', Luckiness.BAD_LUCK))
    static MINOR_STAR_LOST = Object.freeze(new MinorStar('MINOR_STAR_LOST', '地劫', Luckiness.BAD_LUCK))
    static MINOR_STAR_BURNING = Object.freeze(new MinorStar('MINOR_STAR_BURNING', '火星', Luckiness.BAD_LUCK))
    static MINOR_STAR_HIDDEN_FIRE = Object.freeze(new MinorStar('MINOR_STAR_HIDDEN_FIRE', '鈴星', Luckiness.BAD_LUCK))
    static MINOR_STAR_COMPETITION = Object.freeze(new MinorStar('MINOR_STAR_COMPETITION', '擎羊', Luckiness.BAD_LUCK))
    static MINOR_STAR_HINDRANCE = Object.freeze(new MinorStar('MINOR_STAR_HINDRANCE', '陀羅', Luckiness.BAD_LUCK))
    static MINOR_STAR_PEGASUS = Object.freeze(new MinorStar('MINOR_STAR_PEGASUS', '天馬', Luckiness.NEUTRAL))

    static stars = Object.freeze([
        MinorStar.MINOR_STAR_EARN,
        MinorStar.MINOR_STAR_BENEFACTOR_MAN,
        MinorStar.MINOR_STAR_BENEFACTOR_WOMAN,
        MinorStar.MINOR_STAR_CLEVER,
        MinorStar.MINOR_STAR_SKILL,
        MinorStar.MINOR_STAR_SUPPORT_LEFT,
        MinorStar.MINOR_STAR_SUPPORT_RIGHT,
        MinorStar.MINOR_STAR_VOID_GROUND,
        MinorStar.MINOR_STAR_LOST,
        MinorStar.MINOR_STAR_BURNING,
        MinorStar.MINOR_STAR_HIDDEN_FIRE,
        MinorStar.MINOR_STAR_COMPETITION,
        MinorStar.MINOR_STAR_HINDRANCE,
        MinorStar.MINOR_STAR_PEGASUS,
    ])

    static minorStarPlacers: Readonly<Map<MinorStar, MinorStarPlacer>>

    static {
        const minorStarPlacers = new Map<MinorStar, MinorStarPlacer>()

        // 祿存
        minorStarPlacers.set(MinorStar.MINOR_STAR_EARN, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return minorStarPlacers.get(MinorStar.MINOR_STAR_EARN)!.evalRuntimeGround(destinyBoard.config.yearSky)
            },
            hasRuntime: () => true,
            evalRuntimeGround: (sky: Sky) => {
                return Ground.get([2, 3, 5, 6, 5, 6, 8, 9, 11, 0][sky.index])
            },
        })

        // 天魁
        minorStarPlacers.set(MinorStar.MINOR_STAR_BENEFACTOR_MAN, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return minorStarPlacers.get(MinorStar.MINOR_STAR_BENEFACTOR_MAN)!.evalRuntimeGround(destinyBoard.config.yearSky)
            },
            hasRuntime: () => true,
            evalRuntimeGround: (sky: Sky) => {
                return Ground.get([1, 0, 11, 11, 1, 0, 1, 6, 3, 3][sky.index])
            },
        })

        // 天鉞
        minorStarPlacers.set(MinorStar.MINOR_STAR_BENEFACTOR_WOMAN, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return minorStarPlacers.get(MinorStar.MINOR_STAR_BENEFACTOR_WOMAN)!.evalRuntimeGround(destinyBoard.config.yearSky)
            },
            hasRuntime: () => true,
            evalRuntimeGround: (sky: Sky) => {
                return Ground.get([7, 8, 9, 9, 7, 8, 7, 2, 5, 5][sky.index])
            },
        })

        // 文昌
        minorStarPlacers.set(MinorStar.MINOR_STAR_CLEVER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const bornGround = destinyBoard.config.bornTimeGround.ground
                return Ground.get(10).shift(-bornGround.index)
            },
            hasRuntime: () => true,
            evalRuntimeGround: (sky: Sky) => {
                return Ground.get([5, 6, 8, 9, 8, 9, 11, 0, 2, 3][sky.index])
            },
        })

        // 文曲
        minorStarPlacers.set(MinorStar.MINOR_STAR_SKILL, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const bornGround = destinyBoard.config.bornTimeGround.ground
                return Ground.get(4).shift(bornGround.index)
            },
            hasRuntime: () => true,
            evalRuntimeGround: (sky: Sky) => {
                return Ground.get([9, 8, 6, 5, 6, 5, 3, 2, 0, 11][sky.index])
            },
        })

        // 左輔
        minorStarPlacers.set(MinorStar.MINOR_STAR_SUPPORT_LEFT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const month = destinyBoard.config.getLogicalMonth()
                return Ground.get(4).shift(month - 1)
            },
            hasRuntime: () => false,
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            evalRuntimeGround: (sky: Sky) => {
                throw new Error('Runtime not supported')
            },
        })

        // 右弼
        minorStarPlacers.set(MinorStar.MINOR_STAR_SUPPORT_RIGHT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const month = destinyBoard.config.getLogicalMonth()
                return Ground.get(10).shift(-(month - 1))
            },
            hasRuntime: () => false,
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            evalRuntimeGround: (sky: Sky) => {
                throw new Error('Runtime not supported')
            },
        })

        // 地空
        minorStarPlacers.set(MinorStar.MINOR_STAR_VOID_GROUND, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const bornGround = destinyBoard.config.bornTimeGround.ground
                return Ground.get(11).shift(-bornGround.index)
            },
            hasRuntime: () => false,
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            evalRuntimeGround: (sky: Sky) => {
                throw new Error('Runtime not supported')
            },
        })

        // 地劫
        minorStarPlacers.set(MinorStar.MINOR_STAR_LOST, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const bornGround = destinyBoard.config.bornTimeGround.ground
                return Ground.get(11).shift(bornGround.index)
            },
            hasRuntime: () => false,
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            evalRuntimeGround: (sky: Sky) => {
                throw new Error('Runtime not supported')
            },
        })

        // 火星
        minorStarPlacers.set(MinorStar.MINOR_STAR_BURNING, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const yearGround = destinyBoard.config.yearGround
                const bornGround = destinyBoard.config.bornTimeGround.ground

                const mapping = [2, 3, 1, 9, 2, 3, 1, 9, 2, 3, 1, 9]
                return Ground.get(mapping[yearGround.index]).shift(bornGround.index)
            },
            hasRuntime: () => false,
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            evalRuntimeGround: (sky: Sky) => {
                throw new Error('Runtime not supported')
            },
        })

        // 鈴星
        minorStarPlacers.set(MinorStar.MINOR_STAR_HIDDEN_FIRE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const yearGround = destinyBoard.config.yearGround
                const bornGround = destinyBoard.config.bornTimeGround.ground

                if ([2, 6, 10].includes(yearGround.index)) {
                    return Ground.get(3).shift(bornGround.index)
                } else {
                    return Ground.get(10).shift(bornGround.index)
                }
            },
            hasRuntime: () => false,
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            evalRuntimeGround: (sky: Sky) => {
                throw new Error('Runtime not supported')
            },
        })

        // 擎羊
        minorStarPlacers.set(MinorStar.MINOR_STAR_COMPETITION, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return minorStarPlacers.get(MinorStar.MINOR_STAR_COMPETITION)!.evalRuntimeGround(destinyBoard.config.yearSky)
            },
            hasRuntime: () => true,
            evalRuntimeGround: (sky: Sky) => {
                return Ground.get([3, 4, 6, 7, 6, 7, 9, 10, 0, 1][sky.index])
            },
        })

        // 陀羅
        minorStarPlacers.set(MinorStar.MINOR_STAR_HINDRANCE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return minorStarPlacers.get(MinorStar.MINOR_STAR_HINDRANCE)!.evalRuntimeGround(destinyBoard.config.yearSky)
            },
            hasRuntime: () => true,
            evalRuntimeGround: (sky: Sky) => {
                return Ground.get([1, 2, 4, 5, 4, 5, 7, 8, 10, 11][sky.index])
            },
        })

        // 天馬
        minorStarPlacers.set(MinorStar.MINOR_STAR_PEGASUS, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([2, 11, 8, 5, 2, 11, 8, 5, 2, 11, 8, 5][destinyBoard.config.yearGround.index])
            },
            hasRuntime: () => false,
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            evalRuntimeGround: (sky: Sky) => {
                throw new Error('Runtime not supported')
            },
        })

        MinorStar.minorStarPlacers = Object.freeze(minorStarPlacers)
    }

    getType(): string {
        return 'MinorStar'
    }

    getKey() {
        return this.key
    }

    getDisplayName() {
        return this.displayName
    }

    static getByKey(key: string): MinorStar | null {
        return MinorStar.stars.find((star) => star.getKey() === key) ?? null
    }

    static getByName(name: string) {
        return MinorStar.stars.find((star) => star.getDisplayName() === name) ?? null
    }

    equals(star: Star) {
        return star === this || (star.getType() === this.getType() && star.getKey() === this.getKey())
    }
}

declare interface MinorStarPlacer {
    evalGround: (destinyBoard: DestinyBoard) => Ground
    hasRuntime: () => boolean
    evalRuntimeGround: (sky: Sky) => Ground
}

export { MinorStar }
