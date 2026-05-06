import { Cell } from '../model/cell'
import { DestinyBoard } from '../model/destinyBoard'
import { Ground } from '../model/ground'
import { MajorStar } from '../model/majorStar'
import { MiniStar } from '../model/miniStar'
import { MinorStar } from '../model/minorStar'
import { Star } from '../model/star'
import { StarDerivative } from '../model/starDerivative'
import { Temple } from '../model/temple'
import { str2Uni } from '../utils'

enum CellsScope {
    SELF = 'SELF',
    OPPOSITE = 'OPPOSITE',
    SELF_OPPOSITE = 'OPPOSITE',
    SUPPORT = 'SUPPORT',
    TRIANGLE = 'TRIANGLE',
    FOUR = 'FOUR',
}

class BoardCriteria {
    #destinyBoard: DestinyBoard
    #baseCellGround: Ground
    #cellsScope: CellsScope

    constructor(destinyBoard: DestinyBoard, baseCellGround?: Ground, cellsScope: CellsScope = CellsScope.SELF) {
        this.#destinyBoard = destinyBoard
        this.#baseCellGround = baseCellGround ?? destinyBoard.destinyTempleCellGround
        this.#cellsScope = cellsScope
    }

    ofDestinyTemple() {
        return new BoardCriteria(this.#destinyBoard, this.#destinyBoard.destinyTempleCellGround, this.#cellsScope)
    }

    ofTemple(temple: Temple) {
        return new BoardCriteria(this.#destinyBoard, this.#destinyBoard.getCellByTemple(temple).ground, this.#cellsScope)
    }

    ofGroundCell(ground: Ground) {
        return new BoardCriteria(this.#destinyBoard, ground, this.#cellsScope)
    }

    ofCell(cell: Cell) {
        return new BoardCriteria(this.#destinyBoard, cell.ground, this.#cellsScope)
    }

    ofStar(star: Star) {
        const targetCell = this.#destinyBoard.cells.find((cell) => {
            return cell.hasStarInstance(star)
        })
        if (!targetCell) {
            throw new Error('Star not found')
        }
        return new BoardCriteria(this.#destinyBoard, targetCell.ground, this.#cellsScope)
    }

    withCellsType(cellsScope: CellsScope) {
        return new BoardCriteria(this.#destinyBoard, this.#baseCellGround, cellsScope)
    }

    get #__internal_baseCell(): Cell {
        return this.#destinyBoard.getCellByGround(this.#baseCellGround)
    }

    static allStarsNameToKeyMap = ([...MajorStar.stars, ...MinorStar.stars, ...MiniStar.allStars] as Star[]).reduce<Map<string, string>>(
        (prev: Map<string, string>, curr: Star) => {
            if (!prev[curr.getDisplayName()]) {
                prev[curr.getDisplayName()] = curr.getKey()
            }
            return prev
        },
        {} as Map<string, string>,
    )

    hasStar(star: Star) {
        return BoardCriteria.#hasStar(this.#scopedCells, star)
    }

    hasAllStars(stars: Star[]) {
        return BoardCriteria.#hasAllStars(this.#scopedCells, stars)
    }

    hasAnyStars(stars: Star[]) {
        return BoardCriteria.#hasAnyStars(this.#scopedCells, stars)
    }

    notFoundStar(star: Star) {
        return BoardCriteria.#notFoundStar(this.#scopedCells, star)
    }

    notFoundAllStars(stars: Star[]) {
        return BoardCriteria.#notFoundAllStars(this.#scopedCells, stars)
    }

    notFoundAnyStars(stars: Star[]) {
        return BoardCriteria.#notFoundAnyStars(this.#scopedCells, stars)
    }

    get #scopedCells(): Cell[] {
        switch (this.#cellsScope) {
            case CellsScope.SELF:
                return this.#__internal_baseCell.selfWithBorrow
            case CellsScope.OPPOSITE:
                return this.#__internal_baseCell.oppositeCellWithBorrow
            case CellsScope.SELF_OPPOSITE:
                return this.#__internal_baseCell.selfOppositeCellsWithBorrow
            case CellsScope.SUPPORT:
                return this.#__internal_baseCell.supportCellsWithBorrow
            case CellsScope.TRIANGLE:
                return this.#__internal_baseCell.triangleCellsWithBorrow
            case CellsScope.FOUR:
                return this.#__internal_baseCell.fourCellsWithBorrow
            default:
                throw new Error('unknown cells type')
        }
    }

    static #hasStar(cells: Cell[], star: Star) {
        return !!cells.find((cell) => cell.hasStar(star))
    }

    static #hasAllStars(cells: Cell[], stars: Star[]) {
        for (const star of stars) {
            if (!cells.find((cell) => cell.hasStar(star))) {
                return false
            }
        }
        return true
    }

