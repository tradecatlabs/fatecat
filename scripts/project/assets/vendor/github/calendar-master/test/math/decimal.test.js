import * as Decimal from '../../src/math/decimal';
import * as Angle from '../../src/math/angle.js';
import chai from 'chai';

let expect = chai.expect;

const equal = (a, b) => Decimal.lt(Decimal.abs(Decimal.minus(a, b)), Decimal.EPS);

describe("Decimal functions", () => {
    it("abs", () => {
        expect(Decimal.eq(Decimal.abs("-123.34"), Decimal.decimal("123.34"))).to.be.equal(true);
    });
    it("tan", () => {
        expect(equal(Decimal.tan(0), 0)).to.be.equal(true);
        expect(equal(Decimal.tan(Angle.angle("45°")), 1)).to.be.equal(true);
        expect(equal(Decimal.tan(Angle.angle("60°")), Decimal.sqrt(3))).to.be.equal(true);
    });
});
