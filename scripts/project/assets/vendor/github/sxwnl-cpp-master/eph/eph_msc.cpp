#include "../mylib/tool.h"
#include "../mylib/math_patch.h"
#include "eph0.h"
#include "eph.h"
#include "eph_msc.h"

double MSC::T;//TD力学时
double MSC::L;//地理纬度
double MSC::fa;//地理经度
double MSC::dt;//力学-世界时时差
double MSC::jd;//UT世界时
double MSC::dL;//黄经章动
double MSC::dE;//黄纬章动
double MSC::E;//交角章动
double MSC::gst;//真恒星时

double MSC::mHJ;//月球视黄经
double MSC::mHW;//月球视黄纬
double MSC::mR;//地月质心距
double MSC::mCJ;//月球视赤经
double MSC::mCW;//月球视赤纬
double MSC::mShiJ;//月球时角

double MSC::mCJ2;//时差修正后的赤道坐标
double MSC::mCW2;
double MSC::mR2;
double MSC::mDJ;//高度角
double MSC::mDW;//方位角
double MSC::mPJ;//大气折射修正后的高度角
double MSC::mPW;//大气折射修正后的方位角

double MSC::sHJ;//太阳视黄经
double MSC::sHW;//太阳视黄纬
double MSC::sCJ;//太阳视赤经
double MSC::sCW;//太阳视赤纬
double MSC::sCJ2;//时差修正后的赤道坐标
double MSC::sCW2;
double MSC::sR2;
double MSC::sShiJ;//太阳时角

double MSC::sDJ;//高度角
double MSC::sDW;//方位角
double MSC::sR;
double MSC::sPJ;//方位角
double MSC::sPW;//高度角
double MSC::sc;//时差

double MSC::pty;//平恒星时
double MSC::zty;//真恒星时
double MSC::mRad;//月亮视半径
double MSC::sRad;//太阳视半径
double MSC::e_mRad;//月亮地心视半径
double MSC::eShadow;//地本影在月球向径处的半径(角秒)
double MSC::eShadow2;//地半影在月球向径处的半径(角秒)
double MSC::mIll;//月面被照亮比例
double MSC::zx_J;//中心食坐标
double MSC::zx_W;

