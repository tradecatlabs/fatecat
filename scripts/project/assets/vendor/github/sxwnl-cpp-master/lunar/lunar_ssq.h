#ifndef LUNAR_SSQ_H
#define LUNAR_SSQ_H

#include "../mylib/mystl/my_string.h"
#include "../mylib/mystl/static_array.h"

class SSQ
{
	static char *str_qi;
	static char *str_so;
	static double suoKB[];
	static double qiKB[];
	static char* jieya(int mood);
	static double so_low(double W);
	static double qi_low(double W);
	static double qi_high(double W);
	static double so_high(double W);
	static int calc(double jd, int qs);
public:
	static int leap;  //闰月位置
	static mystl::static_array<mystl::string,14> ym;//各月名称
	static int ZQ[25];//中气表
	static int HS[15];//合朔表
	static int dx[14];//各月大小
	static int pe[2]; //补算二气
	static void init();
	static void calcY(double jd);
};

#endif