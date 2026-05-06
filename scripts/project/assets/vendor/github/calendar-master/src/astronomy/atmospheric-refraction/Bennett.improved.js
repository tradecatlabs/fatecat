import * as std from '../../basic.js';
import * as Decimal from '../../math/decimal';
import * as Expression from '../../math/expression.js';
import * as Angle from '../../math/angle.js';

const decimal = Decimal.decimal;
const expression = Expression.expression;
const evaluate = Expression.evaluate;
const angle = Angle.angle;

// Bennett formula with improvement

// The improvement is metioned in Jean Meeus's book, Astronomical Algorithms, chapter 15.
// With improvement, maximum error is 0.015'=0.9"

// It should not be used when h_appreant >= 89.5°, because it gives slighly negative values.

export const R = (ha, P, T) => {
    let R = evaluate(expression("1.0/tan(deg2rad(ha+7.31/(ha+4.4)))"), {
        ha: Angle.rad2deg(angle(ha)) // real height, Radian to degree 
    },{
        deg2rad:Angle.deg2rad
    });
    // improvement
    let dR = evaluate(expression("-0.06*sin(deg2rad(14.7*R+13))"), {
        R: R //Angle.min2deg(R)
    },{
        deg2rad:Angle.deg2rad
    });
    return Angle.min2rad(evaluate(expression("f* (R+dR)"), {
        f: evaluate(expression("(P/101)*(283/(273+T))"), {
            P: P || 101.0, // pressure, default 101.0 kPa
            T: T || 10 // temperature, default 10 °C
        }),
        R: R,
        dR: dR
    })); // arcminutes to Radian
};