import * as std from '../basic.js';
import * as Decimal from './decimal';
const decimal = Decimal.decimal;

// Vector = [Decimal]
export const vector = (...args) => {
    if (args.length === 1) {
        if (Array.isArray(args[0]))
            return args[0].map(x => decimal(x));
        else
            throw new TypeError("Except a vector!");
    }
    return args.map(x => decimal(x));
}
const dimension_check = (u, v) => {
    if (u.length === v.length)
        return true;
    throw new Error("Two vectors must have same dimension!");
}
// Vector->Number
export const dimension = u => u.length;
// Vector -> Vector ->Vector
export const plus = std.uncurry(u => v => dimension_check(u, v) && u.map((x, i) => Decimal.plus(x, v[i])));
export const minus = std.uncurry(u => v => dimension_check(u, v) && u.map((x, i) => Decimal.minus(x, v[i])));
// Vector->Vector
export const neg = u => vector(u).map(x => Decimal.neg(x));
// Vector -> Decimal -> Vector
export const mult = std.uncurry(u => v => decimal(v) && u.map(x => Decimal.mult(x, v)));
export const div = std.uncurry(u => v => decimal(v) && u.map(x => Decimal.div(x, v)));
// Vector -> Vector -> Decimal
export const dot = std.uncurry(u => v => dimension_check(u, v) && u.reduce((sum, x, i) => Decimal.plus(sum, Decimal.mult(x, v[i])), 0));
// Vector->Decimal | Vector
export const cross = std.uncurry(u => v => {
    dimension_check(u, v);
    if (u.length === 2)
        return Decimal.minus(Decimal.mult(u[0], v[1]), Decimal.mult(u[1], v[0]));
    else if (u.length === 3)
        return vector([
            Decimal.minus(Decimal.mult(u[1], v[2]), Decimal.mult(u[2], v[1])),
            Decimal.minus(Decimal.mult(u[2], v[0]), Decimal.mult(u[0], v[2])),
            Decimal.minus(Decimal.mult(u[0], v[1]), Decimal.mult(u[1], v[0]))
        ]);
    throw new Error("Cross product is only defined in 3 dimensional space!");
});
// Vector->Decimal
export const norm = u => Decimal.sqrt(dot(u, u));
// Vector->Vector
export const normalize = u => {
    let n = norm(vector(u));
    return u.map(x => Decimal.div(x, n));
}
// Vector -> Vector -> Boolean
export const equals = std.uncurry(u => v => vector(u).length === vector(v).length && u.every((x, i) => Decimal.eq(x, v[i])));
export const eq = equals;
// Vector->Boolean
export const isZero = u => vector(u).every(x => Decimal.eq(x, 0));
// Vector->String
export const show = u => "(" + vector(u).map(x => Decimal.show(x)).join(",") + ")";
