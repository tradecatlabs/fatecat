/*
 * 天文計算関係スクリプト version 0.22j
 * Copyright (c) 1999-2001, 2004, 2005, 2017, 2021, 2024, 2025 Yoshihiro Sakai & Sakai Institute of Astrology
 * This software is released under the MIT License.
 * http://opensource.org/licenses/mit-license.php
 * 2017/06/05[0.16j] 軌道要素６パラ版に対応
 * 2017/09/15[0.17j] ΔＴの計算式を見直すついでに出典を書く
 * 2021/02/27[0.18j] 二体問題まわりロジック見直し
 * 2024/12/20[0.19j] ΔＴ計算式見直し
 * 2025/04/14[0.20j] 均時差計算式見直し
 * 2025/04/16[0.21j] 地方恒星時・黄道傾斜角計算式見直し
 * 2025/08/18[0.22j] 章動・黄道傾斜角計算ロジック見直し
 */

// グレゴリオ暦専用！
function cnvCalendar( JD ){
	JD += 0.5;
	var Z = Math.floor( JD );
	var F = JD - Z;

	var A = 0;
	if(Z >= 2299161){
		var alpha = Math.floor((Z - 1867216.25) / 36524.25);
		A = Z + 1 + alpha - Math.floor(alpha / 4);
	} else {
		A = Z;
	}

	var B = A + 1524;
	var C = Math.floor((B - 122.1) / 365.25);
	var D = Math.floor(365.25 * C);
	var E = Math.floor((B - D) / 30.6001);

	var da = B - D - Math.floor(30.6001 * E);
	var mo = (E < 13.5) ? (E - 1) : (E - 13);
	var ye = (mo > 2.5) ? (C - 4716) : (C - 4715);

	var ti = F * 24.0;
	var ho = Math.floor(ti);
	var mi = (ti - ho) * 60.0;

	var res = new Array(ye, mo, da, ho, mi);
	return res;
}

// その日のユリウス日を計算する
function calJD(ye, mo, da, ho, mi){ // 実数体上
	var y0 = (mo > 2) ? ye : (ye -  1);
	var m0 = (mo > 2) ? mo : (mo + 12);
	var JD = Math.floor(365.25 * y0) + Math.floor(y0 / 400) - Math.floor(y0 / 100);
	JD	+= Math.floor(30.59 * (m0 - 2)) + da;
	JD	+= ((ho - 9) * 60.0 + mi) / 1440.0 + 1721088.5;

	return JD;
}

function cnvJDr( JD ){ // 実数体→整数環
	var date = cnvCalendar(JD);
	var ye = date[ 0 ];
	var mo = date[ 1 ];
	var da = date[ 2 ];
	var JDz = calJDz(ye, mo, da);

	return JDz;
}

function calJDz(year, month, day){ // 整数環上
	var yt = year;
	var mt = month;
	var dt = day;

	if(month < 3){
		yt--;
		mt += 12;
	}

	var JD = Math.floor(365.25 * yt) + Math.floor(30.6001 * (mt + 1));
	JD += dt + 1720995;
	JD += 2 - Math.floor(yt / 100) + Math.floor(yt / 400);

	return JD;
}

// d, Tを配列で返す。
function calTimeCoefficient( JD ){
	var d = JD - 2451545.0;
	var T = d / 36525.0;
	var coef = new Array(d, T);

	return coef;
}

// 軌道要素６パラ版→通常の軌道要素
// a : semi-major axis (au).
// l : mean longitude (degree).
// h : e * sin(pi).
// k : e * cos(pi).
// p : g * sin(om).
// q : g * cos(om).
// e : eccentricity.
// g : sine of the half inclination.
// pi: longitude of the perihelion.
// om: longitude of the ascending node.
function convertOrbitalElement( a, l, h, k, p, q ) {
	var L = l;
	var e = Math.sqrt( h * h + k * k );
	var g = Math.sqrt( p * p + q * q );
	var i = Math.asin( g ) * 2.0 / deg2rad;
	var opi = Math.atan2( h, k ) / deg2rad;
	var omg = Math.atan2( p, q ) / deg2rad;

	var result = [L, opi, omg, i, e, a];
	return result;
}

