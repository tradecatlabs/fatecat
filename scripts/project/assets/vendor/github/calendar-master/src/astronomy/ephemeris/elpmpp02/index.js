import * as Decimal from '../../../math/decimal';
import * as Angle from '../../../math/angle';
import * as Vector from '../../../math/vector';
import * as Polynomial from '../../../math/polynomial';
import * as Expression from '../../../math/expression';
import * as std from '../../../basic';
import { parse } from './parse.js';
import * as Constant from '../../constant';
import * as Common from './common.js';

const decimal = Decimal.decimal;
const polynomial = Polynomial.polynomial;

/*
 * LUNAR SOLUTION ELP version ELP/MPP02 by Jean Chapront and G´erard Francou
 * ftp://syrte9.obspm.fr/pub/polac/2_lunar_solutions/2_elpmpp02/
 *
 * 文件結構
 *
 * ELP文件對應的公式如下
 * ELP_MAIN 文件内的數據為參數 i1,i2,i3,i4,A,B1,B2..B6 其中Bi是A的校正係數
 * ΣA*sin(i1*D+i2*F+i3*l+i4*l') --- ELP_MAIN.S1 ELP_MAIN.S2    /4i3,2x,f13.5,6f12.2
 * ΣA*cos(i1*D+i2*F+i3*l+i4*l') --- ELP_MAIN.S3                /4i3,2x,f13.5,6f12.2
 *
 * ELP_PERT 文件内的數據為參數 S,C,i1,i2..i13 並且 文件内還按照T的階分了塊
 * t^n*Σ(S*sinφ+C*cosφ)       --- ELP_PERT.S1~3              /5x,2d20.13,13i3
 * φ=i1D+i2F+i3l+i4l'+i5Me+i6V+i7T+i8Ma+i9J+i10S+i11U+i12N+i13ζ
 *
 * 精度
 *
 * 以DE405/406的月球數據為基準
 * 1950-2060年範圍内誤差最大值 經度 0.06" 緯度0.003" 距離4m
 * 1500-2500年範圍内誤差最大值 經度 0.6"  緯度0.05"  距離50m
 *-3000-3000年範圍内誤差最大值 經度50"    緯度5"     距離10km
 *
 * 如果針對DE406進一步校正 則
 *-3000-3000年範圍内誤差最大值 經度3.5"   緯度0.8"   距離1.5km
 *
 * 輸出
 *
 * J2000慣性參考系 直角坐標
 * 距離單位 km
 * 速度單位 km/day
 *
 */

const CalculateComponent = (t, alphaT, period, poisson) => {
    //Main Problem series
    let period_terms = period.map(coeff => {
        let x = coeff.Ci;
        let p = polynomial(coeff.Fi);
        let dp = Polynomial.derivative(p);
        let y = Polynomial.value(p, t);
        let yp = Polynomial.value(dp, t);
        return {
            // ci*sin(f0+f1*t+f2*t^2+f3*t^3+f4*t4) == x*sin(y)
            p: Decimal.mult(x, Decimal.sin(y)),
            // ci*cos(f0+ft*1+f2*t^2+f3*t^3+f4*t4)*(f1+2*f2*t+3*f3*t^2+4*f4*t^3) == x* cos(y)* yp
            v: Decimal.mult(Decimal.mult(x, Decimal.cos(y)), yp)
        };
    });
    // Perturbations series
    let poisson_terms = poisson.map(coeff => {
        let p = polynomial(coeff.Fi);
        let dp = Polynomial.derivative(p);
        let y = Polynomial.value(p, t);
        let yp = Polynomial.value(dp, t);
        let a = coeff.alpha;
        let x = Decimal.mult(coeff.Ci, alphaT[a]); // ci*t^a
        let xp = (a == 0 ? 0 : Decimal.mult(Decimal.mult(a, coeff.Ci), alphaT[a - 1])); // a*ci*t^(a-1)
        return {
            // t^a*ci*sin(f0+f1*t+f2*t^2+f3*t^3+f4*t4) == t^a* x* sin(y)
            p: Decimal.mult(x, Decimal.sin(y)),
            // a*t^(a-1)*ci*sin(f0+f1*t+f2*t^2+f3*t^3+f4*t4)+t^a*ci*cos(f0+ft*1+f2*t^2+f3*t^3+f4*t4)*(f1+2*f2*t+3*f3*t^2+4*f4*t^3)
            // xp* sin(y) + x* cos(y) *yp
            v: Decimal.plus(Decimal.mult(xp, Decimal.sin(y)), Decimal.mult(x, Decimal.mult(yp, Decimal.cos(y))))
        };
    });
    return std.ozipWith(...[Decimal.sum].concat(period_terms.concat(poisson_terms)));
};

