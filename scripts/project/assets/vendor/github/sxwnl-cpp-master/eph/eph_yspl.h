#ifndef EPH_YSPL_H
#define EPH_YSPL_H

#include "../mylib/mystl/my_string.h"
#include "../mylib/mystl/static_array.h"

struct RE0
{
	double e_mRad;
	double eShadow;
	double eShadow2;
	double x;
	double y;
	double mr;
	double er;
	double Er;
	double t;
};

class YS_PL
{ //月食快速计算器
public:
	static mystl::array7 lT;
	static mystl::string LX;
	static double sf;
	static void lecXY(double jd, RE0 &re);
	static double lineT(RE0 G,double v,double u, double r, bool n);
	static void lecMax(double jd);
};

#endif