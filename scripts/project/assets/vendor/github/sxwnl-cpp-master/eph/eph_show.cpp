#include <iostream>
#include "eph_show.h"
#include "eph0.h"
#include "eph.h"
#include "eph_msc.h"
#include "eph_szj.h"
#include "eph_yspl.h"
#include "eph_rsgs.h"
#include "eph_rspl.h"
#include "../mylib/lat_lon_data.h"
#include "../mylib/tool.h"
#include "../mylib/mystl/static_array.h"
#include "../mylib/mystl/map.h"

mystl::string rysCalc(Date d, bool is_utc, bool nasa_r)
{
	double vJ=jw.J/radd;
	double vW=jw.W/radd;
	double jd = toJD(d)-J2000;
	if (is_utc) {
		jd+=-8/24.0+dt_T(jd);
	}
	
	MSC::calc(jd,vJ,vW,0);
	mystl::string s = "",s2;
	double J1, W1, J2, W2;
	double sr, mr, er, Er, d0, d1, d2;
	double msHJ = rad2mrad(MSC::mHJ - MSC::sHJ);
	int i;
	
	if (msHJ < 3 / radd || msHJ > 357 / radd)
	{// 日食图表放大计算
		J1 = MSC::mCJ2, W1 = MSC::mCW2, J2 = MSC::sCJ2, W2 = MSC::sCW2;	// 用未做大气折射的来计算日食
		sr = MSC::sRad, mr = MSC::mRad;
		d1 = j1_j2(J1, W1, J2, W2) * rad, d0 = mr + sr;
		s2 = "此刻月亮本影中心线不经过地球。";
		if (MSC::zx_W != 100)
		{
			mystl::string zxsJ = to_str(MSC::zx_J / _pi * 180, 5);
			mystl::string zxsW = to_str(MSC::zx_W / _pi * 180, 5);
			s2 = "食中心地标：经 " + zxsJ + " 纬 " + zxsW;
		}
		s = "日月站心视半径 " + m2fm(sr, 2, 0) + "及" + m2fm(mr, 2, 0) + " \n\033[31m" + s2 + "\033[0m\n"
			+ "日月中心视距 " + m2fm(d1, 2, 0) + " 日月半径和 " + m2fm(d0, 2, 0) + "\n半径差 " + m2fm(sr - mr, 2, 0) + "\t距外切 " + m2fm(d1 - d0, 2, 0);

		// 显示南北界数据
		RS_PL::nasa_r = nasa_r;		// 视径选择
		s = s + "\n--------------------------------------\n" + JD2str(jd + J2000) + " TD\n--------------------------------------\n" + "南北界点：经度　　　　纬度\n";
		mystl::static_array<mystl::string, 5> mc =
		{
		"食中心点", "本影北界", "本影南界", "半影北界", "半影南界"};
		RS_PL::nbj(jd);
		for (i = 0; i < 5; i++)
		{
			s += mc[i] + "：";
			if (RS_PL::V[i * 2 + 1] == 100)
			{
				s += "无　　　　　无\n";
				continue;
			}
			s += to_str(RS_PL::V[i * 2] * radd, 5) + "　" + to_str(RS_PL::V[i * 2 + 1] * radd, 5) + "\n";
		}
		s += "中心类型：" + RS_PL::Vc + "食\n";
		s += "本影南北界距约" + RS_PL::Vb;

		// 显示食甚等时间
		mystl::string td = " TD";
		mc = {"初亏", "食甚", "复圆", "食既", "生光"};
		RS_PL::secMax(jd, vJ, vW, 0);
		if (RS_PL::LX == "环")
			mc[3] = "环食始", mc[4] = "环食终";	// 环食没有食既和生光
		s = s + "\n--------------------------------------\n" + "时间表 (日" + RS_PL::LX + "食)\n";
		for (i = 0; i < 5; i++)
		{
			jd = RS_PL::sT[i];
			if (!jd)
				continue;
			if (is_utc)
				jd -= -8 / 24.0 + dt_T(jd), td = " UTC";	// 转为UTC(本地时间)
			s += mc[i] + ":" + JD2str(jd + J2000) + td + "\n";
		}
		s += "时长: " + m2fm(RS_PL::dur * 86400, 1, 1) + "\n";
		s += "食分: " + to_str(RS_PL::sf, 5) + "\n";
		s += "月日视径比: " + to_str(RS_PL::b1, 5) + "(全或环食分)\n";
		s += "是否NASA径比(1是,0否): " + to_str(RS_PL::nasa_r) + "\n";
		s += "食分指日面直径被遮比例\n\n";
	}

	if (msHJ > 170 / radd && msHJ < 190 / radd)
	{// 月食图表放大计算
		J1 = MSC::mCJ, W1 = MSC::mCW, J2 = MSC::sCJ + _pi, W2 = -MSC::sCW;
		er = MSC::eShadow, Er = MSC::eShadow2, mr = MSC::e_mRad;	// 用未做大气折射的来计算日食
		d1 = j1_j2(J1, W1, J2, W2) * rad, d0 = mr + er, d2 = mr + Er;
		s = "本影半径 " + m2fm(er, 2, 0) + " 半影半径 " + m2fm(Er, 2,0) +
			" 月亮地心视半径 " + m2fm(mr, 2, 0) + "\n" + "影月中心距 " + m2fm(d1, 2, 0) +
			" 影月半径和 " + m2fm(d0, 2, 0) + " \n距相切 \033[31m" + m2fm(d1 - d0, 2, 0) + "\033[0m 距第二相切 " + m2fm(d1 - d2, 2, 0);

		mystl::string td = " TD";
		mystl::static_array<mystl::string,7> mc = {"初亏", "食甚", "复圆", "半影食始", "半影食终", "食既", "生光"};
		YS_PL::lecMax(jd);
		s = s + "\n\n时间表(月" + YS_PL::LX + "食)\n";
		for (int i = 0; i < 7; i++)
		{
			jd = YS_PL::lT[i];
			if (!jd)
				continue;
			if (is_utc)
				jd -= -8 / 24.0 + dt_T(jd), td = " UTC";	// 转为UTC(本地时间)
			s = s+mc[i] + ":" + JD2str(jd + J2000) + td + "\n";
		}
		s += "食分:" + to_str(YS_PL::sf, 5) + "\n";
		s += "食分指月面直径被遮比例\n\n";
	}
	s += MSC::toStr(true);
	return s;
}

