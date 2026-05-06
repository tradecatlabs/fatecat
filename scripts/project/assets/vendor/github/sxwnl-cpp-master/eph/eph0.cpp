#include <cstring>

#include "eph_data.h"
#include "eph0.h"
#include "../mylib/math_patch.h"

static inline int int2(double v) {return (int)floor(v);};

static double preceTab_IAU1976[] = { IAU1976_DATA };
static double preceTab_IAU2000[] = { IAU2000_DATA };
static double preceTab_P03[] = { P03_DATA };

static double nutB[] = { nutB_DATA };
static double nuTab[] = { nuTab_DATA };

static double X0[] = { X0_DATA };
static double X1[] = { X1_DATA };
static double X2[] = { X2_DATA };
static double X3[] = { X3_DATA };
static double X4[] = { X4_DATA };
static double X5[] = { X5_DATA };
static double X6[] = { X6_DATA };
static double X7[] = { X7_DATA };
static double *XL0[] = { X0, X1, X2, X3, X4, X5, X6, X7 };

static double ML0[] = { ML0_DATA };
static double ML1[] = { ML1_DATA };
static double ML2[] = { ML2_DATA };
static double ML3[] = { ML3_DATA };
static double MB0[] = { MB0_DATA };
static double MB1[] = { MB1_DATA };
static double MB2[] = { MB2_DATA };
static double MR0[] = { MR0_DATA };
static double MR1[] = { MR1_DATA };
static double MR2[] = { MR2_DATA };
static double *ML[] = { ML0, ML1, ML2, ML3 };
static double *MB[] = { MB0, MB1, MB2 };
static double *MR[] = { MR0, MR1, MR2 };
static double **XL1[] = { ML, MB, MR };

static double PL0[] = { PL0_DATA };
static double PL1[] = { PL1_DATA };
static double PL2[] = { PL2_DATA };
static double PL3[] = { PL3_DATA };
static double PL4[] = { PL4_DATA };
static double PL5[] = { PL5_DATA };
static double PL6[] = { PL6_DATA };
static double PL7[] = { PL7_DATA };
static double PL8[] = { PL8_DATA };
static double *XL0Pluto[] = { PL0, PL1, PL2, PL3, PL4, PL5, PL6, PL7, PL8 };

double cs_xxHH[] = { cs_xxHH_DATA };
static double XL0_xzb[] = { XL0_xzb_DATA };

double rad2mrad(double v)
{//对超过0-2PI的角度转为0-2PI
	v = fmod(v, (2 * _pi));
	if (v < 0)
		return v + 2 * _pi;
	return v;
}

double rad2rrad(double v)
{//对超过-PI到PI的角度转为-PI到PI
	v = fmod(v, (2 * _pi));
	if (v <= -_pi)
		return v + 2 * _pi;
	if (v > _pi)
		return v - 2 * _pi;
	return v;
}

mystl::array3 llr2xyz(mystl::array3 JW)
{//球面转直角坐标
	mystl::array3 r = { };
	double J = JW[0], W = JW[1], R = JW[2];
	r[0] = R * cos(W) * cos(J);
	r[1] = R * cos(W) * sin(J);
	r[2] = R * sin(W);
	return r;
}

mystl::array3 xyz2llr(mystl::array3 xyz)
{//直角坐标转球
	mystl::array3 r = { };
	double x = xyz[0], y = xyz[1], z = xyz[2];
	r[2] = sqrt(x * x + y * y + z * z);
	r[1] = asin(z / r[2]);
	r[0] = rad2mrad(atan2(y, x));
	return r;
}

mystl::array3 llrConv(mystl::array3 JW, double E)
{//球面坐标旋转
	//黄道赤道坐标变换
	mystl::array3 r = { };
	double J = JW[0], W = JW[1];
	r[0] = atan2(sin(J) * cos(E) - tan(W) * sin(E), cos(J));
	r[1] = asin(cos(E) * sin(W) + sin(E) * cos(W) * sin(J));
	r[2] = JW[2];
	r[0] = rad2mrad(r[0]);
	return r;
}

mystl::array3 CD2DP(mystl::array3 z, double L, double fa, double gst)
{//赤道坐标转为地平坐标
	mystl::array3 a = { z[0] + _pi / 2 - gst - L, z[1], z[2] };	//转到相对于地平赤道分点的赤道坐标
	a = llrConv(a, _pi / 2 - fa);
	a[0] = rad2mrad(-_pi / 2 - a[0]);
	return a;
}

double j1_j2(double J1, double W1, double J2, double W2)
{//求角度差
	double dJ = rad2rrad(J1 - J2), dW = W1 - W2;
	if (fabs(dJ) < 1 / 1000.0 && fabs(dW) < 1 / 1000.0)
	{
		dJ *= cos((W1 + W2) / 2.0);
		return sqrt(dJ * dJ + dW * dW);
	}
	return acos(sin(W1) * sin(W2) + cos(W1) * cos(W2) * cos(dJ));
}

