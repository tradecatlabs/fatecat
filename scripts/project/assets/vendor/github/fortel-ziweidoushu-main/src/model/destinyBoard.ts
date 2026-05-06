import { mod } from './../utils'
import { Cell, BorrowCell } from './cell'
import { ConfigType, DestinyConfig, Gender } from './destinyConfig'
import { Ground } from './ground'
import { LifeStage } from './lifeStage'
import { MajorStar } from './majorStar'
import { MiniStar } from './miniStar'
import { MinorStar } from './minorStar'
import { Element, ShadowLight, Direction } from './miscEnums'
import { Sky } from './sky'
import { StarDerivative } from './starDerivative'
import { Temple } from './temple'
import util from 'util'
import { Star } from './star'
import type { Calendar } from './../calendar/calender'
import { defaultCalendar, Runtime } from '../main'

class DestinyBoard {
    config: DestinyConfig
    element: Element
    #destinyMaster?: MajorStar | MinorStar
    #bodyMaster?: MajorStar | MinorStar
    #startControl?: Ground
    #cells: Cell[] = []
    #destinyTempleCellGround?: Ground
    // cellGroundZeroIndex?: number
    #bornStarDerivativeMap = new Map<StarDerivative, MajorStar | MinorStar>()

    constructor(destinyConfig: DestinyConfig) {
        this.config = destinyConfig
        this.element = Element.FIRE
        this.#setupStartControl()
        this.#setupDestinyBodyMaster()
        this.#setupBasicTempleCells()
        this.#setupTemples()
        this.#setupElements()
        this.#setupLifeStage()
        this.#setupAgeRange()
        this.#setupMajorStars()
        this.#setupMinorStars()
        this.#setupMiniStars()
        this.#setupBornStarDerivative()
        this.#setupBorrowCells()
        Object.freeze(this)
    }

    get destinyMaster() {
        if (this.#destinyMaster !== undefined) {
            return this.#destinyMaster
        }
        throw new Error('destinyMaster not defined.')
    }

    get bodyMaster() {
        if (this.#bodyMaster !== undefined) {
            return this.#bodyMaster
        }
        throw new Error('bodyMaster not defined.')
    }

    get startControl() {
        if (this.#startControl !== undefined) {
            return this.#startControl
        }
        throw new Error('startControl not defined.')
    }

    get destinyTempleCellGround() {
        if (this.#destinyTempleCellGround !== undefined) {
            return this.#destinyTempleCellGround
        }
        throw new Error('destinyTempleCellGround not defined.')
    }

    get cells() {
        return this.#cells
    }

    get bornStarDerivativeMap() {
        return this.#bornStarDerivativeMap
    }