mystl::string rs_search(int Y, int M, int n, bool fs)
{
    //查找日食
    int i, k;
    _ECFAST r;
    mystl::string s = "", s2 = "";
    double jd = toJD({ Y, M, 1, 0, 0, 0 }) - J2000;     //取屏幕时间
    jd = MS_aLon_t2(int2((jd + 8) / 29.5306) * _pi * 2) * 36525;        //定朔
    for (i = 0, k = 0; i < n; i++) {
        r = ecFast(jd);         //低精度高速搜索
        if (r.lx == "NN") {
            jd += 29.5306;
            continue;
        } 
        //排除不可能的情况，加速计算
        if (!r.ac) {
            if (fs == 0) RS_GS::init(jd, 2);     //低精度
            if (fs == 1) RS_GS::init(jd, 7);     //高精度
            _FEATURE rr = RS_GS::feature(jd);
            r = {rr.jd, rr.jdSuo, r.ac, rr.lx};
        }
        if (r.lx != "N") {
            s += JD2str(r.jd + J2000).substr(0, 11);
            s += r.lx;
            k++;
            if (k % 5 == 0)
                s += "\n";
            if (k % 100 == 0)
                s2 += s, s = "";
        }
        jd = r.jd + 29.5306;
    }
    return s2 + s;
}