mystl::array3 h2g(mystl::array3 z, mystl::array3 a)
{//日心球面转地心球面,Z星体球面坐标,A地球球面坐标
	//本含数是通用的球面坐标中心平移函数,行星计算中将反复使用
	a = llr2xyz(a);	//地球
	z = llr2xyz(z);	//星体
	z[0] -= a[0];
	z[1] -= a[1];
	z[2] -= a[2];
	return xyz2llr(z);
}

double shiChaJ(double gst,double L,double fa,double J,double W)
{ //视差角(不是视差)

 double H=gst+L-J; //天体的时角
 return rad2mrad( atan2(sin(H) , tan(fa)*cos(W) - sin(W)*cos(H)) );

}

double hcjj(double t)
{//返回P03黄赤交角,t是世纪数
	double t2 = t * t, t3 = t2 * t, t4 = t3 * t, t5 = t4 * t;
	return (84381.4060 - 46.836769 * t - 0.0001831 * t2 + 0.00200340 * t3 - 5.76e-7 * t4 - 4.34e-8 * t5) / rad;
}

double dt_ext(double y, double jsd)
{
	double dy = (y - 1820) / 100;
	return -20 + jsd * dy * dy;
}//二次曲线外推

double dt_calc(double y)
{//计算世界时与原子时之差,传入年
	double dt_at[] = { 
		-4000,108371.7,-13036.80,392.000, 0.0000,
 		-500, 17201.0,  -627.82, 16.170,-0.3413,
 		-150, 12200.6,  -346.41,  5.403,-0.1593,
 		 150,  9113.8,  -328.13, -1.647, 0.0377,
 		 500,  5707.5,  -391.41,  0.915, 0.3145,
 		 900,  2203.4,  -283.45, 13.034,-0.1778,
 		1300,   490.1,   -57.35,  2.085,-0.0072,
 		1600,   120.0,    -9.81, -1.532, 0.1403,
 		1700,    10.2,    -0.91,  0.510,-0.0370,
 		1800,    13.4,    -0.72,  0.202,-0.0193,
 		1830,     7.8,    -1.81,  0.416,-0.0247,
 		1860,     8.3,    -0.13, -0.406, 0.0292,
 		1880,    -5.4,     0.32, -0.183, 0.0173,
 		1900,    -2.3,     2.06,  0.169,-0.0135,
 		1920,    21.2,     1.69, -0.304, 0.0167,
 		1940,    24.2,     1.22, -0.064, 0.0031,
 		1960,    33.2,     0.51,  0.231,-0.0109,
 		1980,    51.0,     1.29, -0.026, 0.0032,
 		2000,    63.87,    0.1,   0,     0,
 		2005,    64.7,     0.21,  0,     0,
 		2012,    66.8,     0.22,  0,     0,
 		2018,    69.0,     0.36,  0,     0,
 		2028,    72.6
	};

	int len = sizeof(dt_at) / sizeof(double);
	double y0 = dt_at[len - 2];	//表中最后一年
	double t0 = dt_at[len - 1];	//表中最后一年的deltatT
	if (y >= y0)
	{
		double jsd = 31;		//sjd是y1年之后的加速度估计。瑞士星历表jsd=31,NASA网站jsd=32,skmap的jsd=29
		if (y > y0 + 100)
			return dt_ext(y, jsd);
		double v = dt_ext(y, jsd);	//二次曲线外推
		double dv = dt_ext(y0, jsd) - t0;	//ye年的二次外推与te的差
		return v - dv * (y0 + 100 - y) / 100;
	}
	int i;
	for (i = 0; i < len; i += 5)
	{
		if (y < dt_at[i + 5])
			break;
	}
	double t1 = (y - dt_at[i]) / (dt_at[i + 5] - dt_at[i]) * 10, t2 = t1 * t1, t3 = t2 * t1;
	return dt_at[i + 1] + dt_at[i + 2] * t1 + dt_at[i + 3] * t2 + dt_at[i + 4] * t3;
}

double dt_T(double t)
{//传入儒略日(J2000起算),计算TD-UT(单位:日)
	return dt_calc(t / 365.2425 + 2000) / 86400.0;
}

double prece(double t, const char *ss, const char *mx)
{//t是儒略世纪数,s是岁差量名称,mx是模型
	char s[4] = { };
	strcat(s, ss);
	strcat(s, " ");
	int n = 0;
	double c = 0, *p, tn = 1;

	if (!strcmp(mx, "IAU1976"))
		n = 4, p = preceTab_IAU1976;
	else if (!strcmp(mx, "IAU2000"))
		n = 6, p = preceTab_IAU2000;
	else if (!strcmp(mx, "P03"))
		n = 6, p = preceTab_P03;
	else return 0;

	const char *str = "fi w  P  Q  E  x  pi II p  th Z  z ";
	const char* find_str = strstr(str, s);
	if (find_str == NULL) return 0;
	int sc = (strlen(str) - strlen(find_str)) / 3;

	for (int i = 0; i < n; i++, tn *= t)
		c += p[sc * n + i] * tn;
	return c / rad;
}

