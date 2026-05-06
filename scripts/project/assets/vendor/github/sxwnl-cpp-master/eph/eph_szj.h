#include "../mylib/mystl/my_string.h"
#include "../mylib/mystl/vector.h"

struct SJ
{
	double z;
	double x;
	double s;
	double j;
	double c;
	double h;
	double c2;
	double h2;
	double c3;
	double h3;
	double H0;
	double H;
	double H1;
	double H2;
	double H3;
	double H4;
	mystl::string sm;
};

struct SJ_S
{
	mystl::string s;
	mystl::string z;
	mystl::string j;
	mystl::string c;
	mystl::string h;
	mystl::string ch;
	mystl::string sj;
	mystl::string Ms;
	mystl::string Mz;
	mystl::string Mj;
};


class SZJ
{	//日月的升中天降,不考虑气温和气压的影响  
public:	
	static mystl::vector <SJ_S> rts;	//多天的升中降
	
	static double getH(double h, double w);
	static void Mcoord(double jd, double H0, SJ & r);
	static void Scoord(double jd, int xm, SJ & r);
	static SJ Mt(double jd);
	static SJ Qt(double jd);
	static SJ St(double jd);
	static void calcRTS(double jd, int n, double Jdl, double Wdl, double sq);
		
	static double L;	//站点地理经度,向东测量为正
	static double fa;	//站点地理纬度
	
private:
	static double E;	//黄赤交角
	static double dt;	//TD-UT
};