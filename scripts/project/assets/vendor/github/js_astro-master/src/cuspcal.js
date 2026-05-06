/*
 * ハウスカスプ計算ルーチン
 * Copyright (c) 1999-2001, 2017 Yoshihiro Sakai & Sakai Institute of Astrology
 * This software is released under the MIT License.
 * http://opensource.org/licenses/mit-license.php
 */

// House Cusp Calculating subroutine
function calHouseCusp(ye, mo, da, ho, mi, pid){
	var coor = findPlaceCoor(pid);
	var lo = coor[ 0 ];
	var la = coor[ 1 ];

	var cusp = calHouseCusp2(ye, mo, da, ho, mi, lo, la, 1);
	return cusp;
}

function calHouseCusp2(ye, mo, da, ho, mi, Lon, Lat, htype){
	var cusp = new Array();
	var JD  = calJD(ye, mo, da, ho, mi);
	var lst = calLST(JD, ho, mi, Lon);
	var obl = calOblique(JD);

	switch( htype ) {
		case 1:
			cusp = calHousePlacidus(lst, Lat, obl);
			break;
		case 2:
			cusp = calHouseCampanus(lst, Lat, obl);
			break;
		case 3:
			cusp = calHouseRegiomontanus(lst, Lat, obl);
			break;
		case 4:
			cusp = calHouseKoch(lst, Lat, obl);
			break;
		case 5:
			cusp = calHouseTopocentric(lst, Lat, obl);
			break;
		case 6:
			cusp = calHouseAxial(lst, Lat, obl);
			break;
		case 7:
			cusp = calHouseMorinus(lst, Lat, obl);
			break;
	}

	return cusp;
}

// for Koch & Topocentric House System
function calAsc(lst, lat, obl){
	// ASC計算
	var ASCx = cos4deg(lst);
	var ASCy = -(sin4deg(obl) * tan4deg(lat));
	ASCy    -= cos4deg(obl) * sin4deg(lst);
	var ASC  = mod360(Math.atan2(ASCx, ASCy) / deg2rad);
	if(ASC < 0.0) ASC += 360.0;

	return ASC;
}

//////////////////////
// Placidus House System
function calHousePlacidus(LST, Lat, obl){

	// Initial Setting...LST
	var H    = 0.0;
	var F    = 0.0;
	var P0   = 0.0;
	var P1   = 0.0;
	var X0   = 0.0;
	var X1   = 0.0;
	var d    = 0.0;
	var d0   = 1.0e-03;
	var csp  = 0.0;
	var cspx = 0.0;
	var cspy = 0.0;
	var cusp = new Array();

	var angle = calGeoPoint(LST, Lat, obl);
	var ASC = angle[ 0 ];
	var MC  = angle[ 1 ];

	// Calculating Cusps...
	for( var i = 1; i <= 12; i++ ){
		if(i % 3 == 1){
			cusp[i] = mod360(((i % 6 == 1) ? ASC : MC) +
									((i > 2) && (i < 8) ? 180.0 : 0.0));
		} else {
			nh = i;
			if((i > 4) && (i < 10)){
				nh = (nh + 6) % 12;
				if( nh == 0 ) nh = 12;
			}
			H = mod360((nh + 2) * 30.0);
			F = (nh % 2 == 1) ? (3.0) : (1.5);
			X0 = LST + H;
			do{
				P0  = sin4deg(X0) * tan4deg(obl) * tan4deg(Lat);
				P0 *= ((nh > 7) ? (-1.0) : (+1.0));
				P1  = ((nh > 7) ? (+1.0) : (-1.0)) * acos4deg(P0);
				X1  = LST + P1 / F + ((nh > 7) ? (0.0) : (180.0));
				d   = Math.abs(X0 - X1);
				X0  = X1;
			} while(d > d0);
			cspx = sin4deg(X1);
			cspy = cos4deg(obl) * cos4deg(X1);
			csp  = atan24deg(cspx, cspy);
			csp += ((i > 4) && (i < 10)) ? (180.0) : (0.0);
			cusp[i] = mod360(csp);
		}
	}

	return cusp;
}

// Campanus House Cusp
function calHouseCampanus(LST, Lat, obl){
	var C, Cx, D, H, csp, cspx, cspy, nh;
	var cusp = new Array();

	var angle = calGeoPoint(LST, Lat, obl);
	var ASC = angle[ 0 ];
	var MC  = angle[ 1 ];

	// Calculating Cusps...
	for( var i = 1; i <= 12; i++ ){
		if(i % 3 == 1){
			cusp[i] = mod360(((i % 6 == 1) ? ASC : MC) +
									((i > 2) && (i < 8) ? 180.0 : 0.0));
		} else {
			nh = i;
			if((i > 4) && (i < 10)){
				nh = (nh + 6) % 12;
				if(nh == 0) nh = 12;
			}
			H  = mod360((nh + 2) * 30.0);
			D  = cos4deg(H) / (sin4deg(H) * cos4deg(Lat));
			D  = LST + 90.0 - atan4deg(D);
			Cx = tan4deg(asin4deg(sin4deg(Lat) * sin4deg(H)));
			C  = atan24deg(Cx, cos4deg(D));
			cspx = tan4deg(D) * cos4deg(C);
			cspy = cos4deg(C + obl);
			csp  = atan24deg(cspx, cspy);
			csp += (nh != i) ? (180.0) : (0.0);
			cusp[i] = mod360(csp);
		}
	}

	return cusp;
}