//==========================岁差旋转==========================
mystl::array3 CDllr_J2D(double t, mystl::array3 llr, const char *mx)
{//J2000赤道转Date赤道
	double Z = prece(t, "Z", mx) + llr[0];
	double z = prece(t, "z", mx);
	double th = prece(t, "th", mx);
	double cosW = cos(llr[1]), cosH = cos(th);
	double sinW = sin(llr[1]), sinH = sin(th);
	double A = cosW * sin(Z);
	double B = cosH * cosW * cos(Z) - sinH * sinW;
	double C = sinH * cosW * cos(Z) + cosH * sinW;
	mystl::array3 p = { rad2mrad(atan2(A, B) + z), asin(C), llr[2] };
	return p;
}

mystl::array3 CDllr_D2J(double t, mystl::array3 llr, const char *mx)
{//Date赤道转J2000赤道
	double Z = -prece(t, "z", mx) + llr[0];
	double z = -prece(t, "Z", mx);
	double th = -prece(t, "th", mx);
	double cosW = cos(llr[1]), cosH = cos(th);
	double sinW = sin(llr[1]), sinH = sin(th);
	double A = cosW * sin(Z);
	double B = cosH * cosW * cos(Z) - sinH * sinW;
	double C = sinH * cosW * cos(Z) + cosH * sinW;
	mystl::array3 p = { rad2mrad(atan2(A, B) + z), asin(C), llr[2] };
	return p;
}

mystl::array3 HDllr_J2D(double t, mystl::array3 llr, const char *mx)
{//黄道球面坐标_J2000转Date分点,t为儒略世纪数
	//J2000黄道旋转到Date黄道(球面对球面),也可直接由利用球面旋转函数计算,但交角接近为0时精度很低
	mystl::array3 r = { llr[0], llr[1], llr[2] };
	r[0] += prece(t, "fi", mx);
	r = llrConv(r, prece(t, "w", mx));
	r[0] -= prece(t, "x", mx);
	r = llrConv(r, -prece(t, "E", mx));
	return r;
}

mystl::array3 HDllr_D2J(double t, mystl::array3 llr, const char *mx)
{//黄道球面坐标_Date分点转J2000,t为儒略世纪数
	mystl::array3 r = { llr[0], llr[1], llr[2] };
	r = llrConv(r, prece(t, "E", mx));
	r[0] += prece(t, "x", mx);
	r = llrConv(r, -prece(t, "w", mx));
	r[0] -= prece(t, "fi", mx);
	r[0] = rad2mrad(r[0]);
	return r;
}

double MQC(double h)
{//大气折射,h是真高度
	return 0.0002967 / tan(h + 0.003138 / (h + 0.08919));
}

double MQC2(double ho)
{
	return -0.0002909 / tan(ho + 0.002227 / (ho + 0.07679));
}//大气折射,ho是视高度

mystl::array3 parallax(mystl::array3 z, double H, double fa, double high)
{//视差修正
	//z赤道坐标,fa地理纬度,H时角,high海拔(千米)
	double dw = 1;
	if (z[2] < 500)
		dw = cs_AU;
	z[2] *= dw;
	double r0, x0, y0, z0, f = cs_ba;
	double u = atan(f * tan(fa)), g = z[0] + H;
	r0 = cs_rEar * cos(u) + high * cos(fa);	//站点与地地心向径的赤道投影长度
	z0 = cs_rEar * sin(u) * f + high * sin(fa);	//站点与地地心向径的轴向投影长度
	x0 = r0 * cos(g);
	y0 = r0 * sin(g);
	mystl::array3 s = llr2xyz(z);
	s[0] -= x0, s[1] -= y0, s[2] -= z0;
	s = xyz2llr(s);
	s[2] /= dw;
	return s;
}

mystl::array2 nutation2(double t)
{//中精度章动计算,t是世纪数
	double c, a, t2 = t * t, *B = nutB, dL = 0, dE = 0;
	for (int i = 0; i < sizeof(nutB) / sizeof(double); i += 5)
	{
		c = B[i] + B[i + 1] * t + B[i + 2] * t2;
		if (i == 0)
			a = -1.742 * t;
		else
			a = 0;
		dL += (B[i + 3] + a) * sin(c);
		dE += B[i + 4] * cos(c);
	}
	mystl::array2 nu = { dL / 100 / rad, dE / 100 / rad };
	return nu;					//黄经章动,交角章动
}