const calculate = (JD, periodV, periodU, periodR, poissonV, poissonU, poissonR, Constants) => {
    let T = Decimal.div(Decimal.minus(JD, Constant.J2000), 36525.0); //100 Julian Year since J2000
    // Initialization of time powers, T^0..T^4
    let alphaT = new Array(5).fill().map((x, i) => Decimal.pow(T, i));

    // Evaluation of the series: substitution of time in the series
    // pv1 : Longitude
    // pv2 : Latitude
    // pv3 : Distance
    let pv1 = CalculateComponent(T, alphaT, periodV, poissonV);
    let pv2 = CalculateComponent(T, alphaT, periodU, poissonU);
    let pv3 = CalculateComponent(T, alphaT, periodR, poissonR);

    let v = [0, pv1.p, pv2.p, pv3.p, pv1.v, pv2.v, pv3.v];

    // Computation of the rectangular coordinates (Epoch J2000)

    // Longitude: V = [ periodic series (ELP MAIN.S1) + Poisson series (ELP PERT.S1) ] + W1
    // Latitude:  U = [ periodic series (ELP MAIN.S2) + Poisson series (ELP PERT.S2) ]
    // Distance:  r = [ periodic series (ELP MAIN.S3) + Poisson series (ELP PERT.S3) ] × ra0
    // ra0 = a0(DE405)/a0(ELP)
    let lp = polynomial(Constants.longitudeLunar[1]);
    let dlp = Polynomial.derivative(lp);
    v[1] = Decimal.plus(Angle.sec2rad(v[1]), Polynomial.value(lp, T));
    v[2] = Angle.sec2rad(v[2]);
    v[3] = Decimal.mult(v[3], Constants.ra0);
    // V' U' 修正 r'不用修正
    v[4] = Decimal.plus(Angle.sec2rad(v[4]), Polynomial.value(dlp, T));
    v[5] = Angle.sec2rad(v[5]);


    //坐標轉換+Laskars修正
    // |x2000|   |      1-2P²            2PQ        2P√(1-P²-Q²) |   |r*cosVcosU|
    // |y2000| = |       2PQ            1-2Q²      -2Q√(1-P²-Q²) | * |r*sinVcosU|
    // |z2000|   | -2P√(1-P²-Q²)   2Q√(1-P²-Q²)      1-2P²-2Q²   |   |r*sinU    |
    // TODO: implement matrix operator
    let cosV = Decimal.cos(v[1]); //clamb
    let sinV = Decimal.sin(v[1]); //slamb
    let cosU = Decimal.cos(v[2]); //cbeta
    let sinU = Decimal.sin(v[2]); //sbeta
    let RcosU = Decimal.mult(v[3], cosU); // cw
    let RsinU = Decimal.mult(v[3], sinU); // sw

    // sphere (V,U,R) ---> rectangular (x1, x2, x3)
    let x1 = Decimal.mult(RcosU, cosV); // cw*clamb
    let x2 = Decimal.mult(RcosU, sinV); // cw*slamb
    let x3 = RsinU; // sw
    // x1=R*cosV*cosU, d(x1)/dt= R'*cosV*cosU-R*sinV*V'*cosU-R*cosV*sinU*U'=(R'*cosU-R*sinU*U')*cosV-R*sinV*cosU*V'
    let xp1 = Decimal.minus(Decimal.mult(Decimal.minus(Decimal.mult(v[6], cosU), Decimal.mult(v[5], RsinU)), cosV), Decimal.mult(v[4], x2)); // (v(6)*cbeta-v(5)*sw)*clamb-v(4)*x2
    // x2=R*sinV*cosU, d(x2)/dt= R'*sinV*cosU+R*cosV*V'*cosU-R*sinV*sinU*U'=(R'*cosU-R*sinU*U')*sinV+R*cosV*cosU*V'
    let xp2 = Decimal.plus(Decimal.mult(Decimal.minus(Decimal.mult(v[6], cosU), Decimal.mult(v[5], RsinU)), sinV), Decimal.mult(v[4], x1)); //(v(6) * cbeta - v(5) * sw) * slamb + v(4) * x1
    // x3=RsinU, d(x3)/dt= R'sinU+R*cosU*U'
    let xp3 = Decimal.plus(Decimal.mult(v[6], sinU), Decimal.mult(v[5], RcosU)); //v(6)*sbeta+v(5)*cw

    //Laskars series
    // t*(p1+p2*t+p3*t^2+p4*t^3+p5*t^4)=p(t)
    let pw = Polynomial.value(polynomial(Constants.LaskarsP), T);
    // t*(q1+q2*t+q3*t^2+q4*t^3+q5*t^4)=q(t)
    let qw = Polynomial.value(polynomial(Constants.LaskarsQ), T);

    let ra = Decimal.mult(2, Decimal.sqrt(Decimal.minus(Decimal.minus(1, Decimal.sqr(pw)), Decimal.sqr(qw)))); //2√(1-P²-Q²)
    let pwqw = Decimal.mult(2, Decimal.mult(pw, qw)); //2PQ
    let pw2 = Decimal.minus(1, Decimal.mult(2, Decimal.sqr(pw))); //1-2P²
    let qw2 = Decimal.minus(1, Decimal.mult(2, Decimal.sqr(qw))); //1-2Q²
    let pwra = Decimal.mult(pw, ra); //2P√(1-P²-Q²)
    let qwra = Decimal.mult(qw, ra); //2Q√(1-P²-Q²)

    let result = [0, 0, 0, 0, 0, 0]; //x, y, z, x',y',z'
    // x y z
    result[0] = Vector.dot([pw2, pwqw, pwra], [x1, x2, x3]);
    result[1] = Vector.dot([pwqw, qw2, Decimal.neg(qwra)], [x1, x2, x3]);
    result[2] = Vector.dot([Decimal.neg(pwra), qwra, Decimal.minus(Decimal.plus(pw2, qw2), 1)], [x1, x2, x3]);

    //Laskars series
    //p1+t*(2*p2+3*p3*t+4*p4*t^2+5*p5*t^3)=p1+2*p2*t+3*p3*t^2+4*p4*t^3+5*p5*t^4=p'(t)
    let ppw = Polynomial.value(Polynomial.derivative(polynomial(Constants.LaskarsP)), T);
    //q1+t*(2*q2+3*q3*t+4*q4*t^2+5*q5*t^3)=q1+2*q2*t+3*q3*t^2+4*q4*t^3+5*q5*t^4=q'(t)
    let qpw = Polynomial.value(Polynomial.derivative(polynomial(Constants.LaskarsQ)), T);
    let ppw2 = Decimal.mult(-4, Decimal.mult(pw, ppw));
    let qpw2 = Decimal.mult(-4, Decimal.mult(qw, qpw));
    let ppwqpw = Decimal.mult(2, Decimal.plus(Decimal.mult(ppw, qw), Decimal.mult(pw, qpw)));
    let rap = Decimal.div(Decimal.plus(ppw2, qpw2), ra);
    let ppwra = Decimal.plus(Decimal.mult(ppw, ra), Decimal.mult(pw, rap));
    let qpwra = Decimal.plus(Decimal.mult(qpw, ra), Decimal.mult(qw, rap));

    //x'y'z'
    result[3] = Decimal.div(Vector.dot([pw2, pwqw, pwra, ppw2, ppwqpw, ppwra], [xp1, xp2, xp3, x1, x2, x3]), 36525);
    result[4] = Decimal.div(Vector.dot([pwqw, qw2, Decimal.neg(qwra), ppwqpw, qpw2, Decimal.neg(qpwra)], [xp1, xp2, xp3, x1, x2, x3]), 36525);
    result[5] = Decimal.div(Vector.dot([Decimal.neg(pwra), qwra, Decimal.minus(Decimal.plus(pw2, qw2), 1), Decimal.neg(ppwra), qpwra, Decimal.plus(ppw2, qpw2)], [xp1, xp2, xp3, x1, x2, x3]), 36525);

    return result.map(x => Decimal.toDecimalPosition(x, 7));
}

export const ELPMPP02 = std.memoize((correction) => {
    correction = correction || "LLR";
    return {
        periodV: parse(1, "ELP_MAIN.S1", correction),
        periodU: parse(2, "ELP_MAIN.S2", correction),
        periodR: parse(3, "ELP_MAIN.S3", correction),
        poissonV: parse(4, "ELP_PERT.S1", correction),
        poissonU: parse(5, "ELP_PERT.S2", correction),
        poissonR: parse(6, "ELP_PERT.S3", correction),
        Constants: Common.constant(correction)
    };
});

/*
export const position_velocity = (JD, correction) => {
    let ELP = ELPMPP02(correction);
    console.log(std.omap(ELP, x => x.length + " terms"));
    return calculate(JD, ELP.periodV, ELP.periodU, ELP.periodR, ELP.poissonV, ELP.poissonU, ELP.poissonR, ELP.Constants);
}
*/

export const position_velocity = (elpmpp02, jd) => {
    return calculate(jd, elpmpp02.periodV, elpmpp02.periodU, elpmpp02.periodR, elpmpp02.poissonV, elpmpp02.poissonU, elpmpp02.poissonR, elpmpp02.Constants);
}