// まとめて軌道計算。返値は（黄経、黄緯、動径）。
function orbitWork(L, opi, omg, i, e, a){
	var M = mod360(L - opi);
	var E = mod360(solveKepler(M, e));

	var rE  = E * deg2rad;
	var thv = Math.sqrt( (1 + e) / (1 - e) ) * Math.tan(rE / 2.0);
	var v   = mod360(Math.atan2(thv, 1.0) * 2.0 / deg2rad);
	var r   = a * (1.0 - e * Math.cos(rE));
	var u   = L + v - M - omg;
	
	var ri = i * deg2rad;
	var ru = u * deg2rad;
	var l  = mod360(omg + Math.atan2(Math.cos(ri) * Math.sin(ru), Math.cos(ru)) / deg2rad);

	var rb = Math.asin(Math.sin(ru) * Math.sin(ri));
	var b  = rb / deg2rad;

	var res = new Array(l, b, r);
	return res;
}

// Kepler方程式(M = E - e sinE)を解く。
function solveKepler(M, e){
	var Mr = M * deg2rad;
	var Er = Mr;

	for( var i = 0; i < 20; i++ ){
		Er = Mr + e * Math.sin( Er );
	}

	return Er / deg2rad;
}

// 日心位置から地心位置へコンバートし、地心黄経を返す。
function convertGeocentric( earthCoor, planetCoor ){
	var lp, bp, rp, ls, bs, rs;

	ls = earthCoor[ 0 ];
	bs = earthCoor[ 1 ];
	rs = earthCoor[ 2 ];

	lp = planetCoor[ 0 ];
	bp = planetCoor[ 1 ];
	rp = planetCoor[ 2 ];

	var xs = rs * Math.cos(ls * deg2rad) * Math.cos(bs * deg2rad);
	var ys = rs * Math.sin(ls * deg2rad) * Math.cos(bs * deg2rad);
	var zs = rs *                          Math.sin(bs * deg2rad);
	var xp = rp * Math.cos(lp * deg2rad) * Math.cos(bp * deg2rad);
	var yp = rp * Math.sin(lp * deg2rad) * Math.cos(bp * deg2rad);
	var zp = rp *                          Math.sin(bp * deg2rad);

	var xg = xp + xs;
	var yg = yp + ys;
	var zg = zp + zs;

	var rg = Math.sqrt(xg * xg + yg * yg + zg * zg);
	var lg = Math.atan2(yg, xg) / deg2rad;
	if(lg < 0.0) lg += 360.0;
	var bg = asin4deg(zg / rg);

	var res = new Array(lg, bg, rg);
	return res;
}

// 黄道座標系から赤道座標系へ変換する。
function convertEquatorial(lon, lat, obl){
	var xs = cos4deg(lon) * cos4deg(lat);
	var ys = sin4deg(lon) * cos4deg(lat);
	var zs =                sin4deg(lat);

	var xd = xs;
	var yd = ys * cos4deg(obl) - zs * sin4deg(obl);
	var zd = ys * sin4deg(obl) + zs * cos4deg(obl);

	var RA = atan2(yd, xd) / deg2rad;
	if(RA < 0.0) RA += 360.0;
	var Dec = asin4deg(zd);

	var res = new Array(RA, Dec);
	return res;
}

// 歳差補正
function coordinateConvertFromJ2000( arg ){
	var zeta, zz, theta;
	var x, y, z, xd, yd, zd, xs, ys, zs;

	var xs  = arg[ 0 ];
	var ys  = arg[ 1 ];
	var zs  = arg[ 2 ];
	var tjd = arg[ 3 ];

	var T = (tjd - 2451545.0) / 36525.0;

	var zeta  = ((( 0.017998 * T + 0.30188) * T + 2306.2181) * T) / 3600.0;
	var zz    = ((( 0.018203 * T + 1.09468) * T + 2306.2181) * T) / 3600.0;
	var theta = (((-0.041833 * T - 0.42665) * T + 2004.3109) * T) / 3600.0;

// Step 1
	x =  sin4deg(zeta) * xs + cos4deg(zeta) * ys;
	y = -cos4deg(zeta) * xs + sin4deg(zeta) * ys;
	z = zs;

// Step 2;
// 	x = x;
	y = 0 * x + cos4deg(theta) * y + sin4deg(theta) * z;
	z = 0 * x - sin4deg(theta) * y + cos4deg(theta) * z;

// Step 3
	xd = -sin4deg(zz) * x - cos4deg(zz) * y;
	yd =  cos4deg(zz) * x - sin4deg(zz) * y;
	zd = z;

	var res = new Array(xd, yd, zd);
	return res;
}

