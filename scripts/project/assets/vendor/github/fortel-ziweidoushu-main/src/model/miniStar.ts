import { intDivide, mod } from './../utils'
import { DestinyBoard } from './destinyBoard'
import { Ground } from './ground'
import { Luckiness, Direction } from './miscEnums'
import { MinorStar } from './minorStar'
import { Temple } from './temple'
import util from 'util'
import { Star } from './star'

class MiniStar implements Star {
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

    static MINI_STAR_SKY_NOBLE = Object.freeze(new MiniStar('MINI_STAR_SKY_NOBLE', '天官', Luckiness.LUCK))
    static MINI_STAR_SKY_HAPPINESS = Object.freeze(new MiniStar('MINI_STAR_SKY_HAPPINESS', '天福', Luckiness.LUCK))
    static MINI_STAR_COOK = Object.freeze(new MiniStar('MINI_STAR_COOK', '天廚', Luckiness.LUCK))
    static MINI_STAR_CRY = Object.freeze(new MiniStar('MINI_STAR_CRY', '天哭', Luckiness.BAD_LUCK))
    static MINI_STAR_LOST = Object.freeze(new MiniStar('MINI_STAR_LOST', '天虛', Luckiness.BAD_LUCK))
    static MINI_STAR_SKILL = Object.freeze(new MiniStar('MINI_STAR_SKILL', '龍池', Luckiness.LUCK))
    static MINI_STAR_ART = Object.freeze(new MiniStar('MINI_STAR_ART', '鳳閣', Luckiness.LUCK))
    static MINI_STAR_FESTIVE = Object.freeze(new MiniStar('MINI_STAR_FESTIVE', '紅鸞', Luckiness.LUCK))
    static MINI_STAR_HAPPINESS = Object.freeze(new MiniStar('MINI_STAR_HAPPINESS', '天喜', Luckiness.LUCK))
    static MINI_STAR_LONELY = Object.freeze(new MiniStar('MINI_STAR_LONELY', '孤辰', Luckiness.BAD_LUCK))
    static MINI_STAR_SINGLE = Object.freeze(new MiniStar('MINI_STAR_SINGLE', '寡宿', Luckiness.BAD_LUCK))
    static MINI_STAR_DISSOLVE = Object.freeze(new MiniStar('MINI_STAR_DISSOLVE', '解神', Luckiness.LUCK))
    static MINI_STAR_BROKEN = Object.freeze(new MiniStar('MINI_STAR_BROKEN', '破碎', Luckiness.BAD_LUCK))
    static MINI_STAR_BIG_LOST = Object.freeze(new MiniStar('MINI_STAR_BIG_LOST', '大耗', Luckiness.BAD_LUCK))
    static MINI_STAR_LITTLE_DISASTER = Object.freeze(new MiniStar('MINI_STAR_LITTLE_DISASTER', '劫煞', Luckiness.BAD_LUCK))
    static MINI_STAR_LUST = Object.freeze(new MiniStar('MINI_STAR_LUST', '咸池', Luckiness.NEUTRAL))
    static MINI_STAR_MOON_BENEFACTOR = Object.freeze(new MiniStar('MINI_STAR_MOON_BENEFACTOR', '月德', Luckiness.LUCK))
    static MINI_STAR_GENIUS = Object.freeze(new MiniStar('MINI_STAR_GENIUS', '天才', Luckiness.LUCK))
    static MINI_STAR_LONGEVITY = Object.freeze(new MiniStar('MINI_STAR_LONGEVITY', '天壽', Luckiness.LUCK))
    static MINI_STAR_VOID_SKY = Object.freeze(new MiniStar('MINI_STAR_VOID_SKY', '天空', Luckiness.BAD_LUCK))
    static MINI_STAR_EMPTY = Object.freeze(new MiniStar('MINI_STAR_EMPTY', '旬空', Luckiness.BAD_LUCK))
    static MINI_STAR_EMPTY2 = Object.freeze(new MiniStar('MINI_STAR_EMPTY2', '旬空', Luckiness.BAD_LUCK))
    static MINI_STAR_INTERUPTION = Object.freeze(new MiniStar('MINI_STAR_INTERUPTION', '截空', Luckiness.BAD_LUCK))
    static MINI_STAR_INTERUPTION2 = Object.freeze(new MiniStar('MINI_STAR_INTERUPTION2', '截空', Luckiness.BAD_LUCK))
    static MINI_STAR_PLATFORM = Object.freeze(new MiniStar('MINI_STAR_PLATFORM', '台輔', Luckiness.LUCK))
    static MINI_STAR_FAME = Object.freeze(new MiniStar('MINI_STAR_FAME', '封誥', Luckiness.LUCK))
    static MINI_STAR_PUNISHMENT = Object.freeze(new MiniStar('MINI_STAR_PUNISHMENT', '天刑', Luckiness.BAD_LUCK))
    static MINI_STAR_SEX = Object.freeze(new MiniStar('MINI_STAR_SEX', '天姚', Luckiness.BAD_LUCK))
    static MINI_STAR_WITCH = Object.freeze(new MiniStar('MINI_STAR_WITCH', '天巫', Luckiness.LUCK))
    static MINI_STAR_ILLNESS = Object.freeze(new MiniStar('MINI_STAR_ILLNESS', '天月', Luckiness.BAD_LUCK))
    static MINI_STAR_GHOST = Object.freeze(new MiniStar('MINI_STAR_GHOST', '陰煞', Luckiness.BAD_LUCK))
    static MINI_STAR_DISSOLVE2 = Object.freeze(new MiniStar('MINI_STAR_DISSOLVE2', '解神', Luckiness.LUCK))
    static MINI_STAR_BACKBITING = Object.freeze(new MiniStar('MINI_STAR_BACKBITING', '蜚廉', Luckiness.BAD_LUCK))
    static MINI_STAR_SCHOLAR = Object.freeze(new MiniStar('MINI_STAR_SCHOLAR', '博士', Luckiness.LUCK))
    static MINI_STAR_STRENGTH = Object.freeze(new MiniStar('MINI_STAR_STRENGTH', '力士', Luckiness.NEUTRAL))
    static MINI_STAR_GREEN_DRAGON = Object.freeze(new MiniStar('MINI_STAR_GREEN_DRAGON', '青龍', Luckiness.LUCK))
    static MINI_STAR_SMALL_LOST = Object.freeze(new MiniStar('MINI_STAR_SMALL_LOST', '小耗', Luckiness.BAD_LUCK))
    static MINI_STAR_GENERAL = Object.freeze(new MiniStar('MINI_STAR_GENERAL', '將軍', Luckiness.NEUTRAL))
    static MINI_STAR_LETTER = Object.freeze(new MiniStar('MINI_STAR_LETTER', '奏書', Luckiness.LUCK))
    static MINI_STAR_BACKBITING2 = Object.freeze(new MiniStar('MINI_STAR_BACKBITING2', '蜚廉', Luckiness.BAD_LUCK))
    static MINI_STAR_JOY = Object.freeze(new MiniStar('MINI_STAR_JOY', '喜神', Luckiness.LUCK))
    static MINI_STAR_SICK = Object.freeze(new MiniStar('MINI_STAR_SICK', '病符', Luckiness.BAD_LUCK))
    static MINI_STAR_BIG_LOST2 = Object.freeze(new MiniStar('MINI_STAR_BIG_LOST2', '大耗', Luckiness.BAD_LUCK))
    static MINI_STAR_AMBUSH = Object.freeze(new MiniStar('MINI_STAR_AMBUSH', '伏兵', Luckiness.BAD_LUCK))
    static MINI_STAR_LITIGATION = Object.freeze(new MiniStar('MINI_STAR_LITIGATION', '官府', Luckiness.BAD_LUCK))
    static MINI_STAR_THREE_PODIUM = Object.freeze(new MiniStar('MINI_STAR_THREE_PODIUM', '三台', Luckiness.LUCK))
    static MINI_STAR_EIGHT_SEAT = Object.freeze(new MiniStar('MINI_STAR_EIGHT_SEAT', '八座', Luckiness.LUCK))
    static MINI_STAR_HOLY_LIGHT = Object.freeze(new MiniStar('MINI_STAR_HOLY_LIGHT', '恩光', Luckiness.LUCK))
    static MINI_STAR_NOBLE = Object.freeze(new MiniStar('MINI_STAR_NOBLE', '天貴', Luckiness.LUCK))
    static MINI_STAR_YEAR_GOD = Object.freeze(new MiniStar('MINI_STAR_YEAR_GOD', '太歲', Luckiness.BAD_LUCK))
    static MINI_STAR_PESSIMISTIC = Object.freeze(new MiniStar('MINI_STAR_PESSIMISTIC', '晦氣', Luckiness.BAD_LUCK))
    static MINI_STAR_BEREAVEMENT = Object.freeze(new MiniStar('MINI_STAR_BEREAVEMENT', '喪門', Luckiness.BAD_LUCK))
    static MINI_STAR_TRAP = Object.freeze(new MiniStar('MINI_STAR_TRAP', '貫索', Luckiness.BAD_LUCK))
    static MINI_STAR_LAWSUIT = Object.freeze(new MiniStar('MINI_STAR_LAWSUIT', '官符', Luckiness.BAD_LUCK))
    static MINI_STAR_SMALL_LOST2 = Object.freeze(new MiniStar('MINI_STAR_SMALL_LOST2', '小耗', Luckiness.BAD_LUCK))
    static MINI_STAR_BROKEN_YEAR = Object.freeze(new MiniStar('MINI_STAR_BROKEN_YEAR', '歲破', Luckiness.BAD_LUCK))
    static MINI_STAR_DRAGON_LUCK = Object.freeze(new MiniStar('MINI_STAR_DRAGON_LUCK', '龍德', Luckiness.LUCK))
    static MINI_STAR_WHITE_TIGER = Object.freeze(new MiniStar('MINI_STAR_WHITE_TIGER', '白虎', Luckiness.BAD_LUCK))
    static MINI_STAR_GOD_LUCK = Object.freeze(new MiniStar('MINI_STAR_GOD_LUCK', '天德', Luckiness.LUCK))
    static MINI_STAR_FUNERAL = Object.freeze(new MiniStar('MINI_STAR_FUNERAL', '弔客', Luckiness.BAD_LUCK))
    static MINI_STAR_SICK2 = Object.freeze(new MiniStar('MINI_STAR_SICK2', '病符', Luckiness.BAD_LUCK))
    static MINI_STAR_ANGEL = Object.freeze(new MiniStar('MINI_STAR_ANGEL', '天使', Luckiness.LUCK))
    static MINI_STAR_INJURY = Object.freeze(new MiniStar('MINI_STAR_INJURY', '天傷', Luckiness.BAD_LUCK))
    static MINI_STAR_LEADER = Object.freeze(new MiniStar('MINI_STAR_LEADER', '將星', Luckiness.LUCK))
    static MINI_STAR_MOUNT = Object.freeze(new MiniStar('MINI_STAR_MOUNT', '攀鞍', Luckiness.LUCK))
    static MINI_STAR_TRANSITION = Object.freeze(new MiniStar('MINI_STAR_TRANSITION', '歲驛', Luckiness.NEUTRAL))
    static MINI_STAR_IDLE = Object.freeze(new MiniStar('MINI_STAR_IDLE', '息神', Luckiness.NEUTRAL))
    static MINI_STAR_MYSTIC = Object.freeze(new MiniStar('MINI_STAR_MYSTIC', '華蓋', Luckiness.NEUTRAL))
    static MINI_STAR_LITTLE_DISASTER2 = Object.freeze(new MiniStar('MINI_STAR_LITTLE_DISASTER2', '劫煞', Luckiness.BAD_LUCK))
    static MINI_STAR_DISASTER = Object.freeze(new MiniStar('MINI_STAR_DISASTER', '災煞', Luckiness.BAD_LUCK))
    static MINI_STAR_SKY_DISASTER = Object.freeze(new MiniStar('MINI_STAR_SKY_DISASTER', '天煞', Luckiness.BAD_LUCK))
    static MINI_STAR_BETRAY = Object.freeze(new MiniStar('MINI_STAR_BETRAY', '指背', Luckiness.BAD_LUCK))
    static MINI_STAR_LUST2 = Object.freeze(new MiniStar('MINI_STAR_LUST2', '咸池', Luckiness.NEUTRAL))
    static MINI_STAR_MOON_MONSTER = Object.freeze(new MiniStar('MINI_STAR_MOON_MONSTER', '月煞', Luckiness.BAD_LUCK))
    static MINI_STAR_DEAD = Object.freeze(new MiniStar('MINI_STAR_DEAD', '亡神', Luckiness.BAD_LUCK))

