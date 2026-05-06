import * as std from '../../basic.js';
import { Decimal as DecimalJS } from 'decimal.js';
DecimalJS.set({ precision: 20 });

export const EPS = new DecimalJS("1e-12");

const decjs = d => {
    if (typeof d instanceof DecimalJS) return d;
    throw new TypeError("Except a DecimalJS");
}

// Decimal = String | Number | DecimalJS
export const decimal = x => {
    if (typeof x === "string") {
        x = x.replace(/\s+/g, '');
        if (x[0] === '+') x = x.substr(1); // a bug of decimal.js lib.
        return new DecimalJS(x);
    }
    if (typeof x === "number" || x instanceof DecimalJS) return new DecimalJS(x);
    throw new TypeError("Except a decimal number!");
}
// Decimal->Decimal->Decimal
export const plus = std.uncurry(a => b => decimal(decimal(a).plus(decimal(b))));
export const minus = std.uncurry(a => b => decimal(decimal(a).minus(decimal(b))));
export const mult = std.uncurry(a => b => decimal(decimal(a).times(decimal(b))));
export const div = std.uncurry(a => b => decimal(decimal(a).div(decimal(b))));
export const mod = std.uncurry(a => b => decimal(decimal(a).mod(decimal(b))));
export const atan2 = std.uncurry(a => b => decimal(DecimalJS.atan2(decimal(a), decimal(b))));
export const pow = std.uncurry(a => b => decimal(DecimalJS.pow(decimal(a), decimal(b))));
// Decimal->Decimal
export const neg = a => decimal(decimal(a).negated());
export const abs = a => decimal(DecimalJS.abs(decimal(a)));
export const sqr = a => mult(a, a);
export const cube = a => mult(a, sqr(a));
export const sqrt = a => decimal(DecimalJS.sqrt(decimal(a)));
export const sin = a => decimal(DecimalJS.sin(decimal(a)));
export const cos = a => decimal(DecimalJS.cos(decimal(a)));
export const tan = a => decimal(DecimalJS.tan(decimal(a)));
export const asin = a => decimal(DecimalJS.asin(decimal(a)));
export const acos = a => decimal(DecimalJS.acos(decimal(a)));
export const atan = a => decimal(DecimalJS.atan(decimal(a)));
export const hav = a => decimal(DecimalJS.sqrt(DecimalJS.sin(DecimalJS.mul(0.5, decimal(a)))));
export const ahav = a => decimal(DecimalJS.mul(2, DecimalJS.asin(DecimalJS.sqrt(decimal(a)))));
export const floor = a => decimal(DecimalJS.floor(decimal(a)));
export const ceil = a => decimal(DecimalJS.ceil(decimal(a)));
export const round = a => decimal(DecimalJS.round(decimal(a)));
export const exp = a => decimal(DecimalJS.exp(decimal(a)));
export const log = a => decimal(DecimalJS.log(decimal(a)));
// Decimal->Decimal->Boolean
export const eq = std.uncurry(a => b => std.bool(decimal(a).eq(decimal(b))));
export const lt = std.uncurry(a => b => std.bool(decimal(a).lt(decimal(b))));
export const gt = std.uncurry(a => b => std.bool(decimal(a).gt(decimal(b))));
export const lte = std.uncurry(a => b => std.bool(decimal(a).lte(decimal(b))));
export const gte = std.uncurry(a => b => std.bool(decimal(a).gte(decimal(b))));
export const neq = std.uncurry(a => b => std.bool(!decimal(a).eq(decimal(b))));
// Decimal-> Number
export const sgn = a => std.num(DecimalJS.sign(decimal(a)));
// Decimal->Boolean
export const isPos = a => gt(a, 0);
export const isNeg = a => lt(a, 0);
export const isZero = a => eq(a, 0);
export const isInteger = a => decimal(a).isInteger();
// Decimal->Number->String
export const toFixed = std.uncurry(a => b => std.str(decimal(a).toFixed(std.num(b))));
// Decimal->Number->Decimal
export const toDecimalPosition = std.uncurry(a => b => decimal(toFixed(a, b)));
// Decimal->String
export const show = a => std.str(decimal(a).toString());
// [Decimal]->Decimal
export const sum = (...args) => {
    if (args.length === 1) {
        if (Array.isArray(args[0])) {
            return args[0].reduce((sum, x) => plus(sum, decimal(x)), 0);
        } else {
            return decimal(args[0]);
        }
    } else {
        return args.reduce((sum, x) => plus(sum, decimal(x)), 0);
    }
}
export const max = (...args) => decimal(DecimalJS.max(...args.map(x => decimal(x))));
export const min = (...args) => decimal(DecimalJS.min(...args.map(x => decimal(x))));
// *->Decimal
export const PI = acos(-1);
export const E = exp(1);