/*高精度算章动*/
mystl::array2 nutation(double t, int zq)
{//章动计算,t是J2000.0起算的儒略世纪数,zq表示只计算周期天于zq(天)的项
	mystl::array2 nutation;
	double t2 = t * t, t3 = t2 * t, t4 = t3 * t;	//t的二、三、四次方
	double l = 485868.249036 + 1717915923.2178 * t + 31.8792 * t2 + 0.051635 * t3 - 0.00024470 * t4;
	double l1 = 1287104.79305 + 129596581.0481 * t - 0.5532 * t2 + 0.000136 * t3 - 0.00001149 * t4;
	double F = 335779.526232 + 1739527262.8478 * t - 12.7512 * t2 - 0.001037 * t3 + 0.00000417 * t4;
	double D = 1072260.70369 + 1602961601.2090 * t - 6.3706 * t2 + 0.006593 * t3 - 0.00003169 * t4;
	double Om = 450160.398036 - 6962890.5431 * t + 7.4722 * t2 + 0.007702 * t3 - 0.00005939 * t4;
	double c, q;
	for (int i = 0; i < 77 * 11; i += 11)
	{//周期项取和计算
		c = (nuTab[i] * l + nuTab[i + 1] * l1 + nuTab[i + 2] * F + nuTab[i + 3] * D + nuTab[i + 4] * Om) / rad;
		if (zq)
		{//只算周期大于zq天的项
			q = 36526 * 2 * _pi * rad / (1717915923.2178 * nuTab[i] + 129596581.0481 * nuTab[i + 1] + 1739527262.8478 * nuTab[i + 2] + 1602961601.2090 * nuTab[i + 3] + 6962890.5431 * nuTab[i + 4]);
			if (q < zq)
				continue;
		}
		nutation[0] += (nuTab[i + 5] + nuTab[i + 6] * t) * sin(c) + nuTab[i + 7] * cos(c);
		nutation[1] += (nuTab[i + 8] + nuTab[i + 9] * t) * cos(c) + nuTab[i + 10] * sin(c);
	}
	nutation[0] /= 10000000 * rad;
	nutation[1] /= 10000000 * rad;
	return nutation;//返回IAU2000B章动值, dL是黄经章动,dE是交角章动
}

double nutationLon2(double t)
{//只计算黄经章动
	double a, t2 = t * t, dL = 0, *B = nutB;
	for (int i = 0; i < sizeof(nutB) / sizeof(double); i += 5)
	{
		if (i == 0)
			a = -1.742 * t;
		else
			a = 0;
		dL += (B[i + 3] + a) * sin(B[i] + B[i + 1] * t + B[i + 2] * t2);
	}
	return dL / 100 / rad;
}

/*******************计算行星位置********************/
double XL0_calc(int xt, int zn, double t, int n)
{//xt星体,zn坐标号,t儒略世纪数,n计算项数
	t /= 10;//转为儒略千年数
	int i, j;
	double v = 0, tn = 1, c;
	double *F = XL0[xt];
	int n1, n2, N;
	int n0, pn = zn * 6 + 1, N0 = F[pn + 1] - F[pn];	//N0序列总数
	for (i = 0; i < 6; i++, tn *= t)
	{
		n1 = F[pn + i], n2 = F[pn + 1 + i], n0 = n2 - n1;
		if (!n0)
			continue;
		if (n < 0)
			N = n2;//确定项数
		else
		{
			N = int2(3 * n * n0 / N0 + 0.5) + n1;
			if (i)
				N += 3;
			if (N > n2)
				N = n2;
		}
		for (j = n1, c = 0; j < N; j += 3)
			c += F[j] * cos(F[j + 1] + t * F[j + 2]);
		v += c * tn;
	}
	v /= F[0];
	if (xt == 0)
	{//地球
		double t2 = t * t, t3 = t2 * t;//千年数的各次方
		if (zn == 0)
			v += (-0.0728 - 2.7702 * t - 1.1019 * t2 - 0.0996 * t3) / rad;
		if (zn == 1)
			v += (+0.0000 + 0.0004 * t + 0.0004 * t2 - 0.0026 * t3) / rad;
		if (zn == 2)
			v += (-0.0020 + 0.0044 * t + 0.0213 * t2 - 0.0250 * t3) / 1000000;
	}
	else
	{//其它行星
		double dv = XL0_xzb[(xt - 1) * 3 + zn];
		if (zn == 0)
			v += -3 * t / rad;
		if (zn == 2)
			v += dv / 1000000;
		else
			v += dv / rad;
	}
	return v;
}

