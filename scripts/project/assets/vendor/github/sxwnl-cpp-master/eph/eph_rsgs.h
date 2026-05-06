#ifndef EPH_RSGS_H
#define EPH_RSGS_H

#include "../mylib/mystl/vector.h"
#include "../mylib/mystl/my_string.h"
#include "../mylib/mystl/static_array.h"

struct _VXY
{
	double vx;
	double vy;
	double Vx;
	double Vy;
	double V;	
};

struct _RSM
{
	double r1;
	double r2;
	double ar2;
	double sf;
};

struct _FEATURE
{
	double jdSuo;
	double dT;
	double ds;
	double vx;
	double vy;
	double ax;
	double ay;
	double v;
	double k;

	double t0;
	double jd;
	double xc;
	double yc;
	double zc;
	double D;
	double d;
	mystl::array3 I;
	mystl::array3 gk1;
	mystl::array3 gk2;
	mystl::array3 gk3;
	mystl::array3 gk4;
	mystl::array3 gk5;
	mystl::string lx;

	double zxJ;
	double zxW;
	double dw;
	double sf;
	double tt;
	mystl::array3 Sdp;

	mystl::vector <double> p1;
	mystl::vector <double> p2;
	mystl::vector <double> p3;
	mystl::vector <double> p4;
	mystl::vector <double> q1;
	mystl::vector <double> q2;
	mystl::vector <double> q3;
	mystl::vector <double> q4;
	mystl::vector <double> L0;
	mystl::vector <double> L1;
	mystl::vector <double> L2;
	mystl::vector <double> L3;
	mystl::vector <double> L4;
	mystl::vector <double> L5;
	mystl::vector <double> L6;
};

struct _JIEX2
{
	mystl::vector <double> p1;
	mystl::vector <double> p2;
	mystl::vector <double> p3;
};

struct _FLAG
{
	int f;
	int f2;
};

class RS_GS
{
public:
	
	static double Zjd;
	static void init(double jd,int n);
	static _FEATURE feature(double jd);
	//static _FEATURE __rsGS::jieX(double jd);
	//static _JIEX2 __rsGS::jieX2(double jd);
	static mystl::string jieX3(double jd);
	static inline mystl::array3 sun (double jd){ return chazhi(jd,0); } //传回值可能超过360度
	static inline mystl::array3 moon(double jd){ return chazhi(jd,1); }
	static inline mystl::array3 bse (double jd){ return chazhi(jd,2); }

private:
	static mystl::vector<double> Zs;
	static double Zdt;
	static double dT;
	static double tanf1;
	static double tanf2;
	static double srad;
	static double bba;
	static double bhc;
	static double dyj; 
	
	static mystl::array3 chazhi(double jd,int xt);
	static mystl::array3 cd2bse(mystl::array3 z,mystl::array3 I);
	static mystl::array3 bse2cd(mystl::array3 z,mystl::array3 I );
	static mystl::array3 bse2db(mystl::array3 z,mystl::array3 I ,bool f);
	static mystl::array3 bseXY2db(double x,double y,mystl::array3 I,bool f);
	static mystl::array3 bseM(double jd);
	static _VXY Vxy(double x,double y,double s, double vx,double vy);
	static _RSM rSM(double mR);
	static mystl::array3 qrd(double jd,double dx,double dy,bool fs);
	static void push(mystl::array3 z,mystl::vector<double> &p);
	static mystl::array4 nanbei(mystl::array3 M,double vx0,double vy0, double h,double r,mystl::array3 I);
	static bool mDian(mystl::array3 M,double vx0,double vy0,bool AB, double r,mystl::array3 I,mystl::vector<double> &A);
	//static void __rsGS::elmCpy(mystl::vector<double> &a,int n,mystl::vector<double> b,int m);
	//static void __rsGS::mQie(mystl::array3 M,double vx0,double vy0,double h, double r,mystl::array3 I, mystl::vector<double> &A,_FLAG &FLAG);
	
};

// extern std::map<mystl::string,mystl::string> lxb;
#endif