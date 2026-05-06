import * as Decimal from '../../math/decimal';
import * as Angle from '../../math/angle.js';
import * as Point from './point.js';
const decimal = Decimal.decimal;
const angle = Angle.angle;

// the second equatorial coordinate system
// zh-cn: 第二赤道坐标系
export const equatorial = Point.second_equatorial;

export const show = p => {
    p = equatorial(p);
    return "right ascension:" + Angle.format(p.right_ascension, "HMS", 2) + ", declination:" + Angle.show(p.declination) +
        (p.hasOwnProperty("distance") ? (", distance:" + Decimal.show(p.distance)) : "");
}
