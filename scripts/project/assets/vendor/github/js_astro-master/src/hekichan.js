/*
 * 天体位置計算エンジン「はいぱーへきちゃん」 version 1.00-j08
 * Copyright (c) 1999-2004, 2017, 2021, 2024, 2025 Yoshihiro Sakai & Sakai Institute of Astrology
 * This software is released under the MIT License.
 * http://opensource.org/licenses/mit-license.php
 *
 * This library uses simplified VSOP87-D, ELP2000-82B, PLUTO-95 developed by
 * Bureau des Longitudes, French. This library valids 1700-2100 Common Era.
 * 2000/03/19[h02] 一応、第１次光行差と章動の補正を入れといた。
 * 2000/07/09[h03] 赤道座標系への変換を容易にするためフルセットで返すようにした。
 * 2000/09/25[h04] ノードとリリスの計算法をとある論文に基づき変更。
 * 2001/03/18[h05] 原則として冥王星はAstronomical Algorithms方式で計算する。
 * 2001/04/23[h06] 天体位置計算の仕掛けをちょこっと変更
 * 2001/07/09[h07] 光行差の計算方式を変更
 * 2001/07/13[h08] 月の計算をパワーアップ！
 * 2002/09/14[h09] 太陽と月の速度の計算式を追加
 * 2003/01/01[h10] なぜか入っていたあほなバグを除去。
 * 2003/01/16[h11] なぜか入っていたあほなバグをさらに除去。
 * 2003/08/29[h12] 黄道傾斜角が間違ってました。
 * 2004/01/09[h13] ルナーリターンを計算する関数を追加。
 * 2004/01/11[h14] ソーラーリターン関数を追加、黄道傾斜角と章動を分離。
 * 2004/01/11[h15] 1700～2100年以外の冥王星を軌道要素で計算するようにした。
 * 2017/04/27[j01] JavaScriptに移植。
 * 2017/05/25[j02] 冥王星の軌道要素を別ロジックに入れ替え。
 * 2017/06/05[j03] 軌道要素６パラ版に対応
 * 2017/08/07[j04] 冥王星の計算式がおかしなことになっていた。ついでにj02取り消し
 * 2021/02/27[j05] 冥王星の軌道要素計算式を見直し
 * 2024/12/20[j06] 四大小惑星＆キローンの接触軌道要素近似式対応
 * 2025/02/15[j07] 小惑星の光行差補正を大惑星に合わせる
 * 2025/07/28[j08] 接触軌道要素 Chebyshev 近似多項式を JPL Horizons System 生成結果から再計算
 */

// 冥王星の1700～2100年以外の期間の軌道要素選択フラグ
var jplMode = 1;

// 天体位置を配列で返す統括関数
function calPlanetPosition( ye, mo, da, ho, mi, pid ){
	var coor = new Array( 2 );
	coor = findPlaceCoor( pid );
	var lo = coor[ 0 ];
	var la = coor[ 1 ];

	var res = new Array();
	res = calPlanetPosition2( ye, mo, da, ho, mi, lo, la );

	return res;
}

function calPlanetPosition2( ye, mo, da, ho, mi, lon, lat ){
	var i;

	var JD   = calJD( ye, mo, da, ho, mi );
	var lst  = calLST( JD, ho, mi, lon );
	var date = ye * 10000 + mo * 100 + da * 1;
	var plapos = new Array();

	JD += correctTDT( JD );
	var coef = calTimeCoefficient( JD );
	var d = coef[ 0 ];
	var T = coef[ 1 ];

	plapos[ 0 ] = JD;

	for( var i = 1; i <= 10; i++ ){
		plapos[ i ] = calPlaPos( JD, i );
	}

	var luna = new Array( 2 );
	luna = calPositLuna( JD );
	plapos[ 11 ] = luna[ 0 ];
	plapos[ 12 ] = luna[ 1 ];

	var obl = calOblique( JD );
	var angle = new Array( 2 );
	angle = calGeoPoint( lst, lat, obl );
	plapos[13] = angle[ 0 ];
	plapos[14] = angle[ 1 ];

	for( let i = 0; i < 5; i++ ){
		plapos[15 + i] = calPlaPos(JD, 11 + i);
	}

	var dpsi = calNutation( JD ) / 3600.0;
	for( var i = 1; i <= 19; i++){
		if(i == 13 || i == 14) continue;
		if(Math.abs(plapos[i]) > 360.0) continue;
		plapos[ i ] -= dpsi;
		if( plapos[ i ] <    0.0){
			plapos[ i ] += 360.0;
		} else if( plapos[ i ] >= 360.0){
			plapos[ i ] -= 360.0;
		}
	}

	return plapos;
}

// 各天体の黄経計算／JDは地球力学時基準
function calPlaPos( JD, pid ){
	var T  = ( JD - 2451545.0 ) /  36525.0;
	var T2 = ( JD - 2451545.0 ) / 365250.0;

// 光行差定数
	var C = [0.00347, 0.00484, 0.00700, 0.01298, 0.01756, 0.02490, 0.03121, 0.03461];
	var dl;
	var epos = new Array(3);
	var gpos = new Array(3);
	var ppos = new Array(3);

	epos = calPositSO( T2 );
	if( pid == 1 ){ // 計算目標が太陽の場合
		gpos[ 0 ] = epos[ 0 ] - 0.005693 / epos[ 2 ];
	} else if( pid == 2 ){ // 計算目標が月の場合
		gpos = calPositMO(T);
	} else if ( pid <= 10 ) { // 計算目標が大惑星の場合
		switch( pid ){
			case 3:
				ppos = calPositME( T2 );
				break;
			case 4:
				ppos = calPositVE( T2 );
				break;
			case 5:
				ppos = calPositMA( T2 );
				break;
			case 6:
				ppos = calPositJU( T2 );
				break;
			case 7:
				ppos = calPositSA( T2 );
				break;
			case 8:
				ppos = calPositUR( T2 );
				break;
			case 9:
				ppos = calPositNE( T2 );
				break;
			case 10:
				if( -1.15 <= T && T < 1.0 ){ // Pluto_mee valids thru 1885-2099
					ppos = calPositPL_mee( T );
				} else { // Pluto_obspm valids thru -3000 - 3000, but intentionally uses to 0 - 4000
					ppos = calPositPL_obspm( T );
				}
				ppos[ 0 ] += 5029.0966 / 3600.0 * T;  // 線型近似の歳差補正する
				break;
		}
		gpos = convertGeocentric( epos, ppos );
		dl  = -0.005693  * Math.cos( ( gpos[ 0 ] - epos[ 0 ] ) * Math.PI / 180.0 );
		dl -= C[ pid - 3 ] * Math.cos( ( gpos[ 0 ] - ppos[ 0 ] ) * Math.PI / 180.0 ) / ppos[ 2 ];
		gpos[ 0 ] += dl;
	} else { // 計算目標が小惑星かキローンの場合
		const mid = pid - 11;
		ppos = calAsteroidPosition(JD, mid);
		const meanA = [2.766051, 2.770193, 2.670669, 2.361397, 13.698943];
		const a = meanA[mid];
		const Cp = 0.00558236 * Math.sqrt(a) + 0.00016798;
		if (ppos) {
			ppos[0] += 5029.0966 / 3600.0 * T;  // 線型近似の歳差補正する
			gpos = convertGeocentric( epos, ppos );
			dl  = -0.005693  * Math.cos( ( gpos[ 0 ] - epos[ 0 ] ) * Math.PI / 180.0 );
			dl -= Cp * Math.cos( ( gpos[ 0 ] - ppos[ 0 ] ) * Math.PI / 180.0 ) / ppos[ 2 ];
			gpos[ 0 ] += dl;
		} else {
			gpos[0] = -361.0; // 計算期間外
		}
	}

	return gpos[ 0 ];
}

// 各要素の計算
function calVsopTerm( T, term ){
	var res = 0.0;

	for( var i = term.length - 1; i >= 0; i-- ){
		res = term[ i ] + res * T;
	}

	return res;
}

function calPositSO( T ){
	var lo = 0.0;
	var bo = 0.0;
	var ro = 0.0;
	var Lon = new Array();
	var Lat = new Array();
	var Rad = new Array();

// Earth(Sun)'s Longitude
	Lon[0]  =     1.75347 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[0] +=     0.03342 * Math.cos( 4.66926 +    6283.07585 * T);
	Lon[0] +=     0.00035 * Math.cos( 4.62610 +   12566.15170 * T);
	Lon[1]  =  6283.31967 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[1] +=     0.00206 * Math.cos( 2.67823 +    6283.07585 * T);
	Lon[2]  =     0.00053 * Math.cos( 0.00000 +       0.00000 * T);

// Earth(Sun)'s Radius Vector
	Rad[0]  =     1.00014 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[0] +=     0.01671 * Math.cos( 3.09846 +    6283.07585 * T);
	Rad[0] +=     0.00014 * Math.cos( 3.05525 +   12566.15170 * T);
	Rad[1]  =     0.00103 * Math.cos( 1.10749 +    6283.07585 * T);

	lo = mod360( calVsopTerm( T, Lon ) / deg2rad);
	ro = calVsopTerm( T, Rad );

	lo = mod360( lo + 180.0 );

	var res = new Array( lo, bo, ro );
	return res;
}

