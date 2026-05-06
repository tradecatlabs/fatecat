#ifndef EPH_H
#define EPH_H

#include "../mylib/mystl/my_string.h"
#include "../mylib/mystl/static_array.h"

struct COORDP
{
	double x;
	double y;
	double z;	
	double R1;
	double R2;
	double D;
	double X;
	double J;
	double W;
};

struct NODE
{
	mystl::array3 A;
	mystl::array3 B;
	double R1;
	double R2;
	int n;
};

struct NODEX
{//天象位置(近日，远日，升交点)
	double r, t;
};

//====================================
/*****
ecFast()函数返回参数说明
r.jdSuo 朔时刻
r.lx    日食类型
*****/
typedef struct
{
	double jd;
	double jdSuo;
	double ac;
	mystl::string lx;
}_ECFAST;

//========行星天象及星历=============
double xingJJ(int xt, double t, int jing);
mystl::array2 daJu(int xt, double t, bool dx);
mystl::array3 xingLiu0(int xt, double t, int n, double gxs);
double xingLiu(int xt, double t, bool sn);

mystl::array4 xingMP(int xt, double t, int n, double E, mystl::array4 g);
mystl::array4 xingHY(int xt, double t);
mystl::array4 xingSP(int xt, double t, int n, double w0, double ts, double tp);
mystl::array2 xingHR(int xt, double t, bool f);

mystl::string xingX(int xt,double jd,double L,double fa);
COORDP lineEll(double x1,double y1,double z1, double x2,double y2,double z2, double e,double r);
COORDP lineEar2(double x1,double y1,double z1, double x2,double y2,double z2, double e,double r, mystl::array3 I);
COORDP lineEar(mystl::array3 P,mystl::array3 Q,double gst);

NODE cirOvl(double R,double ba,double R2,double x0,double y0);
NODE lineOvl(double x1,double y1,double dx,double dy,double r,double ba);
_ECFAST ecFast(double jd);

#endif