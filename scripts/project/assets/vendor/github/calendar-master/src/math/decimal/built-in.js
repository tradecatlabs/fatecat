import * as std from '../../basic.js';

// Decimal = String | Number
export const decimal = x => {
    if (typeof x === "number") return x;
    if (typeof(x) === "string") {
        x = x.replace(/\s+/g, '');
        if (/^[+-]?(([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?)$/.test(x))
            return parseFloat(x);
    }
    throw new TypeError("Except a decimal number!");
};
// Decimal->Decimal->Decimal
export const plus = std.uncurry(a => b => decimal(decimal(a) + decimal(b)));
export const minus = std.uncurry(a => b => decimal(decimal(a) - decimal(b)));
export const mult = std.uncurry(a => b => decimal(decimal(a) * decimal(b)));
export const div = std.uncurry(a => b => decimal(decimal(a) / decimal(b)));
export const mod = std.uncurry(a => b => decimal(decimal(a) % decimal(b)));
export const atan2 = std.uncurry(a => b => decimal(Math.atan2(decimal(a), decimal(b))));
// Decimal->Decimal
export const neg = a => decimal(-decimal(a));
export const sqr = a => mult(a, a);
export const cube = a => mult(a, sqr(a));
export const sqrt = a => decimal(Math.sqrt(decimal(a)));
export const sin = a => decimal(Math.sin(decimal(a)));
export const cos = a => decimal(Math.cos(decimal(a)));
export const tan = a => decimal(Math.tan(decimal(a)));
export const asin = a => decimal(Math.asin(decimal(a)));
export const acos = a => decimal(Math.acos(decimal(a)));
export const atan = a => decimal(Math.atan(decimal(a)));
export const hav = a => decimal(Math.sqrt(Math.sin(0.5 * decimal(a))));
export const ahav = a => decimal(2 * Math.asin(Math.sqrt(decimal(a))));
export const floor = a => decimal(Math.floor(decimal(a)));
// Decimal->Decimal->Boolean
export const eq = std.uncurry(a => b => std.bool(decimal(a) === decimal(b)));
export const lt = std.uncurry(a => b => std.bool(decimal(a) < decimal(b)));
export const gt = std.uncurry(a => b => std.bool(decimal(a) > decimal(b)));
export const lte = std.uncurry(a => b => std.bool(decimal(a) <= decimal(b)));
export const gte = std.uncurry(a => b => std.bool(decimal(a) >= decimal(b)));
export const neq = std.uncurry(a => b => std.bool(decimal(a) !== decimal(b)));
// Decimal-> Number
export const sgn = a => std.num(Math.sign(decimal(a)));
// Decimal->Boolean
export const isPos = a => gt(a, 0);
export const isNeg = a => lt(a, 0);
export const isZero = a => eq(a, 0);
// Decimal->Number->String
export const toFixed = std.uncurry(a => b => std.str(decimal(a).toFixed(std.num(b))));
// Decimal->Number->Decimal
export const toDecimalPosition = std.uncurry(a => b => decimal(toFixed(a, b)));
// Decimal->String
export const show = a => std.str(decimal(a).toString());