function calPositMO( T ){
	var mf = new Array();
	var dl, db;

// Mean Longitude of the Moon(J2000.0)
	var W1 = 481266.0 * T;
	W1  = mod360( W1 );
	W1 +=   0.48437 * T;
	W1 -=   0.00163 * T * T;
	W1 += 218.31665;
	W1  = mod360( W1 );

// D : Mean elongation of the Moon
	mf[0]  = 445267.0 * T;
	mf[0]  = mod360( mf[0] );
	mf[0] +=   0.11151 * T;
	mf[0] -=   0.00163 * T * T;
	mf[0] += 297.85020;
	mf[0]  = mod360( mf[0] );

// l' : Mean anomary of the Sun
	mf[1]  =  35999.0 * T;
	mf[1]  = mod360( mf[1] );
	mf[1] +=   0.05029 * T;
	mf[1] -=   0.00015 * T * T;
	mf[1] += 357.51687;
	mf[1]  = mod360( mf[1] );

// l : Mean anomary of the Moon
	mf[2]  = 477198.0 * T;
	mf[2]  = mod360( mf[2] );
	mf[2] +=   0.86763  * T;
	mf[2] +=   0.008997 * T * T;
	mf[2] += 134.96341;
	mf[2]  = mod360( mf[2] );

// F : Argument of latitude of the Moon
	mf[3]  = 483202.0 * T;
	mf[3]  = mod360( mf[3] );
	mf[3] +=   0.01753 * T;
	mf[3] -=   0.00340 * T * T;
	mf[3] +=  93.27210;
	mf[3]  = mod360( mf[3] );

	dl  = +6.28876 * sin4deg(0 * mf[0] + 0 * mf[1] + 1 * mf[2] + 0 * mf[3]);
	dl += +1.27401 * sin4deg(2 * mf[0] + 0 * mf[1] - 1 * mf[2] + 0 * mf[3]);
	dl += +0.65831 * sin4deg(2 * mf[0] + 0 * mf[1] + 0 * mf[2] + 0 * mf[3]);
	dl += +0.21362 * sin4deg(0 * mf[0] + 0 * mf[1] + 2 * mf[2] + 0 * mf[3]);
	dl += -0.18512 * sin4deg(0 * mf[0] + 1 * mf[1] + 0 * mf[2] + 0 * mf[3]);
	dl += -0.11433 * sin4deg(0 * mf[0] + 0 * mf[1] + 0 * mf[2] + 2 * mf[3]);
	dl += +0.05879 * sin4deg(2 * mf[0] + 0 * mf[1] - 2 * mf[2] + 0 * mf[3]);
	dl += +0.05707 * sin4deg(2 * mf[0] - 1 * mf[1] - 1 * mf[2] + 0 * mf[3]);
	dl += +0.05332 * sin4deg(2 * mf[0] + 0 * mf[1] + 1 * mf[2] + 0 * mf[3]);
	dl += +0.04576 * sin4deg(2 * mf[0] - 1 * mf[1] + 0 * mf[2] + 0 * mf[3]);
	dl += -0.04092 * sin4deg(0 * mf[0] + 1 * mf[1] - 1 * mf[2] + 0 * mf[3]);
	dl += -0.03472 * sin4deg(1 * mf[0] + 0 * mf[1] + 0 * mf[2] + 0 * mf[3]);
	dl += -0.03038 * sin4deg(0 * mf[0] + 1 * mf[1] + 1 * mf[2] + 0 * mf[3]);
	dl += +0.01533 * sin4deg(2 * mf[0] + 0 * mf[1] + 0 * mf[2] - 2 * mf[3]);
	dl += -0.01253 * sin4deg(0 * mf[0] + 0 * mf[1] + 1 * mf[2] + 2 * mf[3]);
	dl += +0.01098 * sin4deg(0 * mf[0] + 0 * mf[1] + 1 * mf[2] - 2 * mf[3]);
	dl += +0.01067 * sin4deg(4 * mf[0] + 0 * mf[1] - 1 * mf[2] + 0 * mf[3]);
	dl += +0.01003 * sin4deg(0 * mf[0] + 0 * mf[1] + 3 * mf[2] + 0 * mf[3]);
	dl += +0.00855 * sin4deg(4 * mf[0] + 0 * mf[1] - 2 * mf[2] + 0 * mf[3]);

	db  = +5.12817 * sin4deg(0 * mf[0] + 0 * mf[1] + 0 * mf[2] + 1 * mf[3]);
	db += +0.27769 * sin4deg(0 * mf[0] + 0 * mf[1] + 1 * mf[2] - 1 * mf[3]);
	db += +0.28060 * sin4deg(0 * mf[0] + 0 * mf[1] + 1 * mf[2] + 1 * mf[3]);
	db += +0.00882 * sin4deg(0 * mf[0] + 0 * mf[1] + 2 * mf[2] - 1 * mf[3]);
	db += +0.01720 * sin4deg(0 * mf[0] + 0 * mf[1] + 2 * mf[2] + 1 * mf[3]);
	db += +0.04627 * sin4deg(2 * mf[0] + 0 * mf[1] - 1 * mf[2] - 1 * mf[3]);
	db += +0.05541 * sin4deg(2 * mf[0] + 0 * mf[1] - 1 * mf[2] + 1 * mf[3]);
	db += +0.17324 * sin4deg(2 * mf[0] + 0 * mf[1] + 0 * mf[2] - 1 * mf[3]);
	db += +0.03257 * sin4deg(2 * mf[0] + 0 * mf[1] + 0 * mf[2] + 1 * mf[3]);
	db += +0.00927 * sin4deg(2 * mf[0] + 0 * mf[1] + 1 * mf[2] - 1 * mf[3]);

	W1 += dl + 5029.0966 / 3600.0 * T;

	var res = new Array( W1, db );
	return res;
}

function calPositME( T ){
	var lo = 0.0;
	var bo = 0.0;
	var ro = 0.0;
	var Lon = new Array();
	var Lat = new Array();
	var Rad = new Array();

// Mercury's Longitude
	Lon[0]  =     4.40251 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[0] +=     0.40989 * Math.cos( 1.48302 +   26087.90314 * T);
	Lon[0] +=     0.05046 * Math.cos( 4.47785 +   52175.80628 * T);
	Lon[0] +=     0.00855 * Math.cos( 1.16520 +   78263.70942 * T);
	Lon[0] +=     0.00166 * Math.cos( 4.11969 +  104351.61257 * T);
	Lon[0] +=     0.00035 * Math.cos( 0.77931 +  130439.51571 * T);
	Lon[1]  = 26088.14706 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[1] +=     0.01126 * Math.cos( 6.21704 +   26087.90314 * T);
	Lon[1] +=     0.00303 * Math.cos( 3.05565 +   52175.80628 * T);
	Lon[1] +=     0.00081 * Math.cos( 6.10455 +   78263.70942 * T);
	Lon[1] +=     0.00021 * Math.cos( 2.83532 +  104351.61257 * T);
	Lon[2]  =     0.00053 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[2] +=     0.00017 * Math.cos( 4.69072 +   26087.90314 * T);
// Mercury's Latitude
	Lat[0]  =     0.11738 * Math.cos( 1.98357 +   26087.90314 * T);
	Lat[0] +=     0.02388 * Math.cos( 5.03739 +   52175.80628 * T);
	Lat[0] +=     0.01223 * Math.cos( 3.14159 +       0.00000 * T);
	Lat[0] +=     0.00543 * Math.cos( 1.79644 +   78263.70942 * T);
	Lat[0] +=     0.00130 * Math.cos( 4.83233 +  104351.61257 * T);
	Lat[0] +=     0.00032 * Math.cos( 1.58088 +  130439.51571 * T);
	Lat[1]  =     0.00429 * Math.cos( 3.50170 +   26087.90314 * T);
	Lat[1] +=     0.00146 * Math.cos( 3.14159 +       0.00000 * T);
	Lat[1] +=     0.00023 * Math.cos( 0.01515 +   52175.80628 * T);
	Lat[1] +=     0.00011 * Math.cos( 0.48540 +   78263.70942 * T);
	Lat[2]  =     0.00012 * Math.cos( 4.79066 +   26087.90314 * T);
// Mercury's Radius Vector
	Rad[0]  =     0.39528 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[0] +=     0.07834 * Math.cos( 6.19234 +   26087.90314 * T);
	Rad[0] +=     0.00796 * Math.cos( 2.95990 +   52175.80628 * T);
	Rad[0] +=     0.00121 * Math.cos( 6.01064 +   78263.70942 * T);
	Rad[0] +=     0.00022 * Math.cos( 2.77820 +  104351.61257 * T);
	Rad[1]  =     0.00217 * Math.cos( 4.65617 +   26087.90314 * T);
	Rad[1] +=     0.00044 * Math.cos( 1.42386 +   52175.80628 * T);
	Rad[1] +=     0.00010 * Math.cos( 4.47466 +   78263.70942 * T);

	lo = mod360( calVsopTerm( T, Lon ) / deg2rad);
	bo = calVsopTerm( T, Lat ) / deg2rad;
	ro = calVsopTerm( T, Rad );

	var res = new Array( lo, bo, ro );
	return res;
}

