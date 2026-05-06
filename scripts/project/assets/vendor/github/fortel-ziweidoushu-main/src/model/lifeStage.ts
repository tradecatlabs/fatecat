import util from 'util'
class LifeStage {
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

    static getByName(name: string) {
        return LifeStage.values.find((lifeStage) => lifeStage.displayName === name)
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars
    [util.inspect.custom](depth: number, opts: any): string {
        return this.toString()
    }

    static values = Object.freeze([
        Object.freeze(new LifeStage('長生')),
        Object.freeze(new LifeStage('沐浴')),
        Object.freeze(new LifeStage('冠帶')),
        Object.freeze(new LifeStage('臨官')),
        Object.freeze(new LifeStage('帝旺')),
        Object.freeze(new LifeStage('衰')),
        Object.freeze(new LifeStage('病')),
        Object.freeze(new LifeStage('死')),
        Object.freeze(new LifeStage('墓')),
        Object.freeze(new LifeStage('絕')),
        Object.freeze(new LifeStage('胎')),
        Object.freeze(new LifeStage('養')),
    ])
}

export { LifeStage }
