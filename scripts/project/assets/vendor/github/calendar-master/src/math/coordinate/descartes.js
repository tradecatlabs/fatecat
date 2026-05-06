import * as Decimal from '../decimal';
import * as Angle from '../angle.js';
import * as Vector from '../vector.js';
import * as Quaternion from '../quaternion.js';
import * as DualQuaternion from '../dual-quaternion.js';
import * as Point from './point.js';
const decimal = Decimal.decimal;
const angle = Angle.angle;
const vector = Vector.vector;
const quaternion = Quaternion.quaternion;
const dualquaternion = DualQuaternion.dualquaternion;
const sphere = Point.sphere;

export const descartes = Point.descartes;

export const toSphere = p => {
    let [x, y, z] = descartes(p);
    let proj = Decimal.sqrt(Decimal.plus(Decimal.sqr(x), Decimal.sqr(y)));
    let r = Decimal.sqrt(Decimal.plus(Decimal.sqr(proj), Decimal.sqr(z)));
    let theta = Angle.toZeroDoublePi(Decimal.atan2(proj, z)); // atan2 : (-pi,pi]
    let phi = Angle.toZeroDoublePi(Decimal.atan2(y, x));
    return sphere([r, theta, phi]);
}
export const show = p => {
    return "(" + descartes(p).map(x => Decimal.show(x)).join(",") + ")";
}


// Move orign to new place
export const translation = p => {
    let v = Vector.neg(vector(descartes(p))); // to move coordinate, we need negated vector
    let real = quaternion(1, [0, 0, 0]);
    let dual = Quaternion.mult(quaternion(0, v), 0.5);
    return dualquaternion(real, dual);
}

// a direction vector of axis, an angle
export const rotation = (axis, theta) => {
    theta = Angle.neg(angle(theta)); // to rotate coordinate, all points are rotated in opposite direction
    let half_theta = Decimal.mult(0.5, theta);
    let real = quaternion(Decimal.cos(half_theta), Vector.mult(Vector.normalize(axis), Decimal.sin(half_theta)));
    let dual = quaternion(0, [0, 0, 0]);
    return dualquaternion(real, dual);
}

export const transformation = (...args) => {
    if (args.length === 1) {
        if (Array.isArray(args[0])) {
            args = args[0];
        } else {
            throw new Error("Please give a series of translations/rotations!");
        }
    }
    args = args.map(x => dualquaternion(x));
    let dq = dualquaternion(quaternion(1, [0, 0, 0]), quaternion(0, [0, 0, 0]));
    return args.reduceRight((prod, x) => DualQuaternion.normalize(DualQuaternion.mult(prod, x)), dq);
}

export const transform = (p, t) => {
    let point = dualquaternion(quaternion(1, [0, 0, 0]), quaternion(0, vector(descartes(p))));
    point = DualQuaternion.mult(DualQuaternion.mult(t, point), DualQuaternion.conjugate3(t));
    return descartes(point.dual.vector);
}

export const translate = (p, v) => transform(descartes(p), translation(v));
export const rotateX = (p, theta) => transform(descartes(p), rotation([1, 0, 0], theta));
export const rotateY = (p, theta) => transform(descartes(p), rotation([0, 1, 0], theta));
export const rotateZ = (p, theta) => transform(descartes(p), rotation([0, 0, 1], theta));

export const includedAngle = (p1, p2) => {
    let v1 = vector(descartes(p1)),
        v2 = vector(descartes(p2));
    return Angle.toZeroDoublePi(Decimal.atan2(Vector.norm(Vector.cross(v1, v2)), Vector.dot(v1, v2)));
};