function calPositVE( T ){
	var lo = 0.0;
	var bo = 0.0;
	var ro = 0.0;
	var Lon = new Array();
	var Lat = new Array();
	var Rad = new Array();

// Venus's Longitude
	Lon[0]  =     3.17615 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[0] +=     0.01354 * Math.cos( 5.59313 +   10213.28555 * T);
	Lon[0] +=     0.00090 * Math.cos( 5.30650 +   20426.57109 * T);
	Lon[1]  = 10213.52943 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[1] +=     0.00096 * Math.cos( 2.46424 +   10213.28555 * T);
	Lon[1] +=     0.00014 * Math.cos( 0.51625 +   20426.57109 * T);
	Lon[2]  =     0.00054 * Math.cos( 0.00000 +       0.00000 * T);
// Venus's Latitude
	Lat[0]  =     0.05924 * Math.cos( 0.26703 +   10213.28555 * T);
	Lat[0] +=     0.00040 * Math.cos( 1.14737 +   20426.57109 * T);
	Lat[0] +=     0.00033 * Math.cos( 3.14159 +       0.00000 * T);
	Lat[1]  =     0.00513 * Math.cos( 1.80364 +   10213.28555 * T);
	Lat[2]  =     0.00022 * Math.cos( 3.38509 +   10213.28555 * T);
// Venus's Radius Vector
	Rad[0]  =     0.72335 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[0] +=     0.00490 * Math.cos( 4.02152 +   10213.28555 * T);
	Rad[1]  =     0.00035 * Math.cos( 0.89199 +   10213.28555 * T);

	lo = mod360( calVsopTerm( T, Lon ) / deg2rad);
	bo = calVsopTerm( T, Lat ) / deg2rad;
	ro = calVsopTerm( T, Rad );

	var res = new Array( lo, bo, ro );
	return res;
}

function calPositMA( T ){
	var lo = 0.0;
	var bo = 0.0;
	var ro = 0.0;
	var Lon = new Array();
	var Lat = new Array();
	var Rad = new Array();

// Mars's Longitude
	Lon[0]  =     6.20348 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[0] +=     0.18656 * Math.cos( 5.05037 +    3340.61243 * T);
	Lon[0] +=     0.01108 * Math.cos( 5.40100 +    6681.22485 * T);
	Lon[0] +=     0.00092 * Math.cos( 5.75479 +   10021.83728 * T);
	Lon[0] +=     0.00028 * Math.cos( 5.97050 +       3.52312 * T);
	Lon[0] +=     0.00011 * Math.cos( 2.93959 +    2281.23050 * T);
	Lon[0] +=     0.00012 * Math.cos( 0.84956 +    2810.92146 * T);
	Lon[1]  =  3340.85627 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[1] +=     0.01458 * Math.cos( 3.60426 +    3340.61243 * T);
	Lon[1] +=     0.00165 * Math.cos( 3.92631 +    6681.22485 * T);
	Lon[1] +=     0.00020 * Math.cos( 4.26594 +   10021.83728 * T);
	Lon[2]  =     0.00058 * Math.cos( 2.04979 +    3340.61243 * T);
	Lon[2] +=     0.00054 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[2] +=     0.00014 * Math.cos( 2.45742 +    6681.22485 * T);
// Mars's Latitude
	Lat[0]  =     0.03197 * Math.cos( 3.76832 +    3340.61243 * T);
	Lat[0] +=     0.00298 * Math.cos( 4.10617 +    6681.22485 * T);
	Lat[0] +=     0.00289 * Math.cos( 0.00000 +       0.00000 * T);
	Lat[0] +=     0.00031 * Math.cos( 4.44651 +   10021.83728 * T);
	Lat[1]  =     0.00350 * Math.cos( 5.36848 +    3340.61243 * T);
	Lat[1] +=     0.00014 * Math.cos( 3.14159 +       0.00000 * T);
	Lat[1] +=     0.00010 * Math.cos( 5.47878 +    6681.22485 * T);
	Lat[2]  =     0.00017 * Math.cos( 0.60221 +    3340.61243 * T);
// Mars's Radius Vector
	Rad[0]  =     1.53033 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[0] +=     0.14185 * Math.cos( 3.47971 +    3340.61243 * T);
	Rad[0] +=     0.00661 * Math.cos( 3.81783 +    6681.22485 * T);
	Rad[0] +=     0.00046 * Math.cos( 4.15595 +   10021.83728 * T);
	Rad[1]  =     0.01107 * Math.cos( 2.03251 +    3340.61243 * T);
	Rad[1] +=     0.00103 * Math.cos( 2.37072 +    6681.22485 * T);
	Rad[1] +=     0.00013 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[1] +=     0.00011 * Math.cos( 2.70888 +   10021.83728 * T);
	Rad[2]  =     0.00044 * Math.cos( 0.47931 +    3340.61243 * T);

	lo = mod360( calVsopTerm( T, Lon ) / deg2rad);
	bo = calVsopTerm( T, Lat ) / deg2rad;
	ro = calVsopTerm( T, Rad );

	var res = new Array( lo, bo, ro );
	return res;
}

function calPositJU( T ){
	var lo = 0.0;
	var bo = 0.0;
	var ro = 0.0;
	var Lon = new Array();
	var Lat = new Array();
	var Rad = new Array();

// Jupiter's Longitude
	Lon[0]  =     0.59955 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[0] +=     0.09696 * Math.cos( 5.06192 +     529.69097 * T);
	Lon[0] +=     0.00574 * Math.cos( 1.44406 +       7.11355 * T);
	Lon[0] +=     0.00306 * Math.cos( 5.41735 +    1059.38193 * T);
	Lon[0] +=     0.00097 * Math.cos( 4.14265 +     632.78374 * T);
	Lon[0] +=     0.00073 * Math.cos( 3.64043 +     522.57742 * T);
	Lon[0] +=     0.00064 * Math.cos( 3.41145 +     103.09277 * T);
	Lon[0] +=     0.00040 * Math.cos( 2.29377 +     419.48464 * T);
	Lon[0] +=     0.00039 * Math.cos( 1.27232 +     316.39187 * T);
	Lon[0] +=     0.00028 * Math.cos( 1.78455 +     536.80451 * T);
	Lon[0] +=     0.00014 * Math.cos( 5.77481 +    1589.07290 * T);
	Lon[1]  =   529.93481 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[1] +=     0.00490 * Math.cos( 4.22067 +     529.69097 * T);
	Lon[1] +=     0.00229 * Math.cos( 6.02647 +       7.11355 * T);
	Lon[1] +=     0.00028 * Math.cos( 4.57266 +    1059.38193 * T);
	Lon[1] +=     0.00021 * Math.cos( 5.45939 +     522.57742 * T);
	Lon[1] +=     0.00012 * Math.cos( 0.16986 +     536.80451 * T);
	Lon[2]  =     0.00047 * Math.cos( 4.32148 +       7.11355 * T);
	Lon[2] +=     0.00031 * Math.cos( 2.93021 +     529.69097 * T);
	Lon[2] +=     0.00039 * Math.cos( 0.00000 +       0.00000 * T);
// Jupiter's Latitude
	Lat[0]  =     0.02269 * Math.cos( 3.55853 +     529.69097 * T);
	Lat[0] +=     0.00110 * Math.cos( 3.90809 +    1059.38193 * T);
	Lat[0] +=     0.00110 * Math.cos( 0.00000 +       0.00000 * T);
	Lat[1]  =     0.00177 * Math.cos( 5.70166 +     529.69097 * T);
// Jupiter's Radius Vector
	Rad[0]  =     5.20887 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[0] +=     0.25209 * Math.cos( 3.49109 +     529.69097 * T);
	Rad[0] +=     0.00611 * Math.cos( 3.84115 +    1059.38193 * T);
	Rad[0] +=     0.00282 * Math.cos( 2.57420 +     632.78374 * T);
	Rad[0] +=     0.00188 * Math.cos( 2.07590 +     522.57742 * T);
	Rad[0] +=     0.00087 * Math.cos( 0.71001 +     419.48464 * T);
	Rad[0] +=     0.00072 * Math.cos( 0.21466 +     536.80451 * T);
	Rad[0] +=     0.00066 * Math.cos( 5.97996 +     316.39187 * T);
	Rad[0] +=     0.00029 * Math.cos( 1.67759 +     103.09277 * T);
	Rad[0] +=     0.00030 * Math.cos( 2.16132 +     949.17561 * T);
	Rad[0] +=     0.00023 * Math.cos( 3.54023 +     735.87651 * T);
	Rad[0] +=     0.00022 * Math.cos( 4.19363 +    1589.07290 * T);
	Rad[0] +=     0.00024 * Math.cos( 0.27458 +       7.11355 * T);
	Rad[0] +=     0.00013 * Math.cos( 2.96043 +    1162.47470 * T);
	Rad[0] +=     0.00010 * Math.cos( 1.90670 +     206.18555 * T);
	Rad[0] +=     0.00013 * Math.cos( 2.71550 +    1052.26838 * T);
	Rad[1]  =     0.01272 * Math.cos( 2.64938 +     529.69097 * T);
	Rad[1] +=     0.00062 * Math.cos( 3.00076 +    1059.38193 * T);
	Rad[1] +=     0.00053 * Math.cos( 3.89718 +     522.57742 * T);
	Rad[1] +=     0.00031 * Math.cos( 4.88277 +     536.80451 * T);
	Rad[1] +=     0.00041 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[1] +=     0.00012 * Math.cos( 2.41330 +     419.48464 * T);
	Rad[2]  =     0.00080 * Math.cos( 1.35866 +     529.69097 * T);

	lo = mod360( calVsopTerm( T, Lon ) / deg2rad);
	bo = calVsopTerm( T, Lat ) / deg2rad;
	ro = calVsopTerm( T, Rad );

	var res = new Array( lo, bo, ro );
	return res;
}

