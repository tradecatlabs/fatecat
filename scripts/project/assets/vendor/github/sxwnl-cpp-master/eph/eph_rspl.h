//日食批量快速计算器

#ifndef EPH_RSPL_H
#define EPH_RSPL_H

#include "../mylib/mystl/my_string.h"
#include "../mylib/mystl/static_array.h"

struct _SECXY
{
	double mCJ;
	double mCW;
	double mR;
	double mCJ2;
	double mCW2;
	double mR2;
	
	double sCJ;
	double sCW;
	double sR;
	double sCJ2;
	double sCW2;
	double sR2;	
	
	double mr;
	double sr;
	double x;
	double y;
	double t;
};

struct _ZB
{
	mystl::array3 S;
	mystl::array3 M;
	double sr;
	double mr;
	double x;
	double y;
	double g;
};

struct _GJW
{
	double J;
	double W;
	mystl::string c;
};


class RS_PL
{
public:
	static bool nasa_r;//为1表示采用NASA的视径比
	static mystl::array5 sT;//地方日食时间表
	static mystl::string LX;
	static double sf;
	static double sf2; //食分(日出食分)
    static double sf3; //食分(日没食分)
    static mystl::string sflx; //食分类型
	static double b1;
	static double dur;
	static double sun_s;
	static double sun_j;
	static double P1;
	static double V1;
	static double P2;
	static double V2;
	static void secMax(double jd,double L,double fa,double high);
	static void nbj(double jd);
	//以下涉及南北界计算
	static mystl::array3 A;
	static mystl::array3 B; //本半影锥顶点坐标
	static _ZB P;//t1时刻的日月坐标,g为恒星时
	static _ZB Q;//t2时刻的日月坐标
	static mystl::array10 V;//食界表
	static mystl::string Vc;
	static mystl::string Vb;  //食中心类型,本影南北距离
	
	static double lineT(_SECXY G, double v,double u, double r, bool n);
	static void zbXY(_ZB &p,double L,double fa);
	static void zb0(double jd);
	static void p2p(double L,double fa,_GJW &re,bool fAB,int f);
	static void pp0(_GJW &re);
	static void secXY(double jd,double L,double fa,double high,_SECXY &re);

};

#endif