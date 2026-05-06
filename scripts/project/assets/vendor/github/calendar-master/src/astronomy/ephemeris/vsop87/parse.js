import * as fs from 'fs';
import * as path from "path";
import * as Decimal from '../../../math/decimal';
import * as Expression from '../../../math/expression';
import * as std from '../../../basic';
import { precision } from './precision';
import * as Common from './common';

const decimal = Decimal.decimal;
const expression = Expression.expression;
const evaluate = Expression.evaluate;
const int = parseInt;

const chunk = (s, size) => {
    let groups = [];
    for (let i = 0; i < s.length; i += size) {
        groups.push(s.slice(i, i + size));
    }
    return groups;
};

// There are two kinds of lines in the file
// 1. A one-line descriptor indicating a block of following lines.
/*
Fortran format : 17x,i1,4x,a7,12x,i1,17x,i1,i7
Specifications :
- iv : code of VSOP87 version               integer     i1  col.18
- bo : name of body                         character   a7  col.23-29
- ic : index of coordinate                  integer     i1  col.42
- it : degree alpha of time variable T      integer     i1  col.60
- in : number of terms of series            integer     i7  col.61-67
The code iv of the version is :
iv = 0 for the main version VSOP87
iv = 1 for the version VSOP87A
iv = 2 for the version VSOP87B
iv = 3 for the version VSOP87C
iv = 4 for the version VSOP87D
iv = 5 for the version VSOP87E
The names bo of the bodies are :
MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, SUN,
and EMB for the Earth-Moon Barycenter.
The index ic of the coordinates are :
- for the elliptic coordinates (main version) :
1 : semi-major axis
2 : mean longitude
3 : k = e cos(p)                  e : eccentricity
4 : h = e sin(p)                  p : perihelion longitude
5 : q = sin(g) cos(G)             g : semi-inclination
6 : p = sin(g) sin(G)             G : ascending node longitude
- for the rectangular coordinates (versions A,C,E) :
1 : X
2 : Y
3 : Z
- for the spherical coordinates (versions B,D) :
1 : Longitude
2 : Latitude
3 : Radius
The degree alpha of the time variable is equal to :
0 for periodic series, 1 to 5 for Poisson series.

*/
const head = s => {
    //17x,i1,4x,a7,12x,i1,17x,i1,i7 長度不小於67 實際長度與TermRecord一致
    if (s.length < 67) throw new Error("Invalid block descriptor! " + s);
    return {
        vsopVersion: int(s.substr(17, 1)), //VSOP87文件版本
        astroObjectName: s.substr(22, 7), //星體對象名 開始於1
        coordinateIndex: int(s.substr(41, 1)), //坐標分量序號 對於直角坐標係 1:x 2:y 3:z 對於球面坐標系 1:λ Longitude 2:β Latitude 3:δ Distance (Radius)
        alphaT: int(s.substr(59, 1)), //階數α
        termsCount: int(s.substr(60, 7)), // //本段包含的項數 n
        description: s.substr(67).replace(/(^\s*)|(\s*$)/g, '') //版本描述
    };
};
/*
Fortran format : 1x,4i1,i5,12i3,f15.11,2f18.11,f14.11,f20.11
Specifications :
iv : code of VSOP87 version                 integer     i1  col.02
ib : code of body                           integer     i1  col.03
ic : index of coordinate                    integer     i1  col.04
it : degree alpha of time variable T        integer     i1  col.05
n  : rank of the term in a series           integer     i5  col.06-10
a  : 12 coefficients a of mean longitudes   integer   12i3  col.11-46
S  : amplitude S                            real dp f15.11  col.47-61
K  : amplitude K                            real dp f18.11  col.62-79
A  : amplitude A                            real dp f18.11  col.80-97
B  : phase     B                            real dp f14.11  col.98-111
C  : frequency C                            real dp f20.11  col.112-131
The codes of the bodies are :
 1 : Mercury
 2 : Venus
 3 : Earth for the versions A-E and Earth-Moon Barycenter for the main version
 4 : Mars
 5 : Jupiter
 6 : Saturn
 7 : Uranus
 8 : Neptune
 9 : Earth-Moon barycenter for the version A and Sun for the version E.

 VSOP87 VERSION A1    NEPTUNE   VARIABLE 2 (XYZ)       *T**4      7 TERMS    HELIOCENTRIC DYNAMICAL ECLIPTIC AND EQUINOX J2000
 1824    1  0  0  0  0  5-10  0  0  0  0  0  0  0.00000002656     0.00000003290     0.00000004229 6.14485774863     515.46387109300
 1824    2  0  0  0  0  2 -7  0  0  0  0  0  0 -0.00000003809     0.00000002068     0.00000004334 3.84569500845     433.71173787680
 1824    3  0  0  0  0  0  5  0 -2  0  0  0  0 -0.00000003010     0.00000001875     0.00000003547 1.04321243122     990.22940591440
 1824    4  0  0  0  0  3-10  0  2  0  0  0  0 -0.00000001987    -0.00000002450     0.00000003155 0.14082926066     467.65198782060
 1824    5  0  0  0  0  4-11  0  0  0  0  0  0 -0.00000001950    -0.00000002302     0.00000003017 4.77719363131     227.52618943960
 1824    6  0  0  0  0  2 -6  0  0  0  0  0  0  0.00000001667     0.00000001643     0.00000002341 4.83747395607     220.41264243880
 1824    7  0  0  0  0  2 -4  0  0  0  0  0  0  0.00000001730     0.00000001508     0.00000002295 3.13221204419     206.18554843720
 VSOP87 VERSION A1    NEPTUNE   VARIABLE 3 (XYZ)       *T**0    133 TERMS    HELIOCENTRIC DYNAMICAL ECLIPTIC AND EQUINOX J2000
 1830    1  0  0  0  0  0  0  0  1  0  0  0  0 -0.61877933207    -0.69247566331     0.92866054405 1.44103930278      38.13303563780
 1830    2  0  0  0  0  0  0  0  0  0  0  0  0  0.00000000000     0.01245978462     0.01245978462 0.00000000000       0.00000000000
 1830    3  0  0  0  0  0  0  1 -1  0  0  0  0 -0.00336547707    -0.00334257346     0.00474333567 2.52218774238      36.64856292950
 1830    4  0  0  0  0  0  0  1 -3  0  0  0  0 -0.00277721785     0.00356600203     0.00451987936 3.50949720541      39.61750834610
 1830    5  0  0  0  0  0  0  0  2  0  0  0  0 -0.00417557448    -0.00000719603     0.00417558068 5.91310695421      76.26607127560
 1830    6  0  0  0  0  0  0  1 -2  0  0  0  0 -0.00057524767     0.00061355027     0.00084104329 4.38928900096       1.48447270830
 */
