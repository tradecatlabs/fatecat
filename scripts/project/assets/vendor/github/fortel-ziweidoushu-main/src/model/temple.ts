import util from 'util'
class Temple {
    key: string
    displayName: string
    formalName: string
    index: number

    constructor(key: string, displayName: string, formalName: string, index: number) {
        this.key = key
        this.displayName = displayName
        this.formalName = formalName
        this.index = index
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

    getDisplayName(): string {
        return this.displayName
    }

    getFormalName(): string {
        return this.formalName
    }

    static getByKey(key: string): Temple | null {
        const targetTemple = Temple.TEMPLES.find((temple) => temple.key === key)
        return targetTemple ?? null
    }

    static getByName(name: string) {
        const targetTemple = Temple.TEMPLES.find((temple) => temple.displayName === name || temple.formalName === name)
        if (targetTemple) {
            return targetTemple
        }
    }

    static TEMPLE_DESTINY = Object.freeze(new Temple('TEMPLE_DESTINY', '命宮', '命宮', 0))
    static TEMPLE_BROTHER = Object.freeze(new Temple('TEMPLE_BROTHER', '兄弟', '兄弟宮', 1))
    static TEMPLE_MARRIAGE = Object.freeze(new Temple('TEMPLE_MARRIAGE', '夫妻', '夫妻宮', 2))
    static TEMPLE_CHILDREN = Object.freeze(new Temple('TEMPLE_CHILDREN', '子女', '子女宮', 3))
    static TEMPLE_MONEY = Object.freeze(new Temple('TEMPLE_MONEY', '財帛', '財帛宮', 4))
    static TEMPLE_ILLNESS = Object.freeze(new Temple('TEMPLE_ILLNESS', '疾厄', '疾厄宮', 5))
    static TEMPLE_MOVE = Object.freeze(new Temple('TEMPLE_MOVE', '遷移', '遷移宮', 6))
    static TEMPLE_FRIEND = Object.freeze(new Temple('TEMPLE_FRIEND', '交友', '交友宮', 7))
    static TEMPLE_CAREER = Object.freeze(new Temple('TEMPLE_CAREER', '事業', '事業宮', 8))
    static TEMPLE_HOUSE = Object.freeze(new Temple('TEMPLE_HOUSE', '田宅', '田宅宮', 9))
    static TEMPLE_HAPPINESS = Object.freeze(new Temple('TEMPLE_HAPPINESS', '福德', '福德宮', 10))
    static TEMPLE_PARENT = Object.freeze(new Temple('TEMPLE_PARENT', '父母', '父母宮', 11))
    static TEMPLE_BODY = Object.freeze(new Temple('TEMPLE_BODY', '身宮', '身宮', 0))

    static TEMPLES = Object.freeze([
        Temple.TEMPLE_DESTINY,
        Temple.TEMPLE_BROTHER,
        Temple.TEMPLE_MARRIAGE,
        Temple.TEMPLE_CHILDREN,
        Temple.TEMPLE_MONEY,
        Temple.TEMPLE_ILLNESS,
        Temple.TEMPLE_MOVE,
        Temple.TEMPLE_FRIEND,
        Temple.TEMPLE_CAREER,
        Temple.TEMPLE_HOUSE,
        Temple.TEMPLE_HAPPINESS,
        Temple.TEMPLE_PARENT,
        Temple.TEMPLE_BODY,
    ])

    static LOOP_TEMPLES = Object.freeze([
        Temple.TEMPLE_DESTINY,
        Temple.TEMPLE_BROTHER,
        Temple.TEMPLE_MARRIAGE,
        Temple.TEMPLE_CHILDREN,
        Temple.TEMPLE_MONEY,
        Temple.TEMPLE_ILLNESS,
        Temple.TEMPLE_MOVE,
        Temple.TEMPLE_FRIEND,
        Temple.TEMPLE_CAREER,
        Temple.TEMPLE_HOUSE,
        Temple.TEMPLE_HAPPINESS,
        Temple.TEMPLE_PARENT,
    ])

    equals(temple: Temple) {
        return this === temple || this.key === temple.key
    }
}

export { Temple }