// Regiomontanus House Cusp
function calHouseRegiomontanus(LST, Lat, obl){
	var R, Rx, Ry, H, csp, cspx, cspy, nh;
	var cusp = new Array();

	var angle = calGeoPoint(LST, Lat, obl);
	var ASC = angle[ 0 ];
	var MC  = angle[ 1 ];

	// Calculating Cusps...
	for( var i = 1; i <= 12; i++ ){
		if(i % 3 == 1){
			cusp[i] = mod360(((i % 6 == 1) ? ASC : MC) +
									((i > 2) && (i < 8) ? 180.0 : 0.0));
		} else {
			nh = i;
			if((i > 4) && (i < 10)){
				nh = (nh + 6) % 12;
				if(nh == 0) nh = 12;
			}
			H  = mod360((nh + 2) * 30.0);
			Rx = sin4deg(H) * tan4deg(Lat);
			Ry = cos4deg(LST + H);
			R  = atan24deg(Rx, Ry);
			cspx = cos4deg(R) * tan4deg(LST + H);
			cspy = cos4deg(R + obl);
			csp  = atan24deg(cspx, cspy);
			csp += (nh != i) ? (180.0) : (0.0);
			cusp[i] = mod360(csp);
		}
	}

	return cusp;
}

// Koch House System
function calHouseKoch(LST, Lat, obl){
	var K, dlst, csp, nh;
	var cusp = new Array();

	var angle = calGeoPoint(LST, Lat, obl);
	var ASC = angle[ 0 ];
	var MC  = angle[ 1 ];

	// Calculating Cusps...
	for( var i = 1; i <= 12; i++ ){
		if(i % 3 == 1){
			cusp[i] = mod360(((i % 6 == 1) ? ASC : MC) +
									((i > 2) && (i < 8) ? 180.0 : 0.0));
		} else {
			nh = i;
			if((i > 4) && (i < 10)){
				nh = (nh + 6) % 12;
				if(nh == 0) nh = 12;
			}
			K = asin4deg(sin4deg(MC) * sin4deg(obl));
			K = asin4deg(tan4deg(Lat) * tan4deg(K));
			dlst  = 30.0 + K / 3.0;
			if(nh == 11 || nh == 3) dlst *=  2.0;
			if(nh > 7) dlst *= -1.0;
			cusp[i]  = calAsc(LST + dlst, Lat, obl);
			if((i > 4) && (i < 10))  cusp[i] += 180;
		}
	}

	return cusp;
}

// Topocentric House System
function calHouseTopocentric(LST, Lat, obl){
	var dlst, lat1, csp, nh;
	var cusp = new Array();

	var angle = calGeoPoint(LST, Lat, obl);
	var ASC = angle[ 0 ];
	var MC  = angle[ 1 ];

	// Calculating Cusps...
	for( var i = 1; i <= 12; i++ ){
		if(i % 3 == 1){
			cusp[i] = mod360(((i % 6 == 1) ? ASC : MC) +
									((i > 2) && (i < 8) ? 180.0 : 0.0));
		} else {
			nh = i;
			if((i > 4) && (i < 10)){
				nh = (nh + 6) % 12;
				if(nh == 0) nh = 12;
			}
			dlst  = mod360((nh + 2) * 30.0) - 90.0;
			lat1  = tan4deg(Lat) / 3.0;
			if(nh == 12 || nh == 2) lat1 *= 2.0;
			lat1  = atan4deg(lat1);
			cusp[i]  = calAsc(LST + dlst, lat1, obl);
			if((i > 4) && (i < 10)) cusp[i] += 180;
		}
	}

	return cusp;
}

// Axial Rotation System
function calHouseAxial(LST, Lat, obl){
	var alpha, cspx, cspy;
	var cusp = new Array();

	for(i = 10;i < 16;i++){
		house = ((i > 12) ? i - 12 : i);
		alpha = LST + 60.0 + 30.0 * house;
		cspx  = cos4deg(alpha) * cos4deg(obl);
		cspy  = sin4deg(alpha);
		cusp[house] = atan24deg(cspy, cspx);
	}
	for(i = 4;i < 10;i++){
		var oh = i + 6;
		if(oh > 12){
			oh -= 12;
		}
		cusp[i] = mod360(cusp[oh] + 180.0);
	}

	return cusp;
}

// Morinus House System
function calHouseMorinus(LST, Lat, obl){
	var Z, cspx, cspy;
	var cusp = new Array()

	for(i = 1;i <= 12;i++){
		Z = mod360(LST + 60.0 + 30.0 * i);
		cspx = cos4deg(Z);
		cspy = sin4deg(Z) * cos4deg(obl);
		cusp[i] = atan24deg(cspy, cspx);
	}

	return cusp;
}
