import * as Decimal from '../../math/decimal';
import * as Angle from '../../math/angle.js';
import * as Point from './point.js';
const decimal = Decimal.decimal;
const angle = Angle.angle;

// the first equatorial coordinate system, HA-dec. system.
// zh-cn: 第一赤道坐标系，时角坐标系
export const equatorial = Point.first_equatorial;

export const show = p => {
    p = equatorial(p);
    return "hour angle:" + Angle.format(p.hour_angle, "HMS", 2) + ", declination:" + Angle.show(p.declination) +
        (p.hasOwnProperty("distance") ? (", distance:" + Decimal.show(p.distance)) : "");
}
