import * as std from '../../basic.js';
import * as Decimal from '../../math/decimal';
import * as Expression from '../../math/expression.js';
import * as Angle from '../../math/angle.js';

const decimal = Decimal.decimal;
const expression = Expression.expression;
const evaluate = Expression.evaluate;
const angle = Angle.angle;

// Meeus formula
// It's derived from Smart formula. Hence, it is available only when h > 30°
export const R = (h, P, T) => {
    let R = evaluate(expression("58.276*tan(z)-0.0824*(tan(z))^3"), {
        z: Decimal.minus(Angle.HalfPi, angle(h))
    });
    return Angle.sec2rad(Decimal.mult(R, evaluate(expression("(P/101.0)*(283/(273+T))"), {
        P: P || 101.0, // pressure, default 101.0 kPa
        T: T || 10 // temperature, default 10 °C
    })));
};