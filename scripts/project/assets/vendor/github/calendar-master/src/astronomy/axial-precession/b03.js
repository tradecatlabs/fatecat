import * as Decimal from '../../math/decimal';
import * as Angle from '../../math/angle.js';
import * as Polynomial from '../../math/polynomial.js';

const decimal = Decimal.decimal;
const angle = Angle.angle;
const polynomial = Polynomial.polynomial;

// Bretagnon, P., Fienga, A., & Simon, J.-L. 2003, A&A, 400, 785
const B03 = {
    "psi": "0.0, 5038.478750, -1.0719530, -0.00114366, 0.000132832, -9.40e-8, -3.50e-9, 1.7e-10",
    "omega": "84381.40880, -0.026501, 0.0512769, -0.00772723, -0.000000492, 3.329e-7, -3.1e-10, -6.0e-11",
    "P": "0.0, 4.199604, 0.1939715, -0.00022350, -0.000001035, 1.9e-9, 0.0, 0.0",
    "Q": "0.0, -46.809550, 0.0510421, 0.00052228, -0.000000569, -1.4e-9, 1.0e-11, 0.0",
    "epsilon": "84381.40880, -46.836051, -0.0001667, 0.00199911, -0.000000523, -2.48e-8, -3.0e-11, 0.0",
    "chi": "0.0, 10.557686, -2.3813769, -0.00121258, 0.000170238, -7.70e-8, -3.99e-9, 1.6e-10",
    "pi": "0.0, 46.997560, -0.0335050, -0.00012370, 0.000000030, 0.0, 0.0, 0.0",
    "PI": "629543.988, -867.9218, 0.15342, 0.000005, -0.0000037, -1.0e-8, 0.0, 0.0",
    "p": "0.0, 5028.792262, 1.1124406, 0.00007699, -0.000023479, -1.78e-8, 1.8e-10, 1.0e-11",
    "theta": "0.0, 2004.190936, -0.4266980, -0.04182364, -0.000007291, -1.127e-7, 3.6e-10, 9.0e-11",
    "zeta": "2.72767, 2306.080472, 0.3023262, 0.01801752, -0.000005708, -3.040e-7, -1.3e-10, 0.0",
    "z": "-2.72767, 2306.076070, 1.0956768, 0.01826676, -0.000028276, -2.486e-7, -5.0e-11, 0.0"
};
const array=s=>s.replace(/\s+/g,"").split(",").map(x=>decimal(x));
const calculate = (p, t) => Angle.sec2rad(Polynomial.value(polynomial(array(B03[p])), t));

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