    #setupStartControl(): void {
        this.#startControl = this.config.bornTimeGround.ground.shift(-this.config.getLogicalMonth() + 1)
    }

    #setupDestinyBodyMaster(): void {
        this.#destinyMaster = [
            MajorStar.MAJOR_STAR_GREED,
            MajorStar.MAJOR_STAR_ARGUMENT,
            MinorStar.MINOR_STAR_EARN,
            MinorStar.MINOR_STAR_SKILL,
            MajorStar.MAJOR_STAR_FIRE,
            MajorStar.MAJOR_STAR_GOLD,
            MajorStar.MAJOR_STAR_PIONEER,
            MajorStar.MAJOR_STAR_GOLD,
            MajorStar.MAJOR_STAR_FIRE,
            MinorStar.MINOR_STAR_SKILL,
            MinorStar.MINOR_STAR_EARN,
            MajorStar.MAJOR_STAR_ARGUMENT,
        ][this.config.yearGround.index]

        this.#bodyMaster = [
            MinorStar.MINOR_STAR_BURNING,
            MajorStar.MAJOR_STAR_SUPPORT,
            MajorStar.MAJOR_STAR_RULE,
            MajorStar.MAJOR_STAR_ENJOYMENT,
            MinorStar.MINOR_STAR_CLEVER,
            MajorStar.MAJOR_STAR_CHANGE,
            MinorStar.MINOR_STAR_BURNING,
            MajorStar.MAJOR_STAR_SUPPORT,
            MajorStar.MAJOR_STAR_RULE,
            MajorStar.MAJOR_STAR_ENJOYMENT,
            MinorStar.MINOR_STAR_CLEVER,
            MajorStar.MAJOR_STAR_CHANGE,
        ][this.config.yearGround.index]
    }

    #setupBasicTempleCells(): void {
        const cells: Cell[] = []
        const tempCells: Cell[] = []

        // build cells
        for (let i = 0; i < 12; i++) {
            const cell: Cell = new Cell(Sky.get((this.config.yearSky.index % 5) * 2 + 2 + i), Ground.get(i + 2))
            tempCells.push(cell)
        }
        for (let i = -2; i < -2 + 12; i++) {
            const cell = tempCells[mod(i, 12)]
            cell.cellIndex = cells.length
            //cell.cells = cells
            cell.prevCell = tempCells[mod(i - 1, 12)]
            cell.nextCell = tempCells[mod(i + 1, 12)]
            cells.push(tempCells[mod(i, 12)])
        }

        this.#cells = cells //assign cells

        // store cellGroundZeroIndex
        // for (let i = 0; i < cells.length; i++) {
        //     if (cells[i].ground === Ground.get(0)) {
        //         this.cellGroundZeroIndex = i
        //         break
        //     }
        // }
    }

    #setupTemples(): void {
        // 安身
        const bodyTempleGround = this.config.bornTimeGround.ground.shift(2 + this.config.getLogicalMonth() - 1)

        let destinyTempleCellGround: Ground

        // 安命
        switch (this.config.configType) {
            case ConfigType.GROUND:
                destinyTempleCellGround = bodyTempleGround
                break
            case ConfigType.HUMAN:
                destinyTempleCellGround = Ground.get(-this.config.bornTimeGround.ground.index + 2 + this.config.getLogicalMonth() - 1 + 2)
                break
            case ConfigType.SKY:
            default:
                destinyTempleCellGround = Ground.get(-this.config.bornTimeGround.ground.index + 2 + this.config.getLogicalMonth() - 1)
        }
        this.#destinyTempleCellGround = destinyTempleCellGround

        this.getCellByGround(destinyTempleCellGround).temples.push(Temple.TEMPLE_DESTINY)
        this.getCellByGround(bodyTempleGround).temples.push(Temple.TEMPLE_BODY)

        for (let i = Temple.LOOP_TEMPLES.indexOf(Temple.TEMPLE_BROTHER); i < Temple.LOOP_TEMPLES.length; i++) {
            const templeGround = Ground.get(destinyTempleCellGround.index - i)
            this.getCellByGround(templeGround).temples.push(Temple.LOOP_TEMPLES[i])
        }
    }

    #setupBorrowCells(): void {
        for (const cell of this.#cells) {
            if (cell.majorStars.length == 0) {
                if (cell.getNextICell(4).majorStars.length == 0) {
                    cell.borrowCells.push(
                        Object.freeze(new BorrowCell(cell.getNextICell(6), 54.26)),
                        Object.freeze(new BorrowCell(cell.getPrevICell(4), 32.45)),
                        Object.freeze(new BorrowCell(cell.getPrevICell(2), 13.29)),
                    )
                } else if (cell.getPrevICell(4).majorStars.length == 0) {
                    cell.borrowCells.push(
                        Object.freeze(new BorrowCell(cell.getNextICell(6), 54.26)),
                        Object.freeze(new BorrowCell(cell.getNextICell(4), 32.45)),
                        Object.freeze(new BorrowCell(cell.getNextICell(2), 13.29)),
                    )
                } else {
                    cell.borrowCells.push(
                        Object.freeze(new BorrowCell(cell.getNextICell(6), 51)),
                        Object.freeze(new BorrowCell(cell.getNextICell(4), 24.5)),
                        Object.freeze(new BorrowCell(cell.getPrevICell(4), 24.5)),
                    )
                }
            }
        }
    }

    #setupElements(): void {
        const cell = this.getCellByTemple(Temple.TEMPLE_DESTINY)
        const skyGroup = Math.round(Math.floor(cell.sky.index / 2))
        const groundGroup = Math.round(Math.floor(cell.ground.index / 2))

        if (skyGroup >= 0 && skyGroup < 10 / 2 && groundGroup >= 0 && groundGroup < 12 / 2) {
            const mapping = [
                [Element.GOLD, Element.WATER, Element.FIRE, Element.GOLD, Element.WATER, Element.FIRE],
                [Element.WATER, Element.FIRE, Element.EARTH, Element.WATER, Element.FIRE, Element.EARTH],
                [Element.FIRE, Element.EARTH, Element.WOOD, Element.FIRE, Element.EARTH, Element.WOOD],
                [Element.EARTH, Element.WOOD, Element.GOLD, Element.EARTH, Element.WOOD, Element.GOLD],
                [Element.WOOD, Element.GOLD, Element.WATER, Element.WOOD, Element.GOLD, Element.WATER],
            ]
            this.element = mapping[skyGroup][groundGroup]
        }
    }

    #setupLifeStage(): void {
        let ground: Ground
        if (this.element == Element.WATER) {
            ground = Ground.get(8)
        } else if (this.element == Element.WOOD) {
            ground = Ground.get(11)
        } else if (this.element == Element.GOLD) {
            ground = Ground.get(5)
        } else if (this.element == Element.EARTH) {
            ground = Ground.get(8)
        } else {
            ground = Ground.get(2)
        }

        const direction = this.configDirection
        const beginCell = this.getCellByGround(ground)
        for (let i = 0; i < this.#cells.length; i++) {
            beginCell.getNextICell(i * direction.direction).lifeStage = LifeStage.values[i]
        }
    }

    #setupAgeRange(): void {
        const direction = this.configDirection
        const ageStart = this.element.patternNumber
        const destinyCell = this.getCellByTemple(Temple.TEMPLE_DESTINY)

        for (let i = 0; i < this.#cells.length; i++) {
            destinyCell.getNextICell(i * direction.direction).ageStart = ageStart + 10 * i
        }
    }

    #setupMajorStars(): void {
        for (const [majorStar, majorStarPlacer] of MajorStar.majorStarPlacers.entries()) {
            const ground = majorStarPlacer.evalGround(this)
            const cell = this.getCellByGround(ground)
            cell.majorStars.push(majorStar)
        }
    }

    #setupMinorStars(): void {
        for (const [minorStar, minorStarPlacer] of MinorStar.minorStarPlacers.entries()) {
            const ground = minorStarPlacer.evalGround(this)
            const cell = this.getCellByGround(ground)
            cell.minorStars.push(minorStar)
        }
    }

    #setupMiniStars(): void {
        for (const miniStar of MiniStar.stars) {
            const miniStarPlacer = MiniStar.miniStarPlacers.get(miniStar)
            if (!miniStarPlacer) {
                throw new Error('miniStarPlacer not found')
            }
            const ground = miniStarPlacer.evalGround(this)
            const cell = this.getCellByGround(ground)
            cell.miniStars.push(miniStar)
        }

        for (const miniStar of MiniStar.twelveScholarStars) {
            const miniStarPlacer = MiniStar.miniStarPlacers.get(miniStar)
            if (!miniStarPlacer) {
                throw new Error('miniStarPlacer not found')
            }
            const ground = miniStarPlacer.evalGround(this)
            const cell = this.getCellByGround(ground)
            cell.scholarStar = miniStar
        }

        for (const miniStar of MiniStar.twelveYearGodStars) {
            const miniStarPlacer = MiniStar.miniStarPlacers.get(miniStar)
            if (!miniStarPlacer) {
                throw new Error('miniStarPlacer not found')
            }
            const ground = miniStarPlacer.evalGround(this)
            const cell = this.getCellByGround(ground)
            cell.yearGodStar = miniStar
        }

        for (const miniStar of MiniStar.twelveLeaderStars) {
            const miniStarPlacer = MiniStar.miniStarPlacers.get(miniStar)
            if (!miniStarPlacer) {
                throw new Error('miniStarPlacer not found')
            }
            const ground = miniStarPlacer.evalGround(this)
            const cell = this.getCellByGround(ground)
            cell.leaderStar = miniStar
        }
    }

    #setupBornStarDerivative(): void {
        this.#bornStarDerivativeMap.set(StarDerivative.WEALTHINESS, StarDerivative.getWealthinessStar(this.config.yearSky))
        this.#bornStarDerivativeMap.set(StarDerivative.POWER, StarDerivative.getPowerStar(this.config.yearSky))
        this.#bornStarDerivativeMap.set(StarDerivative.FAME, StarDerivative.getFameStar(this.config.yearSky))
        this.#bornStarDerivativeMap.set(StarDerivative.PROBLEM, StarDerivative.getProblemStar(this.config.yearSky))
        Object.freeze(this.#bornStarDerivativeMap)
    }

    getCellByGround(ground: Ground): Cell {
        return this.#cells[ground.index]
    }

    getCellByTemple(temple: Temple): Cell {
        const targetCell = this.#cells.find((cell) => {
            return cell.temples.map((temple) => temple.key).includes(temple.key)
        })

        if (targetCell) {
            return targetCell
        } else {
            throw new Error('Cannot find cell')
        }
    }

    getCellByStar(star: Star): Cell {
        const targetCell = this.cells.find((cell) => {
            return cell.allStars.includes(star)
        })
        if (!targetCell) {
            throw new Error('Cannot find cell')
        }
        return targetCell
    }

    getTenYearSky(age: number): Sky {
        const direction = this.configDirection.direction
        const destinyCell = this.getCellByTemple(Temple.TEMPLE_DESTINY)

        const cycleAgeEnd = destinyCell.getNextICell(-1 * direction).ageEnd
        const logicalAge = mod(age, cycleAgeEnd)

        let targetCell: Cell | undefined
        for (let i = 0; i < this.#cells.length; i++) {
            const cell = destinyCell.getNextICell(i * direction)
            if (logicalAge <= cell.ageEnd) {
                targetCell = cell
                break
            }
        }

        if (targetCell) {
            return targetCell.sky
        } else {
            throw new Error('Cannot find ten year sky for unknown reason.')
        }
    }

    getTenYearCellGround(age: number): Ground {
        const direction = this.configDirection.direction
        const destinyCell = this.getCellByTemple(Temple.TEMPLE_DESTINY)

        const cycleAgeEnd = destinyCell.getNextICell(-1 * direction).ageEnd
        const logicalAge = mod(age, cycleAgeEnd)

        let targetCell: Cell | undefined
        for (let i = 0; i < this.#cells.length; i++) {
            const cell = destinyCell.getNextICell(i * direction)
            if (logicalAge <= cell.ageEnd) {
                targetCell = cell
                break
            }
        }

        if (targetCell) {
            return targetCell.ground
        } else {
            throw new Error('Cannot find ten year ground for unknown reason.')
        }
    }

    getRuntimContext({
        lunarYear,
        lunarMonth,
        lunarDay,
        leap,
        calendar,
    }: {
        lunarYear: number
        lunarMonth: number
        lunarDay: number
        leap: boolean
        calendar?: Calendar
    }): RuntimeContext {
        calendar = calendar ?? defaultCalendar

        const age = lunarYear - this.config.year + 1
        const tenYearGround = this.getTenYearCellGround(age)

        const runtimeDateContext = {
            age,
            effectiveMonth: lunarMonth + (leap && lunarDay > 15 ? 1 : 0),
            tenYearGround,
            tenYearSky: this.getCellByGround(tenYearGround).sky,
            ...calendar.lunarSkyGround(lunarYear, lunarMonth, lunarDay, leap),
        }

        runtimeDateContext.monthSky = Sky.get((((runtimeDateContext.yearSky.index % 5) + 1) * 2 + (runtimeDateContext.effectiveMonth - 1)) % 10)
        runtimeDateContext.monthGround = Ground.get(runtimeDateContext.effectiveMonth + 1)

        const runtimeBoardState: {
            tenYear: {
                cellGround: Ground | null
                groundStars: Map<Ground, MinorStar[]> | null
                starDerivativeMap: Map<MajorStar | MinorStar, StarDerivative> | null
            }
            year: {
                cellGround: Ground | null
                groundStars: Map<Ground, MinorStar[]> | null
                starDerivativeMap: Map<MajorStar | MinorStar, StarDerivative> | null
            }
            month: {
                cellGround: Ground | null
                groundStars: Map<Ground, MinorStar[]> | null
                starDerivativeMap: Map<MajorStar | MinorStar, StarDerivative> | null
            }
            day: {
                cellGround: Ground | null
                groundStars: Map<Ground, MinorStar[]> | null
                starDerivativeMap: Map<MajorStar | MinorStar, StarDerivative> | null
            }
        } = {
            tenYear: { cellGround: null, groundStars: null, starDerivativeMap: null },
            year: { cellGround: null, groundStars: null, starDerivativeMap: null },
            month: { cellGround: null, groundStars: null, starDerivativeMap: null },
            day: { cellGround: null, groundStars: null, starDerivativeMap: null },
        }

        runtimeBoardState.tenYear.cellGround = runtimeDateContext.tenYearGround
        runtimeBoardState.tenYear.groundStars = Runtime.getRuntimeLocationStars(runtimeDateContext.tenYearSky)
        runtimeBoardState.tenYear.starDerivativeMap = Runtime.getStarToDerivativeMapOf(runtimeDateContext.tenYearSky)

        runtimeBoardState.year.cellGround = runtimeDateContext.yearGround
        runtimeBoardState.year.groundStars = Runtime.getRuntimeLocationStars(runtimeDateContext.yearSky)
        runtimeBoardState.year.starDerivativeMap = Runtime.getStarToDerivativeMapOf(runtimeDateContext.yearSky)

        runtimeBoardState.month.cellGround = this.startControl.shift(runtimeDateContext.yearGround.index).shift(lunarMonth - 1)
        runtimeBoardState.month.groundStars = Runtime.getRuntimeLocationStars(runtimeDateContext.monthSky)
        runtimeBoardState.month.starDerivativeMap = Runtime.getStarToDerivativeMapOf(runtimeDateContext.monthSky)

        runtimeBoardState.day.cellGround = runtimeBoardState.month.cellGround.shift(lunarDay - 1)
        if (leap) {
            runtimeBoardState.day.cellGround = runtimeBoardState.day.cellGround.shift(calendar.lunarMonthDays(lunarYear, lunarMonth, false))
        }
        runtimeBoardState.day.groundStars = Runtime.getRuntimeLocationStars(runtimeDateContext.daySky)
        runtimeBoardState.day.starDerivativeMap = Runtime.getStarToDerivativeMapOf(runtimeDateContext.daySky)

        return {
            ...runtimeDateContext,
            ...runtimeBoardState,
        }
    }

    get shadowLight(): ShadowLight {
        return this.config.yearSky.index % 2 == 0 ? ShadowLight.LIGHT : ShadowLight.SHADOW
    }

    get configDirection(): Direction {
        const direction = this.shadowLight === ShadowLight.LIGHT ? Direction.CLOCKWISE : Direction.ANTI_CLOCKWISE
        return direction.add(this.config.gender == Gender.M ? Direction.CLOCKWISE : Direction.ANTI_CLOCKWISE)
    }

    getMajorStarEnergyLevel(majorStar: MajorStar) {
        return MajorStar.majorStarPlacers.get(majorStar)!.evalEnergyLevel(MajorStar.majorStarPlacers.get(majorStar)!.evalGround(this))
    }

    getMajorStarDerivative(star: MajorStar | MinorStar) {
        if (this.#bornStarDerivativeMap.get(StarDerivative.WEALTHINESS)?.equals(star)) {
            return StarDerivative.WEALTHINESS
        } else if (this.#bornStarDerivativeMap.get(StarDerivative.POWER)?.equals(star)) {
            return StarDerivative.POWER
        } else if (this.#bornStarDerivativeMap.get(StarDerivative.FAME)?.equals(star)) {
            return StarDerivative.FAME
        } else if (this.#bornStarDerivativeMap.get(StarDerivative.PROBLEM)?.equals(star)) {
            return StarDerivative.PROBLEM
        } else {
            return null
        }
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars
    [util.inspect.custom](depth: number, opts: any): string {
        return util.inspect(this.toJSON(), opts)
    }

    toJSON() {
        return {
            config: this.config,
            element: this.element,
            destinyMaster: this.#destinyMaster,
            bodyMaster: this.#bodyMaster,
            startControl: this.#startControl,
            cells: this.#cells,
            bornStarDerivativeMap: Object.fromEntries(this.#bornStarDerivativeMap),
        }
    }

    // prettier-ignore
    toString(): string {
        const cellsString = this.#cells.map((cell) => '        ' + cell.toString()).join(',\n')

        return (
            `DestinyBoard {\n`+
            `    config: ${this.config},\n`+
            `    element: ${this.element},\n`+
            `    destinyMaster: ${this.#destinyMaster},\n`+
            `    bodyMaster: ${this.#bodyMaster},\n`+
            `    startControl: ${this.#startControl},\n`+
            `    cells: [\n`+
                cellsString+'\n'+
            `    ],\n`+
            `    #bornStarDerivativeMap: ${JSON.stringify(Object.fromEntries(this.#bornStarDerivativeMap))}\n`+
            `}`
        )
    }
}

export type RuntimeContext = {
    tenYear: {
        cellGround: Ground | null
        groundStars: Map<Ground, MinorStar[]> | null
        starDerivativeMap: Map<MajorStar | MinorStar, StarDerivative> | null
    }
    year: {
        cellGround: Ground | null
        groundStars: Map<Ground, MinorStar[]> | null
        starDerivativeMap: Map<MajorStar | MinorStar, StarDerivative> | null
    }
    month: {
        cellGround: Ground | null
        groundStars: Map<Ground, MinorStar[]> | null
        starDerivativeMap: Map<MajorStar | MinorStar, StarDerivative> | null
    }
    day: {
        cellGround: Ground | null
        groundStars: Map<Ground, MinorStar[]> | null
        starDerivativeMap: Map<MajorStar | MinorStar, StarDerivative> | null
    }
    yearSky: Sky
    yearGround: Ground
    monthSky: Sky
    monthGround: Ground
    daySky: Sky
    dayGround: Ground
    age: number
    effectiveMonth: number
    tenYearGround: Ground
    tenYearSky: Sky
}

export { DestinyBoard }