// 地方恒星時計算
function calLST_old(JD, ho, mi, lo){
	var JD0 = Math.floor(JD - 0.5) + 0.5;
	var T = (JD0 - 2451545.0) / 36525.0;
	var UT = (JD - JD0) * 360.0 * 1.002737909350795;
	if( UT < 0 ) UT += 360.0;

	//グリニッジ恒星時計算
	var GST  = 0.279057273 + 100.0021390378 * T + 1.077591667e-06 * T * T;
	    GST  = GST - Math.floor(GST);
	    GST *= 360.0;

	// 地方恒星時計算＋章動補正
	var LST = mod360(GST + UT + lo);
	var dpsi = calNutation(JD);
	var eps  = calOblique(JD);
	LST += dpsi * cos4deg(eps) / 3600.0;
	if(LST < 0.0) LST += 360.0;

	return LST;
}

// いまどきの地方恒星時計算
function calLST(JDut, ho, mi, lo) {
	const Du = JDut - 2451545.0;

	const JDtt = JDut + correctTDT( JDut );
	const T = (JDtt - 2451545.0) / 36525.0;

	// Earth Rotation Angle
	let theta = 0.7790572732640 + 1.00273781191135448 * Du;
	theta = theta - Math.floor(theta);

	// Greenwich mean sidereal time
	const GMST = 86400.0 * theta + (0.014506 + T * (4612.156534 + T * (1.3915817 - 0.00000044 * T))) / 15.0;

	// Greenwich apparent sidereal time
	const dpsi = calNutation(JDtt);
	const eps  = calOblique(JDtt);
	const GAST = GMST + dpsi * cos4deg(eps) / 15.0;

	// Local apparent sidereal time in timely seconds
	const LAST = GAST + 3600.0 * lo / 15.0;

	// Local apparent sidereal time in degrees
	let LASTd = LAST / ( 4.0 * 60.0 );
	if (LASTd < 0.0) {
		LASTd += 360.0;
	} else if( LASTd >= 360.0 ){
		LASTd -= 360.0;
	}

	return LASTd;
}

// 黄道傾斜角を計算する関数
function calOblique_old(JD ){
	var T = (JD - 2451545.0) / 36525.0;
	var Omg = mod360(125.00452 - T *   1934.136261);
	var Ls  = mod360(280.4665  + T *  36000.7698);
	var Lm  = mod360(218.3165  + T * 481267.8813);

	var e = 84381.448 + T * (-46.8150 + T * (-0.00059 + T * 0.001813));
	var deps  =  9.20 * cos4deg(1.0 * Omg);
	    deps +=  0.57 * cos4deg(2.0 * Ls);
	    deps +=  0.10 * cos4deg(2.0 * Lm);
	    deps += -0.09 * cos4deg(2.0 * Omg);

	return (e + deps) / 3600.0;
}

function calOblique( JD ){
	const T = (JD - 2451545.0) / 36525.0;
	const Omg = (125.00452 - T *   1934.136261) * deg2rad;
	const Ls  = (280.4665  + T *  36000.7698) * deg2rad;
	const Lm  = (218.3165  + T * 481267.8813) * deg2rad;

	const e = 84381.406 + T * (-46.836769 + T * (-0.0001831 + T * 0.00200340));
	const C0 = [ 9.205, 0.573, 0.098, -0.089 ];
	const C1 = [ 0.001, 0.000, 0.000,  0.000 ];
	const S0 = [ 0.002, 0.000, 0.000,  0.000 ];
	const th = [ 1.0 * Omg, 2.0 * Ls, 2.0 * Lm, 2.0 * Omg ];

	let deps = 0.0;
	for( let i = 0; i < th.length; i++ ){
		deps += (C0[i] + C1[i] * T) * Math.cos(th[i]) + S0[i] * Math.sin(th[i]);
	}

	return (e + deps) / 3600.0;
}

// 章動を計算する関数（簡略版）
function calNutation( JD ){
	const T = (JD - 2451545.0) / 36525.0;

	const Omg = (125.00452 - T *   1934.136261) * deg2rad;
	const Ls  = (280.4665  + T *  36000.7698) * deg2rad;
	const Lm  = (218.3165  + T * 481267.8813) * deg2rad;
	const M   = (357.52772 + T *  35999.0503) * deg2rad;

	const S0 = [-17.206, -1.317, -0.227, +0.207, +0.147];
	const S1 = [ -0.017, -0.000, -0.000, +0.000, -0.000];
	const C0 = [ +0.003, -0.001, +0.000, +0.000, +0.001];
	const th = [ 1.0 * Omg, 2.0 * Ls, 2.0 * Lm, 2.0 * Omg, 1.0 * M ];

	let dpsi = 0.0;
	for( let i = 0; i < th.length; i++ ){
		dpsi += (S0[i] + S1[i] * T) * Math.sin(th[i]) + C0[i] * Math.cos(th[i]);
	}

	return dpsi;
}

