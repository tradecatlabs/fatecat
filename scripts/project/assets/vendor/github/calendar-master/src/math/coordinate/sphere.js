import * as Decimal from '../decimal';
import * as Angle from '../angle.js';
import * as Point from './point.js';
const descartes = Point.descartes;
const decimal = Decimal.decimal;
const angle = Angle.angle;

export const sphere = Point.sphere;

export const toDescartes = p => {
    p = sphere(p);
    let [r, theta, phi] = p;
    let proj = Decimal.mult(r, Decimal.sin(theta));
    return descartes([
        Decimal.mult(proj, Decimal.cos(phi)),
        Decimal.mult(proj, Decimal.sin(phi)),
        Decimal.mult(r, Decimal.cos(theta))
    ]);
}
export const show = p => {
    let [r, theta, phi] = sphere(p);
    return "(" + Decimal.show(r) + "," + Angle.show(theta) + "," + Angle.show(phi) + ")";
}
