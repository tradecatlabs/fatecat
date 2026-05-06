import * as Decimal from '../../src/math/decimal';
import * as Angle from '../../src/math/angle.js';
import * as AtomsphereRefraction from '../../src/astronomy/atmospheric-refraction';
import chai from 'chai';

let expect = chai.expect;

const equal=(a,b)=>Decimal.lt(Decimal.abs(Decimal.minus(a,b)),Decimal.EPS);
const equalWithError=(a,b,eps)=>Decimal.lt(Decimal.abs(Decimal.minus(a,b)),eps);

describe("Atomspheric Refraction",()=>{
    it("Bennett formula (improved) : test 90° ",()=>{
        expect(Decimal.lte(Decimal.abs(AtomsphereRefraction.Bennett.R("90°")),Angle.angle("0.9\""))).to.be.equal(true);
    });
    it("Saemundsson formula (with true altitude=23°): It is consistent with Bennett’s formula within 0.1′",()=>{
        let ha=Angle.angle("23°");
        let R1=AtomsphereRefraction.Bennett.R(ha);
        let h=Decimal.minus(ha,R1);
        let R2=AtomsphereRefraction.Saemundsson.R(h);
        let ha1=Decimal.plus(h,R2);
        expect(equalWithError(ha,ha1,Angle.angle("0.1'"))).to.be.equal(true);
    });
    it("Saemundsson formula (with true altitude=56°34'23\".5) : It is consistent with Bennett’s formula within 0.1′",()=>{
        let ha=Angle.angle("56°34'23\".5");
        let R1=AtomsphereRefraction.Bennett.R(ha);
        let h=Decimal.minus(ha,R1);
        let R2=AtomsphereRefraction.Saemundsson.R(h);
        let ha1=Decimal.plus(h,R2);
        expect(equalWithError(ha,ha1,Angle.angle("0.1'"))).to.be.equal(true);
    });
    it("Smart formula (err<1\") compared with Bennett formula (err<0.9\")",()=>{
        expect(equalWithError(AtomsphereRefraction.Bennett.R("45°"),AtomsphereRefraction.Smart.R("45°"),Angle.angle("1.9\""))).to.be.equal(true);
        expect(equalWithError(AtomsphereRefraction.Bennett.R("75°"),AtomsphereRefraction.Smart.R("75°"),Angle.angle("1.9\""))).to.be.equal(true);
        expect(equalWithError(AtomsphereRefraction.Bennett.R("95°"),AtomsphereRefraction.Smart.R("95°"),Angle.angle("1.9\""))).to.be.equal(true);
    });
    it("Meeus formular should be consistent with Smart formula.",()=>{
        let ha=Angle.angle("56°34'23\".5");
        let R1=AtomsphereRefraction.Smart.R(ha);
        let h=Decimal.minus(ha,R1);
        let R2=AtomsphereRefraction.Meeus.R(h);
        let ha1=Decimal.plus(h,R2);
        expect(equalWithError(ha,ha1,Angle.angle("0.2\""))).to.be.equal(true);
    });
});