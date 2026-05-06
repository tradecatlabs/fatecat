import * as Decimal from '../../math/decimal';
import * as Angle from '../../math/angle.js';
import * as Polynomial from '../../math/polynomial.js';

const decimal = Decimal.decimal;
const angle = Angle.angle;
const polynomial = Polynomial.polynomial;

// Capitaine, N., Wallace, P. T., & Chapront, J. 2003b, A&A, 412, 567
const P03 = {
    "psi": "0, 5038.481507, -1.0790069, -0.00114045, +0.000132851, -9.51e-8 ",
    "omega": "84381.406000, -0.025754, +0.0512623, -0.00772503, -4.67e-7, +3.337e-7",
    "P": "0, 4.199094, +0.1939873, -0.00022466, -9.12e-7, +1.20e-8",
    "Q": "0, -46.811015, +0.0510283, +0.00052413, -6.46e-7, -1.72e-8",
    "epsilon": "84381.406000, -46.836769, -0.0001831, +0.00200340, -5.76e-7, -4.34e-8",
    "chi": "0, 10.556403, -2.3814292, -0.00121197, +0.000170663, -5.60e-8",
    "pi": "0, 46.998973, -0.0334926, -0.00012559, +1.13e-7, -2.2e-9", //
    "PI": "629546.7936, -867.95758, +0.157992, -0.0005371, -0.00004797, +7.2e-8", //
    "p": "0, 5028.796195, +1.1054348, +0.00007964, -0.000023857, +3.83e-8",
    "theta": "0, 2004.191903, -0.4294934, -0.04182264, -7.089e-6, -1.274e-7",
    "zeta": "2.650545, 2306.083227, +0.2988499, +0.01801828, -5.971e-6, -3.173e-7",
    "z": "-2.650545, 2306.077181, +1.0927348, +0.01826837, -0.000028596, -2.904e-7"
};

const array=s=>s.replace(/\s+/g,"").split(",").map(x=>decimal(x));
const calculate = (p, t) => Angle.sec2rad(Polynomial.value(polynomial(array(P03[p])), t));

export const psi = t => calculate("psi", t);
export const omega = t => calculate("omega", t);
export const P = t => calculate("P", t);
export const Q = t => calculate("Q", t);
export const epsilon = t => calculate("epsilon", t);
export const chi = t => calculate("chi", t);
export const pi = t => calculate("pi", t);
export const PI = t => calculate("PI", t);
export const p = t => calculate("p", t);
export const theta = t => calculate("theta", t);
export const zeta = t => calculate("zeta", t);
export const z = t => calculate("z", t);
