import * as VSOP87 from '../../../src/astronomy/ephemeris/vsop87';
import * as Angle from '../../../src/math/angle';
import * as Decimal from '../../../src/math/decimal';

const vsop = VSOP87.earth_heliocentric_spherical_J2000(Angle.angle("0.1s"), 3);
//const vsop = VSOP87.earth_heliocentric_spherical_J2000(Decimal.decimal("0.000004848"), 3);
//const vsop=VSOP87.earth_heliocentric_spherical_J2000();

console.time("vsop");

for (let jd = 2457755; jd < 2457855; jd++) {
    console.log("jd : " + jd);
    const p = VSOP87.position(vsop, jd);
    console.log("Longitude : " + Decimal.show(p[0]) + " rad");
    console.log("Latitude  : " + Decimal.show(p[1]) + " rad");
    console.log("Radius    : " + Decimal.show(p[2]) + " au");

    const v = VSOP87.velocity(vsop, jd);
    console.log("vitesse : " + Decimal.show(v[0]) + " rad/d");
    console.log("vitesse : " + Decimal.show(v[1]) + " rad/d");
    console.log("vitesse : " + Decimal.show(v[2]) + " au/d");
}

console.timeEnd("vsop");