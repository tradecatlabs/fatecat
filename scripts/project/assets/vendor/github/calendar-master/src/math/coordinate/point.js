import * as Decimal from '../decimal';
import * as Angle from '../angle.js';
const decimal = Decimal.decimal;
const angle = Angle.angle;

const check_sphere_point = (r, theta, phi) => {
    if (Decimal.gte(decimal(r), 0)) {
        theta = angle(theta);
        if (Decimal.eq(theta, 0) || Decimal.eq(theta, Angle.PI))
            return true;
        if (Decimal.gte(Decimal.gt(theta, 0) && Decimal.lt(Angle.PI))) {
            phi = angle(phi);
            return Decimal.gte(phi, 0) && Decimal.lt(phi, Angle.DoublePi);
        }
    }
    return false;
}

export const sphere = (...args) => {
    if (args.length === 1) {
        if (Array.isArray(args[0]) && args[0].length === 3) {
            let [r, theta, phi] = args[0];
            if (check_sphere_point(r, theta, phi)) {
                return [decimal(r), angle(theta), angle(phi)];
            }
        } else {
            throw new TypeError("Except a 3d point!");
        }
    } else if (args.length === 3) {
        if (check_sphere_point(args[0], args[1], args[2])) {
            return args.map(x => decimal(x));
        }
    }
    throw new TypeError("Invalid 3d point!");
}

export const descartes = (...args) => {
    if (args.length === 1) {
        if (Array.isArray(args[0]) && args[0].length === 3) {
            return args[0].map(x => decimal(x));
        } else {
            throw new TypeError("Except a 3d point!");
        }
    } else if (args.length === 3) {
        return args.map(x => decimal(x));
    }
    throw new TypeError("Invalid 3d point!");
}