void MSC::calc(double T, double L, double fa, double high)
{								//sun_moon类的成员函数。参数：T是力学时,站点经纬L,fa,海拔high(千米)
	//基本参数计算
	MSC::T = T, MSC::L = L, MSC::fa = fa;
	MSC::dt = dt_T(T);			//TD-UT
	MSC::jd = T - MSC::dt;	//UT
	T /= 36525.0;
	mystl::array2 zd = nutation2(T);
	MSC::dL = zd[0];			//黄经章
	MSC::dE = zd[1];			//交角章动
	MSC::E = hcjj(T) + MSC::dE;	//真黄赤交角
	MSC::gst = pGST(MSC::jd, MSC::dt) + MSC::dL * cos(MSC::E);	//真恒星时(不考虑非多项式部分)
	mystl::array3 z;

	//=======月亮========
	//月亮黄道坐标
	z = m_coord(T, -1, -1, -1);	//月球坐标
	z[0] = rad2mrad(z[0] + gxc_moonLon(T) + MSC::dL);
	z[1] += gxc_moonLat(T);		//补上月球光行差及章动
	MSC::mHJ = z[0];
	MSC::mHW = z[1];
	MSC::mR = z[2];			//月球视黄经,视黄纬,地月质心距

	//月球赤道坐标
	z = llrConv(z, MSC::E);	//转为赤道坐标
	MSC::mCJ = z[0];
	MSC::mCW = z[1];			//月球视赤经,月球赤纬

	//月亮时角计算
	MSC::mShiJ = rad2mrad(MSC::gst + L - z[0]);	//得到此刻天体时角
	if (MSC::mShiJ > _pi)
		MSC::mShiJ -= pi2;

	//修正了视差的赤道坐标
	z = parallax(z, MSC::mShiJ, fa, high);	//视差修正
	MSC::mCJ2 = z[0], MSC::mCW2 = z[1], MSC::mR2 = z[2];

	//月亮时角坐标
	z[0] += _pi / 2 - MSC::gst - L;	//转到相对于地平赤道分点的赤道坐标(时角坐标)

	//月亮地平坐标
	z = llrConv(z, _pi / 2 - fa);	//转到地平坐标(只改经纬度)
	z[0] = rad2mrad(-_pi / 2 - z[0]);
	MSC::mDJ = z[0];
	MSC::mDW = z[1];			//方位角,高度角
	if (z[1] > 0)
		z[1] += MQC(z[1]);		//大气折射修正
	MSC::mPJ = z[0];
	MSC::mPW = z[1];			//方位角,高度角

	//=======太阳========
	//太阳黄道坐标
	z = e_coord(T, -1, -1, -1);	//地球坐标
	z[0] = rad2mrad(z[0] + _pi + gxc_sunLon(T) + MSC::dL);	//补上太阳光行差及章动
	z[1] = -z[1] + gxc_sunLat(T);	//z数组为太阳地心黄道视坐标
	MSC::sHJ = z[0];
	MSC::sHW = z[1];
	MSC::sR = z[2];			//太阳视黄经,视黄纬,日地质心距

	//太阳赤道坐标
	z = llrConv(z, MSC::E);	//转为赤道坐标
	MSC::sCJ = z[0];
	MSC::sCW = z[1];			//太阳视赤经,视赤纬

	//太阳时角计算
	MSC::sShiJ = rad2mrad(MSC::gst + L - z[0]);	//得到此刻天体时角
	if (MSC::sShiJ > _pi)
		MSC::sShiJ -= pi2;

	//修正了视差的赤道坐标
	z = parallax(z, MSC::sShiJ, fa, high);	//视差修正
	MSC::sCJ2 = z[0], MSC::sCW2 = z[1], MSC::sR2 = z[2];

	//太阳时角坐标
	z[0] += _pi / 2 - MSC::gst - L;	//转到相对于地平赤道分点的赤道坐标

	//太阳地平坐标
	z = llrConv(z, _pi / 2 - fa);
	z[0] = rad2mrad(-_pi / 2 - z[0]);
	//z[1] -= 8.794/rad/z[2]*cos(z[1]); //直接在地平坐标中视差修正(这里把地球看为球形,精度比parallax()稍差一些)
	MSC::sDJ = z[0];
	MSC::sDW = z[1];			//方位角,高度角

	if (z[1] > 0)
		z[1] += MQC(z[1]);		//大气折射修正
	MSC::sPJ = z[0];
	MSC::sPW = z[1];			//方位角,高度角

	//=======其它========
	//时差计算
	double t = T / 10, t2 = t * t, t3 = t2 * t, t4 = t3 * t, t5 = t4 * t;
	double Lon = (1753470142 + 6283319653318 * t + 529674 * t2 + 432 * t3 - 1124 * t4 - 9 * t5) / 1000000000 + _pi - 20.5 / rad;	//修正了光行差的太阳平黄经
	Lon = rad2mrad(Lon - (MSC::sCJ - MSC::dL * cos(MSC::E)));	//(修正了光行差的平黄经)-(不含dL*cos(E)的视赤经)
	if (Lon > _pi)
		Lon -= pi2;				//得到时差,单位是弧度
	MSC::sc = Lon / pi2;		//时差(单位:日)

	//真太阳与平太阳
	MSC::pty = MSC::jd + L / pi2;	//平太阳时
	MSC::zty = MSC::jd + L / pi2 + MSC::sc;	//真太阳时

	//视半径
	// MSC::mRad = moonRad(MSC::mR,MSC::mDW);  //月亮视半径(角秒)
	MSC::mRad = cs_sMoon / MSC::mR2;	//月亮视半径(角秒)
	MSC::sRad = 959.63 / MSC::sR2;	//太阳视半径(角秒)
	MSC::e_mRad = cs_sMoon / MSC::mR;	//月亮地心视半径(角秒)
	MSC::eShadow = (cs_rEarA / MSC::mR * rad - (959.63 - 8.794) / MSC::sR) * 51 / 50;	//地本影在月球向径处的半径(角秒),式中51/50是大气厚度补偿
	MSC::eShadow2 = (cs_rEarA / MSC::mR * rad + (959.63 + 8.794) / MSC::sR) * 51 / 50;	//地半影在月球向径处的半径(角秒),式中51/50是大气厚度补偿
	MSC::mIll = moonIll(T);	//月亮被照面比例

	//中心食计算
	if (fabs(rad2rrad(MSC::mCJ - MSC::sCJ)) < 50.0 / 180.0 * _pi)
	{
		COORDP pp = lineEar({ MSC::mCJ, MSC::mCW, MSC::mR }
							, { MSC::sCJ, MSC::sCW, MSC::sR * cs_AU }
							, MSC::gst);
		MSC::zx_J = pp.J;
		MSC::zx_W = pp.W;		//无解返回值是100
	}
	else
		MSC::zx_J = MSC::zx_W = 100;
}

