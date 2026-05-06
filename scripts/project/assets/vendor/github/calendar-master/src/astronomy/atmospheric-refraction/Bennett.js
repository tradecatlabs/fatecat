import * as std from '../../basic.js';
import * as Decimal from '../../math/decimal';
import * as Expression from '../../math/expression.js';
import * as Angle from '../../math/angle.js';

const decimal = Decimal.decimal;
const expression = Expression.expression;
const evaluate = Expression.evaluate;
const angle = Angle.angle;

// Bennett formula
// 1982, The calculation of astronomical refraction in marine navigation, Journal of the Institute of Navigation, 35, 255.
// low-presion . maximum error is 0.07'=4.2", when h_appreant=12°
// valid for h_appreant > 30°
export const R = (ha, P, T) => {
    let R = evaluate(expression("1.0/tan(deg2rad(ha+7.31/(ha+4.4)))"), {
        ha: Angle.rad2deg(angle(ha))
    }, {
        deg2rad: Angle.deg2rad
    });
    return Angle.min2rad(Decimal.mult(R, evaluate(expression("(P/101)*(283/(273+T))"), {
        P: P || 101.0, // pressure, default 101.0 kPa
        T: T || 10 // temperature, default 10 °C
    })));
};