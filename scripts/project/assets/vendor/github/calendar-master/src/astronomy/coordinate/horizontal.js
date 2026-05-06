import * as Decimal from '../../math/decimal';
import * as Angle from '../../math/angle.js';
import * as Point from './point.js';
const decimal = Decimal.decimal;
const angle = Angle.angle;

// horizontal coordinate system
// zh-cn: 地平坐标系
export const horizontal = Point.horizontal;

export const show = p => {
    p = horizontal(p);
    return "azimuth angle:" + Angle.show(p.azimuth) + ", altitude:" + Angle.show(p.altitude) +
        (p.hasOwnProperty("distance") ? (", distance:" + Decimal.show(p.distance)) : "");
}