function calPositSA( T ){
	var lo = 0.0;
	var bo = 0.0;
	var ro = 0.0;
	var Lon = new Array();
	var Lat = new Array();
	var Rad = new Array();

// Saturn's Longitude
	Lon[0]  =     0.87401 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[0] +=     0.11108 * Math.cos( 3.96205 +     213.29910 * T);
	Lon[0] +=     0.01414 * Math.cos( 4.58582 +       7.11355 * T);
	Lon[0] +=     0.00398 * Math.cos( 0.52112 +     206.18555 * T);
	Lon[0] +=     0.00351 * Math.cos( 3.30330 +     426.59819 * T);
	Lon[0] +=     0.00207 * Math.cos( 0.24658 +     103.09277 * T);
	Lon[0] +=     0.00079 * Math.cos( 3.84007 +     220.41264 * T);
	Lon[0] +=     0.00024 * Math.cos( 4.66977 +     110.20632 * T);
	Lon[0] +=     0.00017 * Math.cos( 0.43719 +     419.48464 * T);
	Lon[0] +=     0.00015 * Math.cos( 5.76903 +     316.39187 * T);
	Lon[0] +=     0.00016 * Math.cos( 0.93809 +     632.78374 * T);
	Lon[0] +=     0.00015 * Math.cos( 1.56519 +       3.93215 * T);
	Lon[0] +=     0.00013 * Math.cos( 4.44891 +      14.22709 * T);
	Lon[0] +=     0.00015 * Math.cos( 2.71670 +     639.89729 * T);
	Lon[0] +=     0.00013 * Math.cos( 5.98119 +      11.04570 * T);
	Lon[0] +=     0.00011 * Math.cos( 3.12940 +     202.25340 * T);
	Lon[1]  =   213.54296 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[1] +=     0.01297 * Math.cos( 1.82821 +     213.29910 * T);
	Lon[1] +=     0.00564 * Math.cos( 2.88500 +       7.11355 * T);
	Lon[1] +=     0.00098 * Math.cos( 1.08070 +     426.59819 * T);
	Lon[1] +=     0.00108 * Math.cos( 2.27770 +     206.18555 * T);
	Lon[1] +=     0.00040 * Math.cos( 2.04128 +     220.41264 * T);
	Lon[1] +=     0.00020 * Math.cos( 1.27955 +     103.09277 * T);
	Lon[1] +=     0.00011 * Math.cos( 2.74880 +      14.22709 * T);
	Lon[2]  =     0.00116 * Math.cos( 1.17988 +       7.11355 * T);
	Lon[2] +=     0.00092 * Math.cos( 0.07425 +     213.29910 * T);
	Lon[2] +=     0.00091 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[2] +=     0.00015 * Math.cos( 4.06492 +     206.18555 * T);
	Lon[2] +=     0.00011 * Math.cos( 0.25778 +     220.41264 * T);
	Lon[2] +=     0.00011 * Math.cos( 5.40964 +     426.59819 * T);
	Lon[3]  =     0.00016 * Math.cos( 5.73945 +       7.11355 * T);
// Saturn's Latitude
	Lat[0]  =     0.04331 * Math.cos( 3.60284 +     213.29910 * T);
	Lat[0] +=     0.00240 * Math.cos( 2.85238 +     426.59819 * T);
	Lat[0] +=     0.00085 * Math.cos( 0.00000 +       0.00000 * T);
	Lat[0] +=     0.00031 * Math.cos( 3.48442 +     220.41264 * T);
	Lat[0] +=     0.00034 * Math.cos( 0.57297 +     206.18555 * T);
	Lat[0] +=     0.00015 * Math.cos( 2.11847 +     639.89729 * T);
	Lat[0] +=     0.00010 * Math.cos( 5.79003 +     419.48464 * T);
	Lat[1]  =     0.00398 * Math.cos( 5.33290 +     213.29910 * T);
	Lat[1] +=     0.00049 * Math.cos( 3.14159 +       0.00000 * T);
	Lat[1] +=     0.00019 * Math.cos( 6.09919 +     426.59819 * T);
	Lat[1] +=     0.00015 * Math.cos( 2.30586 +     206.18555 * T);
	Lat[1] +=     0.00010 * Math.cos( 1.69675 +     220.41264 * T);
	Lat[2]  =     0.00021 * Math.cos( 0.50482 +     213.29910 * T);
// Saturn's Radius Vector
	Rad[0]  =     9.55758 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[0] +=     0.52921 * Math.cos( 2.39226 +     213.29910 * T);
	Rad[0] +=     0.01874 * Math.cos( 5.23550 +     206.18555 * T);
	Rad[0] +=     0.01465 * Math.cos( 1.64763 +     426.59819 * T);
	Rad[0] +=     0.00822 * Math.cos( 5.93520 +     316.39187 * T);
	Rad[0] +=     0.00548 * Math.cos( 5.01533 +     103.09277 * T);
	Rad[0] +=     0.00372 * Math.cos( 2.27115 +     220.41264 * T);
	Rad[0] +=     0.00362 * Math.cos( 3.13904 +       7.11355 * T);
	Rad[0] +=     0.00141 * Math.cos( 5.70407 +     632.78374 * T);
	Rad[0] +=     0.00109 * Math.cos( 3.29314 +     110.20632 * T);
	Rad[0] +=     0.00069 * Math.cos( 5.94100 +     419.48464 * T);
	Rad[0] +=     0.00061 * Math.cos( 0.94038 +     639.89729 * T);
	Rad[0] +=     0.00049 * Math.cos( 1.55733 +     202.25340 * T);
	Rad[0] +=     0.00034 * Math.cos( 0.19519 +     277.03499 * T);
	Rad[0] +=     0.00032 * Math.cos( 5.47085 +     949.17561 * T);
	Rad[0] +=     0.00021 * Math.cos( 0.46349 +     735.87651 * T);
	Rad[0] +=     0.00021 * Math.cos( 1.52103 +     433.71174 * T);
	Rad[0] +=     0.00021 * Math.cos( 5.33256 +     199.07200 * T);
	Rad[0] +=     0.00015 * Math.cos( 3.05944 +     529.69097 * T);
	Rad[0] +=     0.00014 * Math.cos( 2.60434 +     323.50542 * T);
	Rad[0] +=     0.00012 * Math.cos( 5.98051 +     846.08283 * T);
	Rad[0] +=     0.00011 * Math.cos( 1.73106 +     522.57742 * T);
	Rad[0] +=     0.00013 * Math.cos( 1.64892 +     138.51750 * T);
	Rad[0] +=     0.00010 * Math.cos( 5.20476 +    1265.56748 * T);
	Rad[1]  =     0.06183 * Math.cos( 0.25844 +     213.29910 * T);
	Rad[1] +=     0.00507 * Math.cos( 0.71115 +     206.18555 * T);
	Rad[1] +=     0.00341 * Math.cos( 5.79636 +     426.59819 * T);
	Rad[1] +=     0.00188 * Math.cos( 0.47216 +     220.41264 * T);
	Rad[1] +=     0.00186 * Math.cos( 3.14159 +       0.00000 * T);
	Rad[1] +=     0.00144 * Math.cos( 1.40745 +       7.11355 * T);
	Rad[1] +=     0.00050 * Math.cos( 6.01744 +     103.09277 * T);
	Rad[1] +=     0.00021 * Math.cos( 5.09246 +     639.89729 * T);
	Rad[1] +=     0.00020 * Math.cos( 1.17560 +     419.48464 * T);
	Rad[1] +=     0.00019 * Math.cos( 1.60820 +     110.20632 * T);
	Rad[1] +=     0.00013 * Math.cos( 5.94330 +     433.71174 * T);
	Rad[1] +=     0.00014 * Math.cos( 0.75886 +     199.07200 * T);
	Rad[2]  =     0.00437 * Math.cos( 4.78672 +     213.29910 * T);
	Rad[2] +=     0.00072 * Math.cos( 2.50070 +     206.18555 * T);
	Rad[2] +=     0.00050 * Math.cos( 4.97168 +     220.41264 * T);
	Rad[2] +=     0.00043 * Math.cos( 3.86940 +     426.59819 * T);
	Rad[2] +=     0.00030 * Math.cos( 5.96310 +       7.11355 * T);
	Rad[3]  =     0.00020 * Math.cos( 3.02187 +     213.29910 * T);

	lo = mod360( calVsopTerm( T, Lon ) / deg2rad);
	bo = calVsopTerm( T, Lat ) / deg2rad;
	ro = calVsopTerm( T, Rad );

	var res = new Array( lo, bo, ro );
	return res;
}

