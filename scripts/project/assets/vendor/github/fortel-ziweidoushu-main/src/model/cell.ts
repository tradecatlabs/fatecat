import { Ground } from './ground'
import { LifeStage } from './lifeStage'
import { MajorStar } from './majorStar'
import { MiniStar } from './miniStar'
import { MinorStar } from './minorStar'
import { Sky } from './sky'
import { Temple } from './temple'
import util from 'util'
import { mod } from './../utils'
import { Star } from './star'

class Cell {
    #sky: Sky
    #ground: Ground
    #temples: Temple[] = []
    #majorStars: MajorStar[] = []
    #minorStars: MinorStar[] = []
    #miniStars: MiniStar[] = []

    #borrowCells: Readonly<BorrowCell>[] = []

    #leaderStar?: MiniStar
    #yearGodStar?: MiniStar
    #scholarStar?: MiniStar

    #ageStart?: number

    #lifeStage?: LifeStage

    //metadata

    #cellIndex?: number

    //cells: Cell[] = []
    #prevCell?: Cell
    #nextCell?: Cell

    constructor(sky: Sky, ground: Ground) {
        this.#sky = sky
        this.#ground = ground
    }

    get sky(): Sky {
        return this.#sky
    }

    get ground(): Ground {
        return this.#ground
    }

    get temples(): Temple[] {
        return this.#temples
    }

    get majorStars(): MajorStar[] {
        return this.#majorStars
    }

    get minorStars(): MinorStar[] {
        return this.#minorStars
    }

    get miniStars(): MiniStar[] {
        return this.#miniStars
    }

