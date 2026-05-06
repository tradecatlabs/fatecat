#ifndef EPH_MSC_H
#define EPH_MSC_H

#include "../mylib/mystl/my_string.h"

//========太阳月亮计算类=============
class MSC
{
public:
	static double T;	//TD力学时
	static double L;	//地理纬度
	static double fa;	//地理经度
	static double dt;	//力学-世界时时差
	static double jd;	//UT世界时
	static double dL;	//黄经章动
	static double dE;	//黄纬章动
	static double E;	//交角章动
	static double gst;	//真恒星时
	
	static double mHJ;	//月球视黄经
	static double mHW;	//月球视黄纬
	static double mR;	//地月质心距
	static double mCJ;	//月球视赤经
	static double mCW;	//月球视赤纬
	static double mShiJ;	//月球时角
	
	static double mCJ2;	//时差修正后的赤道坐标
	static double mCW2;	
	static double mR2;
	static double mDJ;	//高度角
	static double mDW;	//方位角
	static double mPJ;	//大气折射修正后的高度角
	static double mPW;	//大气折射修正后的方位角
	
	static double sHJ;	//太阳视黄经
	static double sHW;	//太阳视黄纬
	static double sCJ;	//太阳视赤经
	static double sCW;	//太阳视赤纬
	static double sCJ2;	//时差修正后的赤道坐标
	static double sCW2;	
	static double sR2;
	static double sShiJ;	//太阳时角
		
	static double sDJ;	//高度角
	static double sDW;	//方位角
	static double sR;
	static double sPJ;	//方位角
	static double sPW;	//高度角
	static double sc;	//时差

	static double pty;	//平恒星时
	static double zty;	//真恒星时
	static double mRad;	//月亮视半径
	static double sRad;	//太阳视半径
	static double e_mRad;	//月亮地心视半径
	static double eShadow;	//地本影在月球向径处的半径(角秒)
	static double eShadow2;	//地半影在月球向径处的半径(角秒)
	static double mIll;	//月面被照亮比例
	static double zx_J;	//中心食坐标
	static double zx_W;

	static void calc(double T,double L,double fa,double high);
	static mystl::string toStr(bool fs);
};
#endif