import * as Decimal from '../../../math/decimal';
import * as Vector from '../../../math/vector';
import * as Angle from '../../../math/angle';
import * as Expression from '../../../math/expression';
import * as std from '../../../basic';

const decimal = Decimal.decimal;
const angle = Angle.angle;

export const constant = std.memoize((corrections) => {
    const a0ELP = decimal("384747.980674318"); //a0 for ELP
    const a0DE405 = decimal("384747.9613701725"); //a0 for DE405
    const ra0 = Decimal.div(a0DE405, a0ELP); //比例係數 a0(DE405)/a0(ELP)

    //Derivatives B'(i,j) used for the corrections δW2 and δW3
    const dBp = [ //dBp[1-5][1-2]
        [],
        [0, "+0.311079095", "-0.103837907"], //ν
        [0, "-0.004482398", "+0.000668287"], //Γ
        [0, "-0.001102485", "-0.001298072"], //E
        [0, "+0.001056062", "-0.000178028"], //e'
        [0, "+0.000050928", "-0.000037342"] //n'
    ];

    //     Moon constants:
    //     nu        : mean motion of the Moon (W1(1,1))                 (Nu)
    //     g         : half coefficient of sin(F) in latitude         (Gamma)
    //     e         : half coefficient of sin(l) in longitude            (E)
    //     np        : mean motion of EMB (eart(1))                      (n')
    //     ep        : eccentricity of EMB                               (e')

    //     alpha     : Ratio of the semi-major axis (Moon / EMB) α=a0/a' a0 and a' are the kleperian semi-major axis of the Moon and the Earth-Moon barycenter
    //     am        : Ratio of the mean motions (EMB / Moon) ratioMeanMotion=n'/ν,ν^2*a0^3=G(mT+mL) and n'^2*a'^3=G(mS+mT+mL). mS, mT and mL are respectively Sun, Earth and Moon masses.
    //     dtasm     : (2*alpha) / (3*am)
    const ratioSemiMajorAxis = "0.002571881"; // alpha
    const ratioMeanMotion = "0.074801329"; // am
    const rSMA2d3 = Decimal.div(Decimal.mult(2.0, ratioSemiMajorAxis), 3.0); //(2*alpha)/3
    const rSMA2drMM3 = Decimal.div(rSMA2d3, ratioMeanMotion); // dtasm=(2*alpha)/(3*am)

    // p is the IAU 1976 precession constant:5029.0966"/cy
    // Δp, an additive correction from (Herring et al., 2002): -0.29965"/cy.
    const IAUPrecession = "5029.0966";
    const deltaIAUPrecession = "-0.29965";


    //Values of the corrections to the constants
    let dlongitudeLunar1_0; //ΔW1(0)
    let dlongitudeLunar2_0; //ΔW2(0)
    let dlongitudeLunar3_0; //ΔW3(0)
    let dlongitudeLunar1_1; //ΔW1(1) =Δν
    let dlongitudeLunar2_1; //ΔW2(1)
    let dlongitudeLunar3_1; //ΔW3(1)
    let dlongitudeLunar1_2; //ΔW1(2)
    let dGAMMA; //ΔΓ
    let dE; //ΔE
    let dlongitudeEMB_0; //ΔT(0)
    let dlongitudeEMB_1; //ΔT(1) =Δn'
    let dperihelionEMB; //ΔωBAR'
    let dEp; //Δe'
    if (corrections === "LLR") {
        //Values of the corrections to the constants fitted to LLR.
        // Fit 13-05-02 (2 iterations) except Phi and eps w2_1 et w3_1
        dlongitudeLunar1_0 = "-0.10525"; //ΔW1(0)
        dlongitudeLunar2_0 = "+0.16826"; //ΔW2(0)
        dlongitudeLunar3_0 = "-0.10760"; //ΔW3(0)
        dlongitudeLunar1_1 = "-0.32311"; //ΔW1(1) =Δν
        dlongitudeLunar2_1 = "+0.08017"; //ΔW2(1)
        dlongitudeLunar3_1 = "-0.04317"; //ΔW3(1)
        dlongitudeLunar1_2 = "-0.03743"; //ΔW1(2)
        dGAMMA = "+0.00069"; //ΔΓ
        dE = "+0.00005"; //ΔE
        dlongitudeEMB_0 = "-0.04012"; //ΔT(0)
        dlongitudeEMB_1 = "+0.01442"; // ΔT(1) =Δn'
        dperihelionEMB = "-0.04854"; //ΔωBAR'
        dEp = "+0.00226"; //Δe'
    } else {
        //Values of the corrections to the constants fitted to DE405 over the time interval (1950-2060)
        dlongitudeLunar1_0 = "-0.07008"; //ΔW1(0)
        dlongitudeLunar2_0 = "+0.20794"; //ΔW2(0)
        dlongitudeLunar3_0 = "-0.07215"; //ΔW3(0)
        dlongitudeLunar1_1 = "-0.35106"; //ΔW1(1) =Δν
        dlongitudeLunar2_1 = "+0.08017"; //ΔW2(1)
        dlongitudeLunar3_1 = "-0.04317"; //ΔW3(1)
        dlongitudeLunar1_2 = "-0.03743"; //ΔW1(2)
        dGAMMA = "+0.00085"; //ΔΓ
        dE = "-0.00006"; //ΔE
        dlongitudeEMB_0 = "-0.00033"; //ΔT(0)
        dlongitudeEMB_1 = "+0.00732"; //ΔT(1) =Δn'
        dperihelionEMB = "-0.00749"; //ΔωBAR'
        dEp = "+0.00224"; //Δe'
    }


    //Fundamental arguments (Moon and EMB)
    //     Moon elements (polynomials coefficients until order 4):
    //     w(1,0:4)  : mean longitude of the Moon                        (W1)
    //     w(2,0:4)  : mean longitude of the lunar perigee               (W2)
    //     w(3,0:4)  : mean longitude of the lunar ascending node        (W3)
    //     zeta(0:4) : mean longitude of the Moon + precession        (W1+pt)
    //                 p is the precession rate and t is the time
    let longitudeLunar = Array.from({ length: 4 }, () => new Array(5).fill(0)); //w[1-3][0-4]
    let longitudeLunarZeta = new Array(5).fill(0); //zeta[0-4]
    longitudeLunar[1][0] = Decimal.plus(angle("218°18'59.95571\""), Angle.sec2rad(dlongitudeLunar1_0)); //***** ELP
    longitudeLunar[1][1] = Angle.sec2rad(Decimal.plus("1732559343.73604", dlongitudeLunar1_1)); //***** ELP
    longitudeLunar[1][2] = Angle.sec2rad(Decimal.plus("-6.8084", dlongitudeLunar1_2)); //***** DE405
    longitudeLunar[1][3] = Angle.sec2rad("0.66040e-2"); //***** ELP
    longitudeLunar[1][4] = Angle.sec2rad("-0.31690e-4"); //***** ELP

    longitudeLunar[2][0] = Decimal.plus(angle("83°21'11.67475\""), Angle.sec2rad(dlongitudeLunar2_0)); //***** ELP
    longitudeLunar[2][1] = Angle.sec2rad(Decimal.plus("14643420.3171", dlongitudeLunar2_1)); //***** DE405
    longitudeLunar[2][2] = Angle.sec2rad("-38.2631"); //***** DE405
    longitudeLunar[2][3] = Angle.sec2rad("-0.45047e-1"); //***** ELP
    longitudeLunar[2][4] = Angle.sec2rad("0.21301e-3"); //***** ELP

    longitudeLunar[3][0] = Decimal.plus(angle("125°2'40.39816\""), Angle.sec2rad(dlongitudeLunar3_0)); //***** ELP
    longitudeLunar[3][1] = Angle.sec2rad(Decimal.plus("-6967919.5383", dlongitudeLunar3_1)); //***** DE405
    longitudeLunar[3][2] = Angle.sec2rad("6.3590"); //***** DE405
    longitudeLunar[3][3] = Angle.sec2rad("0.76250e-2"); //***** ELP
    longitudeLunar[3][4] = Angle.sec2rad("-0.35860e-4"); //***** ELP

    //     Earth-Moon (EMB) elements (polynomials coefficients until order 4):
    //     eart(0:4) : mean longitude of EMB                             (Te)
    //     peri(0:4) : mean longitude of the perihelion of EMB   (Pip,ωBar')
    let longitudeEMB = new Array(5).fill(0); //eart[0-4]
    let perihelionEMB = new Array(5).fill(0); //peri[0-4]
    longitudeEMB[0] = Decimal.plus(angle("100°27'59.13885\""), Angle.sec2rad(dlongitudeEMB_0)); //***** VSOP2000
    longitudeEMB[1] = Angle.sec2rad(Decimal.plus("129597742.29300", dlongitudeEMB_1)); //***** VSOP2000
    longitudeEMB[2] = Angle.sec2rad("-0.020200"); //***** ELP
    longitudeEMB[3] = Angle.sec2rad("0.90000e-5"); //***** ELP
    longitudeEMB[4] = Angle.sec2rad("0.15000e-6"); //***** ELP

    perihelionEMB[0] = Decimal.plus(angle("102°56'14.45766\""), Angle.sec2rad(dperihelionEMB)); //***** VSOP2000
    perihelionEMB[1] = Angle.sec2rad("1161.24342"); //***** VSOP2000
    perihelionEMB[2] = Angle.sec2rad("0.529265"); //***** VSOP2000
    perihelionEMB[3] = Angle.sec2rad("-0.11814e-3"); //***** VSOP2000
    perihelionEMB[4] = Angle.sec2rad("0.11379e-4"); //***** VSOP2000

    if (corrections === "DE406") {
        //除了DE405的Δ項外，還要考慮更高階數
        //Corrections to the secular terms of Moon angles
        longitudeLunar[1][3] = Decimal.plus(longitudeLunar[1][3], Angle.sec2rad("-0.00018865")); //ΔW1(3)*
        longitudeLunar[1][4] = Decimal.plus(longitudeLunar[1][4], Angle.sec2rad("-0.00001024")); //ΔW1(4)*
        longitudeLunar[2][2] = Decimal.plus(longitudeLunar[2][2], Angle.sec2rad("+0.00470602")); //ΔW2(2)*
        longitudeLunar[2][3] = Decimal.plus(longitudeLunar[2][3], Angle.sec2rad("-0.00025213")); //ΔW2(3)*
        longitudeLunar[3][2] = Decimal.plus(longitudeLunar[3][2], Angle.sec2rad("-0.00261070")); //ΔW3(2)*
        longitudeLunar[3][3] = Decimal.plus(longitudeLunar[3][3], Angle.sec2rad("-0.00010712")); //ΔW3(3)*
    }

    //Corrections to the mean motions of the Moon angles W2 and W3
    //infered from the modifications of the constants
    let x2 = Decimal.div(longitudeLunar[2][1], longitudeLunar[1][1]);
    let x3 = Decimal.div(longitudeLunar[3][1], longitudeLunar[1][1]);
    let y2 = Decimal.plus(Decimal.mult(ratioMeanMotion, dBp[1][1]), Decimal.mult(rSMA2d3, dBp[5][1]));
    let y3 = Decimal.plus(Decimal.mult(ratioMeanMotion, dBp[1][2]), Decimal.mult(rSMA2d3, dBp[5][2]));

    let d21 = Decimal.minus(x2, y2);
    let d22 = Decimal.mult(longitudeLunar[1][1], dBp[2][1]);
    let d23 = Decimal.mult(longitudeLunar[1][1], dBp[3][1]);
    let d24 = Decimal.mult(longitudeLunar[1][1], dBp[4][1]);
    let d25 = Decimal.div(y2, ratioMeanMotion);

    let d31 = Decimal.minus(x3, y3);
    let d32 = Decimal.mult(longitudeLunar[1][1], dBp[2][2]);
    let d33 = Decimal.mult(longitudeLunar[1][1], dBp[3][2]);
    let d34 = Decimal.mult(longitudeLunar[1][1], dBp[4][2]);
    let d35 = Decimal.div(y3, ratioMeanMotion);

    let corrW2_1 = Vector.dot([d21, d22, d23, d24, d25], [dlongitudeLunar1_1, dGAMMA, dE, dEp, dlongitudeEMB_1]);
    let corrW3_1 = Vector.dot([d31, d32, d33, d34, d35], [dlongitudeLunar1_1, dGAMMA, dE, dEp, dlongitudeEMB_1]);

    longitudeLunar[2][1] = Decimal.plus(longitudeLunar[2][1], Angle.sec2rad(corrW2_1));
    longitudeLunar[3][1] = Decimal.plus(longitudeLunar[3][1], Angle.sec2rad(corrW3_1));

    //Arguments of Delaunay
    //     Delaunay arguments (polynomials coefficients until order 4):
    //     del(1,0:4): D  =  W1 - Te + 180 degrees                        (D)
    //     del(2,0:4): F  =  W1 - W3                                      (F)
    //     del(3,0:4): l  =  W1 - W2   mean anomaly of the Moon           (l)
    //     del(4,0:4): l' =  Te - Pip  mean anomaly of EMB               (l')
    let Delaunay = Array.from({ length: 5 }, () => new Array(5).fill(0)); //del[1-4][0-4]
    for (let i = 0; i < 5; i++) {
        Delaunay[1][i] = Decimal.minus(longitudeLunar[1][i], longitudeEMB[i]); //D
        Delaunay[2][i] = Decimal.minus(longitudeLunar[1][i], longitudeLunar[3][i]); //F
        Delaunay[3][i] = Decimal.minus(longitudeLunar[1][i], longitudeLunar[2][i]); //l
        Delaunay[4][i] = Decimal.minus(longitudeEMB[i], perihelionEMB[i]); //l'
    }
    Delaunay[1][0] = Decimal.plus(Delaunay[1][0], Angle.PI);

    //Planetary arguments (mean longitudes and mean motions)
    //     Planetary arguments (mean longitudes at J2000 and mean motions):
    //     p(1,0:1)  : mean longitude of Mercury
    //     p(2,0:1)  : mean longitude of Venus
    //     p(3,0:1)  : mean longitude of EMB (eart(0:1))
    //     p(4,0:1)  : mean longitude of Mars
    //     p(5,0:1)  : mean longitude of Jupiter
    //     p(6,0:1)  : mean longitude of Saturn
    //     p(7,0:1)  : mean longitude of Uranus
    //     p(8,0:1)  : mean longitude of Neptune
    let Planetary = Array.from({ length: 9 }, () => new Array(5).fill(0)); //p[1-8][0-4]
    Planetary[1][0] = angle("252°15'3.216919\""); //***** VSOP2000
    Planetary[2][0] = angle("181°58'44.758419\""); //***** VSOP2000
    Planetary[3][0] = angle("100°27'59.138850\""); //***** VSOP2000
    Planetary[4][0] = angle("355°26'3.642778\""); //***** VSOP2000
    Planetary[5][0] = angle("34°21'5.379392\""); //***** VSOP2000
    Planetary[6][0] = angle("50°4'38.902495\""); //***** VSOP2000
    Planetary[7][0] = angle("314°3'4.354234\""); //***** VSOP2000
    Planetary[8][0] = angle("304°20'56.808371\""); //***** VSOP2000

    Planetary[1][1] = Angle.sec2rad("538101628.66888"); //***** VSOP2000
    Planetary[2][1] = Angle.sec2rad("210664136.45777"); //***** VSOP2000
    Planetary[3][1] = Angle.sec2rad("129597742.29300"); //***** VSOP2000
    Planetary[4][1] = Angle.sec2rad("68905077.65936"); //***** VSOP2000
    Planetary[5][1] = Angle.sec2rad("10925660.57335"); //***** VSOP2000
    Planetary[6][1] = Angle.sec2rad("4399609.33632"); //***** VSOP2000
    Planetary[7][1] = Angle.sec2rad("1542482.57845"); //***** VSOP2000
    Planetary[8][1] = Angle.sec2rad("786547.89700"); //***** VSOP2000

    //Zeta : Mean longitude W1 + Rate of the precession
    longitudeLunarZeta[0] = longitudeLunar[1][0];
    longitudeLunarZeta[1] = Decimal.plus(longitudeLunar[1][1], Angle.sec2rad(Decimal.plus(IAUPrecession, deltaIAUPrecession)));
    longitudeLunarZeta[2] = longitudeLunar[1][2];
    longitudeLunarZeta[3] = longitudeLunar[1][3];
    longitudeLunarZeta[4] = longitudeLunar[1][4];

    //Corrections to the parameters: Nu, E, Gamma, n'and e'
    //     Corrections to the constants Nu, Gamma, E, n', e':
    //     delnu     : to the mean motion of the Moon
    //     delg      : to the half coefficient of sin(F) in latitude
    //     dele      : to the half coefficient of sin(l) in longitude
    //     delnp     : to the mean motion of EMB
    //     delep     : to the eccentricity of EMB
    const deltaNU = Decimal.div(Angle.sec2rad(Decimal.plus("+0.55604", dlongitudeLunar1_1)), longitudeLunar[1][1]); //***** ELP
    const deltaE = Angle.sec2rad(Decimal.plus("+0.01789", dE)); //***** ELP
    const deltaGamma = Angle.sec2rad(Decimal.plus("-0.08066", dGAMMA)); //***** ELP
    const deltaNp = Decimal.div(Angle.sec2rad(Decimal.plus("-0.06424", dlongitudeEMB_1)), longitudeLunar[1][1]); //***** ELP
    const deltaEp = Angle.sec2rad(Decimal.plus("-0.12879", dEp)); //***** ELP

    //     Precession of the longitude of the ascending node of the mean
    //     ecliptic of date on fixed ecliptic J2000
    //     pi(i=1,5) : sine coefficients
    //     qi(i=1,5) : cosine coefficients
    const LaskarsP = [0, "+0.10180391e-04", "+0.47020439e-06", "-0.5417367e-09", "-0.2507948e-11", "+0.463486e-14"];
    const LaskarsQ = [0, "-0.113469002e-03", "+0.12372674e-06", "+0.1265417e-08", "-0.1371808e-11", "-0.320334e-14"];

    return {
        ra0: ra0,
        ratioMeanMotion: ratioMeanMotion,
        rSMA2drMM3: rSMA2drMM3,
        deltaNU: deltaNU,
        deltaE: deltaE,
        deltaGamma: deltaGamma,
        deltaNp: deltaNp,
        deltaEp: deltaEp,
        Delaunay: Delaunay,
        Planetary: Planetary,
        longitudeLunarZeta: longitudeLunarZeta,
        longitudeLunar: longitudeLunar,
        LaskarsP: LaskarsP,
        LaskarsQ: LaskarsQ
    };
});