// 均時差を計算する関数
function calEqT_old( JD ){
	var  T = ( JD - 2451545.0 ) / 36525.0;

	var L0  = mod360( 36000.76983 * T );
		L0  = mod360( 280.46646 + L0 + 0.0003032 * T * T );
		L0 *= deg2rad;

	var  M  = mod360( 35999.05029 * T );
		 M  = mod360( 357.52911 + M  - 0.0001537 * T * T );
		 M *= deg2rad;

	var  e  = 0.016708634 + T * ( -0.000042037 - 0.0000001267 * T );

	var  y  = calOblique( JD );
		 y  = tan4deg( y / 2.0 );
		 y  = y * y;

	var  E  = y * Math.sin( 2 * L0 ) - 2.0 * e * Math.sin( M );
		 E += 4.0 * e * y * Math.sin( M ) * Math.cos( 2.0 * L0 );
		 E -= y * y * Math.sin( 4.0 * L0 ) / 2.0;
		 E -= 5.0 * e * e * Math.sin( 2.0 * M ) / 4.0;

	E /= deg2rad;
	return ( E * 4.0 );
}

// cf. https://aa.usno.navy.mil/faq/sun_approx
// 軌道要素： https://ssd.jpl.nasa.gov/planets/approx_pos.html
function calEqT( JD ) {
	const T = (JD - 2451545.0) / 36525.0;

	const l  = mod360( 100.46457166 + 35999.37244981 * T );
	const p  = 102.93768193 + 0.32327364 * T;
	const rM = (l - p) * deg2rad;
	const e  = 0.01671123 - 0.00004392 * T;
	const rC = 2 * e * Math.sin( rM ) + ( 5.0 / 4.0 * e * e ) * Math.sin( 2.0 * rM );
	const L  = mod360( l + 180.0 + rC / deg2rad );

	const obl = calOblique( JD );
	const ce  = Math.cos( obl * deg2rad );
	const rL  = L * deg2rad;
	const sL  = Math.sin( rL );
	const cL  = Math.cos( rL );
	const rRA = Math.atan2( ce * sL, cL );
	const RA  = mod360(rRA / deg2rad);

	let EqT = (l + 180.0) - RA; // in degree
	if( EqT > 180.0 ){
		EqT -= 360.0;
	} else if ( EqT < -180.0 ){
		EqT += 360.0;
	}
	return 4.0 * EqT; // in minutes
}


////////////////////////////////

// カレンダー関係。
function calDayOfWeek(year, month, day){
	var JD = calJDz(year, month, day);
	var you = (JD + 1) % 7;
	return you;
}

function chkLeap( year ){
	var chk = 0;

	if(year %   4 == 0) chk = 1;
	if(year % 100 == 0) chk = 0;
	if(year % 400 == 0) chk = 1;

	return chk;
}

