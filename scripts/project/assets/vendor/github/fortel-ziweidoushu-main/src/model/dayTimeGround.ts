import { Ground } from './ground'
import { mod } from './../utils'
import util from 'util'

class DayTimeGround {
    index: number
    displayName: string
    ground: Ground
    hourStart: number
    hourEnd: number

    constructor(index: number, displayName: string, ground: Ground, hourStart: number, hourEnd: number) {
        this.index = index
        this.displayName = displayName
        this.ground = ground
        this.hourStart = hourStart
        this.hourEnd = hourEnd
    }

    toJSON() {
        return this.displayName
    }

    toString(): string {
        return this.displayName
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars, @typescript-eslint/no-unused-vars
    [util.inspect.custom](depth: number, opts: any): string {
        return this.toString()
    }

    static get(i: number): DayTimeGround {
        return DAY_TIME_GROUNDS[mod(i, DAY_TIME_GROUNDS.length)]
    }

    static getByName(name: string): DayTimeGround {
        const target = DAY_TIME_GROUNDS.filter((dayTimeGround) => dayTimeGround.displayName === name)[0]
        if (target) {
            return target
        } else {
            throw new Error('Not found')
        }
    }

    static getByStartHour(hour: number): DayTimeGround {
        const target = DAY_TIME_GROUNDS.filter((dayTimeGround) => dayTimeGround.hourStart === hour)[0]
        if (target) {
            return target
        } else {
            throw new Error('Not found')
        }
    }

    static getByHour(hour: number): DayTimeGround {
        const target = DAY_TIME_GROUNDS.filter((dayTimeGround) => dayTimeGround.hourStart <= hour && hour < dayTimeGround.hourEnd)[0]
        if (target) {
            return target
        } else {
            throw new Error('Not found')
        }
    }

    static values(): readonly Readonly<DayTimeGround>[] {
        return DAY_TIME_GROUNDS
    }
}

const DAY_TIME_GROUNDS = Object.freeze([
    Object.freeze(new DayTimeGround(0, '早子時', Ground.get(0), 0, 1)),
    ...Ground.GROUNDS.slice(1).map((ground) => {
        const i = ground.index
        return Object.freeze(new DayTimeGround(i, ground.displayName + '時', ground, -1 + i * 2, 1 + i * 2))
    }),
    Object.freeze(new DayTimeGround(12, '夜子時', Ground.get(0), 23, 24)),
])

export { DayTimeGround, DAY_TIME_GROUNDS }