function calPositUR( T ){
	var lo = 0.0;
	var bo = 0.0;
	var ro = 0.0;
	var Lon = new Array();
	var Lat = new Array();
	var Rad = new Array();

// Uranus's Longitude
	Lon[0]  =     5.48129 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[0] +=     0.09260 * Math.cos( 0.89106 +      74.78160 * T);
	Lon[0] +=     0.01504 * Math.cos( 3.62719 +       1.48447 * T);
	Lon[0] +=     0.00366 * Math.cos( 1.89962 +      73.29713 * T);
	Lon[0] +=     0.00272 * Math.cos( 3.35824 +     149.56320 * T);
	Lon[0] +=     0.00070 * Math.cos( 5.39254 +      63.73590 * T);
	Lon[0] +=     0.00069 * Math.cos( 6.09292 +      76.26607 * T);
	Lon[0] +=     0.00062 * Math.cos( 2.26952 +       2.96895 * T);
	Lon[0] +=     0.00062 * Math.cos( 2.85099 +      11.04570 * T);
	Lon[0] +=     0.00026 * Math.cos( 3.14152 +      71.81265 * T);
	Lon[0] +=     0.00026 * Math.cos( 6.11380 +     454.90937 * T);
	Lon[0] +=     0.00021 * Math.cos( 4.36059 +     148.07872 * T);
	Lon[0] +=     0.00018 * Math.cos( 1.74437 +      36.64856 * T);
	Lon[0] +=     0.00015 * Math.cos( 4.73732 +       3.93215 * T);
	Lon[0] +=     0.00011 * Math.cos( 5.82682 +     224.34480 * T);
	Lon[0] +=     0.00011 * Math.cos( 0.48865 +     138.51750 * T);
	Lon[0] +=     0.00010 * Math.cos( 2.95517 +      35.16409 * T);
	Lon[1]  =    75.02543 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[1] +=     0.00154 * Math.cos( 5.24202 +      74.78160 * T);
	Lon[1] +=     0.00024 * Math.cos( 1.71256 +       1.48447 * T);
	Lon[2]  =     0.00053 * Math.cos( 0.00000 +       0.00000 * T);
// Uranus's Latitude
	Lat[0]  =     0.01346 * Math.cos( 2.61878 +      74.78160 * T);
	Lat[0] +=     0.00062 * Math.cos( 5.08111 +     149.56320 * T);
	Lat[0] +=     0.00062 * Math.cos( 3.14159 +       0.00000 * T);
	Lat[0] +=     0.00010 * Math.cos( 1.61604 +      76.26607 * T);
	Lat[0] +=     0.00010 * Math.cos( 0.57630 +      73.29713 * T);
	Lat[1]  =     0.00206 * Math.cos( 4.12394 +      74.78160 * T);
// Uranus's Radius Vector
	Rad[0]  =    19.21265 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[0] +=     0.88785 * Math.cos( 5.60378 +      74.78160 * T);
	Rad[0] +=     0.03441 * Math.cos( 0.32836 +      73.29713 * T);
	Rad[0] +=     0.02056 * Math.cos( 1.78295 +     149.56320 * T);
	Rad[0] +=     0.00649 * Math.cos( 4.52247 +      76.26607 * T);
	Rad[0] +=     0.00602 * Math.cos( 3.86004 +      63.73590 * T);
	Rad[0] +=     0.00496 * Math.cos( 1.40140 +     454.90937 * T);
	Rad[0] +=     0.00339 * Math.cos( 1.58003 +     138.51750 * T);
	Rad[0] +=     0.00244 * Math.cos( 1.57087 +      71.81265 * T);
	Rad[0] +=     0.00191 * Math.cos( 1.99809 +       1.48447 * T);
	Rad[0] +=     0.00162 * Math.cos( 2.79138 +     148.07872 * T);
	Rad[0] +=     0.00144 * Math.cos( 1.38369 +      11.04570 * T);
	Rad[0] +=     0.00093 * Math.cos( 0.17437 +      36.64856 * T);
	Rad[0] +=     0.00071 * Math.cos( 4.24509 +     224.34480 * T);
	Rad[0] +=     0.00090 * Math.cos( 3.66105 +     109.94569 * T);
	Rad[0] +=     0.00039 * Math.cos( 1.66971 +      70.84945 * T);
	Rad[0] +=     0.00047 * Math.cos( 1.39977 +      35.16409 * T);
	Rad[0] +=     0.00039 * Math.cos( 3.36235 +     277.03499 * T);
	Rad[0] +=     0.00037 * Math.cos( 3.88649 +     146.59425 * T);
	Rad[0] +=     0.00030 * Math.cos( 0.70100 +     151.04767 * T);
	Rad[0] +=     0.00029 * Math.cos( 3.18056 +      77.75054 * T);
	Rad[0] +=     0.00020 * Math.cos( 1.55589 +     202.25340 * T);
	Rad[0] +=     0.00026 * Math.cos( 5.25656 +     380.12777 * T);
	Rad[0] +=     0.00026 * Math.cos( 3.78538 +      85.82730 * T);
	Rad[0] +=     0.00023 * Math.cos( 0.72519 +     529.69097 * T);
	Rad[0] +=     0.00020 * Math.cos( 2.79640 +      70.32818 * T);
	Rad[0] +=     0.00018 * Math.cos( 0.55455 +       2.96895 * T);
	Rad[0] +=     0.00012 * Math.cos( 5.96039 +     127.47180 * T);
	Rad[0] +=     0.00015 * Math.cos( 4.90434 +     108.46122 * T);
	Rad[0] +=     0.00011 * Math.cos( 0.43774 +      65.22037 * T);
	Rad[0] +=     0.00016 * Math.cos( 5.35405 +      38.13304 * T);
	Rad[0] +=     0.00011 * Math.cos( 1.42105 +     213.29910 * T);
	Rad[0] +=     0.00012 * Math.cos( 3.29826 +       3.93215 * T);
	Rad[0] +=     0.00012 * Math.cos( 1.75044 +     984.60033 * T);
	Rad[0] +=     0.00013 * Math.cos( 2.62154 +     111.43016 * T);
	Rad[0] +=     0.00012 * Math.cos( 0.99343 +      52.69020 * T);
	Rad[1]  =     0.01480 * Math.cos( 3.67206 +      74.78160 * T);
	Rad[1] +=     0.00071 * Math.cos( 6.22601 +      63.73590 * T);
	Rad[1] +=     0.00069 * Math.cos( 6.13411 +     149.56320 * T);
	Rad[1] +=     0.00021 * Math.cos( 5.24625 +      11.04570 * T);
	Rad[1] +=     0.00021 * Math.cos( 2.60177 +      76.26607 * T);
	Rad[1] +=     0.00024 * Math.cos( 3.14159 +       0.00000 * T);
	Rad[1] +=     0.00011 * Math.cos( 0.01848 +      70.84945 * T);
	Rad[2]  =     0.00022 * Math.cos( 0.69953 +      74.78160 * T);

	lo = mod360( calVsopTerm( T, Lon ) / deg2rad);
	bo = calVsopTerm( T, Lat ) / deg2rad;
	ro = calVsopTerm( T, Rad );

	var res = new Array( lo, bo, ro );
	return res;
}

function calPositNE( T ){
	var lo = 0.0;
	var bo = 0.0;
	var ro = 0.0;
	var Lon = new Array();
	var Lat = new Array();
	var Rad = new Array();

// Neptune's Longitude
	Lon[0]  =     5.31189 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[0] +=     0.01798 * Math.cos( 2.90101 +      38.13304 * T);
	Lon[0] +=     0.01020 * Math.cos( 0.48581 +       1.48447 * T);
	Lon[0] +=     0.00125 * Math.cos( 4.83008 +      36.64856 * T);
	Lon[0] +=     0.00042 * Math.cos( 5.41055 +       2.96895 * T);
	Lon[0] +=     0.00038 * Math.cos( 6.09222 +      35.16409 * T);
	Lon[0] +=     0.00034 * Math.cos( 1.24489 +      76.26607 * T);
	Lon[0] +=     0.00016 * Math.cos( 0.00008 +     491.55793 * T);
	Lon[1]  =    38.37688 * Math.cos( 0.00000 +       0.00000 * T);
	Lon[1] +=     0.00017 * Math.cos( 4.86319 +       1.48447 * T);
	Lon[1] +=     0.00016 * Math.cos( 2.27923 +      38.13304 * T);
	Lon[2]  =     0.00054 * Math.cos( 0.00000 +       0.00000 * T);
// Neptune's Latitude
	Lat[0]  =     0.03089 * Math.cos( 1.44104 +      38.13304 * T);
	Lat[0] +=     0.00028 * Math.cos( 5.91272 +      76.26607 * T);
	Lat[0] +=     0.00028 * Math.cos( 0.00000 +       0.00000 * T);
	Lat[0] +=     0.00015 * Math.cos( 2.52124 +      36.64856 * T);
	Lat[0] +=     0.00015 * Math.cos( 3.50877 +      39.61751 * T);
	Lat[1]  =     0.00227 * Math.cos( 3.80793 +      38.13304 * T);
	Lat[2]  =     0.00010 * Math.cos( 5.57124 +      38.13304 * T);
// Neptune's Radius Vector
	Rad[0]  =    30.07013 * Math.cos( 0.00000 +       0.00000 * T);
	Rad[0] +=     0.27062 * Math.cos( 1.32999 +      38.13304 * T);
	Rad[0] +=     0.01692 * Math.cos( 3.25186 +      36.64856 * T);
	Rad[0] +=     0.00808 * Math.cos( 5.18593 +       1.48447 * T);
	Rad[0] +=     0.00538 * Math.cos( 4.52114 +      35.16409 * T);
	Rad[0] +=     0.00496 * Math.cos( 1.57106 +     491.55793 * T);
	Rad[0] +=     0.00275 * Math.cos( 1.84552 +     175.16606 * T);
	Rad[0] +=     0.00135 * Math.cos( 3.37221 +      39.61751 * T);
	Rad[0] +=     0.00122 * Math.cos( 5.79754 +      76.26607 * T);
	Rad[0] +=     0.00101 * Math.cos( 0.37703 +      73.29713 * T);
	Rad[0] +=     0.00070 * Math.cos( 3.79617 +       2.96895 * T);
	Rad[0] +=     0.00047 * Math.cos( 5.74938 +      33.67962 * T);
	Rad[0] +=     0.00025 * Math.cos( 0.50802 +     109.94569 * T);
	Rad[0] +=     0.00017 * Math.cos( 1.59422 +      71.81265 * T);
	Rad[0] +=     0.00014 * Math.cos( 1.07786 +      74.78160 * T);
	Rad[0] +=     0.00012 * Math.cos( 1.92062 +    1021.24889 * T);
	Rad[1]  =     0.00236 * Math.cos( 0.70498 +      38.13304 * T);
	Rad[1] +=     0.00013 * Math.cos( 3.32015 +       1.48447 * T);

	lo = mod360( calVsopTerm( T, Lon ) / deg2rad);
	bo = calVsopTerm( T, Lat ) / deg2rad;
	ro = calVsopTerm( T, Rad );

	var res = new Array( lo, bo, ro );
	return res;
}

