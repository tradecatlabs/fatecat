import * as std from '../../basic.js';
import * as Angle from '../../math/angle.js';
import * as Decimal from '../../math/decimal';
const decimal = Decimal.decimal;
const angle = Angle.angle;
//////////////////////////////////////////////////////
// NOTE: 天文坐标系通常只有两个维度，不包含距离。
// 因为多数天体的距离十分遥远，通常视为半径无穷大的天球上的投影。
// 但是研究较近的天体，例如太阳系的行星，月球等，则会考虑到距离。

///////////////////////////////////////////////////////
const distance = (d) => {
    d = decimal(d);
    if (Decimal.gte(d, 0)) return d;
    throw new Error("Invalid distance value!");
}
const interval_neg90_pos90 = (x, name) => {
    x = decimal(x);
    if (Decimal.gte(x, Angle.neg(Angle.HalfPi)) && Decimal.lte(x, Angle.HalfPi)) return x;
    throw new Error("Invalid " + name + " value!");
}
const interval_0_360 = (x, name) => {
    x = decimal(x);
    if (Decimal.gte(x, 0) && Decimal.lt(x, Angle.DoublePi)) return x;
    throw new Error("Invalid " + name + " value!");
}
/////////////////////////////////////////////////////
// Equatorial system
const right_ascension = ra => interval_0_360(angle(ra), "right ascension");
const declination = dec => interval_neg90_pos90(angle(dec), "declination");
const hour_angle = ha => interval_0_360(angle(ha), "hour angle");
export const first_equatorial = (...args) => {
    if (args.length === 1) {
        let p = std.obj(args[0]);
        if (!p.hasOwnProperty("right_ascension") && p.hasOwnProperty("hour_angle") && p.hasOwnProperty("declination")) {
            if (p.hasOwnProperty("distance")) {
                return {
                    hour_angle: hour_angle(p.hour_angle),
                    declination: declination(p.declination),
                    distance: distance(p.distance)
                };
            }
            return {
                hour_angle: hour_angle(p.hour_angle),
                declination: declination(p.declination)
            };
        }
    } else if (args.length === 2) {
        return {
            hour_angle: hour_angle(args[0]),
            declination: declination(args[1])
        };
    } else if (args.length === 3) {
        return {
            hour_angle: hour_angle(args[0]),
            declination: declination(args[1]),
            distance: distance(args[2])
        };
    }
    throw new TypeError("Invalid position!");
}
export const second_equatorial = (...args) => {
    if (args.length === 1) {
        let p = std.obj(args[0]);
        if (!p.hasOwnProperty("hour_angle") && p.hasOwnProperty("right_ascension") && p.hasOwnProperty("declination")) {
            if (p.hasOwnProperty("distance")) {
                return {
                    right_ascension: right_ascension(p.right_ascension),
                    declination: declination(p.declination),
                    distance: distance(p.distance)
                };
            }
            return {
                right_ascension: right_ascension(p.right_ascension),
                declination: declination(p.declination)
            };
        }
    } else if (args.length === 2) {
        return {
            right_ascension: right_ascension(args[0]),
            declination: declination(args[1])
        };
    } else if (args.length === 3) {
        return {
            right_ascension: right_ascension(args[0]),
            declination: declination(args[1]),
            distance: distance(args[2])
        };
    }
    throw new TypeError("Invalid position!");
}
//////////////////////////////////////////////////
// Ecliptic system
const longitude = l => interval_0_360(angle(l), "longitude");
const latitude = b => interval_neg90_pos90(angle(b), "latitude");

export const ecliptic = (...args) => {
    if (args.length === 1) {
        let p = std.obj(args[0]);
        if (p.hasOwnProperty("longitude") && p.hasOwnProperty("latitude")) {
            if (p.hasOwnProperty("distance")) {
                return {
                    longitude: longitude(p.longitude),
                    latitude: latitude(p.latitude),
                    distance: distance(p.distance)
                };
            }
            return {
                longitude: longitude(p.longitude),
                latitude: latitude(p.latitude)
            };
        }
    } else if (args.length === 2) {
        return {
            longitude: longitude(args[0]),
            latitude: latitude(args[1])
        };
    } else if (args.length === 3) {
        return {
            longitude: longitude(args[0]),
            latitude: latitude(args[1]),
            distance: distance(args[2])
        };
    }
    throw new TypeError("Invalid position!");
}
//////////////////////////////////////////////////
// Horizontal system
// ch-zn: 方位角
const azimuth = az => interval_0_360(angle(az), "azimuth");
// zh-cn： 高度角
const altitude = alt => interval_neg90_pos90(angle(alt), "altitude");

export const horizontal = (...args) => {
    if (args.length === 1) {
        let p = std.obj(args[0]);
        if (p.hasOwnProperty("azimuth") && p.hasOwnProperty("altitude")) {
            if (p.hasOwnProperty("distance")) {
                return {
                    azimuth: azimuth(p.azimuth),
                    altitude: altitude(p.altitude),
                    distance: distance(p.distance)
                };
            }
            return {
                azimuth: azimuth(p.azimuth),
                altitude: altitude(p.altitude)
            };
        }
    } else if (args.length === 2) {
        return {
            azimuth: azimuth(args[0]),
            altitude: altitude(args[1])
        };
    } else if (args.length === 3) {
        return {
            azimuth: azimuth(args[0]),
            altitude: altitude(args[1]),
            distance: distance(args[2])
        };
    }
    throw new TypeError("Invalid position!");
}
