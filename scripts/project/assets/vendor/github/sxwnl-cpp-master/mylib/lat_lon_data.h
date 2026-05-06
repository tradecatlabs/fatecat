#ifndef LAT_LON_DATA_H
#define LAT_LON_DATA_H

struct JINGWEI
{
	double J;//经度
	double W;//纬度
	char s[48];//省市
	char x[48];//区县
};

extern JINGWEI jw;
JINGWEI GeographicalPosition(void);
#endif