function calPositPL_mee( T ){
	var lo = 238.9581 + 144.96 * T;
	var bo =  -3.9082;
	var ro =  40.7241;

	var Ju = mod360( 34.35 + 3034.9057 * T);
	var Sa = mod360( 50.58 + 1222.1138 * T);
	var Pl = mod360(238.96 +  144.9600 * T);

// Pluto's Longitude
	lo += -19.7998 * sin4deg(Pl * 1.0) + 19.8501 * cos4deg(Pl * 1.0);
	lo +=   0.8971 * sin4deg(Pl * 2.0) -  4.9548 * cos4deg(Pl * 2.0);
	lo +=   0.6111 * sin4deg(Pl * 3.0) +  1.2110 * cos4deg(Pl * 3.0);
	lo +=  -0.3412 * sin4deg(Pl * 4.0) -  0.1896 * cos4deg(Pl * 4.0);
	lo +=   0.1293 * sin4deg(Pl * 5.0) -  0.0350 * cos4deg(Pl * 5.0);
	lo +=  -0.0382 * sin4deg(Pl * 6.0) +  0.0309 * cos4deg(Pl * 6.0);
	lo +=   0.0204 * sin4deg(Sa -  Pl) -  0.0100 * cos4deg(Sa -  Pl);
	lo +=  -0.0041 * sin4deg(Sa * 1.0) -  0.0051 * cos4deg(Sa * 1.0);
	lo +=  -0.0060 * sin4deg(Sa +  Pl) -  0.0033 * cos4deg(Sa +  Pl);

// Pluto's Latitude
	bo +=  -5.4529 * sin4deg(Pl * 1.0) - 14.9749 * cos4deg(Pl * 1.0);
	bo +=   3.5278 * sin4deg(Pl * 2.0) +  1.6728 * cos4deg(Pl * 2.0);
	bo +=  -1.0507 * sin4deg(Pl * 3.0) +  0.3276 * cos4deg(Pl * 3.0);
	bo +=   0.1787 * sin4deg(Pl * 4.0) -  0.2922 * cos4deg(Pl * 4.0);
	bo +=   0.0187 * sin4deg(Pl * 5.0) +  0.1003 * cos4deg(Pl * 5.0);
	bo +=  -0.0307 * sin4deg(Pl * 6.0) -  0.0258 * cos4deg(Pl * 6.0);
	bo +=   0.0049 * sin4deg(Sa -  Pl) +  0.0112 * cos4deg(Sa -  Pl);
	bo +=   0.0020 * sin4deg(Sa +  Pl) -  0.0008 * cos4deg(Sa +  Pl);

// Pluto's Radius Vector
	ro +=   6.6865 * sin4deg(Pl * 1.0) +  6.8952 * cos4deg(Pl * 1.0);
	ro +=  -1.1828 * sin4deg(Pl * 2.0) -  0.0332 * cos4deg(Pl * 2.0);
	ro +=   0.1593 * sin4deg(Pl * 3.0) -  0.1439 * cos4deg(Pl * 3.0);
	ro +=  -0.0018 * sin4deg(Pl * 4.0) +  0.0483 * cos4deg(Pl * 4.0);
	ro +=  -0.0065 * sin4deg(Pl * 5.0) -  0.0085 * cos4deg(Pl * 5.0);
	ro +=   0.0031 * sin4deg(Pl * 6.0) -  0.0006 * cos4deg(Pl * 6.0);
	ro +=  -0.0006 * sin4deg(Sa -  Pl) -  0.0022 * cos4deg(Sa -  Pl);
	ro +=   0.0005 * sin4deg(Sa * 1.0) -  0.0004 * cos4deg(Sa * 1.0);
	ro +=  -0.0002 * sin4deg(Sa +  Pl);

	var res = new Array( lo, bo, ro );
	return res;
}

// Taken from ftp://cyrano-se.obspm.fr/pub/3_solar_system/3_pluto/notice.txt
function calPositPL_obspm( T ) {
	var T2 = T  * T;
	var T3 = T2 * T;

	var a = 39.5404;
       a += +0.004471   * T;
       a += +0.0315           * Math.sin(  2.545150 * T + 1.8271 );
       a += +0.0490           * Math.sin( 18.787117 * T + 4.4687 );
       a += +0.0536           * Math.sin( 47.883664 * T + 3.8553 );
       a += +0.2141           * Math.sin( 50.426476 * T + 4.1802 );
       a += +0.0004           * Math.sin( 47.883664 * T + 4.1379 );
       a += +0.0066           * Math.sin( 50.426476 * T + 5.1987 );
       a += +0.0091           * Math.sin( 47.883664 * T + 5.6881 );
       a += +0.0200           * Math.sin( 50.426476 * T + 6.0165 );
       a += +0.000018   * T   * Math.sin( 47.883664 * T + 4.1379 );
       a += +0.000330   * T   * Math.sin( 50.426476 * T + 5.1987 );
       a += +0.000905   * T   * Math.sin( 47.883664 * T + 5.6881 );
       a += +0.001990   * T   * Math.sin( 50.426476 * T + 6.0165 );
       a += +0.00002256 * T2  * Math.sin( 47.883664 * T + 5.6881 );
       a += +0.00004958 * T2  * Math.sin( 50.426476 * T + 6.0165 );

	var l =  4.1702;
       l += +2.533953     * T;
       l += -0.00021295   * T2;
       l += +0.0000001231 * T3;
       l += +0.0014            * Math.sin(  0.199159 * T + 5.8539 );
       l += +0.0050            * Math.sin(  0.364944 * T + 1.2137 );
       l += +0.0055            * Math.sin(  0.397753 * T + 4.9469 );
       l += +0.0002            * Math.sin(  2.543029 * T + 3.0186 );
       l += +0.0012            * Math.sin( 18.787098 * T + 3.4938 );
       l += +0.0008            * Math.sin( 18.817229 * T + 2.0097 );
       l += +0.0050            * Math.sin( 50.426472 * T + 2.6252 );
       l += +0.0015            * Math.sin( 52.969319 * T + 6.1048 );
       l += +0.0008            * Math.sin(292.208471 * T + 4.7603 );
       l += +0.0008            * Math.sin(292.265343 * T + 2.8055 );
       l += +0.0031            * Math.sin(  0.364944 * T + 2.7888 );
       l += +0.0004            * Math.sin(  2.543029 * T + 0.5111 );
       l += +0.0003            * Math.sin( 18.787098 * T + 6.1336 );
       l += +0.0000            * Math.sin( 50.426472 * T + 2.2515 );
       l += +0.0004            * Math.sin(292.208471 * T + 0.0813 );
       l += +0.0004            * Math.sin(292.265343 * T + 1.2477 );
       l += +0.0004            * Math.sin( 50.426472 * T + 4.2694 );
       l += +0.000156   * T    * Math.sin(  0.364944 * T + 2.7888 );
       l += +0.000020   * T    * Math.sin(  2.543029 * T + 0.5111 );
       l += +0.000017   * T    * Math.sin( 18.787098 * T + 6.1336 );
       l += +0.000000   * T    * Math.sin( 50.426472 * T + 2.2515 );
       l += +0.000022   * T    * Math.sin(292.208471 * T + 0.0813 );
       l += +0.000022   * T    * Math.sin(292.265343 * T + 1.2477 );
       l += +0.000044   * T    * Math.sin( 50.426472 * T + 4.2694 );
       l += +0.00000110 * T2   * Math.sin( 50.426472 * T + 4.2694 );
       l /= deg2rad;

    var h = -0.1733;
       h += -0.000013   * T;
       h += +0.0012            * Math.sin(  2.541849 * T + 3.9572 );
       h += +0.0008            * Math.sin( 21.329808 * T + 0.8858 );
       h += +0.0012            * Math.sin( 47.883781 * T + 1.4929 );
       h += +0.0005            * Math.sin( 50.426641 * T + 5.3286 );
       h += +0.0037            * Math.sin( 52.969135 * T + 0.6139 );

    var k = -0.1787;
       k += -0.000070   * T;
       k += +0.0006            * Math.sin(  2.512561 * T + 3.8516 );
       k += +0.0013            * Math.sin(  2.543100 * T + 0.0218 );
       k += +0.0008            * Math.sin( 21.329765 * T + 2.4324 );
       k += +0.0012            * Math.sin( 47.883788 * T + 6.2432 );
       k += +0.0005            * Math.sin( 50.426611 * T + 3.0920 );
       k += +0.0038            * Math.sin( 52.969155 * T + 2.1566 );
       k += +0.0004            * Math.sin(  2.512561 * T + 5.3919 );
       k += +0.000022   * T    * Math.sin(  2.512561 * T + 5.3919 );

    var p = +0.1398;
       p += +0.000007   * T;
       p += +0.0002            * Math.sin( 50.426871 * T + 0.6705 );
       p += +0.0002            * Math.sin( 55.512211 * T + 6.0770 );

    var q = -0.0517;
       q += +0.000020   * T;
       q += +0.0002            * Math.sin( 50.426859 * T + 5.4131 );
       q += +0.0002            * Math.sin( 55.512206 * T + 1.3314 );

	// my( $L, $opi, $omg, $i, $e, $a ) = convertOrbitalElement( $a, $l, $h, $k, $p, $q );
	var orbitalElements = convertOrbitalElement( a, l, h, k, p, q );
	return orbitWork( ...orbitalElements );
}