mystl::array3 pluto_coord(double t)
{// 返回冥王星J2000直角坐标
	double c0 = _pi / 180 / 100000;
	double x = -1 + 2 * (t * 36525 + 1825394.5) / 2185000;
	double T = t / 100000000;
	double r[3] = { };
	mystl::array3 p = { };

	int len[] = {
		sizeof(PL0) / sizeof(double),
		sizeof(PL1) / sizeof(double),
		sizeof(PL2) / sizeof(double),
		sizeof(PL3) / sizeof(double),
		sizeof(PL4) / sizeof(double),
		sizeof(PL5) / sizeof(double),
		sizeof(PL6) / sizeof(double),
		sizeof(PL7) / sizeof(double),
		sizeof(PL8) / sizeof(double),
	};
	for (int i = 0; i < 9; i++)
	{
		double *ob = XL0Pluto[i], v = 0;
		for (int j = 0; j < len[i]; j += 3)
			v += ob[j] * sin(ob[j + 1] * T + ob[j + 2] * c0);
		if (i % 3 == 1)
			v *= x;
		if (i % 3 == 2)
			v *= x * x;
		r[int2(i / 3)] += v / 100000000;
	}
	p[0] = r[0] += 9.922274 + 0.154154 * x;
	p[1] = r[1] += 10.016090 + 0.064073 * x;
	p[2] = r[2] += -3.947474 - 0.042746 * x;
	return p;
}

mystl::array3 p_coord(int xt, double t, int n1, int n2, int n3)
{//xt星体,T儒略世纪数,TD
	mystl::array3 z = { };
	if (xt < 8)
	{
		z[0] = XL0_calc(xt, 0, t, n1);
		z[1] = XL0_calc(xt, 1, t, n2);
		z[2] = XL0_calc(xt, 2, t, n3);
	}
	else if (xt == 8)
	{//冥王星
		z = pluto_coord(t);
		z = xyz2llr(z);
		z = HDllr_J2D(t, z, "P03");

	}
	return z;
}

mystl::array3 e_coord(double t, int n1, int n2, int n3)
{//返回地球坐标,t为世纪数
	mystl::array3 re = { };
	re[0] = XL0_calc(0, 0, t, n1);
	re[1] = XL0_calc(0, 1, t, n2);
	re[2] = XL0_calc(0, 2, t, n3);
	return re;
}

/*数组长度表 */
static int len0[]   = {4, 3, 3 };
static int len_ML[] = {2652, 894, 204, 12};
static int len_MB[] = {1236, 270, 72	 };
static int len_MR[] = {1326, 312, 72 	};
static int *len_M[] = {len_ML, len_MB, len_MR};

double XL1_calc(int zn, double t, int n)
{//计算月亮

	int i, j, N;
	double **ob = XL1[zn], *F;
	double tn = 1, v = 0, c;
	double t2 = t * t, t3 = t2 * t, t4 = t3 * t, t5 = t4 * t, tx = t - 10;
	if (zn == 0)
	{
		v += (3.81034409 + 8399.684730072 * t - 3.319e-05 * t2 + 3.11e-08 * t3 - 2.033e-10 * t4) * rad;	//月球平黄经(弧度)
		v += 5028.792262 * t + 1.1124406 * t2 + 0.00007699 * t3 - 0.000023479 * t4 - 0.0000000178 * t5;	//岁差(角秒)
		if (tx > 0)
			v += -0.866 + 1.43 * tx + 0.054 * tx * tx;	//对公元3000年至公元5000年的拟合,最大误差小于10角秒
	}
	t2 /= 1e4, t3 /= 1e8, t4 /= 1e8;
	n *= 6;
	if (n < 0) n = len_M[zn][0];
	for (i = 0; i < len0[zn]; i++, tn *= t)
	{
		F = ob[i];
		N = int2(n * len_M[zn][i] / len_M[zn][0] + 0.5);
		if (i) N += 6;
		if (N >= len_M[zn][i]) N = len_M[zn][i];
		for (j = 0, c = 0; j < N; j += 6)
			c += F[j] * cos(F[j + 1] + t * F[j + 2] + t2 * F[j + 3] + t3 * F[j + 4] + t4 * F[j + 5]);
		v += c * tn;
	}
	if (zn != 2) v /= rad;
	return v;
}

mystl::array3 m_coord(double t, int n1, int n2, int n3)
{//返回月球坐标,t为世纪数
	mystl::array3 re = { };
	re[0] = XL1_calc(0, t, n1);
	re[1] = XL1_calc(1, t, n2);
	re[2] = XL1_calc(2, t, n3);
	return re;
}

double gxc_sunLon(double t)
{//太阳光行差,t是世纪数
	double v = -0.043126 + 628.301955 * t - 0.000002732 * t * t;	//平近点角
	double e = 0.016708634 - 0.000042037 * t - 0.0000001267 * t * t;
	return (-20.49552 * (1 + e * cos(v))) / rad;	//黄经光行差
}

double gxc_sunLat(double t)
{//黄纬光行差
	return 0;
}

double gxc_moonLon(double t)
{//月球经度光行差,误差0.07"
	return -3.4E-6;
}

