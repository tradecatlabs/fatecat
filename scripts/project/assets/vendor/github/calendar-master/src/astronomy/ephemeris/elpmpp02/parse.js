import * as fs from 'fs';
import * as path from "path";
import * as Decimal from '../../../math/decimal';
import * as Vector from '../../../math/vector';
import * as Angle from '../../../math/angle';
import * as Expression from '../../../math/expression';
import * as std from '../../../basic';
import * as Common from './common';

const decimal = Decimal.decimal;
const integer = Decimal.decimal;

const expression = Expression.expression;
const evaluate = Expression.evaluate;

// transpose :: [[a]] -> [[a]]
const transpose = xs => xs[0].map((_, iCol) => xs.map((row) => row[iCol]));

const ELPFileCount = 6; //ELP文件數量 對應文件序號 1-6

const ELPCoefficient = (Ci, Fi, alpha) => ({
    Ci: Ci || 0, //constant
    Fi: Fi || [0, 0, 0, 0, 0], //functional
    alpha: alpha || 0 //power
});
const pertTitleLineBegin = "PERTURBATIONS";
// TODO:: a lexer for fortran I/O format
const Offsets = [
    [1, 4, 7, 10, 15, 30, 42, 54, 66, 78, 90], //4i3,2x,f13.5,6f12.2
    [1, 4, 7, 10, 15, 30, 42, 54, 66, 78, 90], //4i3,2x,f13.5,6f12.2
    [5, 25, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81] //5x,2d20.13,13i3
];
const Lens = [
    [3, 3, 3, 3, 13, 10, 10, 10, 10, 10, 10],
    [3, 3, 3, 3, 13, 10, 10, 10, 10, 10, 10],
    [20, 20, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
];
const Types = [
    ['I', 'I', 'I', 'I', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
    ['I', 'I', 'I', 'I', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
    ['F', 'F', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I']
];

const splitFORTRAN = (line, offset, len, type) => {
    if (offset.length !== len.length || len.length !== type.length) throw new Error("Error Fortran format!");
    let items = [];
    for (let i = 0; i < offset.length; i++) {
        let s = line.substr(offset[i], len[i]).replace(/[Dd]/g, "E"); // fortran double to standard scientific notation
        switch (type[i]) {
            case "I":
                items.push(integer(s));
                break;
            case "F":
                items.push(decimal(s));
                break;
            default:
                ;
        }
    }
    return items;
}

const parseSin = (line, Constants) => {
    //讀入 4i3,2x,f13.5,6f12.2
    let items = splitFORTRAN(line, Offsets[0], Lens[0], Types[0]);
    let I = [0].concat(items.slice(0, 4)); //I [1-4]
    let A = items[4]; //A
    let B = [0].concat(items.slice(5, 11)); //B [1-6]
    //生成中間係數
    //C=A+ΔA,其中ΔA=(B1+2ratioSemiMajorAxis*B5/3m)(-mΔν/ν + Δn'/ν)+(B2ΔΓ+B3ΔE+B4Δe')
    let Ci = evaluate(expression("A+(B1+rSMA2drMM3*B5)*(-m*dnu + dnp)+(B2*dG+B3*dE+B4*de)"), {
        A: A,
        B1: B[1],
        B2: B[2],
        B3: B[3],
        B4: B[4],
        B5: B[5],
        rSMA2drMM3: Constants.rSMA2drMM3,
        dnp: Constants.deltaNp,
        dE: Constants.deltaE,
        de: Constants.deltaEp,
        dnu: Constants.deltaNU,
        dG: Constants.deltaGamma,
        m: Constants.ratioMeanMotion
    });
    //F組
    let D = transpose(Constants.Delaunay); // transpose, Delaunay[i][a]==>D[a][i]
    let Fi = D.map(d => Vector.dot(I, d)); //F=i1D+i2F+i3l+i4l' 階數a=0-4
    return ELPCoefficient(Ci, Fi); //將結果添加進返回數組
}

const parseCos = (line, Constants) => {
    //讀入 4i3,2x,f13.5,6f12.2
    let items = splitFORTRAN(line, Offsets[1], Lens[1], Types[1]);
    let I = [0].concat(items.slice(0, 4)); //I [1-4]
    let A = items[4]; //A
    let B = [0].concat(items.slice(5, 11)); //B [1-6]
    //距離項 先做Δν修正 A=A-2*A*Δν/3
    A = evaluate(expression("A- 2.0 * A * deltaNU / 3.0"), {
        A: A,
        deltaNU: Constants.deltaNU
    });
    //C=A+ΔA,其中ΔA=(B1+2ratioSemiMajorAxis*B5/3m)(-mΔν/ν + Δn'/ν)+(B2ΔΓ+B3ΔE+B4Δe')
    let Ci = evaluate(expression("A+(B1+rSMA2drMM3*B5)*(-m*dnu + dnp)+(B2*dG+B3*dE+B4*de)"), {
        A: A,
        B1: B[1],
        B2: B[2],
        B3: B[3],
        B4: B[4],
        B5: B[5],
        rSMA2drMM3: Constants.rSMA2drMM3,
        dnp: Constants.deltaNp,
        dE: Constants.deltaE,
        de: Constants.deltaEp,
        dnu: Constants.deltaNU,
        dG: Constants.deltaGamma,
        m: Constants.ratioMeanMotion
    });
    //F組
    let D = transpose(Constants.Delaunay); // transpose, Delaunay[i][a]==>D[a][i]
    let Fi = D.map(d => Vector.dot(I, d)); //F=i1D+i2F+i3l+i4l' 階數a=0-4
    //CosF->Sin(F+π/2) 以後計算函數中統一用Sin
    Fi[0] = Decimal.plus(Fi[0], Angle.HalfPi);
    return ELPCoefficient(Ci, Fi); //將結果添加進返回數組
}

const parsePert = (line, Constants, alpha) => {
    //讀入 5x,2d20.13,13i3
    let items = splitFORTRAN(line, Offsets[2], Lens[2], Types[2]);
    let S = items[0]; //Sin coefficient
    let C = items[1]; //Cos coefficient
    let I = [0].concat(items.slice(2, 15)); //I [1-13]

    //C 處理為 √S²+C²
    let Ci = Decimal.sqrt(Decimal.plus(Decimal.sqr(S), Decimal.sqr(C)));

    //F組
    let Fi = [Angle.toZeroDoublePi(Decimal.atan2(C, S)), 0, 0, 0, 0]; //0階項初值置為Atan(C,S) 高階項初值為0
    //φ=i1D+i2F+i3l+i4l'+i5Me+i6V+i7T+i8Ma+i9J+i10S+i11U+i12N+i13ζ 階數0-4
    let D = transpose(Constants.Delaunay); // transpose, Delaunay[i][a]==>D[a][i]
    let P = transpose(Constants.Planetary);
    //i1D+i2F+i3l+i4l'
    //i5Me+i6V+i7T+i8Ma+i9J+i10S+i11U+i12N
    //i13ζ
    Fi = Fi.map((fi, a) => Decimal.plus(fi, Vector.dot(I.slice(1, 14), D[a].slice(1, 5).concat(P[a].slice(1, 9)).concat([Constants.longitudeLunarZeta[a]]))));

    return ELPCoefficient(Ci, Fi, alpha);
}

export const parse = std.memoize((elpFileID, elpFileName, correction) => {
    const Constants = Common.constant(correction);

    let patternID = -1;
    //判斷文件記錄格式類型
    if (elpFileID > 0 && elpFileID <= ELPFileCount) {
        if (elpFileID <= 3) { //ELP_MAIN
            patternID = (elpFileID == 3 ? 1 : 0); //ELP_MAIN.S3取值1 ELP_MAIN.S1和ELP_MAIN.S2取值0
        } else { //ELP_PERT
            patternID = 2; //ELP_PERT取值2
        }
    } else {
        throw new Error("Invalid ELP file ID!");
    }

    let result = [];
    //開始讀文件
    let text = fs.readFileSync(path.join(__dirname, "data/" + elpFileName), 'ascii');
    let lines = text.split(/\r\n|[\n\v\f\r\x85\u2028\u2029]/);

    let ptr = 0; // line number
    ptr++; //開頭一行是文件註釋

    let alphaT = 0; //T的階 用於ELP_PERT
    while (ptr < lines.length) { // EOF
        let line = lines[ptr++]; //讀入第一行數據
        if (line.replace(/\s+/g, '') === "") continue;
        switch (patternID) { //按記錄格式類型進行對應解析
            case 0: //ELP_MAIN.S1~2 Sin序列
                result.push(parseSin(line, Constants));
                break;
            case 1: //ELP_MAIN.S3 Cos序列
                result.push(parseCos(line, Constants));
                break;
            case 2: //ELP_PERT 中間係數作了轉換
                if (line.indexOf(pertTitleLineBegin) < 0) { //如果該行不是標題
                    result.push(parsePert(line, Constants, alphaT));
                } else {
                    alphaT++; //如果該行不是數據而是標題 則遞增alphaT
                }
                break;
            default:
                throw new Error("Access Impossible Position!");
        }
    }
    return result;
});
