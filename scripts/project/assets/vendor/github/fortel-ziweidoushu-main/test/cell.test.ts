import { DestinyBoard } from './../src/model/destinyBoard'
import { Ground } from './../src/model/ground'
import { Sky } from './../src/model/sky'
import { DestinyConfigBuilder } from '../src/util/destinyConfigBuilder'
import { MajorStar } from '../src/model/majorStar'
import { MinorStar } from '../src/model/minorStar'
import { Temple } from '../src/model/temple'
import { MiniStar } from '../src/model/miniStar'
import { LifeStage } from '../src/model/lifeStage'
import { Cell } from '../src/model/cell'

const cellsEqual = (expectCells: Cell[], actualCells: Cell[]) => {
    if (expectCells.length !== actualCells.length) {
        return false
    }
    for (const actualCell of actualCells) {
        if (!expectCells.find((expectCell) => expectCell.equals(actualCell))) {
            return false
        }
    }
    return true
}

describe('Test Cell', () => {
    it('Test cell get value', () => {
        const destinyBoard: DestinyBoard = new DestinyBoard(DestinyConfigBuilder.withText('1952年12月15日寅時天盤女'))

        /**
         * Test cell[0] get values
         */
        expect(destinyBoard.cells[0].sky).toBe(Sky.getByName('壬'))
        expect(destinyBoard.cells[0].ground).toBe(Ground.getByName('子'))

        expect(destinyBoard.cells[0].temples).toStrictEqual([Temple.TEMPLE_PARENT])

        expect(destinyBoard.cells[0].majorStars).toStrictEqual([MajorStar.MAJOR_STAR_GOLD, MajorStar.MAJOR_STAR_TREASURY])
        expect(destinyBoard.cells[0].minorStars).toStrictEqual([MinorStar.MINOR_STAR_HIDDEN_FIRE, MinorStar.MINOR_STAR_COMPETITION])
        expect(destinyBoard.cells[0].miniStars).toStrictEqual([MiniStar.MINI_STAR_SEX])
        expect(destinyBoard.cells[0].scholarStar).toStrictEqual(MiniStar.MINI_STAR_LITIGATION)
        expect(destinyBoard.cells[0].yearGodStar).toBe(MiniStar.MINI_STAR_WHITE_TIGER)
        expect(destinyBoard.cells[0].leaderStar).toBe(MiniStar.MINI_STAR_LEADER)

        expect(destinyBoard.cells[0].allMiniStars.length).toBe(4)
        expect(destinyBoard.cells[0].allMiniStars).toStrictEqual([
            MiniStar.MINI_STAR_SEX,
            MiniStar.MINI_STAR_LITIGATION,
            MiniStar.MINI_STAR_WHITE_TIGER,
            MiniStar.MINI_STAR_LEADER,
        ])

        expect(destinyBoard.cells[0].allStars.length).toBe(8)
        expect(destinyBoard.cells[0].allStars).toStrictEqual([
            MajorStar.MAJOR_STAR_GOLD,
            MajorStar.MAJOR_STAR_TREASURY,
            MinorStar.MINOR_STAR_HIDDEN_FIRE,
            MinorStar.MINOR_STAR_COMPETITION,
            MiniStar.MINI_STAR_SEX,
            MiniStar.MINI_STAR_LITIGATION,
            MiniStar.MINI_STAR_WHITE_TIGER,
            MiniStar.MINI_STAR_LEADER,
        ])

        expect(destinyBoard.cells[0].hasMajorMinorStar(MajorStar.MAJOR_STAR_GOLD)).toBe(true)
        expect(destinyBoard.cells[0].hasMajorMinorStar(MinorStar.MINOR_STAR_HIDDEN_FIRE)).toBe(true)

        expect(destinyBoard.cells[8].hasStarInstance(MiniStar.MINI_STAR_SMALL_LOST)).toBe(true)
        expect(destinyBoard.cells[8].hasStarInstance(MiniStar.MINI_STAR_SMALL_LOST2)).toBe(false)
        expect(destinyBoard.cells[9].hasStarInstance(MiniStar.MINI_STAR_SMALL_LOST)).toBe(false)
        expect(destinyBoard.cells[9].hasStarInstance(MiniStar.MINI_STAR_SMALL_LOST2)).toBe(true)

        expect(destinyBoard.cells[8].hasStar(MiniStar.MINI_STAR_SMALL_LOST)).toBe(true)
        expect(destinyBoard.cells[9].hasStar(MiniStar.MINI_STAR_SMALL_LOST)).toBe(true)
        expect(destinyBoard.cells[8].hasStar(MiniStar.MINI_STAR_SMALL_LOST2)).toBe(true)
        expect(destinyBoard.cells[9].hasStar(MiniStar.MINI_STAR_SMALL_LOST2)).toBe(true)

        expect(destinyBoard.cells[0].hasAllStars([MajorStar.MAJOR_STAR_GOLD, MinorStar.MINOR_STAR_HIDDEN_FIRE])).toBe(true)
        expect(destinyBoard.cells[0].hasAllStars([MajorStar.MAJOR_STAR_GOLD, MajorStar.MAJOR_STAR_ENJOYMENT])).toBe(false)
        expect(destinyBoard.cells[0].hasAnyStars([MajorStar.MAJOR_STAR_GOLD, MajorStar.MAJOR_STAR_ENJOYMENT])).toBe(true)
        expect(destinyBoard.cells[0].hasAnyStars([MajorStar.MAJOR_STAR_ENJOYMENT])).toBe(false)

        expect(destinyBoard.cells[0].hasTemple(Temple.TEMPLE_PARENT)).toBe(true)

        expect(destinyBoard.cells[0].lifeStage).toBe(LifeStage.getByName('衰'))

        expect(destinyBoard.cells[0].ageStart).toBe(114)
        expect(destinyBoard.cells[0].ageEnd).toBe(123)
    })

    it('Test cell transverse movement', () => {
        const destinyBoard: DestinyBoard = new DestinyBoard(DestinyConfigBuilder.withText('1952年12月15日寅時天盤女'))

        expect(destinyBoard.cells[0].nextCell).toBe(destinyBoard.cells[1])
        expect(destinyBoard.cells[0].prevCell).toBe(destinyBoard.cells[11])
        expect(destinyBoard.cells[0].getNextICell(4)).toBe(destinyBoard.cells[4])
        expect(destinyBoard.cells[0].getNextICell(-4)).toBe(destinyBoard.cells[8])
        expect(destinyBoard.cells[0].getPrevICell(4)).toBe(destinyBoard.cells[8])
        expect(destinyBoard.cells[0].getPrevICell(-4)).toBe(destinyBoard.cells[4])
        expect(destinyBoard.cells[0].getCellNextDist(destinyBoard.cells[4])).toBe(4)
        expect(destinyBoard.cells[0].getCellNextDist(destinyBoard.cells[8])).toBe(8)
        expect(destinyBoard.cells[0].getCellPrevDist(destinyBoard.cells[4])).toBe(8)
        expect(destinyBoard.cells[0].getCellPrevDist(destinyBoard.cells[8])).toBe(4)
        expect(destinyBoard.cells[0].getCellDist(destinyBoard.cells[4])).toBe(4)
        expect(destinyBoard.cells[0].getCellDist(destinyBoard.cells[8])).toBe(4)

        expect(
            cellsEqual(destinyBoard.cells[7].selfWithBorrow, [
                destinyBoard.cells[7],
                destinyBoard.cells[1],
                destinyBoard.cells[11],
                destinyBoard.cells[3],
            ]),
        ).toBe(true)

        expect(destinyBoard.cells[1].oppositeCell).toBe(destinyBoard.cells[7])

        expect(
            cellsEqual(destinyBoard.cells[1].oppositeCellWithBorrow, [
                destinyBoard.cells[7],
                destinyBoard.cells[1],
                destinyBoard.cells[11],
                destinyBoard.cells[3],
            ]),
        ).toBe(true)

        expect(cellsEqual(destinyBoard.cells[0].selfOppositeCells, [destinyBoard.cells[0], destinyBoard.cells[6]])).toBe(true)

        expect(cellsEqual(destinyBoard.cells[0].selfOppositeCellsWithBorrow, [destinyBoard.cells[0], destinyBoard.cells[6]])).toBe(true)

        expect(cellsEqual(destinyBoard.cells[0].supportCells, [destinyBoard.cells[4], destinyBoard.cells[8]])).toBe(true)

        expect(cellsEqual(destinyBoard.cells[0].supportCellsWithBorrow, [destinyBoard.cells[4], destinyBoard.cells[8]])).toBe(true)

        expect(cellsEqual(destinyBoard.cells[0].triangleCells, [destinyBoard.cells[0], destinyBoard.cells[4], destinyBoard.cells[8]])).toBe(true)

        expect(cellsEqual(destinyBoard.cells[0].triangleCellsWithBorrow, [destinyBoard.cells[0], destinyBoard.cells[4], destinyBoard.cells[8]])).toBe(
            true,
        )

        expect(
            cellsEqual(destinyBoard.cells[0].fourCells, [destinyBoard.cells[0], destinyBoard.cells[6], destinyBoard.cells[4], destinyBoard.cells[8]]),
        ).toBe(true)

        expect(
            cellsEqual(destinyBoard.cells[0].fourCellsWithBorrow, [
                destinyBoard.cells[0],
                destinyBoard.cells[6],
                destinyBoard.cells[4],
                destinyBoard.cells[8],
            ]),
        ).toBe(true)

        expect(
            cellsEqual(destinyBoard.cells[7].fourCells, [
                destinyBoard.cells[7],
                destinyBoard.cells[1],
                destinyBoard.cells[11],
                destinyBoard.cells[3],
            ]),
        ).toBe(true)

        expect(
            cellsEqual(destinyBoard.cells[7].fourCellsWithBorrow, [
                destinyBoard.cells[7],
                destinyBoard.cells[1],
                destinyBoard.cells[11],
                destinyBoard.cells[3],
            ]),
        ).toBe(true)
    })
})