double gxc_moonLat(double t)
{//月球纬度光行差,误差0.006"
	return 0.063 * sin(0.057 + 8433.4662 * t + 0.000064 * t * t) / rad;
}

double E_Lon(double t, int n)
{//地球经度计算,返回Date分点黄经,传入世纪数、取项数
	return XL0_calc(0, 0, t, n);
}

double M_Lon(double t, int n)
{//月球经度计算,返回Date分点黄经,传入世纪数,n是项数比例
	return XL1_calc(0, t, n);
}

double pGST(double T, double dt)
{//传入T是2000年首起算的日数(UT),dt是deltatT(日),精度要求不高时dt可取值为0
	//返回格林尼治平恒星时(不含赤经章动及非多项式部分),即格林尼治子午圈的平春风点起算的赤经
	double t = (T + dt) / 36525, t2 = t * t, t3 = t2 * t, t4 = t3 * t;
	return pi2 * (0.7790572732640 + 1.00273781191135448 * T)	//T是UT,下一行的t是力学时(世纪数)
		+ (0.014506 + 4612.15739966 * t + 1.39667721 * t2 - 0.00009344 * t3 + 0.00001882 * t4) / rad;
}

double pGST2(double jd)
{//传入力学时J2000起算日数，返回平恒星时
	double dt = dt_T(jd);
	return pGST(jd - dt, dt);
}

double E_v(double t)
{//地球速度,t是世纪数,误差小于万分3
	double f = 628.307585 * t;
	return 628.332 + 21 * sin(1.527 + f) + 0.44 * sin(1.48 + f * 2) + 0.129 * sin(5.82 + f) * t + 0.00055 * sin(4.21 + f) * t * t;
}

double M_v(double t)
{//月球速度计算,传入世经数
	double v = 8399.71 - 914 * sin(0.7848 + 8328.691425 * t + 0.0001523 * t * t);	//误差小于5%
	v   -= 179 * sin(2.543 + 15542.7543 * t)	//误差小于0.3%
		+ 160 * sin(0.1874 + 7214.0629 * t)
		+ 62 * sin(3.14 + 16657.3828 * t)
		+ 34 * sin(4.827 + 16866.9323 * t)
		+ 22 * sin(4.9 + 23871.4457 * t)
		+ 12 * sin(2.59 + 14914.4523 * t)
		+ 7 * sin(0.23 + 6585.7609 * t) 
		+ 5 * sin(0.9 + 25195.624 * t) 
		+ 5 * sin(2.32 - 7700.3895 * t) 
		+ 5 * sin(3.88 + 8956.9934 * t) 
		+ 5 * sin(0.49 + 7771.3771 * t);
	return v;
}

double MS_aLon(double t, int Mn, int Sn)
{//月日视黄经的差值
	return M_Lon(t, Mn) + gxc_moonLon(t) - (E_Lon(t, Sn) + gxc_sunLon(t) + _pi);
}

double S_aLon(double t, int n)
{//太阳视黄经
	return E_Lon(t, n) + nutationLon2(t) + gxc_sunLon(t) + _pi;	//注意，这里的章动计算很耗时
}

/*****************反求时间类函数**********************/
double MS_aLon_t(double W)
{//已知月日视黄经差求时间
	double t, v = 7771.37714500204;
	t = (W + 1.08472) / v;
	t += (W - MS_aLon(t, 3, 3)) / v;
	v = M_v(t) - E_v(t);//v的精度0.5%，详见原文
	t += (W - MS_aLon(t, 20, 10)) / v;
	t += (W - MS_aLon(t, -1, 60)) / v;
	return t;
}

double S_aLon_t(double W)
{//已知太阳视黄经反求时间
	double t, v = 628.3319653318;
	t = (W - 1.75347 - _pi) / v;
	v = E_v(t);//v的精度0.03%，详见原文
	t += (W - S_aLon(t, 10)) / v;
	v = E_v(t);//再算一次v有助于提高精度,不算也可以
	t += (W - S_aLon(t, -1)) / v;
	return t;
}

double MS_aLon_t2(double W)
{//已知月日视黄经差求时间,高速低精度,误差不超过600秒(只验算了几千年)
	double t, v = 7771.37714500204;
	t = (W + 1.08472) / v;
	double L, t2 = t * t;
	t -= (-0.00003309 * t2 + 0.10976 * cos(0.784758 + 8328.6914246 * t + 0.000152292 * t2) + 0.02224 * cos(0.18740 + 7214.0628654 * t - 0.00021848 * t2) - 0.03342 * cos(4.669257 +
			628.307585 * t)) / v;
	L = M_Lon(t,
		20) - (4.8950632 + 628.3319653318 * t + 0.000005297 * t * t + 0.0334166 * cos(4.669257 + 628.307585 * t) + 0.0002061 * cos(2.67823 + 628.307585 * t) * t + 0.000349 * cos(4.6261 +
			1256.61517 * t) - 20.5 / rad);
	v = 7771.38 - 914 * sin(0.7848 + 8328.691425 * t + 0.0001523 * t * t) - 179 * sin(2.543 + 15542.7543 * t) - 160 * sin(0.1874 + 7214.0629 * t);
	t += (W - L) / v;
	return t;
}