    static doubleStars = Object.freeze([
        MiniStar.MINI_STAR_EMPTY,
        MiniStar.MINI_STAR_INTERUPTION,
        MiniStar.MINI_STAR_DISSOLVE,
        MiniStar.MINI_STAR_BACKBITING,
        MiniStar.MINI_STAR_BIG_LOST,
        MiniStar.MINI_STAR_SMALL_LOST,
        MiniStar.MINI_STAR_SICK,
        MiniStar.MINI_STAR_LITTLE_DISASTER,
        MiniStar.MINI_STAR_LUST,
    ])

    static stars = Object.freeze([
        MiniStar.MINI_STAR_SKY_NOBLE,
        MiniStar.MINI_STAR_SKY_HAPPINESS,
        MiniStar.MINI_STAR_COOK,
        MiniStar.MINI_STAR_CRY,
        MiniStar.MINI_STAR_LOST,
        MiniStar.MINI_STAR_SKILL,
        MiniStar.MINI_STAR_ART,
        MiniStar.MINI_STAR_FESTIVE,
        MiniStar.MINI_STAR_HAPPINESS,
        MiniStar.MINI_STAR_LONELY,
        MiniStar.MINI_STAR_SINGLE,
        MiniStar.MINI_STAR_DISSOLVE,
        MiniStar.MINI_STAR_BROKEN,
        MiniStar.MINI_STAR_BIG_LOST,
        MiniStar.MINI_STAR_LITTLE_DISASTER,
        MiniStar.MINI_STAR_LUST,
        MiniStar.MINI_STAR_MOON_BENEFACTOR,
        MiniStar.MINI_STAR_GENIUS,
        MiniStar.MINI_STAR_LONGEVITY,
        MiniStar.MINI_STAR_VOID_SKY,
        MiniStar.MINI_STAR_EMPTY,
        MiniStar.MINI_STAR_EMPTY2,
        MiniStar.MINI_STAR_INTERUPTION,
        MiniStar.MINI_STAR_INTERUPTION2,
        MiniStar.MINI_STAR_PLATFORM,
        MiniStar.MINI_STAR_FAME,
        MiniStar.MINI_STAR_PUNISHMENT,
        MiniStar.MINI_STAR_SEX,
        MiniStar.MINI_STAR_WITCH,
        MiniStar.MINI_STAR_ILLNESS,
        MiniStar.MINI_STAR_GHOST,
        MiniStar.MINI_STAR_DISSOLVE2,
        MiniStar.MINI_STAR_BACKBITING,
        MiniStar.MINI_STAR_THREE_PODIUM,
        MiniStar.MINI_STAR_EIGHT_SEAT,
        MiniStar.MINI_STAR_HOLY_LIGHT,
        MiniStar.MINI_STAR_NOBLE,
        MiniStar.MINI_STAR_ANGEL,
        MiniStar.MINI_STAR_INJURY,
    ])