// 太陽と月の速度
function calSolarVelocity( JD ){
	var T = ( JD - 2451545.0 ) / 365250.0;
	var vel  = 3548.330;
		vel +=  118.568 * sin4deg( 87.5287 + 359993.7286 * T );
	return vel / 3600.0;
}

function calLunarVelocity( JD ){
	var T = ( JD - 2451545.0 ) / 36525.0;
	var mf = new Array();
	var vel;

// D : Mean elongation of the Moon
	mf[0]  = 445267.0 * T;
	mf[0]  = mod360( mf[0] );
	mf[0] +=   0.11151 * T;
	mf[0] -=   0.00163 * T * T;
	mf[0] += 297.85020;
	mf[0]  = mod360( mf[0] );

// l' : Mean anomary of the Sun
	mf[1]  =  35999.0 * T;
	mf[1]  = mod360( mf[1] );
	mf[1] +=   0.05029 * T;
	mf[1] -=   0.00015 * T * T;
	mf[1] += 357.51687;
	mf[1]  = mod360( mf[1] );

// l : Mean anomary of the Moon
	mf[2]  = 477198.0 * T;
	mf[2]  = mod360( mf[2] );
	mf[2] +=   0.86763  * T;
	mf[2] +=   0.008997 * T * T;
	mf[2] += 134.96341;
	mf[2]  = mod360( mf[2] );

// F : Argument of latitude of the Moon
	mf[3]  = 483202.0 * T;
	mf[3]  = mod360( mf[3] );
	mf[3] +=   0.01753 * T;
	mf[3] -=   0.00340 * T * T;
	mf[3] +=  93.27210;
	mf[3]  = mod360( mf[3] );

	vel  = 13.176397;
	vel +=  1.434006 * cos4deg(mf[2]);
	vel +=  0.280135 * cos4deg(2.0 * mf[0]);
	vel +=  0.251632 * cos4deg(2.0 * mf[0] - mf[2]);
	vel +=  0.097420 * cos4deg(2.0 * mf[2]);
	vel -=  0.052799 * cos4deg(2.0 * mf[3]);
	vel +=  0.034848 * cos4deg(2.0 * mf[0] + mf[2]);
	vel +=  0.018732 * cos4deg(2.0 * mf[0] - mf[1]);
	vel +=  0.010316 * cos4deg(2.0 * mf[0] - mf[1] - mf[2]);
	vel +=  0.008649 * cos4deg(mf[1] - mf[2]);
	vel -=  0.008642 * cos4deg(2.0 * mf[3] + mf[2]);
	vel -=  0.007471 * cos4deg(mf[1] + mf[2]);
	vel -=  0.007387 * cos4deg(mf[0]);
	vel +=  0.006864 * cos4deg(3.0 * mf[2]);
	vel +=  0.006650 * cos4deg(4.0 * mf[0] - mf[2]);

	return vel;
}

// ノード、リリス
// This function from "Numerical expressions for precession formulae
// and mean elements for the Moon and the planets" J. L. Simon, et al.,
// Astron. Astrophys., 282, 663-683(1994).
function calPositLuna( JD ){
	var d = JD - 2451545.0;
	var T =  d / 36525.0;
	var D, F, l, l1, omg, opi, DH, LT ;

	omg = mod360(125.0445550 -  0.0529537628 * d + 0.0020761667 * T * T);
	opi = mod360( 83.3532430 +  0.1114308160 * d - 0.0103237778 * T * T);

	D   = mod360(297.8502042 + 12.19074912 * d - 0.0016299722 * T * T);
	F   = mod360( 93.2720993 + 13.22935024 * d - 0.0034029167 * T * T);
	l   = mod360(134.9634114 + 13.06499295 * d + 0.0089970278 * T * T);
	l1  = mod360(357.5291092 +  0.98560028 * d - 0.0001536667 * T * T);

// ノード補正
	DH  = omg;
	DH -= 1.4978 * sin4deg(2.0 * (D - F));
	DH -= 0.1500 * sin4deg(l1);
	DH -= 0.1225 * sin4deg(2.0 * D);
	DH += 0.1175 * sin4deg(2.0 * F);
	DH -= 0.0800 * sin4deg(2.0 * (l - F));
	DH  = mod360(DH);

// リリス補正
	LT  = opi + 180.0;
	LT -= 15.4469 * sin4deg(2.0 * D - l);
	LT -=  9.6419 * sin4deg(2.0 * (D - l));
	LT -=  2.7200 * sin4deg(l);
	LT +=  2.6069 * sin4deg(4.0 * D - 3.0 * l);
	LT +=  2.0847 * sin4deg(4.0 * D - 2.0 * l);
	LT +=  1.4772 * sin4deg(2.0 * D + l);
	LT +=  0.9678 * sin4deg(4.0 * (D - l));
	LT -=  0.9412 * sin4deg(2.0 * D - l1 - l);
	LT -=  0.7028 * sin4deg(6.0 * D - 4.0 * l);
	LT -=  0.6600 * sin4deg(2.0 * D);
	LT -=  0.5764 * sin4deg(2.0 * D - 3.0 * l);
	LT -=  0.5231 * sin4deg(2.0 * l);
	LT -=  0.4822 * sin4deg(6.0 * D - 5.0 * l);
	LT +=  0.4517 * sin4deg(l1);
	LT -=  0.3806 * sin4deg(6.0 * D - 3.0 * l);
	LT  = mod360(LT);

	var luna = new Array( DH, LT );
	return luna;
}

// ASC・MC計算
function calGeoPoint( lst, la, obl ){
	// MC計算
	var MCx = sin4deg(lst);
	var MCy = cos4deg(lst) * cos4deg(obl);
	var MC  = mod360( Math.atan2( MCx, MCy ) / deg2rad );
	if( MC < 0.0 ){
		MC += 360.0;
	}

	// ASC計算
	var ASCx  = cos4deg(lst);
	var ASCy  = -(sin4deg(obl) * tan4deg(la));
	    ASCy -= cos4deg(obl) * sin4deg(lst);
	var ASC   = mod360( Math.atan2( ASCx, ASCy ) / deg2rad );
	if( ASC < 0.0 ){
		ASC += 360.0;
	}

	var res = new Array( ASC, MC );
	return res;
}

/* ========== */