mystl::string MSC::toStr(bool fs)
{
	mystl::string s;
	s = "-------------------------------------------\n";
	s = s + "平太阳 " + timeStr(MSC::pty) + " 真太阳 " + timeStr(MSC::zty) + "\n";
	s = s + "时差 " + m2fm(MSC::sc * 86400, 2, 1) + " 月亮被照亮 " + to_str(MSC::mIll * 100, 2) + "% ";
	s = s + "\n";

	s = s + "-------------------------------------------\n表一       月亮            太阳\n";
	s = s + "视黄经 " + rad2str(MSC::mHJ, 0) + "  " + rad2str(MSC::sHJ, 0) + "\n";
	s = s + "视黄纬 " + rad2str(MSC::mHW, 0) + "  " + rad2str(MSC::sHW, 0) + "\n";
	s = s + "视赤经 " + rad2str(MSC::mCJ, 1) + "  " + rad2str(MSC::sCJ, 1) + "\n";
	s = s + "视赤纬 " + rad2str(MSC::mCW, 0) + "  " + rad2str(MSC::sCW, 0) + "\n";
	s = s + "距离    " + to_str(MSC::mR, 2) + "千米    " + to_str(MSC::sR, 8) + "AU" + "\n";

	s = s + "-------------------------------------------\n表二       月亮            太阳\n";
	s = s + "方位角 " + rad2str(MSC::mPJ, 0) + "  " + rad2str(MSC::sPJ, 0) + "\n";
	s = s + "高度角 " + rad2str(MSC::mPW, 0) + "  " + rad2str(MSC::sPW, 0) + "\n";
	s = s + "时角   " + rad2str(MSC::mShiJ, 0) + "  " + rad2str(MSC::sShiJ, 0) + "\n";
	s = s + "视半径   " + m2fm(MSC::mRad, 2, 0) + "       " + m2fm(MSC::sRad, 2, 0) + " (观测点)\n";

	if (fs)
	{
		s = s + "-------------------------------------------\n";
		s = s + "力学时" + JD2str(MSC::T + J2000);
		s = s + " ΔT=" + to_str(MSC::dt * 86400, 1) + "秒\n";
		s = s + "黄经章 " + to_str(MSC::dL / pi2 * 360 * 3600, 2) + "\" ";
		s = s + "交角章 " + to_str(MSC::dE / pi2 * 360 * 3600, 2) + "\" ";
		s = s + "ε=" + rad2str(MSC::E, 0) + "\n";
		s = s + "-------------------------------------------\n";

	}
	return s;
}