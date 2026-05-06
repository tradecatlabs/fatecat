///////////////////////////////////////////////////////////
// DualQuaternion, combine dual number with quaternion
// -- p + eq, where p,q is Quaternion and e*e=0
import * as std from '../basic.js';
import * as Decimal from './decimal';
import * as DualNumber from './dual-number.js';
import * as Quaternion from './quaternion.js';
const decimal = Decimal.decimal;
const dualnumber = DualNumber.dualnumber;
const quaternion = Quaternion.quaternion;

export const dualquaternion = ( ...args ) => {
  if ( args.length === 1 ) {
    let q = std.obj(args[0]);
    if (q.hasOwnProperty( "real" ) && q.hasOwnProperty( "dual" )) {
      return {
        real: quaternion( q.real ),
        dual: quaternion( q.dual )
      }; // construct
    }
  } else if ( args.length === 2 ) {
    let r = quaternion(args[0]),
      d = quaternion(args[1]);
    return { real: r, dual: d };
  }
  throw new TypeError( "Except a DualQuaternion!" );
}
export const plus = std.uncurry(p => q => {
  p = dualquaternion( p ),
  q = dualquaternion( q );
  return dualquaternion(Quaternion.plus( p.real, q.real ), Quaternion.plus( p.dual, q.dual ));
});
// (A+eB)(C+eD)=AC+e(AD+BC)
export const mult = std.uncurry(p => q => {
  p = dualquaternion( p ),
  q = dualquaternion( q );
  return dualquaternion(Quaternion.grossman( p.real, q.real ), Quaternion.plus(Quaternion.grossman( p.real, q.dual ), Quaternion.grossman( p.dual, q.real )));
});
export const scale = std.uncurry(q => r => {
  q = dualquaternion( q ),
  r = decimal( r );
  return dualquaternion(Quaternion.mult( q.real, r ), Quaternion.mult( q.dual, r ));
});
export const dot = std.uncurry(p => q => {
  p = dualquaternion( p ),
  q = dualquaternion( q );
  return Quaternion.dot( p.real, q.real );
});
export const conjugate1 = q => {
  q = dualquaternion( q );
  return dualquaternion(q.real, Quaternion.mult( q.dual, -1 ));
}
export const conjugate2 = q => {
  q = dualquaternion( q );
  return dualquaternion(Quaternion.conjugate( q.real ), Quaternion.conjugate( q.dual ));
}
export const conjugate3 = q => {
  q = dualquaternion( q );
  return dualquaternion(Quaternion.conjugate( q.real ), Quaternion.mult( Quaternion.conjugate( q.dual ), -1 ));
}
export const conjugate = conjugate2;
/* norm(Q)
 * = sqrt(QQ*)
 * = sqrt(q1q1*+e(q1q2*+q2q1*))
 * = sqrt(q1q1*)+e[(q1q2*+q2q1*)/2]/sqrt(q1q1*)
 * = norm(q1)+e(q1.q2/norm(q1))
 */
export const norm = q => {
  q = dualquaternion( q );
  let real_norm = Quaternion.norm( q.real );
  return dualnumber(real_norm, Quaternion.div( Quaternion.dot( q.real, q.dual ), real_norm ));
}
/* Q/norm(Q)
 * = (q1+eq2)/[norm(q1)+e(q1.q2/norm(q1))]
 * = (q1+eq2)[norm(q1)-e(q1.q2/norm(q1))]/norm(q1)^2
 * = {q1norm(q1)+e[q2norm(q1)-q1(q1.q2/norm(q1))]}/norm(q1)^2
 * = q1/norm(q1)+e[q2/norm(q1)-q1(q1.q2/norm(q1)^3)]
 */
export const normalize = q => {
  q = dualquaternion( q );
  let inv = Decimal.div(1.0, Quaternion.norm( q.real ));
  return dualquaternion(Quaternion.mult( q.real, inv ), Quaternion.minus(Quaternion.mult( q.dual, inv ), Quaternion.mult(q.real, Decimal.mult(Decimal.cube( inv ), Quaternion.dot( q.real, q.dual )))));
}

export const eq = std.uncurry(a => b => {
  a = dualquaternion( a ),
  b = dualquaternion( b );
  return Quaternion.eq( a.real, b.real ) && Quaternion.eq( a.dual, b.dual );
});
export const neq = std.uncurry(a => b => !eq( a, b ));

export const show = a => {
  a = dualquaternion( a );
  return Quaternion.show( a.real ) + " + ε(" + Quaternion.show( a.dual ) + ")";
}
