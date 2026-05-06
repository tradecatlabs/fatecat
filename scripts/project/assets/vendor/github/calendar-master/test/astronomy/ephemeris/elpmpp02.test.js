import * as ELPMPP02 from '../../../src/astronomy/ephemeris/elpmpp02';
import * as Angle from '../../../src/math/angle';
import * as Decimal from '../../../src/math/decimal';

console.time("load elpmpp02");
const elpmpp02 = ELPMPP02.ELPMPP02("LLR");
console.timeEnd("load elpmpp02");

console.time("elpmpp02");
let jd = 2444239.5;
console.log("JD " + jd);
const pv = ELPMPP02.position_velocity(elpmpp02, jd);
console.log("X = " + Decimal.show(pv[0]) + ", Y = " + Decimal.show(pv[1]) + ", Z = " + Decimal.show(pv[2]) + " km");
console.log("X'= " + Decimal.show(pv[3]) + ", Y'= " + Decimal.show(pv[4]) + ", Z'= " + Decimal.show(pv[5]) + " km/day");
console.timeEnd("elpmpp02");
