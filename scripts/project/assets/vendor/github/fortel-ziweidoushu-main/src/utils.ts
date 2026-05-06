const mod = (a: number, b: number): number => {
    return ((a % b) + b) % b
}

const intDivide = (a: number, b: number): number => {
    return Math.round((a - mod(a, b)) / b)
}

const str2Uni = (str: string): string => {
    let outStr = ''
    for (let i = 0; i < str.length; i++) {
        outStr += '\\u' + str.charCodeAt(i).toString(16)
    }
    return outStr
}

export { mod, intDivide, str2Uni }
