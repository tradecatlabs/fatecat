import * as std from '../../basic.js';
import * as Decimal from '../../math/decimal';
import * as Expression from '../../math/expression.js';
import * as Angle from '../../math/angle.js';

const decimal = Decimal.decimal;
const expression = Expression.expression;
const evaluate = Expression.evaluate;
const angle = Angle.angle;

// formula used by Jianwei Xu
export const R = h => evaluate(expression("0.0002967 / tan(h + 0.003138 / (h + 0.08919))"), { h: angle(h) });