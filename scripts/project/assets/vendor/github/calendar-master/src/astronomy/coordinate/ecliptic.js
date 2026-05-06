import * as Decimal from '../../math/decimal';
import * as Angle from '../../math/angle.js';
import * as Point from './point.js';
const decimal = Decimal.decimal;
const angle = Angle.angle;

// ecliptic coordinate system
// zh-cn: 黄道坐标系
export const ecliptic = Point.ecliptic;

export const show = p => {
    p = ecliptic(p);
    return "ecliptic longitude:" + Angle.show(p.longitude) + ", ecliptic latitude:" + Angle.show(p.latitude) +
        (p.hasOwnProperty("distance") ? (", distance:" + Decimal.show(p.distance)) : "");
}