double S_aLon_t2(double W)
{//已知太阳视黄经反求时间,高速低精度,最大误差不超过600秒
	double t, L, v = 628.3319653318;
	t = (W - 1.75347 - _pi) / v;
	t -= (0.000005297 * t * t + 0.0334166 * cos(4.669257 + 628.307585 * t) + 0.0002061 * cos(2.67823 + 628.307585 * t) * t) / v;
	t += (W - E_Lon(t, 8) - _pi + (20.5 + 17.2 * sin(2.1824 - 33.75705 * t)) / rad) / v;
	return t;
}


mystl::array2 moonMinR(double t, bool min)
{//求月亮近点时间和距离,t为儒略世纪数力学时
	double a = 27.55454988 / 36525, b;
	if (min)
		b = -10.3302 / 36525;
	else
		b = 3.4471 / 36525;
	t = b + a * int2((t - b) / a + 0.5);//平近(远)点时间
	double r1, r2, r3, dt;
	//初算二次
	dt = 2.0 / 36525;
	r1 = XL1_calc(2, t - dt, 10);
	r2 = XL1_calc(2, t, 10);
	r3 = XL1_calc(2, t + dt, 10);
	t += (r1 - r3) / (r1 + r3 - 2 * r2) * dt / 2.0;
	dt = 0.5 / 36525;
	r1 = XL1_calc(2, t - dt, 20);
	r2 = XL1_calc(2, t, 20);
	r3 = XL1_calc(2, t + dt, 20);
	t += (r1 - r3) / (r1 + r3 - 2 * r2) * dt / 2.0;
	//精算
	dt = 1200.0 / 86400.0 / 36525.0;
	r1 = XL1_calc(2, t - dt, -1);
	r2 = XL1_calc(2, t, -1);
	r3 = XL1_calc(2, t + dt, -1);
	t += (r1 - r3) / (r1 + r3 - 2 * r2) * dt / 2.0;
	r2 += (r1 - r3) / (r1 + r3 - 2 * r2) * (r3 - r1) / 8.0;
	return {t, r2};
}

mystl::array2 moonNode(double t, double asc)
{//月亮升交点
	double a = 27.21222082 / 36525, b;
	if (asc)
		b = 21.0 / 36525;
	else
		b = 35.0 / 36525;
	t = b + a * int2((t - b) / a + 0.5);//平升(降)交点时间
	double w, v, w2, dt;
	dt = 0.5 / 36525;
	w = XL1_calc(1, t, 10);
	w2 = XL1_calc(1, t + dt, 10);
	v = (w2 - w) / dt;
	t -= w / v;
	dt = 0.05 / 36525;
	w = XL1_calc(1, t, 40);
	w2 = XL1_calc(1, t + dt, 40);
	v = (w2 - w) / dt;
	t -= w / v;
	w = XL1_calc(1, t, -1);
	t -= w / v;
	return {t, XL1_calc(0, t, -1)};
}

mystl::array2 earthMinR(double t, bool min)
{//地球近远点
	double a = 365.25963586 / 36525, b;
	if (min)
		b = 1.7 / 36525;
	else
		b = 184.5 / 36525;
	t = b + a * int2((t - b) / a + 0.5);//平近(远)点时间
	double r1, r2, r3, dt;
	//初算二次
	dt = 3.0 / 36525;
	r1 = XL0_calc(0, 2, t - dt, 10);
	r2 = XL0_calc(0, 2, t, 10);
	r3 = XL0_calc(0, 2, t + dt, 10);
	t += (r1 - r3) / (r1 + r3 - 2 * r2) * dt / 2.0;	//误差几个小时
	dt = 0.2 / 36525;
	r1 = XL0_calc(0, 2, t - dt, 80);
	r2 = XL0_calc(0, 2, t, 80);
	r3 = XL0_calc(0, 2, t + dt, 80);
	t += (r1 - r3) / (r1 + r3 - 2 * r2) * dt / 2.0;	//误差几分钟
	//精算
	dt = 0.01 / 36525;
	r1 = XL0_calc(0, 2, t - dt, -1);
	r2 = XL0_calc(0, 2, t, -1);
	r3 = XL0_calc(0, 2, t + dt, -1);
	t += (r1 - r3) / (r1 + r3 - 2 * r2) * dt / 2.0;	//误差小于秒
	r2 += (r1 - r3) / (r1 + r3 - 2 * r2) * (r3 - r1) / 8.0;
	return {t, r2};
}

/*=============一些天文基本问题==============*/
int suoN(double jd)
{//返回朔日的编号,jd应在朔日附近，允许误差数天
	return int2((jd + 8) / 29.5306);
}

