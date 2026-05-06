import { DestinyBoard } from './destinyBoard'
import { Element } from './miscEnums'
import { Ground } from './ground'
import { Star } from './star'
import util from 'util'

/**
 * 主星
 */
class MajorStar implements Star {
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

    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars
    [util.inspect.custom](depth: number, opts: any): string {
        return this.toString()
    }

    static MAJOR_STAR_EMPEROR = Object.freeze(new MajorStar('MAJOR_STAR_EMPEROR', '紫微'))
    static MAJOR_STAR_CHANGE = Object.freeze(new MajorStar('MAJOR_STAR_CHANGE', '天機'))
    static MAJOR_STAR_SUN = Object.freeze(new MajorStar('MAJOR_STAR_SUN', '太陽'))
    static MAJOR_STAR_GOLD = Object.freeze(new MajorStar('MAJOR_STAR_GOLD', '武曲'))
    static MAJOR_STAR_ENJOYMENT = Object.freeze(new MajorStar('MAJOR_STAR_ENJOYMENT', '天同'))
    static MAJOR_STAR_FIRE = Object.freeze(new MajorStar('MAJOR_STAR_FIRE', '廉貞'))
    static MAJOR_STAR_TREASURY = Object.freeze(new MajorStar('MAJOR_STAR_TREASURY', '天府'))
    static MAJOR_STAR_MOON = Object.freeze(new MajorStar('MAJOR_STAR_MOON', '太陰'))
    static MAJOR_STAR_GREED = Object.freeze(new MajorStar('MAJOR_STAR_GREED', '貪狼'))
    static MAJOR_STAR_ARGUMENT = Object.freeze(new MajorStar('MAJOR_STAR_ARGUMENT', '巨門'))
    static MAJOR_STAR_SUPPORT = Object.freeze(new MajorStar('MAJOR_STAR_SUPPORT', '天相'))
    static MAJOR_STAR_RULE = Object.freeze(new MajorStar('MAJOR_STAR_RULE', '天梁'))
    static MAJOR_STAR_GENERAL = Object.freeze(new MajorStar('MAJOR_STAR_GENERAL', '七殺'))
    static MAJOR_STAR_PIONEER = Object.freeze(new MajorStar('MAJOR_STAR_PIONEER', '破軍'))

    static stars = Object.freeze([
        MajorStar.MAJOR_STAR_EMPEROR,
        MajorStar.MAJOR_STAR_CHANGE,
        MajorStar.MAJOR_STAR_SUN,
        MajorStar.MAJOR_STAR_GOLD,
        MajorStar.MAJOR_STAR_ENJOYMENT,
        MajorStar.MAJOR_STAR_FIRE,
        MajorStar.MAJOR_STAR_TREASURY,
        MajorStar.MAJOR_STAR_MOON,
        MajorStar.MAJOR_STAR_GREED,
        MajorStar.MAJOR_STAR_ARGUMENT,
        MajorStar.MAJOR_STAR_SUPPORT,
        MajorStar.MAJOR_STAR_RULE,
        MajorStar.MAJOR_STAR_GENERAL,
        MajorStar.MAJOR_STAR_PIONEER,
    ])

    static majorStarPlacers: Readonly<Map<MajorStar, MajorStarPlacer>>