    static twelveScholarStars = Object.freeze([
        MiniStar.MINI_STAR_SCHOLAR,
        MiniStar.MINI_STAR_STRENGTH,
        MiniStar.MINI_STAR_GREEN_DRAGON,
        MiniStar.MINI_STAR_SMALL_LOST,
        MiniStar.MINI_STAR_GENERAL,
        MiniStar.MINI_STAR_LETTER,
        MiniStar.MINI_STAR_BACKBITING2,
        MiniStar.MINI_STAR_JOY,
        MiniStar.MINI_STAR_SICK,
        MiniStar.MINI_STAR_BIG_LOST2,
        MiniStar.MINI_STAR_AMBUSH,
        MiniStar.MINI_STAR_LITIGATION,
    ])

    static twelveYearGodStars = Object.freeze([
        MiniStar.MINI_STAR_YEAR_GOD,
        MiniStar.MINI_STAR_PESSIMISTIC,
        MiniStar.MINI_STAR_BEREAVEMENT,
        MiniStar.MINI_STAR_TRAP,
        MiniStar.MINI_STAR_LAWSUIT,
        MiniStar.MINI_STAR_SMALL_LOST2,
        MiniStar.MINI_STAR_BROKEN_YEAR,
        MiniStar.MINI_STAR_DRAGON_LUCK,
        MiniStar.MINI_STAR_WHITE_TIGER,
        MiniStar.MINI_STAR_GOD_LUCK,
        MiniStar.MINI_STAR_FUNERAL,
        MiniStar.MINI_STAR_SICK2,
    ])

