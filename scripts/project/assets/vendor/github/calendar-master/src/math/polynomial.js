import * as std from '../basic.js';
import * as Decimal from './decimal';
import * as Vector from './vector.js';
const decimal = Decimal.decimal;
const vector = Vector.vector;

// Polynomial =[Decimal]
export const polynomial = vector;

export const value = std.uncurry(p => x => {
  p = polynomial( p ),
  x = decimal( x );
  return p.reduceRight( ( sum, a ) => Decimal.plus( Decimal.mult( sum, x ), a ), 0 );
});

export const valueOfLimitedItems = std.uncurry(p => x => truncation => {
  p = polynomial( p ),
  x = decimal( x ),
  truncation = std.nat32( truncation );
  return value( p.slice( 0, truncation ), x );
});

export const derivative = p => polynomial( p ).map(( x, i ) => Decimal.mult( x, i )).slice( 1 );

export const show = p => polynomial( p ).map(( x, i ) => ( i === 0 || Decimal.isNeg( x ) ? " " : " +" ) + Decimal.show( x ) + ( i ? "x^" + i : "" )).join( "" );
