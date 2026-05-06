// Quaternion in R4
// -- combine a real number with a 3d-vector
import * as std from '../basic.js';
import * as Decimal from './decimal';
import * as Vector from './vector.js';
const decimal = Decimal.decimal;
const vector = Vector.vector;

// Quaternion = {scalar: Decimal, vector:Vector3}
export const quaternion = ( ...args ) => {
  if ( args.length === 1 ) { // contract
    let q = std.obj(args[0]);
    if (q.hasOwnProperty( "scalar" ) && q.hasOwnProperty( "vector" )) {
      return {
        scalar: decimal( q.scalar ),
        vector: vector( q.vector )
      }; // construct
    }
  } else if ( args.length === 2 ) {
    let s = decimal(args[0]),
      v = vector(args[1]);
    if ( Vector.dimension( v ) !== 3 )
      throw new TypeError( "Except a 3d vector!" );
    return { scalar: s, vector: v }; // construct
  }
  throw new TypeError( "Except a quaternion!" );
};
// Quaternion -> Quaternion
export const conjugate = a => {
  a = quaternion( a );
  return quaternion(a.scalar, Vector.neg( a.vector ));
}
// Quaternion->Quaternion->Quaternion
export const plus = std.uncurry(a => b => {
  a = quaternion( a ),
  b = quaternion( b );
  return quaternion(Decimal.plus( a.scalar, b.scalar ), Vector.plus( a.vector, b.vector ));
});
// Quaternion->Decimal->Quaternion
export const mult = std.uncurry(a => b => {
  a = quaternion( a ),
  b = decimal( b );
  return quaternion(Decimal.mult( a.scalar, b ), Vector.mult( a.vector, b ));
});
// Quaternion->Quaternion->Quaternion
export const minus = std.uncurry(a => b => plus(a, mult( b, -1 )));
// Quaternion->Decimal->Quaternion
export const div = std.uncurry(a => b => mult(a, Decimal.div( 1, b )));

// Hamilton product, or Grossman product
// -- Grossman product(p,q) denoted by pq
// p=a+u, q=t+v ==>pq= at-u.v + (av+tu+uxv)
export const grossman = std.uncurry(p => q => {
  p = quaternion( p ),
  q = quaternion( q );
  return quaternion(Decimal.minus(Decimal.mult( p.scalar, q.scalar ), Vector.dot( p.vector, q.vector )), Vector.plus(Vector.plus(Vector.mult( q.vector, p.scalar ), Vector.mult( p.vector, q.scalar )), Vector.cross( p.vector, q.vector )));
});
// Grossman even/inner product, or symmetric product
// -- Grossman even product(p,q)=(pq+qp)/2
export const even = std.uncurry(p => q => div( plus(grossman( p, q ), grossman( q, p )), 2 ));
/*
export const even= std.uncurry(p=> q=> {
  p=quaternion(p), q=quaternion(q);
  return quaternion(
    Decimal.minus(Decimal.mult(p.scalar, q.scalar), Vector.dot(p.vector, q.vector)),
    Vector.plus(Vector.mult(q.vector, p.scalar), Vector.mult(p.vector, q.scalar))
  );
});
*/

// the antisymmetric part of Grossman product, or Grossman outer pruduct
// -- Grossman odd product(p,q)=(pq-qp)/2
export const odd = std.uncurry(p => q => div( minus(grossman( p, q ), grossman( q, p )), 2 ));
/*
export const odd = std.uncurry(p=> q=> {
  p=quaternion(p), q=quaternion(q);
  return quaternion(0,Vector.cross(p.vector, q.vector));
});
*/

// Euclidean product
// -- Euclidean product(p,q)=p'q,  where p' denotes the conjugate of p
export const euclidean = std.uncurry(p => q => grossman( conjugate( p ), q ));
// Euclidean even/inner product
// -- Euclidean even product(p,q)=(p'q+q'p)/2
// Quaternion->Quaternion->Decimal
export const dot = std.uncurry( p => q => div( plus(grossman( conjugate( p ), q ), grossman( conjugate( q ), p )), 2 ).scalar );
/*
export const dot = std.uncurry(p=> q=> {
  p=quaternion(p), q=quaternion(q);
  return decimal(Decimal.plus(Decimal.mult(p.scalar, q.scalar), Vector.dot(p.vector, q.vector)));
});
*/
// Euclidean odd/outer product
// -- Euclidean odd product(p,q)=(p'q-q'p)/2
// Quaternion->Quaternion->Vector
export const cross = std.uncurry( p => q => div( minus(grossman( conjugate( p ), q ), grossman( conjugate( q ), p )), 2 ).vector );
/*
export const cross = std.uncurry(p=> q=> {
  p=quaternion(p), q=quaternion(q);
  return Vector.minus(Vector.minus(Vector.mult(q.vector, p.scalar), Vector.mult(p.vector, q.scalar)), Vector.cross(p.vector, q.vector));
};
*/

// |q|=sqrt(qq'), notice that qq' only has a scalar part
export const norm = q => Decimal.sqrt( grossman(q, conjugate( q )).scalar );
/*
export const norm = q=>{
  q=quaternion(q);
  return Decimal.sqrt(Decimal.plus(Decimal.mult(q.scalar,q.scalar), Vector.dot(q.vector,q.vector)));
}
*/
export const normalize = q => div(q, norm( q ));
export const inverse = q => {
  let n = norm( q );
  if (Decimal.isZero( n ))
    throw new Error( "No inverse of ZERO quaternion!" );
  return div(conjugate( q ), Decimal.sqr( n ));
}
export const eq = std.uncurry(p => q => {
  p = quaternion( p ),
  q = quaternion( q );
  return Decimal.eq( p.scalar, q.scalar ) && Vector.eq( p.vector, q.vector );
});
export const neq = std.uncurry(p => q => !eq( p, q ));

export const show = q => {
  q = quaternion( q );
  return Decimal.show( q.scalar ) + " " + q.vector.map(( x, i ) => ( !Decimal.isNeg( x ) ? "+" : "" ) + Decimal.show( x ) + [ "i", "j", "k" ][i ]).join( " " );
}
