import { mod } from './../utils'
import util from 'util'

const SKY_WORDS = Object.freeze(['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'])

class Sky {
    index: number
    displayName: string

    constructor(index: number, displayName: string) {
        this.index = index
        this.displayName = displayName
    }

    shift(i: number): Sky {
        return Sky.get(this.index + i)
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

    static get(i: number): Sky {
        return Sky.SKYS[mod(i, Sky.SKYS.length)]
    }

    static getByName(name: string): Sky {
        const index = SKY_WORDS.indexOf(name)
        if (index !== -1) {
            return Sky.get(index)
        } else {
            throw new Error('Not found')
        }
    }

    static SKYS = Object.freeze(
        SKY_WORDS.map((word, i) => {
            return Object.freeze(new Sky(i, word))
        }),
    )

    static values(): readonly Readonly<Sky>[] {
        return Sky.SKYS
    }

    equals(sky: Sky): boolean {
        return this === sky || this.index === sky.index
    }
}

export { Sky }
