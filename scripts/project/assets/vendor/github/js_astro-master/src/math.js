/*
 * 定数定義／数学関数スクリプト version 0.001j at 2017/04/27
 * Copyright (c) 1999-2001, 2017 Yoshihiro Sakai & Sakai Institute of Astrology
 * This software is released under the MIT License.
 * http://opensource.org/licenses/mit-license.php
 */

// $PI = 3.141592653589793;
deg2rad = Math.PI / 180.0;

function sin4deg( X ){
	return Math.sin( X * deg2rad );
}

function cos4deg( X ){
	return Math.cos( X * deg2rad );
}

function tan4deg( X ){
	return Math.tan( X * deg2rad );
}

function asin4deg( X ){
	return Math.asin( X ) / deg2rad;
}

function acos4deg( X ){
	return Math.acos( X ) / deg2rad;
}

function atan4deg( X ){
	return Math.atan( X ) / deg2rad;
}

function atan24deg( X, Y ){
	return Math.atan2( X, Y ) / deg2rad;
}

function sgn( X ){
	return Math.sign( X );
}

function fmod( X, t ){
	var res = 0.0;
	res = X - Math.floor( X / t ) * t;
	if( res < 0.0 ){
		res += t;
	}
	return res;
}

function mod360( X ){
	return X - Math.floor( X / 360.0 ) * 360.0;
}

function floor( X ){
	return Math.floor( X );
}

function ceil( X ){
	return Math.ceil( X );
}

// x in [-1, +1]
function calChebyshevPolynomial(x, coefs) {
	const t = Math.acos(x);

	let y = 0;
	for(let i = 0; i < coefs.length; i++) {
		y += coefs[ i ] * Math.cos(i * t);
	}

	return y;
}
