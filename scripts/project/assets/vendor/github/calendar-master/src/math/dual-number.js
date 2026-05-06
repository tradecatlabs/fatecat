//////////////////////////////////////////////////////
// a+eb， where e*e=0
import * as std from '../basic.js';
import * as Decimal from './decimal';
const decimal = Decimal.decimal;

export const dualnumber = (...args) => {
    if (args.length === 1) {
        let q = std.obj(args[0]);
        if (q.hasOwnProperty("real") && q.hasOwnProperty("dual")) {
            return {
                real: decimal(q.real),
                dual: decimal(q.dual)
            }; // construct
        }
    } else if (args.length === 2) {
        let r = decimal(args[0]),
            d = decimal(args[1]);
        return { real: r, dual: d };
    }
    throw new TypeError("Except a dual number!");
}
export const plus = std.uncurry(a => b => {
    a = dualnumber(a),
        b = dualnumber(b);
    return dualnumber(Decimal.plus(a.real, b.real), Decimal.plus(a.dual, b.dual));
});
export const scale = std.uncurry(a => r => {
    a = dualnumber(a),
        r = decimal(r);
    return dualnumber(Decimal.mult(a.real, r), Decimal.mult(a.dual, r));
});
export const mult = std.uncurry(a => b => {
    a = dualnumber(a),
        b = dualnumber(b);
    return dualnumber(Decimal.mult(a.real, b.real), Decimal.plus(Decimal.mult(a.real, b.dual), Decimal.mult(a.dual, b.real)));
});
// just like the complex number
// (a+eb)/(c+ed)=[(a+eb)(c-ed)]/c^2=a/c+e(bc-ad)/c^2, where e denotes nilpotent
export const div = std.uncurry(a => b => {
    a = dualnumber(a),
        b = dualnumber(b);
    if (Decimal.isZero(b.real))
        throw new Error("Divided by Zero!");
    return dualnumber(Decimal.div(a.real, b.real), Decimal.div(Decimal.minus(Decimal.mult(a.dual, b.real), Decimal.mult(a.real, b.dual)), Decimal.sqr(b.real)));
});
// (1+e0)/(a+eb)=1/a-eb/a^2, where e denotes nilpotent
export const inverse = a => {
    a = dualnumber(a);
    if (Decimal.isZero(a.real))
        throw new Error("Non-inverse!");
    return dualnumber(Decimal.div(1.0, a.real), Decimal.div(Decimal.negated(a.dual), Decimal.sqr(a.real)));
};
// c+ed=(a+eb)^2=a^2+2eab --> a=sqrt(c), b=d/2a=d/(2sqrt(c))
export const sqrt = a => {
    a = dualnumber(a);
    if (Decimal.isNeg(a.real))
        throw new Error("Illegal usage of sqrt!");
    return dualnumber(Decimal.sqrt(a.real), Decimal.div(a.dual, Decimal.mult(2, Decimal.sqr(a.real))));
}

export const eq = std.uncurry(a => b => {
    a = dualnumber(a),
        b = dualnumber(b);
    return Decimal.eq(a.real, b.real) && Decimal.eq(a.dual, b.dual);
});
export const neq = std.uncurry(a => b => !eq(a, b));

export const show = a => {
    a = dualnumber(a);
    return Decimal.show(a.real) + (Decimal.isNeg(a.dual) ? "" : "+") + Decimal.show(a.dual) + " ε";
}
