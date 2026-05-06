import * as Decimal from '../../math/decimal';
import * as Angle from '../../math/angle.js';
import * as Polynomial from '../../math/polynomial.js';

const decimal = Decimal.decimal;
const angle = Angle.angle;
const polynomial = Polynomial.polynomial;

// Lieske, J. H., Lederle, T., Fricke, W., & Morando, B. 1977, A&A, 58, 1
const L77 = {
    "psi": "0, 5038.7784, -1.07259, -0.001147", //赤道岁差、日月岁差，J2000黄道上的岁差，Date平赤道与J2000赤道的角距离
    "omega": "84381.448, 0, +0.05127, -0.007726", //J2000黄道与Date平赤道的夹角
    "P": "0, +4.1976, +0.19447, -0.000179", //Date平赤道坐标系天北极在J2000赤道坐标系中的赤纬
    "Q": "0, -46.8150, +0.05059, +0.000344", //Date平赤道坐标系天北极在J2000赤道坐标系中的赤经
    "epsilon": "84381.448, -46.8150, -0.00059, +0.001813", //当日的黄赤交角
    "chi": "0, +10.5526, -2.38064, -0.001125", //黄道岁差，行星岁差
    "p": "0, 5029.0966, +1.11113, +0.000006", //黄经总岁差
    "theta": "0, 2004.3109, -0.42665, -0.041833", //旋转参数
    "zeta": "0, 2306.2181, +0.30188, +0.017998",
    "z": "0, 2306.2181, +1.09468, +0.018203"
};

const array=s=>s.replace(/\s+/g,"").split(",").map(x=>decimal(x));
const calculate = (p, t) => Angle.sec2rad(Polynomial.value(polynomial(array(L77[p])), t));

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
