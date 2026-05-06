import * as std from '../basic.js';
import * as Decimal from './decimal';
const decimal = Decimal.decimal;

export const PI = Decimal.PI;
export const DoublePi = Decimal.plus(PI, PI);
export const HalfPi = Decimal.mult(PI, 0.5);

export const DegreePerRadian = Decimal.div(180, PI);
export const MinutePerRadian = Decimal.mult(DegreePerRadian, 60);
export const SecondPerRadian = Decimal.mult(MinutePerRadian, 60);

export const deg2rad= d=> Decimal.div(decimal(d),DegreePerRadian);
export const deg2min= d=> Decimal.mult(decimal(d),60); 
export const deg2sec= d=> Decimal.mult(decimal(d),60*60);
export const min2rad= m=> Decimal.div(decimal(m),MinutePerRadian);
export const min2deg= m=> Decimal.div(decimal(m),60);
export const min2sec= m=> Decimal.mult(decimal(m),60);
export const sec2rad= s=> Decimal.div(decimal(s),SecondPerRadian);
export const sec2deg= s=> Decimal.div(decimal(s),60*60); 
export const sec2min= s=> Decimal.div(decimal(s),60);
export const rad2deg= r=> Decimal.mult(decimal(r),DegreePerRadian);
export const rad2min= r=> Decimal.mult(decimal(r),MinutePerRadian); 
export const rad2sec= r=> Decimal.mult(decimal(r),SecondPerRadian);

// Char -> Boolean
const isHA = x => x === 'h' || x === 'h' || x === 's';
const isH = x => x === 'h' || x === '°' || x === '\u00b0';
const isM = x => x === 'm' || x === '\'' || x === '\u2032';
const isS = x => x === 's' || x === '"' || x === '\u2033';