    static #hasAnyStars(cells: Cell[], stars: Star[]) {
        for (const star of stars) {
            if (cells.find((cell) => cell.hasStar(star))) {
                return true
            }
        }
        return false
    }

    static #notFoundStar(cells: Cell[], star: Star) {
        return !BoardCriteria.#hasStar(cells, star)
    }

    static #notFoundAllStars(cells: Cell[], stars: Star[]) {
        return !BoardCriteria.#hasAnyStars(cells, stars)
    }

    static #notFoundAnyStars(cells: Cell[], stars: Star[]) {
        return !BoardCriteria.#hasAllStars(cells, stars)
    }

    static fromDescription(destinyBoard: DestinyBoard, description: string) {
        let cell: Cell | null = null
        let cellsScope: CellsScope | null = null
        let stars: Star[] = []
        const starDerivatives: StarDerivative[] = []

        let isBothEarn = false

        if ((!cellsScope && description.includes('入命')) || description.includes('在命')) {
            cell = destinyBoard.getCellByTemple(Temple.TEMPLE_DESTINY)
            cellsScope = CellsScope.SELF
        }

        if (!cellsScope && description.includes('三方四正')) {
            cellsScope = CellsScope.FOUR
        }

        const templeChar = str2Uni('宮')
        {
            const matches = description.match(new RegExp(`.*?(.{1,2}${templeChar})`, 'u'))
            if (matches && matches[1]) {
                const targetTemple = Temple.TEMPLES.find((temple) => matches[1].includes(temple.getDisplayName()))
                if (targetTemple) {
                    cell = destinyBoard.getCellByTemple(targetTemple)

                    // 入XX宮
                    if (description.match(new RegExp(`${str2Uni('入')}(.{1,2})${templeChar}`, 'u'))) {
                        cellsScope = CellsScope.SELF
                    }
                    // 在XX宮
                    if (description.match(new RegExp(`${str2Uni('在')}(.{1,2})${templeChar}`, 'u'))) {
                        cellsScope = CellsScope.SELF
                    }
                }
            }
        }

        if (!cellsScope && description.includes('在')) {
            cellsScope = CellsScope.SELF
        }

        if (!cellsScope && description.includes('有')) {
            cellsScope = CellsScope.SELF
        }

        if (!cellsScope && description.includes('見')) {
            cellsScope = CellsScope.FOUR
        }

        if (!cellsScope && description.includes('會')) {
            cellsScope = CellsScope.FOUR
        }

        stars = Object.keys(BoardCriteria.allStarsNameToKeyMap)
            .filter((starName) => description.includes(starName))
            .map((starName) => {
                const key = BoardCriteria.allStarsNameToKeyMap[starName]
                return MajorStar.getByKey(key) ?? MinorStar.getByKey(key) ?? MiniStar.getByKey(key)
            })
            .filter((star) => star) as Star[]

        if (description.includes('火')) {
            stars.push(MinorStar.MINOR_STAR_BURNING)
        }
        if (description.includes('鈴')) {
            stars.push(MinorStar.MINOR_STAR_HIDDEN_FIRE)
        }
        if (description.includes('羊')) {
            stars.push(MinorStar.MINOR_STAR_COMPETITION)
        }
        if (description.includes('陀')) {
            stars.push(MinorStar.MINOR_STAR_HINDRANCE)
        }

        {
            const matches = description.match(new RegExp(`${str2Uni('見')}${str2Uni('祿')}(${str2Uni('存')})?`, 'u'))
            if (matches) {
                cellsScope = CellsScope.FOUR
                if (!matches[1]) {
                    isBothEarn = true
                }
            }
        }

        if (description.includes('化祿')) {
            starDerivatives.push(StarDerivative.WEALTHINESS)
        }
        if (description.includes('科')) {
            starDerivatives.push(StarDerivative.FAME)
        }
        if (description.includes('忌')) {
            starDerivatives.push(StarDerivative.PROBLEM)
        }

        if (!cell) {
            cell = destinyBoard.getCellByTemple(Temple.TEMPLE_DESTINY)
        }
        if (!cellsScope) {
            cellsScope = CellsScope.SELF
        }

        const starDerivativeStars = starDerivatives.map((starDerivative) => destinyBoard.bornStarDerivativeMap.get(starDerivative)!)

        const criteria = new BoardCriteria(destinyBoard).ofCell(cell).withCellsType(cellsScope)
        if (isBothEarn) {
            stars = stars.filter((star) => !star.equals(MinorStar.MINOR_STAR_EARN))
            return (
                criteria.hasAllStars(stars) &&
                criteria.hasAnyStars([MinorStar.MINOR_STAR_EARN, destinyBoard.bornStarDerivativeMap.get(StarDerivative.WEALTHINESS)!])
            )
        } else {
            return criteria.hasAllStars([...stars, ...starDerivativeStars])
        }
    }
}

export { BoardCriteria, CellsScope }