function maxday(year, month){
	var mday = [31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
	var md = mday[ month ];
	if( month == 2 && chkLeap( year ) ){
		md = 29;
	}

	return md;
}

// ΔＴを管理する関数
// formula A : Notes Scientifiques et Techniques du Bureau des Longitudes, nr. S055
// from ftp://cyrano-se.obspm.fr/pub/6_documents/4_lunar_tables/newexp.pdf
// formula D : Addendum 2020 to ‘Measurement of the Earth’s rotation: 720 BC to AD 2015
// from https://royalsocietypublishing.org/doi/suppl/10.1098/rspa.2020.0776
function correctTDT(JD){
	var year = ( JD - 2451545.0 ) / 365.2425 + 2000.0;
	var t, dt;

	if( year < 2019.0 ){ // formula D
		const from = [-720, -100, 400, 1000, 1150, 1300, 1500, 1600, 1650, 1720, 1800, 1810, 1820, 1830, 1840, 1850, 1855, 1860, 1865, 1870, 1875, 1880, 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1930, 1935, 1940, 1945, 1950, 1953, 1956, 1959, 1962, 1965, 1968, 1971, 1974, 1977, 1980, 1983, 1986, 1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016];
		const to   = [-100, 400, 1000, 1150, 1300, 1500, 1600, 1650, 1720, 1800, 1810, 1820, 1830, 1840, 1850, 1855, 1860, 1865, 1870, 1875, 1880, 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1930, 1935, 1940, 1945, 1950, 1953, 1956, 1959, 1962, 1965, 1968, 1971, 1974, 1977, 1980, 1983, 1986, 1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019];
		const a0   = [20371.848, 11557.668, 6535.116, 1650.393, 1056.647, 681.149, 292.343, 109.127, 43.952, 12.068, 18.367, 15.678, 16.516, 10.804, 7.634, 9.338, 10.357, 9.04, 8.255, 2.371, -1.126, -3.21, -4.388, -3.884, -5.017, -1.977, 4.923, 11.142, 17.479, 21.617, 23.789, 24.418, 24.164, 24.426, 27.05, 28.932, 30.002, 30.76, 32.652, 33.621, 35.093, 37.956, 40.951, 44.244, 47.291, 50.361, 52.936, 54.984, 56.373, 58.453, 60.678, 62.898, 64.083, 64.553, 65.197, 66.061, 66.92, 68.109];
		const a1   = [-9999.586, -5822.27, -5671.519, -753.21, -459.628, -421.345, -192.841, -78.697, -68.089, 2.507, -3.481, 0.021, -2.157, -6.018, -0.416, 1.642, -0.486, -0.591, -3.456, -5.593, -2.314, -1.893, 0.101, -0.531, 0.134, 5.715, 6.828, 6.33, 5.518, 3.02, 1.333, 0.052, -0.419, 1.645, 2.499, 1.127, 0.737, 1.409, 1.577, 0.868, 2.275, 3.035, 3.157, 3.199, 3.069, 2.878, 2.354, 1.577, 1.648, 2.235, 2.324, 1.804, 0.674, 0.466, 0.804, 0.839, 1.007, 1.277];
		const a2   = [776.247, 1303.151, -298.291, 184.811, 108.771, 61.953, -6.572, 10.505, 38.333, 41.731, -1.126, 4.629, -6.806, 2.944, 2.658, 0.261, -2.389, 2.284, -5.148, 3.011, 0.269, 0.152, 1.842, -2.474, 3.138, 2.443, -1.329, 0.831, -1.643, -0.856, -0.831, -0.449, -0.022, 2.086, -1.232, 0.22, -0.61, 1.282, -1.115, 0.406, 1.002, -0.242, 0.364, -0.323, 0.193, -0.384, -0.14, -0.637, 0.708, -0.121, 0.21, -0.729, -0.402, 0.194, 0.144, -0.109, 0.277, -0.007];
		const a3   = [409.16, -503.433, 1085.087, -25.346, -24.641, -29.414, 16.197, 3.018, -2.127, -37.939, 1.918, -3.812, 3.25, -0.096, -0.539, -0.883, 1.558, -2.477, 2.72, -0.914, -0.039, 0.563, -1.438, 1.871, -0.232, -1.257, 0.72, -0.825, 0.262, 0.008, 0.127, 0.142, 0.702, -1.106, 0.614, -0.277, 0.631, -0.799, 0.507, 0.199, -0.414, 0.202, -0.229, 0.172, -0.192, 0.081, -0.165, 0.448, -0.276, 0.11, -0.313, 0.109, 0.199, -0.017, -0.084, 0.128, -0.095, -0.139];

		for( let i = 0; i < a0.length; i++ ){
			if (from[i] <= year && year < to[i]) {
				t = ( year - from[i] ) / ( to[i] - from[i] );
				dt = a0[i] + t * ( a1[i] + t * ( a2[i] + t * a3[i] ) );
				break;
			}
		}
	} else { // formula A.25
		t = ( JD - 2451545.0 ) / 36525.0;
		dt =  102.0 + t * ( 102.0 + t * 25.3 );
		if( year < 2100 ){
			dt += 0.37 * ( year - 2100 ); // from "Astronomical Algorithms" p.78
		}
	}

	dt /= 86400.0;
	return dt;
}

function advanceDate( date, step ){
	return encodeDate(...cnvCalendar(calJDz(...decodeDate(date)) + step));
}

function calDist(sy, sm, sd, ey, em, ed){
	return calJDz(ey, em, ed) - calJDz(sy, sm, sd);
}

function decodeDate( date ){
	var ye = Math.floor( date / 10000 );
	var mo = Math.floor((date % 10000) / 100);
	var da =             date %   100;

	var res = new Array(ye, mo, da);
	return res;
}

function decodeTime( time ){
	var ho = Math.floor(time / 100);
	var mi = fmod(time, 100);

	var res = new Array(ho, mi);
	return res;
}

function encodeDate(ye, mo, da){
	return ye * 10000 + mo * 100 + da;
}

function encodeTime(ho, mi){
	return ho * 100 + mi;
}