const term = s => {
    //1x,4i1,i5,12i3,f15.11,2f18.11,f14.11,f20.11 長度等於131 或者132(+\r) 或者133(+\r\n)
    if (s.length < 131) throw Error("invalid lenght of term! " + s);
    return {
        vsopVersion: int(s.substr(1, 1)),
        astroObject: int(s.substr(2, 1)),
        coordinateIndex: int(s.substr(3, 1)),
        alphaT: int(s.substr(4, 1)),

        termIndex: int(s.substr(5, 5)),
        coefficients: chunk(s.substr(10, 12 * 3), 3).map(x => decimal(x)),

        amplitudeS: decimal(s.substr(46, 15)),
        amplitudeK: decimal(s.substr(61, 18)),
        amplitudeA: decimal(s.substr(79, 18)),
        phaseB: decimal(s.substr(97, 14)),
        frequencyC: decimal(s.substr(111, 20))
    };
};

export const validate = (vsopFile) => {
    let text = fs.readFileSync(path.join(__dirname, "data/" + vsopFile), 'ascii');
    let lines = text.split(/\r\n|[\n\v\f\r\x85\u2028\u2029]/);
    let header_record = head(lines[0]);
    let term_record = term(lines[1]);
    if (term_record.vsopVersion === header_record.vsopVersion) {
        return {
            vsopVersion: term_record.vsopVersion,
            vsopObject: term_record.astroObject
        }
    }
    throw new Error("Invalid VSOP87 data file!");
}

export const parse = std.memoize((vsopFile, vsopFileVersion, vsopObject, prec, t) => {
    t = t || 10;
    let span = Common.span(vsopObject, vsopFileVersion); //精度時間範圍
    if (Decimal.lt(t, span)) span = t; //如果需要的精度時間範圍比行星的標準精度時間範圍小 則意味著或許可以截掉更多的項

    let truncate = null,
        coordUnitIsAU;
    if (prec) {
        // 現在 0<span=Min(輸入精度時間範圍,標準精度時間範圍),
        // precision將在EvalPrecision中被規範為[MinPrecision MaxPrecision]之間
        truncate = precision(vsopObject, vsopFileVersion, prec, span);
        if (truncate.truncate) {
            coordUnitIsAU = Common.coordinate(vsopFileVersion);
        }
    }
    let text = fs.readFileSync(path.join(__dirname, "data/" + vsopFile), 'ascii');
    let lines = text.split(/\r\n|[\n\v\f\r\x85\u2028\u2029]/);

    let description = null;

    let aTs = [];
    let cods = [];

    let ampAs = [];
    let phBs = [];
    let freqCs = [];

    let blocks = [];

    let i = 0;
    while (true) {
        if (i < lines.length) { // not EOF
            if (lines[i].length === 0) break;

            let header = head(lines[i++]);

            if (description === null) description = ["VSOP version ", header.vsopVersion, " * ", header.astroObjectName, " => ", header.description].join();

            if (i + header.termsCount >= lines.length) throw new Error("Block size error.");
            let block = lines.slice(i, i + header.termsCount).map(line => term(line));

            i += header.termsCount;

            if (!block.every((term, n) => term.termIndex === (n + 1) &&
                    term.coordinateIndex === header.coordinateIndex &&
                    term.alphaT === header.alphaT &&
                    term.vsopVersion === header.vsopVersion)) {
                throw new Error("Verification error");
            }
            if (truncate !== null && truncate.truncate) {
                block = block.filter(term => {
                    let threshold = truncate.p[coordUnitIsAU[term.coordinateIndex - 1]][term.alphaT];
                    return Decimal.gte(Decimal.abs(term.amplitudeA), threshold);
                });
            }
            blocks.push({
                alphaTs: header.alphaT,
                coords: header.coordinateIndex, //1開始的坐標分量序號
                terms: block.map(t => ({
                    amplitudeAs: t.amplitudeA,
                    phaseBs: t.phaseB,
                    frequencyCs: t.frequencyC
                }))
            });
        }
    }
    if (blocks.length === 0) {
        throw new Error("No terms for given precision.");
    }
    return {
        description: description,
        blocks: blocks
    };
});
