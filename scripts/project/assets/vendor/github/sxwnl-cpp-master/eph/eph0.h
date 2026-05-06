#ifndef EPH_0_H
#define EPH_0_H

#include "../mylib/mystl/static_array.h"

#define _pi	3.14159265358979323846
#define cs_rEar  6378.1366 //地球赤道半径(千米)
#define cs_rEarA (0.99834*cs_rEar) //平均半径
#define cs_ba  0.99664719 //地球极赤半径比
#define cs_ba2  (cs_ba*cs_ba) //地球极赤半径比的平方
#define cs_AU    1.49597870691e8 //天文单位长度(千米)
#define cs_sinP  (cs_rEar/cs_AU)   //sin(太阳视差)
#define cs_PI    asin(cs_sinP) //太阳视差
#define cs_GS  299792.458 //光速(行米/秒)
#define cs_Agx  (cs_AU/cs_GS/86400.0/36525) //每天文单位的光行时间(儒略世纪)
#define rad   (180*3600/_pi) //每弧度的角秒数
#define radd  (180/_pi) //每弧度的度数

#define pi2   (_pi*2)
#define pi_2  (_pi/2)
#define J2000  2451545

#define cs_k  0.2725076 //月亮与地球的半径比(用于半影计算)
#define cs_k2 0.2722810 //月亮与地球的半径比(用于本影计算)
#define cs_k0 109.1222  //太阳与地球的半径比(对应959.64)
#define cs_sMoon  (cs_k*cs_rEar*1.0000036*rad)  //用于月亮视半径计算
#define cs_sMoon2 (cs_k2*cs_rEar*1.0000036*rad) //用于月亮视半径计算
#define cs_sSun  959.64 //用于太阳视半径计算
#define cs_xxHH_DATA 116,584,780,399,378,370,367,367

extern double cs_xxHH[];

double rad2mrad(double v);
double rad2rrad(double v);

mystl::array3 llr2xyz(mystl::array3 JW);
mystl::array3 xyz2llr(mystl::array3 xyz);
mystl::array3 llrConv(mystl::array3 JW, double E);
mystl::array3 CD2DP(mystl::array3 z, double L, double fa, double gst);
double j1_j2(double J1, double W1, double J2, double W2);
mystl::array3 h2g(mystl::array3 z, mystl::array3 a);
double shiChaJ(double gst,double L,double fa,double J,double W);
double hcjj(double t);
double dt_calc(double y);
double dt_T(double t);
mystl::array3 CDllr_J2D(double t, mystl::array3 llr, const char *mx);
mystl::array3 CDllr_D2J(double t, mystl::array3 llr, const char *mx);
mystl::array3 HDllr_J2D(double t, mystl::array3 llr, const char *mx);
mystl::array3 HDllr_D2J(double t, mystl::array3 llr, const char *mx);
double MQC(double h);
double MQC2(double ho);
mystl::array3 parallax(mystl::array3 z, double H, double fa, double high);
mystl::array2 nutation2(double t);
mystl::array2 nutation(double t, int zq);
double nutationLon2(double t);
double XL0_calc(int xt, int zn, double t, int n);
mystl::array3 pluto_coord(double t);
mystl::array3 p_coord(int xt, double t, int n1, int n2, int n3);
mystl::array3 e_coord(double t, int n1, int n2, int n3);
double XL1_calc(int zn, double t, int n);
mystl::array3 m_coord(double t, int n1, int n2, int n3);
double gxc_sunLon(double t);
double gxc_sunLat(double t);
double gxc_moonLon(double t);
double gxc_moonLat(double t);
double E_Lon(double t, int n);
double M_Lon(double t, int n);
double pGST(double T, double dt);
double pGST2(double jd);
double E_v(double t);
double M_v(double t);
double MS_aLon(double t, int Mn, int Sn);
double S_aLon(double t, int n);
double MS_aLon_t(double W);
double S_aLon_t(double W);
double MS_aLon_t2(double W);
double S_aLon_t2(double W);

mystl::array2 moonMinR(double t, bool min);
mystl::array2 moonNode(double t, double asc);
mystl::array2 earthMinR(double t, bool min);

int suoN(double jd);
double sunShengJ(double jd, double L, double fa, int sj);
double pty_zty(double t);
double pty_zty2(double t);
double moonIll(double t);
double moonRad(double r, double h);

#endif