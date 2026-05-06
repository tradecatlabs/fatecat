import * as Decimal from '../../math/decimal';
import * as Angle from '../../math/angle.js';
import * as Polynomial from '../../math/polynomial.js';

const decimal = Decimal.decimal;
const angle = Angle.angle;
const polynomial = Polynomial.polynomial;

// IAU 1976 ecliptic precession (Lieske et al. 1977, A&A, 58, 1) 
// and the precession part of the IAU 2000A equator adopted by IAU 2000 Resolution B1.6
// (Mathews et al. 2002, J. Geophys. Res., 107, B4, 10.1029/2001JB000390)
const IAU2000 = {
    "psi": "0, 5038.478750, -1.07259, -0.001147",
    "omega": "84381.448, -0.025240, +0.05127, -0.007726",
    "P": "0, +4.1976, +0.19447, -0.000179",
    "Q": "0, -46.8150, +0.05059, +0.000344",
    "epsilon": "84381.448, -46.84024, -0.00059, +0.001813",
    "chi": "0, +10.5526, -2.38064, -0.001125",
    "p": "0, 5028.79695, +1.11113, +0.000006",
    "theta": "0, 2004.1917476, -0.4269353, -0.0418251, -0.0000601, -0.0000001",
    "zeta": "+2.5976176, 2306.0809506, +0.3019015, +0.0179663, -0.0000327, -0.0000002",
    "z": "-2.5976176, 2306.0803226, +1.0947790, +0.0182273, +0.0000470, -0.0000003"
};

const array=s=>s.replace(/\s+/g,"").split(",").map(x=>decimal(x));
const calculate = (p, t) => Angle.sec2rad(Polynomial.value(polynomial(array(IAU2000[p])), t));

export const psi = t => calculate("psi", t);
export const omega = t => calculate("omega", t);
export const P = t => calculate("P", t);
export const Q = t => calculate("Q", t);
export const epsilon = t => calculate("epsilon", t);
export const chi = t => calculate("chi", t);
//export const pi = t => calculate("pi", t);
//export const PI = t => calculate("PI", t);
export const p = t => calculate("p", t);
export const theta = t => calculate("theta", t);
export const zeta = t => calculate("zeta", t);
export const z = t => calculate("z", t);