    static twelveLeaderStars = Object.freeze([
        MiniStar.MINI_STAR_LEADER,
        MiniStar.MINI_STAR_MOUNT,
        MiniStar.MINI_STAR_TRANSITION,
        MiniStar.MINI_STAR_IDLE,
        MiniStar.MINI_STAR_MYSTIC,
        MiniStar.MINI_STAR_LITTLE_DISASTER2,
        MiniStar.MINI_STAR_DISASTER,
        MiniStar.MINI_STAR_SKY_DISASTER,
        MiniStar.MINI_STAR_BETRAY,
        MiniStar.MINI_STAR_LUST2,
        MiniStar.MINI_STAR_MOON_MONSTER,
        MiniStar.MINI_STAR_DEAD,
    ])

    static allStars = Object.freeze([
        ...MiniStar.stars,
        ...MiniStar.twelveScholarStars,
        ...MiniStar.twelveYearGodStars,
        ...MiniStar.twelveLeaderStars,
    ])

    static miniStarPlacers: Readonly<Map<MiniStar, MiniStarPlacer>>

    static {
        const miniStarPlacers = new Map<MiniStar, MiniStarPlacer>()

        // 天官
        miniStarPlacers.set(MiniStar.MINI_STAR_SKY_NOBLE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([7, 4, 5, 2, 3, 9, 11, 9, 10, 6][destinyBoard.config.yearSky.index])
            },
        })

        // 天福
        miniStarPlacers.set(MiniStar.MINI_STAR_SKY_HAPPINESS, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([9, 8, 0, 11, 3, 2, 6, 5, 6, 5][destinyBoard.config.yearSky.index])
            },
        })

        // 天廚
        miniStarPlacers.set(MiniStar.MINI_STAR_COOK, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([5, 6, 0, 5, 6, 8, 2, 6, 9, 11][destinyBoard.config.yearSky.index])
            },
        })

        // 天哭
        miniStarPlacers.set(MiniStar.MINI_STAR_CRY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(6).shift(-destinyBoard.config.yearGround.index)
            },
        })

        // 天虛
        miniStarPlacers.set(MiniStar.MINI_STAR_LOST, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(6).shift(destinyBoard.config.yearGround.index)
            },
        })

        // 龍池
        miniStarPlacers.set(MiniStar.MINI_STAR_SKILL, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(4).shift(destinyBoard.config.yearGround.index)
            },
        })

        // 鳳閣
        miniStarPlacers.set(MiniStar.MINI_STAR_ART, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(10).shift(-destinyBoard.config.yearGround.index)
            },
        })

        // 紅鸞
        miniStarPlacers.set(MiniStar.MINI_STAR_FESTIVE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(3).shift(-destinyBoard.config.yearGround.index)
            },
        })

        // 天喜
        miniStarPlacers.set(MiniStar.MINI_STAR_HAPPINESS, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(9).shift(-destinyBoard.config.yearGround.index)
            },
        })

        // 孤辰
        miniStarPlacers.set(MiniStar.MINI_STAR_LONELY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([2, 2, 5, 5, 5, 8, 8, 8, 11, 11, 11, 2][destinyBoard.config.yearGround.index])
            },
        })

        // 寡宿
        miniStarPlacers.set(MiniStar.MINI_STAR_SINGLE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([10, 10, 1, 1, 1, 4, 4, 4, 7, 7, 7, 10][destinyBoard.config.yearGround.index])
            },
        })

        // 解神
        miniStarPlacers.set(MiniStar.MINI_STAR_DISSOLVE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(10).shift(-destinyBoard.config.yearGround.index)
            },
        })

        // 破碎
        miniStarPlacers.set(MiniStar.MINI_STAR_BROKEN, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([5, 1, 9, 5, 1, 9, 5, 1, 9, 5, 1, 9][destinyBoard.config.yearGround.index])
            },
        })

        // 大耗
        miniStarPlacers.set(MiniStar.MINI_STAR_BIG_LOST, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([7, 6, 9, 8, 11, 10, 1, 0, 3, 2, 5, 4][destinyBoard.config.yearGround.index])
            },
        })

        // 劫煞
        miniStarPlacers.set(MiniStar.MINI_STAR_LITTLE_DISASTER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([5, 2, 11, 8, 5, 2, 11, 8, 5, 2, 11, 8][destinyBoard.config.yearGround.index])
            },
        })

        // 咸池
        miniStarPlacers.set(MiniStar.MINI_STAR_LUST, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([9, 6, 3, 0, 9, 6, 3, 0, 9, 6, 3, 0][destinyBoard.config.yearGround.index])
            },
        })

        // 月德
        miniStarPlacers.set(MiniStar.MINI_STAR_MOON_BENEFACTOR, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(5).shift(destinyBoard.config.yearGround.index)
            },
        })

        // 天才
        miniStarPlacers.set(MiniStar.MINI_STAR_GENIUS, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.getCellByTemple(Temple.TEMPLE_DESTINY).getNextICell(destinyBoard.config.yearGround.index).ground
            },
        })

        // 天壽
        miniStarPlacers.set(MiniStar.MINI_STAR_LONGEVITY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.getCellByTemple(Temple.TEMPLE_BODY).getNextICell(destinyBoard.config.yearGround.index).ground
            },
        })

        // 天空
        miniStarPlacers.set(MiniStar.MINI_STAR_VOID_SKY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0][destinyBoard.config.yearGround.index])
            },
        })

        // 旬空
        miniStarPlacers.set(MiniStar.MINI_STAR_EMPTY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const offset = mod(destinyBoard.config.yearSky.index - destinyBoard.config.yearGround.index, 12) / 2
                return Ground.get(10 - 2 * offset)
            },
        })

        // 旬空2
        miniStarPlacers.set(MiniStar.MINI_STAR_EMPTY2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const offset = mod(destinyBoard.config.yearSky.index - destinyBoard.config.yearGround.index, 12) / 2
                return Ground.get(10 - 2 * offset + 1)
            },
        })

        // 截空
        miniStarPlacers.set(MiniStar.MINI_STAR_INTERUPTION, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(8 - ((destinyBoard.config.yearSky.index * 2) % 10))
            },
        })

        // 截空2
        miniStarPlacers.set(MiniStar.MINI_STAR_INTERUPTION2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(8 - ((destinyBoard.config.yearSky.index * 2) % 10) + 1)
            },
        })

        // 台輔
        miniStarPlacers.set(MiniStar.MINI_STAR_PLATFORM, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(6).shift(destinyBoard.config.bornTimeGround.ground.index)
            },
        })

        // 封誥
        miniStarPlacers.set(MiniStar.MINI_STAR_FAME, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(2).shift(destinyBoard.config.bornTimeGround.ground.index)
            },
        })

        // 天刑
        miniStarPlacers.set(MiniStar.MINI_STAR_PUNISHMENT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(9).shift(destinyBoard.config.getLogicalMonth() - 1)
            },
        })

        // 天姚
        miniStarPlacers.set(MiniStar.MINI_STAR_SEX, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get(1).shift(destinyBoard.config.getLogicalMonth() - 1)
            },
        })

        // 天巫
        miniStarPlacers.set(MiniStar.MINI_STAR_WITCH, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([5, 8, 2, 11, 5, 8, 2, 11, 5, 8, 2, 11][destinyBoard.config.getLogicalMonth() - 1])
            },
        })

        // 天月
        miniStarPlacers.set(MiniStar.MINI_STAR_ILLNESS, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([10, 5, 4, 2, 7, 3, 11, 7, 2, 6, 10, 2][destinyBoard.config.getLogicalMonth() - 1])
            },
        })

        // 陰煞
        miniStarPlacers.set(MiniStar.MINI_STAR_GHOST, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([2, 0, 10, 8, 6, 4, 2, 0, 10, 8, 6, 4][destinyBoard.config.getLogicalMonth() - 1])
            },
        })

        // 解神2
        miniStarPlacers.set(MiniStar.MINI_STAR_DISSOLVE2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([8, 8, 10, 10, 0, 0, 2, 2, 4, 4, 6, 6][destinyBoard.config.getLogicalMonth() - 1])
            },
        })

        // 蜚廉
        // 子丑寅年在申酉戍, 卯辰巳年在巳午未, 午未申年在寅卯辰, 酉戍亥年在亥子丑
        miniStarPlacers.set(MiniStar.MINI_STAR_BACKBITING, {
            evalGround: (destinyBoard: DestinyBoard) => {
                const yearSkyGroundIndex = destinyBoard.config.yearGround.index
                if (intDivide(yearSkyGroundIndex, 3) === 0) {
                    // 子丑寅
                    return Ground.get(8 + (yearSkyGroundIndex % 3))
                } else if (intDivide(yearSkyGroundIndex, 3) === 1) {
                    // 卯辰巳
                    return Ground.get(5 + (yearSkyGroundIndex % 3))
                } else if (intDivide(yearSkyGroundIndex, 3) === 2) {
                    // 午未申
                    return Ground.get(2 + (yearSkyGroundIndex % 3))
                } else if (intDivide(yearSkyGroundIndex, 3) === 3) {
                    // 酉戍亥
                    return Ground.get(11 + (yearSkyGroundIndex % 3))
                }
                throw new Error('Cannot eval')
            },
        })

        // 博士
        miniStarPlacers.set(MiniStar.MINI_STAR_SCHOLAR, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers.get(MinorStar.MINOR_STAR_EARN)!.evalGround(destinyBoard)
            },
        })

        // 力士
        miniStarPlacers.set(MiniStar.MINI_STAR_STRENGTH, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction)
            },
        })

        // 青龍
        miniStarPlacers.set(MiniStar.MINI_STAR_GREEN_DRAGON, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 2)
            },
        })

        // 小耗
        miniStarPlacers.set(MiniStar.MINI_STAR_SMALL_LOST, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 3)
            },
        })

        // 將軍
        miniStarPlacers.set(MiniStar.MINI_STAR_GENERAL, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 4)
            },
        })

        // 奏書
        miniStarPlacers.set(MiniStar.MINI_STAR_LETTER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 5)
            },
        })

        // 蜚廉2
        miniStarPlacers.set(MiniStar.MINI_STAR_BACKBITING2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 6)
            },
        })

        // 喜神
        miniStarPlacers.set(MiniStar.MINI_STAR_JOY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 7)
            },
        })

        // 病符
        miniStarPlacers.set(MiniStar.MINI_STAR_SICK, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 8)
            },
        })

        // 大耗2
        miniStarPlacers.set(MiniStar.MINI_STAR_BIG_LOST2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 9)
            },
        })

        // 伏兵
        miniStarPlacers.set(MiniStar.MINI_STAR_AMBUSH, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 10)
            },
        })

        // 官府
        miniStarPlacers.set(MiniStar.MINI_STAR_LITIGATION, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_EARN)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.configDirection.direction * 11)
            },
        })

        // 三台
        miniStarPlacers.set(MiniStar.MINI_STAR_THREE_PODIUM, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_SUPPORT_LEFT)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.config.day - 1)
            },
        })

        // 八座
        miniStarPlacers.set(MiniStar.MINI_STAR_EIGHT_SEAT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_SUPPORT_RIGHT)!
                    .evalGround(destinyBoard)
                    .shift(-(destinyBoard.config.day - 1))
            },
        })

        // 恩光
        miniStarPlacers.set(MiniStar.MINI_STAR_HOLY_LIGHT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_CLEVER)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.config.day - 2)
            },
        })

        // 天貴
        miniStarPlacers.set(MiniStar.MINI_STAR_NOBLE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return MinorStar.minorStarPlacers
                    .get(MinorStar.MINOR_STAR_SKILL)!
                    .evalGround(destinyBoard)
                    .shift(destinyBoard.config.day - 2)
            },
        })

        // 太歲
        miniStarPlacers.set(MiniStar.MINI_STAR_YEAR_GOD, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround
            },
        })

        // 晦氣
        miniStarPlacers.set(MiniStar.MINI_STAR_PESSIMISTIC, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(1)
            },
        })

        // 喪門
        miniStarPlacers.set(MiniStar.MINI_STAR_BEREAVEMENT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(2)
            },
        })

        // 貫索
        miniStarPlacers.set(MiniStar.MINI_STAR_TRAP, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(3)
            },
        })

        // 官符
        miniStarPlacers.set(MiniStar.MINI_STAR_LAWSUIT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(4)
            },
        })

        // 小耗
        miniStarPlacers.set(MiniStar.MINI_STAR_SMALL_LOST2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(5)
            },
        })

        // 歲破
        miniStarPlacers.set(MiniStar.MINI_STAR_BROKEN_YEAR, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(6)
            },
        })

        // 龍德
        miniStarPlacers.set(MiniStar.MINI_STAR_DRAGON_LUCK, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(7)
            },
        })

        // 白虎
        miniStarPlacers.set(MiniStar.MINI_STAR_WHITE_TIGER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(8)
            },
        })

        // 天德
        miniStarPlacers.set(MiniStar.MINI_STAR_GOD_LUCK, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(9)
            },
        })

        // 弔客
        miniStarPlacers.set(MiniStar.MINI_STAR_FUNERAL, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(10)
            },
        })

        // 病符
        miniStarPlacers.set(MiniStar.MINI_STAR_SICK2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return destinyBoard.config.yearGround.shift(11)
            },
        })

        // 天使
        miniStarPlacers.set(MiniStar.MINI_STAR_ANGEL, {
            evalGround: (destinyBoard: DestinyBoard) => {
                if (destinyBoard.configDirection === Direction.CLOCKWISE) {
                    return destinyBoard.getCellByTemple(Temple.TEMPLE_ILLNESS).ground
                }
                return destinyBoard.getCellByTemple(Temple.TEMPLE_FRIEND).ground
            },
        })

        // 天傷
        miniStarPlacers.set(MiniStar.MINI_STAR_INJURY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                if (destinyBoard.configDirection === Direction.CLOCKWISE) {
                    return destinyBoard.getCellByTemple(Temple.TEMPLE_FRIEND).ground
                }
                return destinyBoard.getCellByTemple(Temple.TEMPLE_ILLNESS).ground
            },
        })

        // 將星
        miniStarPlacers.set(MiniStar.MINI_STAR_LEADER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([0, 9, 6, 3, 0, 9, 6, 3, 0, 9, 6, 3][destinyBoard.config.yearGround.index])
            },
        })

        // 攀鞍
        miniStarPlacers.set(MiniStar.MINI_STAR_MOUNT, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([1, 10, 7, 4, 1, 10, 7, 4, 1, 10, 7, 4][destinyBoard.config.yearGround.index])
            },
        })

        // 歲驛
        miniStarPlacers.set(MiniStar.MINI_STAR_TRANSITION, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([2, 11, 8, 5, 2, 11, 8, 5, 2, 11, 8, 5][destinyBoard.config.yearGround.index])
            },
        })

        // 息神
        miniStarPlacers.set(MiniStar.MINI_STAR_IDLE, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([3, 0, 9, 6, 3, 0, 9, 6, 3, 0, 9, 6][destinyBoard.config.yearGround.index])
            },
        })

        // 華蓋
        miniStarPlacers.set(MiniStar.MINI_STAR_MYSTIC, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([4, 1, 10, 7, 4, 1, 10, 7, 4, 1, 10, 7][destinyBoard.config.yearGround.index])
            },
        })

        // 劫煞2
        miniStarPlacers.set(MiniStar.MINI_STAR_LITTLE_DISASTER2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([5, 2, 11, 8, 5, 2, 11, 8, 5, 2, 11, 8][destinyBoard.config.yearGround.index])
            },
        })

        // 災煞
        miniStarPlacers.set(MiniStar.MINI_STAR_DISASTER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([6, 3, 0, 9, 6, 3, 0, 9, 6, 3, 0, 9][destinyBoard.config.yearGround.index])
            },
        })

        // 天煞
        miniStarPlacers.set(MiniStar.MINI_STAR_SKY_DISASTER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([7, 4, 1, 10, 7, 4, 1, 10, 7, 4, 1, 10][destinyBoard.config.yearGround.index])
            },
        })

        // 天煞
        miniStarPlacers.set(MiniStar.MINI_STAR_BETRAY, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([8, 5, 2, 11, 8, 5, 2, 11, 8, 5, 2, 11][destinyBoard.config.yearGround.index])
            },
        })

        // 咸池2
        miniStarPlacers.set(MiniStar.MINI_STAR_LUST2, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([9, 6, 3, 0, 9, 6, 3, 0, 9, 6, 3, 0][destinyBoard.config.yearGround.index])
            },
        })

        // 月煞
        miniStarPlacers.set(MiniStar.MINI_STAR_MOON_MONSTER, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([10, 7, 4, 1, 10, 7, 4, 1, 10, 7, 4, 1][destinyBoard.config.yearGround.index])
            },
        })

        // 亡神
        miniStarPlacers.set(MiniStar.MINI_STAR_DEAD, {
            evalGround: (destinyBoard: DestinyBoard) => {
                return Ground.get([11, 8, 5, 2, 11, 8, 5, 2, 11, 8, 5, 2][destinyBoard.config.yearGround.index])
            },
        })

        MiniStar.miniStarPlacers = Object.freeze(miniStarPlacers)
    }

    getType(): string {
        return 'MiniStar'
    }

    getKey() {
        return this.key
    }

    getDisplayName() {
        return this.displayName
    }

    static getByKey(key: string): MiniStar | null {
        return MiniStar.allStars.find((star) => star.getKey() === key) ?? null
    }

    static getByName(name: string) {
        const isSecond = name.endsWith('2')
        if (isSecond) {
            name = name.replace('2', '')
        }
        return MiniStar.allStars.find((star) => star.getDisplayName() === name && star.key.endsWith('2') === isSecond) ?? null
    }

    equals(star: Star) {
        return star === this || (star.getType() === this.getType() && star.getKey() === this.getKey())
    }
}

declare interface MiniStarPlacer {
    evalGround: (destinyBoard: DestinyBoard) => Ground
}

export { MiniStar }