mystl::string rs2_calc(uint8_t fs,double jd0, double step)
{
 if (fs==0) return "";
 static double jd = 2454679.926741-J2000; //取屏幕时间
 
 if(fs==1) jd = jd0;
// if(fs==2) ; //保持时间不变
 if(fs==3) jd -= step;
 if(fs==4) jd += step;
 jd = MS_aLon_t2( int2((jd+8)/29.5306)*_pi*2 )*36525.0; //归朔
 //Cp10_jd.value = Cp10_jd2.value = (jd+J2000),6);    //保存在屏幕上
 std::cout<<JD2str(jd+J2000)<<std::endl; //显示时间串
 
 mystl::map<mystl::string,mystl::string> lxb={{"T","全食"},{"A","环食"},{"P","偏食"},{"T0","无中心全食"},{"T1","部分本影有中心全食"},{"A0","无中心环食"},{"A1","部分伪本影有中心全食"},{"H","全环全"},{"H2","全全环"},{"H3","环全全"}};

 mystl::string s="";
 //计算单个日食
 if(fs==1||fs==2||fs==3||fs==4)
 {
  RS_GS::init(jd,7);
  _FEATURE r = RS_GS::feature(jd); //特征计算
  if (r.lx == "N") { s = "无日食"; }
  else {
	  s = s + "\n"
		  + "\033[1m本次日食概述(力学时)\033[0m\n"

		  + "偏食始：" + JD2str(r.gk3[2] + J2000) + " " + rad2str2(r.gk3[0]) + "," + rad2str2(r.gk3[1]) + "\n"
		  + "中心始：" + JD2str(r.gk1[2] + J2000) + " " + rad2str2(r.gk1[0]) + "," + rad2str2(r.gk1[1]) + "\n"
		  + (r.gk5[1] != 100 ?
			  "视午食：" + JD2str(r.gk5[2] + J2000) + " " + rad2str2(r.gk5[0]) + "," + rad2str2(r.gk5[1]) + "\n" : "")
		  + "中心终：" + JD2str(r.gk2[2] + J2000) + " " + rad2str2(r.gk2[0]) + "," + rad2str2(r.gk2[1]) + "\n"
		  + "偏食终：" + JD2str(r.gk4[2] + J2000) + " " + rad2str2(r.gk4[0]) + "," + rad2str2(r.gk4[1]) + "\n"

		  + "\033[1m中心点特征\033[0m\n"
		  + "影轴地心距 γ = " + to_str(r.D, 4) + "\n"
		  + "中心地标 (经,纬) = " + to_str((r.zxJ * radd), 2) + "," + to_str((r.zxW * radd), 2) + "\n"
		  + "中心时刻 tm = " + JD2str(r.jd + J2000) + "\n"
		  + "太阳方位 (经,纬) = " + to_str((r.Sdp[0] * radd), 0) + "," + to_str((r.Sdp[1] * radd), 0) + "\n"
		  + "日食类型 LX = " + r.lx + " " + lxb[r.lx] + "\n"
		  + "食分=" + to_str(r.sf, 4) + ", 食延=" + m2fm(r.tt * 86400, 0, 2) + ", 食带=" + to_str(r.dw, 0) + "km\n"
		  + "\n";
  }
  // std::cout<<s<<std::endl;
  return s;
 }

 //计算多个日食
 if(fs==5)
 {
  int i;
  _FEATURE r;
  int bn = 100; //并设置为多步
  s = "\033[33;1m       力学时           γ      型      中心地标      方位角           食分   食带  食延 \n\033[0m";
  for(i=0;i<bn;i++,jd+=step)
  {
   RS_GS::init(jd,3);  //中精度计算
   r = RS_GS::feature(jd);
   if(r.lx=="N") continue;
   s = s
     + "\033[31;1m"+JD2str(r.jd+J2000)  //时间
     + "  \033[33m" + to_str(r.D, 4, 7, true)     //伽马
     + "  \033[32m" + fill_str(r.lx, 2, " ") + "  \033[35m" //类型
     + to_str((r.zxJ*radd),2, 7) + "," + to_str((r.zxW*radd),2, 7)  + "  \033[34m"
     + to_str((r.Sdp[0]*radd),2,7) + "," + to_str((r.Sdp[1]*radd),2,7) + "  "
     + to_str(r.sf,4) + "  \033[36m" + to_str(r.dw,0, 3) 
     + "  \033[37m" + m2fm(r.tt*86400,0,2) + "\033[0m\n";
  }
  //std::cout<<s<<std::endl;
  return s;
 }
}

