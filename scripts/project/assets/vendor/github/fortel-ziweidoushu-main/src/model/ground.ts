import { mod } from './../utils'
import util from 'util'

const GROUND_WORDS = Object.freeze(['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'])

class Ground {
    index: number
    displayName: string

    constructor(index: number, displayName: string) {
        this.index = index
        this.displayName = displayName
    }

    shift(i: number): Ground {
        return Ground.get(this.index + i)
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

    static get(i: number): Ground {
        return Ground.GROUNDS[mod(i, 12)]
    }

    static getByName(name: string): Ground {
        const index = GROUND_WORDS.indexOf(name)
        if (index !== -1) {
            return Ground.get(index)
        } else {
            throw new Error('Not found')
        }
    }

    static GROUNDS = Object.freeze(
        GROUND_WORDS.map((word, i) => {
            return Object.freeze(new Ground(i, word))
        }),
    )

    static values(): readonly Readonly<Ground>[] {
        return Ground.GROUNDS
    }

    equals(ground: Ground): boolean {
        return this === ground || this.index === ground.index
    }
}

export { Ground }