// 小惑星位置計算（ mid: 0 - 4 ）
function calAsteroidPosition( JD, mid ){
	// 接触軌道要素 Chebyshev 近似多項式
	// セレス・パラス・ジュノー・ベスタ・キローンの順
	const table_a = [
		[ 2.76711779e+00,  2.15588896e-04,  4.18512586e-05,  2.26138300e-04,  3.86165691e-05,  1.91170823e-04, -8.39240862e-06,  3.35452977e-05, -1.10608695e-04,  1.78833020e-04, -1.11806922e-04],
		[ 2.77119808e+00, -1.71285605e-04,  2.00062860e-04, -4.63357591e-04,  3.14209339e-04, -4.67291723e-04,  5.23136581e-04,  1.22366585e-03,  1.14800009e-04,  1.00782980e-05,  9.21893412e-05],
		[ 2.66938983e+00, -5.58767630e-04,  9.71892794e-05, -5.25892029e-04,  4.80754712e-05, -4.12944301e-04, -4.21683699e-05, -1.55317615e-04, -7.74511898e-05,  1.33065727e-04,  8.85253545e-05],
		[ 2.36152015e+00, -1.04764702e-04,  1.51345367e-05, -1.24604711e-04,  1.75466175e-05, -1.27884260e-04, -2.82042495e-08, -7.86785081e-05, -9.47050606e-06,  4.50426634e-05, -2.07991972e-06],
		[ 1.36332843e+01, -6.70856570e-02, -5.83311367e-02, -2.55566089e-02, -1.39190695e-02,  7.60072532e-03,  6.18181056e-03,  6.84496732e-03,  1.11875722e-02, -8.61162420e-04, -6.71308839e-04]
	];
	const table_l = [
		[ 1.37451305e+02,  1.36474253e+02,  2.86739521e-04, -3.38100115e-04, -2.83810396e-04, -6.52393123e-04, -9.70412475e-04, -8.52015032e-04,  7.85090698e-04, -2.69285873e-04, -4.53944560e-04],
		[ 1.36602244e+02,  1.36195471e+02, -5.61095275e-03,  1.75277234e-03,  1.99849869e-04,  1.96613577e-03,  1.14023797e-02, -1.96926622e-03, -5.77789611e-03,  3.29420972e-04,  7.04968934e-04],
		[ 1.48034350e+02,  1.44043472e+02,  1.42453884e-03, -2.52520760e-04,  1.82515207e-03, -3.65225255e-04,  2.33525950e-03,  3.08490809e-05,  2.12579241e-03,  8.53758306e-04,  9.27513152e-04],
		[ 1.79311426e+02,  1.73116916e+02, -2.12528722e-04, -6.22949127e-06,  3.61381204e-04, -2.49440160e-04,  9.79735546e-04, -1.20857263e-04,  1.54380738e-03,  1.56449678e-05,  8.19069438e-04],
		[ 1.31825341e+01,  1.24784109e+01,  1.25828123e-02,  1.48639107e-02,  5.45958071e-03,  2.76968634e-03,  2.78518711e-04, -1.57461439e-03, -1.37777312e-03, -9.30931762e-04, -6.13863244e-04]
	];
	const table_h = [
		[ 3.44841967e-02, -2.80369598e-03, -2.77700177e-04, -5.50244058e-04, -4.90367580e-04, -5.54870187e-04, -6.49050387e-04, -5.58184267e-04, -8.28288956e-05, -2.81387461e-04, -1.78969059e-04],
		[ 1.92788854e-01, -4.17600516e-03, -3.53852452e-04,  8.94642819e-05, -2.95771068e-05,  1.50904643e-04,  4.87835447e-04, -2.57755985e-04, -5.06040669e-04,  1.37114802e-04, -9.00980971e-05],
		[ 2.18075322e-01,  3.03175763e-03, -2.04237900e-04,  3.67825969e-04, -4.52055200e-06,  2.59933948e-04,  2.28934806e-04,  1.30738664e-05,  3.12635297e-04, -3.07187433e-04, -9.22044695e-05],
		[-8.61833802e-02, -1.13536520e-03,  6.24925321e-05, -3.84265911e-04,  1.23049486e-04, -4.08800447e-04,  1.84805184e-04, -2.60876512e-04,  2.39209089e-04,  1.06542651e-04,  1.39881925e-04],
		[-0.05742006,     -0.00146158,      0.00160014,     -0.00056073,      0.00106266,      0.00051392,     -0.00065326,      0.00085371,     -0.0011434,       0.00018113,     -0.00093444]
	];
	const table_k = [
		[-6.94987523e-02, -3.56976031e-04,  4.99461528e-05,  3.47613842e-04,  5.71046667e-06,  3.00842486e-04, -9.30292633e-05, -3.81063392e-05, -3.37083364e-04,  3.98651768e-04, -3.12100259e-04],
		[-1.26885608e-01,  3.44407444e-03,  1.87675931e-04, -2.08395160e-04,  2.87142598e-04, -1.94074092e-04,  3.63882223e-04,  7.09527286e-04,  1.31201039e-05,  4.87736223e-05, -4.91413553e-05],
		[ 1.36201199e-01, -2.48177096e-03,  1.92884427e-04,  6.77846984e-04,  7.80635133e-05,  5.25831425e-04, -7.04536645e-05,  1.29070085e-04, -1.23828293e-04, -3.11641283e-04,  4.75774636e-05],
		[-2.37212685e-02,  1.66347359e-03, -4.08010582e-06, -1.06093987e-04, -1.40528262e-04, -8.91935216e-05, -3.68766676e-04, -4.10595162e-05, -5.43769082e-04,  7.30782843e-05, -2.85835916e-04],
		[-3.74756741e-01,  2.07101135e-03,  1.47689886e-03,  2.10497175e-04,  3.83197122e-05, -9.88419764e-04, -5.71096764e-04, -1.48078047e-03, -6.23303012e-04, -3.30756440e-04, -9.48782339e-04]
	];
	const table_p = [
		[ 9.09220870e-02, -5.37497147e-04, -2.04307806e-05,  2.17239615e-05,  3.37683256e-06,  1.50307720e-05,  1.04571373e-05, -2.79958623e-05, -7.37494065e-06,  2.86355438e-05,  1.93835974e-06],
		[ 3.67147349e-02,  5.43921781e-03, -7.14465444e-05,  2.76441434e-05, -6.59724572e-05,  2.76643946e-05, -7.32536480e-05, -9.19004748e-05, -2.51473853e-06, -9.00612465e-06,  1.65482262e-05],
		[ 2.00644037e-02,  3.50101359e-03, -2.68715277e-05, -1.03247623e-04, -1.19970108e-05, -8.09699210e-05,  1.20535685e-05, -2.19946555e-05,  1.70194363e-05,  4.24006842e-05, -7.89530908e-06],
		[ 6.04750810e-02,  2.83747880e-04, -3.49557711e-06,  6.39204512e-06, -5.30809659e-06,  7.30451674e-06, -1.70745057e-05,  5.21230752e-06, -2.65701744e-05, -7.27216097e-07, -1.44525009e-05],
		[-2.95413282e-02,  2.82455135e-04,  6.64898456e-05,  2.94015020e-05, -4.56415088e-07, -3.20204607e-05, -3.10206039e-05, -3.10706092e-05,  1.29270458e-05, -1.15253338e-05,  1.01777489e-05]
	];
	const table_q = [
		[ 1.57391682e-02,  2.35500022e-03,  1.68532656e-05,  5.81613238e-06,  4.89171400e-05,  9.57097837e-06,  7.26537831e-05,  2.66626834e-05, -6.29940204e-06, -9.09627788e-07,  1.44009044e-05],
		[-2.97426707e-01, -5.18639429e-04,  3.61692505e-05, -8.21785552e-05,  5.11353270e-05, -7.68331553e-05,  1.33616115e-04,  1.51115415e-04, -2.65942075e-05,  1.09696084e-05,  4.78558858e-06],
		[-1.11191863e-01,  8.16434116e-04,  1.76558356e-05, -2.28093253e-05,  1.88458405e-05, -2.08074251e-05,  4.55881375e-05, -1.59194286e-05,  5.36771112e-05, -1.83828895e-05,  3.43121527e-06],
		[-1.47823248e-02,  9.50927526e-04,  5.39974031e-07,  1.90785840e-05, -8.00951960e-07,  2.10372511e-05, -3.92981897e-07,  1.44182656e-05, -3.20311655e-07, -3.20630756e-06, -4.34637604e-07],
		[-5.27699356e-02, -3.71957289e-04, -4.77751902e-05, -8.98537573e-05, -1.68400061e-05,  2.27906342e-05,  5.55114272e-06,  2.57456091e-05, -3.02298236e-05,  7.84796059e-06, -3.18100566e-05]
	];

	// 軌道要素から日心位置を算出
	const x = ( JD - 2460675.0 ) / 36525.0 ;
	if ( Math.abs(x) > 1.0 ) {
		return null; // 計算対象範囲外
	}

	const r_a = table_a[ mid ];
	const r_l = table_l[ mid ];
	const r_h = table_h[ mid ];
	const r_k = table_k[ mid ];
	const r_p = table_p[ mid ];
	const r_q = table_q[ mid ];

	const a = calChebyshevPolynomial( x, r_a );
	const l = calChebyshevPolynomial( x, r_l ) / deg2rad;
	const h = calChebyshevPolynomial( x, r_h );
	const k = calChebyshevPolynomial( x, r_k );
	const p = calChebyshevPolynomial( x, r_p );
	const q = calChebyshevPolynomial( x, r_q );

	var orbitalElements = convertOrbitalElement( a, l, h, k, p, q );
	return orbitWork( ...orbitalElements );
}

/* ---- 当面はソーラーリターン、ルナーリターンは使わない。使う時に復活させる
///// Return 計算関数
// Solar Return
function calAfterSolarReturn{
	my($nSu, $date0) = @_;
	my($tJD0) = CalJD(DecodeDate($date0), 0, 0);
	$tJD0 += CorrectTDT($tJD0);
	my($tJD) = $tJD0;
	my($delta, $tSu, $vSu, $bSu, $rSu);
	my($eps) = 1.0 / 1440.0;
	my($isFirst) = 1;

	do{
		if(!$isFirst){
			$tJD += 365.24219;
		} else {
			$isFirst = 0;
		}
		do{
			($tSu, $bSu, $rSu) = CalPositSO(($tJD - 2451545.0) / 365250.0);
			$tSu += CalNutation($JD) / 3600.0;
			$tSu -= 0.005693 / $rSu;
			$vSu = CalSolarVelocity($tJD);
			$delta = angle1($tSu, $nSu) / $vSu;
			$tJD -= $delta;
		}while(abs($delta) > $eps);
	}while($tJD < $tJD0);

	$tJD -= CorrectTDT($tJD);
	CnvCalendar($tJD + 9.0 / 24.0);
}

// Lunar Return
function calAfterLunarReturn{
	my($nMo, $date0) = @_;
	my($tJD0) = CalJD(DecodeDate($date0), 0, 0);
	$tJD0 += CorrectTDT($tJD0);
	my($tJD) = $tJD0;
	my($delta, $tMo, $vMo, $bMo);
	my($eps) = 1.0 / 1440.0;
	my($isFirst) = 1;

	do{
		if(!$isFirst){
			$tJD += 27.321582;
		} else {
			$isFirst = 0;
		}
		do{
			($tMo, $bMo) = CalPositMO(($tJD - 2451545.0) / 36525.0);
			$tMo += CalNutation($JD) / 3600.0;
			$vMo = CalLunarVelocity($tJD);
			$delta = angle1($tMo, $nMo) / $vMo;
			$tJD -= $delta;
		}while(abs($delta) > $eps);
	}while($tJD < $tJD0);

	$tJD -= CorrectTDT($tJD);
	CnvCalendar($tJD + 9.0 / 24.0);
}
*/