    static {
        const majorStarPlacers = new Map<MajorStar, MajorStarPlacer>()

        // 紫微
        majorStarPlacers.set(MajorStar.MAJOR_STAR_EMPEROR, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const mapping = new Map()
                mapping.set(Element.WATER, [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 0, 0, 1, 1, 2, 2, 3, 3, 4])
                mapping.set(Element.WOOD, [4, 1, 2, 5, 2, 3, 6, 3, 4, 7, 4, 5, 8, 5, 6, 9, 6, 7, 10, 7, 8, 11, 8, 9, 0, 9, 10, 1, 10, 11])
                mapping.set(Element.GOLD, [11, 4, 1, 2, 0, 5, 2, 3, 1, 6, 3, 4, 2, 7, 4, 5, 3, 8, 5, 6, 4, 9, 6, 7, 5, 10, 7, 8, 6, 11])
                mapping.set(Element.EARTH, [6, 11, 4, 1, 2, 7, 0, 5, 2, 3, 8, 1, 6, 3, 4, 9, 2, 7, 4, 5, 10, 3, 8, 5, 6, 11, 4, 9, 6, 7])
                mapping.set(Element.FIRE, [9, 6, 11, 4, 1, 2, 10, 7, 0, 5, 2, 3, 11, 8, 1, 6, 3, 4, 0, 9, 2, 7, 4, 5, 1, 10, 3, 8, 5, 6])

                return Ground.get(mapping.get(destinyBoard.element)[destinyBoard.config.day - 1])
            },
            evalEnergyLevel: (ground: Ground) => {
                return [0, 2, 2, 1, -1, 1, 2, 2, 1, 0, 0, 1][ground.index]
            },
        })

        // 天機
        majorStarPlacers.set(MajorStar.MAJOR_STAR_CHANGE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_EMPEROR)!.evalGround(destinyBoard).shift(-1)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [2, -1, 1, 1, 2, 0, 2, -1, 0, 1, 2, 0][ground.index]
            },
        })

        // 太陽
        majorStarPlacers.set(MajorStar.MAJOR_STAR_SUN, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_EMPEROR)!.evalGround(destinyBoard).shift(-3)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [-1, -1, 1, 2, 1, 1, 2, 0, 0, 0, -1, -1][ground.index]
            },
        })

        // 武曲
        majorStarPlacers.set(MajorStar.MAJOR_STAR_GOLD, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_EMPEROR)!.evalGround(destinyBoard).shift(-4)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [1, 2, 0, -1, 2, 0, 1, 2, 0, 1, 2, 0][ground.index]
            },
        })

        // 天同
        majorStarPlacers.set(MajorStar.MAJOR_STAR_ENJOYMENT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_EMPEROR)!.evalGround(destinyBoard).shift(-5)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [1, -1, 0, 2, 0, 2, -1, -1, 1, 0, 0, 2][ground.index]
            },
        })

        // 廉貞
        majorStarPlacers.set(MajorStar.MAJOR_STAR_FIRE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_EMPEROR)!.evalGround(destinyBoard).shift(-8)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [0, 1, 2, 0, 1, -1, 0, 2, 2, 0, 1, -1][ground.index]
            },
        })

        // 天府
        majorStarPlacers.set(MajorStar.MAJOR_STAR_TREASURY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const ground = majorStarPlacers.get(MajorStar.MAJOR_STAR_EMPEROR)!.evalGround(destinyBoard)
                const emperorCell = destinyBoard.getCellByGround(ground)
                const emperorCellOffset = emperorCell.getCellNextDist(destinyBoard.getCellByGround(Ground.get(2)))
                return emperorCell.getNextICell(emperorCellOffset * 2).ground
            },
            evalEnergyLevel: (ground: Ground) => {
                return [2, 2, 2, 0, 2, 0, 1, 2, 0, -1, 2, 1][ground.index]
            },
        })

        // 太陰
        majorStarPlacers.set(MajorStar.MAJOR_STAR_MOON, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_TREASURY)!.evalGround(destinyBoard).shift(1)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [2, 2, 0, -1, 0, -1, -1, 0, 0, 1, 1, 2][ground.index]
            },
        })

        // 貪狼
        majorStarPlacers.set(MajorStar.MAJOR_STAR_GREED, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_TREASURY)!.evalGround(destinyBoard).shift(2)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [1, 2, 0, 0, 2, -1, 1, 2, 0, 0, 2, -1][ground.index]
            },
        })

        // 巨門
        majorStarPlacers.set(MajorStar.MAJOR_STAR_ARGUMENT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_TREASURY)!.evalGround(destinyBoard).shift(3)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [1, 1, 2, 2, 0, 0, 1, -1, 2, 2, 1, 1][ground.index]
            },
        })

        // 天相
        majorStarPlacers.set(MajorStar.MAJOR_STAR_SUPPORT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_TREASURY)!.evalGround(destinyBoard).shift(4)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [2, 2, 2, -1, 1, 0, 1, 0, 2, -1, 0, 0][ground.index]
            },
        })

        // 天梁
        majorStarPlacers.set(MajorStar.MAJOR_STAR_RULE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_TREASURY)!.evalGround(destinyBoard).shift(5)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [2, 1, 2, 2, 1, -1, 2, 1, -1, 0, 1, -1][ground.index]
            },
        })

        // 七殺
        majorStarPlacers.set(MajorStar.MAJOR_STAR_GENERAL, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_TREASURY)!.evalGround(destinyBoard).shift(6)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [1, 2, 2, -1, 1, 0, 1, 1, 2, 0, 2, 0][ground.index]
            },
        })

        // 七殺
        majorStarPlacers.set(MajorStar.MAJOR_STAR_PIONEER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return majorStarPlacers.get(MajorStar.MAJOR_STAR_TREASURY)!.evalGround(destinyBoard).shift(-2)
            },
            evalEnergyLevel: (ground: Ground) => {
                return [2, 1, -1, 1, 1, 0, 2, 2, -1, -1, 1, 0][ground.index]
            },
        })

        MajorStar.majorStarPlacers = Object.freeze(majorStarPlacers)
    }

    getType(): string {
        return 'MajorStar'
    }

    getKey() {
        return this.key
    }

    getDisplayName() {
        return this.displayName
    }

    static getByKey(key: string): MajorStar | null {
        return MajorStar.stars.find((star) => star.getKey() === key) ?? null
    }

    static getByName(name: string) {
        return MajorStar.stars.find((star) => star.getDisplayName() === name) ?? null
    }

    equals(star: Star) {
        return star === this || (star.getType() === this.getType() && star.getKey() === this.getKey())
    }
}

declare interface MajorStarPlacer {
    evalGround: (destinyBoard: DestinyBoard) => Ground
    evalEnergyLevel: (ground: Ground) => number
}

export { MajorStar }
