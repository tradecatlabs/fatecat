import * as Decimal from '../../src/math/decimal';
import * as Angle from '../../src/math/angle.js';
import chai from 'chai';

let expect = chai.expect;

describe("readable string of angle in degree/arcminute/arcsecond", () => {
    it("Obvisouly, degree/arcminute/arcsecond symbol must occur at most once.", () => {
        expect(() => { Angle.angle("+18°20'34.5\"") }).to.not.throw(Error);
        expect(() => { Angle.angle("-18°20'34\".5") }).to.not.throw(Error);
        expect(() => { Angle.angle("18°18°20'34.5\"") }).to.throw(Error);
        expect(() => { Angle.angle("18°20'20'34\".5") }).to.throw(Error);
        expect(() => { Angle.angle("18°20'34\"34\".5") }).to.throw(Error);
    });
    it("If it only contains one of degree/arcminute/arcsecond, it can be any real number.", () => {
        expect(() => { Angle.angle("1.8e-2°") }).to.not.throw(Error);
        expect(() => { Angle.angle("-1.8e-2'") }).to.not.throw(Error);
        expect(() => { Angle.angle("+1.8e-2\"") }).to.not.throw(Error);
    });
    it("If it contains both degree and arcminute (or both arcminute and arcsecond), the degree part must be integer and the arcminute part must less than 60.", () => {
        expect(() => { Angle.angle("18°20.5'") }).to.not.throw(Error);
        expect(() => { Angle.angle("1.8e3°20.5'") }).to.not.throw(Error);
        expect(() => { Angle.angle("18.5°20.5'") }).to.throw(Error);
        expect(() => { Angle.angle("18°60'") }).to.throw(Error);
        expect(() => { Angle.angle("18'20.5\"") }).to.not.throw(Error);
        expect(() => { Angle.angle("18.5'20.5\"") }).to.throw(Error);
        expect(() => { Angle.angle("18'60\"") }).to.throw(Error);
    });
    it("If it contains all three degree, arcminute and arcsecond, the degree and arcminute parts must be integers and the arcminute and arcsecond parts must less than 60.", () => {
        expect(() => { Angle.angle("+18°60.5'34\".5") }).to.throw(Error);
        expect(() => { Angle.angle("-18°20.5'34\".5") }).to.throw(Error);
        expect(() => { Angle.angle("+18°20'60\"") }).to.throw(Error);
        expect(() => { Angle.angle("-18.5°20'34\".5") }).to.throw(Error);
        expect(() => { Angle.angle("18°20'34\".5") }).to.not.throw(Error);
    });
});

const equal=(a,b)=>Decimal.lt(Decimal.abs(Decimal.minus(a,b)),Decimal.EPS);
describe("radian and degree/arcminute/arcsecond", () => {
    it("convert", () => {
        expect(equal(Angle.deg2rad(360),Angle.DoublePi)).to.be.equal(true);
        expect(equal(Angle.min2rad(90*60),Angle.HalfPi)).to.be.equal(true);
        expect(equal(Angle.sec2rad(180*60*60),Angle.PI)).to.be.equal(true);
    });
    it("parse",()=>{
        expect(equal(Angle.angle("+45°"),Decimal.div(Angle.PI,4))).to.be.equal(true);
    });
});