double sunShengJ(double jd, double L, double fa, int sj)
{//太阳升降计算。jd儒略日(须接近L当地平午UT)，L地理经度，fa地理纬度，sj=-1升,sj=1降
	int i;
	jd = floor(jd + 0.5) - L / pi2;
	for (i = 0; i < 2; i++)
	{
		double T = jd / 36525, E = (84381.4060 - 46.836769 * T) / rad;//黄赤交角
		double t = T + (32 * (T + 1.8) * (T + 1.8) - 20) / 86400 / 36525;//儒略世纪年数,力学时
		double J = (48950621.66 + 6283319653.318 * t + 53 * t * t - 994
			+ 334166 * cos(4.669257 + 628.307585 * t) + 3489 * cos(4.6261 + 1256.61517 * t) + 2060.6 * cos(2.67823 + 628.307585 * t) * t) / 10000000;
		double sinJ = sin(J), cosJ = cos(J);//太阳黄经以及它的正余弦值
		double gst = (0.7790572732640 + 1.00273781191135448 * jd) * pi2 + (0.014506 + 4612.15739966 * T + 1.39667721 * T * T) / rad;	//恒星时(子午圈位置)
		double A = atan2(sinJ * cos(E), cosJ);//太阳赤经
		double D = asin(sin(E) * sinJ);//太阳赤纬
		double cosH0 = (sin(-50 * 60 / rad) - sin(fa) * sin(D)) / (cos(fa) * cos(D));
		if (fabs(cosH0) >= 1)
			return 0;//太阳在地平线上的cos(时角)计算
		jd += rad2rrad(sj * acos(cosH0) - (gst + L - A)) / 6.28;	//(升降时角-太阳时角)/太阳速度
	}
	return jd;//反回格林尼治UT
}

double pty_zty(double t)
{//时差计算(高精度),t力学时儒略世纪数
	double t2 = t * t, t3 = t2 * t, t4 = t3 * t, t5 = t4 * t;
	double L = (1753470142 + 628331965331.8 * t + 5296.74 * t2 + 0.432 * t3 - 0.1124 * t4 - 0.00009 * t5) / 1000000000 + _pi - 20.5 / rad;

	double E, dE, dL, f;
	mystl::array3 z = { };
	dL = -17.2 * sin(2.1824 - 33.75705 * t) / rad;//黄经章
	dE = 9.2 * cos(2.1824 - 33.75705 * t) / rad;//交角章
	E = hcjj(t) + dE;//真黄赤交角

	//地球坐标
	z[0] = XL0_calc(0, 0, t, 50) + _pi + gxc_sunLon(t) + dL;
	z[1] = -(2796 * cos(3.1987 + 8433.46616 * t) + 1016 * cos(5.4225 + 550.75532 * t) + 804 * cos(3.88 + 522.3694 * t)) / 1000000000;

	z = llrConv(z, E);//z太阳地心赤道坐标
	z[0] -= dL * cos(E);

	L = rad2rrad(L - z[0]);
	return L / pi2;//单位是周(天)
}

double pty_zty2(double t)
{//时差计算(低精度),误差约在1秒以内,t力学时儒略世纪数
	double L = (1753470142 + 628331965331.8 * t + 5296.74 * t * t) / 1000000000 + _pi;
	mystl::array3 z = { };
	double E = (84381.4088 - 46.836051 * t) / rad;
	z[0] = XL0_calc(0, 0, t, 5) + _pi, z[1] = 0;	//地球坐标
	z = llrConv(z, E);//z太阳地心赤道坐标
	L = rad2rrad(L - z[0]);
	return L / pi2;//单位是周(天)
}

double moonIll(double t)
{//月亮被照亮部分的比例
	double t2 = t * t, t3 = t2 * t, t4 = t3 * t;
	double D, M, m, a, dm = _pi / 180;
	D = (297.8502042 + 445267.1115168 * t - 0.0016300 * t2 + t3 / 545868 - t4 / 113065000) * dm;	//日月平距角
	M = (357.5291092 + 35999.0502909 * t - 0.0001536 * t2 + t3 / 24490000) * dm;	//太阳平近点
	m = (134.9634114 + 477198.8676313 * t + 0.0089970 * t2 + t3 / 69699 - t4 / 14712000) * dm;	//月亮平近点
	a = _pi - D + (-6.289 * sin(m) + 2.100 * sin(M) - 1.274 * sin(D * 2 - m) - 0.658 * sin(D * 2) - 0.214 * sin(m * 2) - 0.110 * sin(D)) * dm;
	return (1 + cos(a)) / 2;
}

double moonRad(double r, double h)
{//转入地平纬度及地月质心距离,返回站心视半径(角秒)
	return cs_sMoon / r * (1 + sin(h) * cs_rEar / r);
}