// data dhms = {dh:: Decimal, m:: Decimal, s::Decimal}
// dh-- degree/ hour, m--minitue, s: second
const DHMS = (dh, m, s) => {
    if(dh===null){
        if(m===null){
            if(s===null){
                throw new Error("Impossible place!");
            }else{
                return { dh: decimal(0), m: decimal(0), s: decimal(s) };
            }
        }else{
            if(s===null){
                return { dh: decimal(0), m: decimal(m), s: decimal(0) };
            }else{
                m=decimal(m);
                s=decimal(s);
                if(Decimal.isInteger(m) && Decimal.gte(s,0) && Decimal.lt(s,60)){
                    return { dh: decimal(0), m: decimal(m), s: decimal(s) };
                }
            }
        }
    }else{
        if(m===null){
            if(s===null){
                return { dh: decimal(dh), m: decimal(0), s: decimal(0) };
            }else{
                throw new Error("Impossible place!");
            }
        }else{
            if(s===null){
                dh=decimal(dh);
                m=decimal(m);
                if(Decimal.isInteger(dh) && Decimal.gte(m,0) && Decimal.lt(m,60)){
                    return { dh: decimal(dh), m: decimal(m), s: decimal(0) };
                }
            }else{
                dh=decimal(dh);
                m=decimal(m);
                s=decimal(s);
                if(Decimal.isInteger(dh) && Decimal.gte(m,0) && Decimal.lt(m,60)&& Decimal.gte(s,0) && Decimal.lt(s,60)){
                    return { dh: decimal(dh), m: decimal(m), s: decimal(s) };
                }
            }
        }
    }
    throw new Error("Illegal Angle!");
};
// data matched = {neg:: Boolean, dhms:: dhms, dh:: Boolean}
// neg: is negative, dhms: see dhms definition, dh:
const matched = (neg, dhms, ha) => ({ neg: neg, dhms: dhms, ha: ha });
const matcher = (re, parser) => ({ regexp: re, parser: parser });
// const data
const matchers = [
    matcher(new RegExp(/^([+-]?)(([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?)([hms°'"\u00b0\u2032\u2033])$/, "iu"), g => matched(g[1] !== '-', DHMS(isH(g[5]) ? g[2] : null, isM(g[5]) ? g[2] : null, isS(g[5]) ? g[2] : null), isHA(g[5]))),
    matcher(new RegExp(/^([+-]?)([0-9]+)([hms°'"\u00b0\u2032\u2033])(\.[0-9]+)$/, "iu"), g => matched(g[1] !== '-', DHMS(isH(g[3]) ? g[2] + g[4] : null, isM(g[3]) ? g[2] + g[4] : null, isS(g[3]) ? g[2] + g[4] : null), isHA(g[3]))),
    matcher(new RegExp(/^([+-]?)(([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?)([h°\u00b0])([0-5]?[0-9](\.[0-9]+)?)([m'\u2032])$/, "iu"), g => matched(g[1] !== '-', DHMS(g[2], g[6], null), isHA(g[5]))),
    matcher(new RegExp(/^([+-]?)(([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?)([h°\u00b0])([0-5]?[0-9])([m'\u2032])(\.[0-9]+)?$/, "iu"), g => matched(g[1] !== '-', DHMS(g[2], g[6] + g[8], null), isHA(g[5]))),
    matcher(new RegExp(/^([+-]?)(([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?)([m'\u2032])([0-5]?[0-9](\.[0-9]+)?)([s"\u2033])$/, "iu"), g => matched(g[1] !== '-', DHMS(null, g[2], g[6]), isHA(g[5]))),
    matcher(new RegExp(/^([+-]?)(([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?)([m'\u2032])([0-5]?[0-9])([s"\u2033])(\.[0-9]+)?$/, "iu"), g => matched(g[1] !== '-', DHMS(null, g[2], g[6] + g[8]), isHA(g[5]))),
    matcher(new RegExp(/^([+-]?)(([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?)([h°\u00b0])([0-5]?[0-9])([m'\u2032])([0-5]?[0-9](\.[0-9]+)?)[s"\u2033]$/, "iu"), g => matched(g[1] !== '-', DHMS(g[2], g[6], g[8]), isHA(g[5]))),
    matcher(new RegExp(/^([+-]?)(([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?)([h°\u00b0])([0-5]?[0-9])([m'\u2032])([0-5]?[0-9])[s"\u2033](\.[0-9]+)?$/, "iu"), g => matched(g[1] !== '-', DHMS(g[2], g[6], g[8] + g[9]), isHA(g[5])))
];
// String -> matched
const match = s => {
    for (let m of matchers) {
        let groups = m.regexp.exec(s);
        if (groups) {
            return m.parser(groups);
        }
    }
    throw new Error("Parse Error!");
}
// Decimal->Decimal
const arcsec = std.uncurry(a => ha => ha ? Decimal.mult(a, 15) : a);
const dhms2sec = dhms => Decimal.plus(Decimal.plus(Decimal.mult(dhms.dh, 3600), Decimal.mult(dhms.m, 60)), dhms.s);
const sign = std.uncurry(a => sgn => sgn ? a : Decimal.neg(a));
const mathced2rad = m => sign(sec2rad(arcsec(dhms2sec(m.dhms), m.ha)), m.neg);
// String -> Angle
export const parse = s => angle(mathced2rad(match(s.replace(/\s+/g, ''))));
// Angle = Decimal | String
export const angle = x => typeof x === "string" ? parse(x) : decimal(x);
// dms | HMS,  case sensitive
const sym = fmt => /^H?M?S?$/.test(fmt) ? "hms" : "\u00b0\u2032\u2033";
// String -> Boolean
const isHMS = fmt => /^H?M?S?$/.test(format);

// Decimal -> Boolean -> [Decimal]
const rad2hdms = std.uncurry(rad => isHMS => {
    let res = [];
    res[0] = Decimal.div(Decimal.mult(rad, isHMS ? 12 : 180), PI); // hour, degree
    res[1] = Decimal.mult(res[0], 60); // m
    res[2] = Decimal.mult(res[1], 60); // s
    return res;
});

// [Decimal] -> [Decimal]
const carry_out = arr => {
    for (let i = arr.length; i-- > 1;) {
        if (Decimal.gte(arr[i], 60)) {
            arr[i - 1] = Decimal.plus(arr[i - 1], 1);
            arr[i] = Decimal.minus(arr[i], 60);
        } else {
            break;
        }
    }
    return arr;
}

// Decimal->String->Number->String
const rad2str = std.uncurry(radian => format => fixed => {
    if (false == /^(H?M?S?)|(d?m?s?)$/.test(format))
        throw new Error("Illegal format!");
    let symbol = sym(format);
    let sign = "+";
    if (Decimal.isNeg(radian))
        sign = "-",
        radian = Decimal.neg(radian);
    let parts = rad2hdms(radian)(/^H?M?S?$/.test(format));
    if (format === "H" || format === "d")
        return sign + Decimal.toFixed(parts[0], fixed) + symbol[0];
    else if (format === "M" || format === "m")
        return sign + Decimal.toFixed(parts[1], fixed) + symbol[1];
    else if (format === "S" || format === "s")
        return sign + Decimal.toFixed(parts[2], fixed) + symbol[2];
    else if (format === "HM" || format === "dm") {
        let hm = carry_out([
            Decimal.floor(parts[0]),
            Decimal.toDecimalPosition(Decimal.mod(parts[1], 60), fixed)
        ]);
        return sign + Decimal.toFixed(hm[0], 0) + symbol[0] + Decimal.toFixed(hm[1], fixed) + symbol[1];
    } else if (format === "MS" || format === "ms") {
        let ms = carry_out([
            Decimal.floor(parts[1]),
            Decimal.toDecimalPosition(Decimal.mod(parts[2], 60), fixed)
        ]);
        return sign + Decimal.toFixed(ms[0], 0) + symbol[1] + Decimal.toFixed(ms[1], fixed) + symbol[2];
    } else if (format === "HMS" || format === "dms") {
        let hms = carry_out([
            Decimal.floor(parts[0]),
            Decimal.floor(Decimal.mod(parts[1], 60)),
            Decimal.toDecimalPosition(Decimal.mod(parts[2], 60), fixed)
        ]);
        return sign + Decimal.toFixed(hms[0], 0) + symbol[0] + Decimal.toFixed(hms[1], 0) + symbol[1] + Decimal.toFixed(hms[2], fixed) + symbol[2];
    } else
        throw new Error("Illegal format!");
});
// Angle -> Angle -> Angle
export const plus = std.uncurry(a => b => angle(Decimal.plus(angle(a), angle(b))));
export const minus = std.uncurry(a => b => angle(Decimal.minus(angle(a), angle(b))));
// Angle -> Decimal -> Angle
export const mult = std.uncurry(a => b => angle(Decimal.mult(angle(a), decimal(b))));
export const div = std.uncurry(a => b => angle(Decimal.div(angle(a), decimal(b))));
// Angle -> Angle
export const toZeroDoublePi = a => {
    a = Decimal.mod(angle(a), DoublePi);
    if (Decimal.isNeg(a))
        return angle(Decimal.plus(a, DoublePi));
    return angle(a);
};
export const toPlusMinusPi = a => {
    a = Decimal.mod(angle(a), DoublePi);
    if (Decimal.lte(a, Decimal.neg(PI)))
        return angle(Decimal.plus(a, DoublePi));
    if (Decimal.gt(a, PI))
        return angle(Decimal.minus(a, DoublePi));
    return angle(a);
};
export const neg = a => angle(Decimal.neg(angle(a)));
// Angle-> String-> Number -> String
export const format = std.uncurry(a => fmt => dp => rad2str(a, fmt, dp));
// String -> Angle
export const show = a => rad2str(a, "dms", 2);

// Angle->Angle->Boolean
export const eq = std.uncurry(a => b => Decimal.eq(toZeroDoublePi(a), toZeroDoublePi(b)));
export const lt = std.uncurry(a => b => Decimal.lt(toZeroDoublePi(a), toZeroDoublePi(b)));
export const gt = std.uncurry(a => b => Decimal.gt(toZeroDoublePi(a), toZeroDoublePi(b)));
export const lte = std.uncurry(a => b => Decimal.lte(toZeroDoublePi(a), toZeroDoublePi(b)));
export const gte = std.uncurry(a => b => Decimal.gte(toZeroDoublePi(a), toZeroDoublePi(b)));
export const neq = std.uncurry(a => b => Decimal.neq(toZeroDoublePi(a), toZeroDoublePi(b)));