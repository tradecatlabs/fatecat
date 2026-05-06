import * as std from '../../basic.js';
import * as Decimal from '../../math/decimal';
import * as Expression from '../../math/expression.js';
import * as Angle from '../../math/angle.js';

const decimal = Decimal.decimal;
const expression = Expression.expression;
const evaluate = Expression.evaluate;
const angle = Angle.angle;

// NOTE:: 
// Some people also call it as Meeus formula,
// but actually in Jean Meeus's book, Astronomical Algorithms, chapter 15,
// he states that the formula is given by Smart.

// Smart formula
// when h_appreant > 30° , maximum error is 1"
// when h_appreant < 15° , totally meaningless
export const R = (ha, P, T) => {
    let R = evaluate(expression("58.294*tan(z)-0.0668*(tan(z))^3"), {
        z: Decimal.minus(Angle.HalfPi, angle(ha))
    });
    return Angle.sec2rad(Decimal.mult(R, evaluate(expression("(P/101)*(283/(273+T))"), {
        P: P || 101.0, // pressure, default 101.0 kPa
        T: T || 10 // temperature, default 10 °C
    })));
}; 