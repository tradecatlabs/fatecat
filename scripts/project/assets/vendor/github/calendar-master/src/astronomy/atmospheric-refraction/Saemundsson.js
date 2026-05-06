import * as std from '../../basic.js';
import * as Decimal from '../../math/decimal';
import * as Expression from '../../math/expression.js';
import * as Angle from '../../math/angle.js';

const decimal = Decimal.decimal;
const expression = Expression.expression;
const evaluate = Expression.evaluate;
const angle = Angle.angle;

// Sæmundsson formula (1972)
// It is consistent with Bennett’s formula within 0.1′
export const R = (h, P, T) => Angle.min2rad(evaluate(expression("f* 1.02 / tan( deg2rad(h + 10.3/ (h + 5.11)))"), {
    f: evaluate(expression("(P/101)*(283.15/(273.15+T))"), {
        P: P || 101.0, // pressure, default 101.0 kPa
        T: T || 10 // temperature, default 10 °C
    }),
    h: Angle.rad2deg(angle(h)) // real height, Radian to degree 
}, {
    deg2rad: Angle.deg2rad
})); // arc of minutes to Radian