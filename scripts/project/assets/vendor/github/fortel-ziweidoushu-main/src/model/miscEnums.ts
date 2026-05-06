import util from 'util'

enum Luckiness {
    LUCK = 1,
    NEUTRAL = 0,
    BAD_LUCK = -1,
}

class ShadowLight {
    displayName: string
    constructor(displayName: string) {
        this.displayName = displayName
    }

    toJSON() {
        return this.displayName
    }

    toString(): string {
        return this.displayName
    }

    static SHADOW = Object.freeze(new ShadowLight('陰'))
    static LIGHT = Object.freeze(new ShadowLight('陽'))
}

class Direction {
    direction: number

    constructor(direction: number) {
        this.direction = direction
    }

    add(direction: Direction): Direction {
        if (this.direction * direction.direction === 1) {
            return Direction.CLOCKWISE
        }
        return Direction.ANTI_CLOCKWISE
    }

    static CLOCKWISE = Object.freeze(new Direction(1))
    static ANTI_CLOCKWISE = Object.freeze(new Direction(-1))
}

class Element {
    code: string
    displayName: string
    patternNumber: number

    constructor(code: string, displayName: string, patternNumber: number) {
        this.code = code
        this.displayName = displayName
        this.patternNumber = patternNumber
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

    static get(code: string): Element {
        const element = Element.#ELEMENTS[code]
        if (element) {
            return element
        } else {
            throw new Error('Element not found')
        }
    }

    static GOLD = Object.freeze(new Element('GOLD', '金四局', 4))
    static WOOD = Object.freeze(new Element('WOOD', '木三局', 3))
    static EARTH = Object.freeze(new Element('EARTH', '土五局', 5))
    static WATER = Object.freeze(new Element('WATER', '水二局', 2))
    static FIRE = Object.freeze(new Element('FIRE', '火六局', 6))

    static #ELEMENTS = Object.freeze({
        GOLD: Element.GOLD,
        WOOD: Element.WOOD,
        EARTH: Element.EARTH,
        WATER: Element.WATER,
        FIRE: Element.FIRE,
    })
}

export { Element, Luckiness, ShadowLight, Direction }
