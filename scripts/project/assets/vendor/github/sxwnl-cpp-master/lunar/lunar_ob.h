#ifndef LUNAR_OB_H
#define LUNAR_OB_H

#include "../mylib/mystl/my_string.h"
#include "../mylib/mystl/vector.h"

struct OB_DAY
{
	/* 日的公历信息 */
	int d0;		// 2000.0起算儒略日,北京时12:00
	int di;		// 所在公历月内日序数
	int y;
	int m;
	int d; 		// 日名称(公历)
	int dn;
	int week0;
	int week;  	// 星期
	int weeki; 	// 在本月中的周序号
	int weekN; 	// 本月的总周数
	/* 日的农历信息 */
	int Ldi;	   // 日距农历月首偏移
	mystl::string Ldc;   // 日名称(农历),即'初一,初二等'
	
	int cur_dz; //冬至的天数
	int cur_xz; //夏至的天数
	int cur_lq; //立秋的天数
	int cur_mz; //芒种的天数
	int cur_xs; //小暑的天数
	mystl::string Lmc;
	mystl::string Lmc2;  // 月名称
	int Ldn;   		// 月大小
	mystl::string Lleap; 	// 闰状况 
	/* 日的农历纪年、月、日、时及星座 */
	int Lyear;		 	// 农历纪年(10进制,1984年起算,分界点可以是立春也可以是春节,在程序中选择一个)
	int Lyear0;
	mystl::string Lyear2;	// 干支纪年
	mystl::string Lyear3;	// 干支纪年(春节)
	int Lyear4;			// 干支纪年(黄帝纪元)
	int Lmonth;			// 纪月处理,1998年12月7日(大雪)开始连续进行节气计数,0为甲子
	mystl::string Lmonth2;   // 干支纪月
	mystl::string Lday2; 	// 纪日
	mystl::string Ltime2;	// 纪时
	mystl::string Ljq;	   // 节气
	mystl::string XiZ;   	// 星座
	/* 日的回历信息 */
	int Hyear;	 	// 年(回历)
	int Hmonth;		// 月(回历)
	int Hday;	  	// 日(回历)
	/* 日的其它信息 */
	mystl::string yxmc;	// 月相名称
	double yxjd;   	  // 月相时刻(儒略日)
	mystl::string yxsj;	// 月相时间串
	mystl::string jqmc;	// 节气名称
	double jqjd;	     // 节气时刻(儒略日)
	mystl::string jqsj;	// 节气时间串
	
	bool Fjia;
	mystl::string A;
	mystl::string B;
	mystl::string C;
};

struct MLBZ
{
	mystl::string bz_jn;
	mystl::string bz_jy;
	mystl::string bz_jr;
	mystl::string bz_js;
	mystl::string bz_JS;
	mystl::string bz_zty;
};

class OBA
{
public:
	static void init();
	static void getDayName(OB_DAY &r);
	static void getHuiLi(double d0,OB_DAY &r);

private:
	static mystl::vector<mystl::vector<mystl::string>> sFtv; //假日表,由init初始化
	static mystl::vector<mystl::string> wFtv;
};

class OBB//农历对象，气朔计算等
{
public:
	static void init();
	static mystl::string getNH(int y);
	static void getDayName2(OB_DAY &r);
	static void mingLiBaZi(double jd, double J, MLBZ &ob);
	static double qi_accurate(double W);
	static double so_accurate(double W);
	static double qi_accurate2(double jd);
	static double so_accurate2(double jd);
	
private:
	static mystl::vector<mystl::string> JNB;
};

extern const char *str_num[];
extern const char *str_ymc[];
extern const char *str_yxmc[];
extern const char *str_jqmc[];
extern const char *str_gan[];
extern const char *str_zhi[];
extern const char *str_sxmc[];
extern const char *str_nywx[];
extern const char *str_xqmc[];
extern const char *str_rmc[];
extern const char *str_rmc0[];
extern const char *str_xz[];
extern const char *str_dx[];
extern const char *str_ago[];
extern const char *str_fw[];
extern const char *str_sjd[];
extern const char *str_ry[];
extern const char *str_ry2[];
extern const char *str_yx[];

#endif