    get allStars(): Star[] {
        return [...this.#majorStars, ...this.#minorStars, ...this.allMiniStars]
    }

    get allMiniStars(): MiniStar[] {
        return [...this.#miniStars, this.#scholarStar!, this.#yearGodStar!, this.#leaderStar!]
    }

    get borrowCells(): Readonly<BorrowCell>[] {
        return this.#borrowCells
    }

    get leaderStar(): MiniStar {
        if (this.#leaderStar) {
            return this.#leaderStar
        }
        throw new Error('Leader Star not found.')
    }

    set leaderStar(leaderStar: MiniStar) {
        this.#leaderStar = leaderStar
    }

    get yearGodStar(): MiniStar {
        if (this.#yearGodStar) {
            return this.#yearGodStar
        }
        throw new Error('Year God Star not found.')
    }

    set yearGodStar(yearGodStar: MiniStar) {
        this.#yearGodStar = yearGodStar
    }

    get scholarStar(): MiniStar {
        if (this.#scholarStar) {
            return this.#scholarStar
        }
        throw new Error('Scholar Star not found.')
    }

    set scholarStar(scholarStar: MiniStar) {
        this.#scholarStar = scholarStar
    }

    get ageStart(): number {
        if (this.#ageStart !== undefined) {
            return this.#ageStart
        }
        throw new Error('Age Start not found.')
    }

    set ageStart(ageStart: number) {
        this.#ageStart = ageStart
    }

    get ageEnd(): number {
        if (this.#ageStart !== undefined) {
            return this.#ageStart + 9
        }
        throw new Error('Age End not found.')
    }

    get lifeStage(): LifeStage {
        if (this.#lifeStage !== undefined) {
            return this.#lifeStage
        }
        throw new Error('Life Stage not found.')
    }

    set lifeStage(lifeStage: LifeStage) {
        this.#lifeStage = lifeStage
    }

    get cellIndex(): number {
        if (this.#cellIndex !== undefined) {
            return this.#cellIndex
        }
        throw new Error('Cell Index not found.')
    }

    set cellIndex(cellIndex: number) {
        this.#cellIndex = cellIndex
    }

    get prevCell(): Cell {
        if (this.#prevCell !== undefined) {
            return this.#prevCell
        }
        throw new Error('prevCell not found.')
    }

    set prevCell(cell: Cell) {
        this.#prevCell = cell
    }

    get nextCell(): Cell {
        if (this.#nextCell !== undefined) {
            return this.#nextCell
        }
        throw new Error('nextCell not found.')
    }

    set nextCell(cell: Cell) {
        this.#nextCell = cell
    }

    get self(): Cell {
        return this
    }

    getPrevICell(i: number): Cell {
        if (i < 0) {
            return this.getNextICell(-i)
        }
        let cell: Cell = this.self
        for (let j = 0; j < i; j++) {
            if (cell.prevCell === undefined) {
                throw new Error('Prev Cell not defined!')
            }
            cell = cell.prevCell
        }
        return cell
        // return this.cells![mod(this.cellIndex! - i, this.cells!.length)]
    }

    getNextICell(i: number): Cell {
        if (i < 0) {
            return this.getPrevICell(-i)
        }
        let cell: Cell = this.self
        for (let j = 0; j < i; j++) {
            if (cell.nextCell === undefined) {
                throw new Error('Next Cell not defined!')
            }
            cell = cell.nextCell
        }
        return cell
        // return this.cells![mod(this.cellIndex! + i, this.cells!.length)]
    }

    getCellNextDist(cell: Cell): number {
        return mod(cell.cellIndex - this.cellIndex, 12)
    }

    getCellPrevDist(cell: Cell): number {
        return mod(this.cellIndex - cell.cellIndex, 12)
    }

    getCellDist(cell: Cell): number {
        const nextDist = this.getCellNextDist(cell)
        return Math.min(nextDist, 12 - nextDist)
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars
    [util.inspect.custom](depth: number, opts: any): string {
        return util.inspect(this.toJSON(), opts)
    }

    toJSON() {
        return {
            sky: this.#sky,
            ground: this.#ground,
            temples: this.#temples,
            majorStars: this.#majorStars,
            minorStars: this.#minorStars,
            miniStars: this.#miniStars,
            miscStars: this.allMiniStars,
            ageStart: this.#ageStart,
            ageEnd: this.#ageStart ? this.ageEnd : undefined,
            lifeStage: this.#lifeStage,
        }
    }

    toString(): string {
        return (
            `Cell {${this.sky.displayName}${this.ground.displayName}, temples=[${this.temples}]` +
            `, majorStars=[${this.majorStars?.map(
                (star) => star.displayName + ' ' + MajorStar.majorStarPlacers.get(star)?.evalEnergyLevel(this.ground!),
            )}]` +
            `, minorStars=[${this.minorStars}]` +
            `, miniStars=[${this.miniStars}], miscStars=[${[this.#scholarStar, this.#yearGodStar, this.#leaderStar]}]` +
            `, ageRange=[${this.#ageStart ?? ''}-${this.#ageStart ? this.#ageStart + 9 : ''}], lifeStage=[${this.#lifeStage ?? ''}]` +
            `}`
        )
    }

    equals(cell: Cell) {
        if (this === cell) {
            return true
        } else if (this.toJSON() === cell.toJSON()) {
            return true
        }
        return false
    }

    get selfWithBorrow(): Cell[] {
        return [this, ...this.#borrowCells.map((borrowCell) => borrowCell.cell)]
    }

    get oppositeCell(): Cell {
        return this.getNextICell(6)
    }

    get oppositeCellWithBorrow(): Cell[] {
        return this.oppositeCell.selfWithBorrow
    }

    get selfOppositeCells(): [Cell, Cell] {
        return [this, this.oppositeCell]
    }

    get selfOppositeCellsWithBorrow(): Cell[] {
        return Cell.cellsWithBorrowCells([this, this.oppositeCell])
    }

    get supportCells(): [Cell, Cell] {
        return [this.getNextICell(4), this.getPrevICell(4)]
    }

    get supportCellsWithBorrow(): Cell[] {
        return Cell.cellsWithBorrowCells(this.supportCells)
    }

    get triangleCells(): [Cell, Cell, Cell] {
        return [this, ...this.supportCells]
    }

    get triangleCellsWithBorrow(): Cell[] {
        return Cell.cellsWithBorrowCells(this.triangleCells)
    }

    get fourCells(): [Cell, Cell, Cell, Cell] {
        return [this, this.oppositeCell, ...this.supportCells]
    }

    get fourCellsWithBorrow(): Cell[] {
        return Cell.cellsWithBorrowCells(this.fourCells)
    }

    static cellsWithBorrowCells(cells: Cell[]): Cell[] {
        const allCells: Cell[] = cells.flatMap((cell) => {
            return [cell, ...cell.#borrowCells.map((borrowCell) => borrowCell.cell)]
        })
        const uniqueCells = allCells.filter((value, index, array) => {
            return array.indexOf(value) === index
        })
        return uniqueCells
    }

    hasMajorMinorStar(targetStar: Star): boolean {
        return !!(
            this.#majorStars.find((star: MajorStar) => {
                return star.equals(targetStar)
            }) ??
            this.#minorStars.find((star: MinorStar) => {
                return star.equals(targetStar)
            })
        )
    }

    hasStarInstance(targetStar: Star): boolean {
        return !!(
            this.#majorStars.find((star: MajorStar) => {
                return star.equals(targetStar)
            }) ??
            this.#minorStars.find((star: MinorStar) => {
                return star.equals(targetStar)
            }) ??
            this.allMiniStars.find((star: MinorStar) => {
                return star.equals(targetStar)
            })
        )
    }

    hasStar(targetStar: Star): boolean {
        return !!(
            this.#majorStars.find((star: MajorStar) => {
                return star.equals(targetStar)
            }) ??
            this.#minorStars.find((star: MinorStar) => {
                return star.equals(targetStar)
            }) ??
            this.allMiniStars.find((star: MinorStar) => {
                return star.getDisplayName() === targetStar.getDisplayName()
            })
        )
    }

    hasAllStars(targetStars: Star[]): boolean {
        for (const targetStar of targetStars) {
            if (!this.hasStar(targetStar)) {
                return false
            }
        }
        return true
    }

    hasAnyStars(targetStars: Star[]): boolean {
        for (const targetStar of targetStars) {
            if (this.hasStar(targetStar)) {
                return true
            }
        }
        return false
    }

    hasTemple(targetTemple: Temple): boolean {
        return !!this.temples.find((temple: Temple) => {
            return temple.equals(targetTemple)
        })
    }
}

class BorrowCell {
    cell: Cell
    cellRatio: number

    constructor(cell: Cell, cellRatio: number) {
        this.cell = cell
        this.cellRatio = cellRatio
    }
}

export { Cell, BorrowCell }