mystl::string rs2_jxb()
{ //显示界线表
 double jd = 2454679.926741-J2000; //取屏幕时间
 jd = MS_aLon_t2( int2((jd+8)/29.5306)*_pi*2 )*36525; //归朔
 RS_GS::init(jd,7);
 //std::cout<<RS_GS::jieX3(jd)<<std::endl;
 return RS_GS::jieX3(jd);
}

mystl::string shengjiang(int y, int m, int d)
{
	Date dt = { y, m, d, 12, 0, 0 };
	SZJ::L = jw.J / radd;		//设置站点参数
	SZJ::fa = jw.W / radd;
	double jd = toJD(dt) - J2000;	//取屏幕时间
	double sq = SZJ::L / pi2 * 24.0;

	mystl::string s = "\033[31;1m北京时间(转为格林尼治时间请减8小时)：\033[0m\n";
	SJ r;
	double c = J2000 + 8 / 24.0;

	r = SZJ::St(jd - sq / 24.0);
	s += "太阳升起 " + JD2str(r.s + c) + " 太阳降落 " + JD2str(r.j + c) + "\n";
	s += "日上中天 " + JD2str(r.z + c) + " 日下中天 " + JD2str(r.x + c) + "\n";
	s += "民用天亮 " + JD2str(r.c + c) + " 民用天黑 " + JD2str(r.h + c) + "\n";
	s += "航海天亮 " + JD2str(r.c2 + c) + " 航海天黑 " + JD2str(r.h2 + c) + "\n";
	s += "天文天亮 " + JD2str(r.c3 + c) + " 天文天黑 " + JD2str(r.h3 + c) + "\n";
	s += "日照长度  " + timeStr(r.j - r.s - 0.5) + " \n日光长度  " + timeStr(r.h - r.c - 0.5) + "\n";
	if (r.sm.length())
		s += "注：" + r.sm + "\n";
	r = SZJ::Mt(jd - sq / 24.0);
	s += "月亮升起 " + JD2str(r.s + c) + " 月亮降落 " + JD2str(r.j + c) + "\n";
	s += "月上中天 " + JD2str(r.z + c) + " 月下中天 " + JD2str(r.x + c) + "\n";
//	std::cout << s << std::endl;
	return s;
}

mystl::string shengjiang2(int y)
{								//太阳升降快算
	double L = jw.J / radd;		//设置站点参数
	double fa = jw.W / radd;
	Date dt = { y, 1, 1, 12 };
	double jd = toJD(dt) - J2000;	//取屏幕时间
	int i;
	mystl::string s = "", s2 = "";
	double t;
	for (i = 0; i < 368; i++)
	{
		t = sunShengJ(jd + i, L, fa, -1) + J2000 + 8 / 24.0;
		s2 += "  \033[31m" + JD2str(t).substr(1, 14) + "\033[0m  ";
		t = sunShengJ(jd + i, L, fa, 1) + J2000 + 8 / 24.0;
		s2 += timeStr(t) + "\n";
	}
	//std::cout<<;
	return to_str(y)+"年太阳年度升降表\n        升        降\n" + s + s2;
	
}

mystl::string shengjiang3(int y)
{	//年度时差
	Date dt = { y, 1, 1, 12 };
	double jd = toJD(dt);
	int i;
	double t, D;
	mystl::string s = "", s2 = "";
	for (i = 0; i < 368; i++)
	{
		D = jd + i - 8 / 24.0 - J2000, D += dt_T(D);
		t = pty_zty(D / 36525.0);
		s2 += JD2str(jd + i).substr(0, 11) + " \033[31m" + m2fm(t * 86400, 2, 2) + "\033[0m\n";
	}
//	std::cout
    return "太阳时差表(所用时间为北京时间每日12点)\n" + s + s2;
}
/*
main()
{
	rysCalc();
	std::cout<<rs_search(2008,8,200,1)<<std::endl;
	rs2_calc(5,0);
	rs2_jxb();
}
*/