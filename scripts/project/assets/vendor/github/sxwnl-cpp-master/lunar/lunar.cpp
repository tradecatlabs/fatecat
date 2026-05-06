#include <cstring>
#include "lunar.h"
#include "lunar_ssq.h"
#include "../eph/eph0.h"
#include "../mylib/tool.h"
#include "../mylib/math_patch.h"

void init_ob()
{
	OBA::init();
	OBB::init();
	SSQ::init();
}

/*返回公历某一个月的'公农回'三合历*/
OB_LUN yueLiCalc(int By, int Bm)
{
	int i, j, k, D, Bd0, Bdn, xn;
	//日历物件初始化
	Date JD = { By, Bm, 1, 12, 0, 0.1 };
	Bd0 = int2(toJD(JD)) - J2000;	//公历月首,中午
	JD.M++;
	if (JD.M > 12)
		JD.Y++, JD.M = 1;
	Bdn = int2(toJD(JD)) - J2000 - Bd0;	//本月天数(公历)

	OB_LUN lun;
	lun.w0 = (Bd0 + J2000 + 1 + 7000000) % 7;	//本月第一天的星期
	lun.y = By;	//公历年份
	lun.m = Bm;	//公历月分
	lun.d0 = Bd0;
	lun.dn = Bdn;
	
	lun.nianhao = OBB::getNH(By);
	
	double w;
	OB_DAY *ob,*ob2;
	//提取各日信息
	for (i = 0, j = 0; i < Bdn; i++)
	{
		ob = &lun.day[i];
		ob->d0 = Bd0 + i;		//儒略日,北京时12:00
		ob->di = i;				//公历月内日序数
		ob->y  = By;    //公历年
		ob->m  = Bm;    //公历月
		ob->dn = Bdn;   //公历月天数
		ob->week0 = lun.w0; //月首的星期
		ob->week = (lun.w0 + i) % 7;	//当前日的星期
		ob->weeki = int2((lun.w0 + i) / 7);	//本日所在的周序号
		ob->weekN = int2((lun.w0 + Bdn - 1) / 7) + 1;	//本月的总周数
		JD = setFromJD(ob->d0 + J2000);
		ob->d = JD.D;			//公历日名称

		//农历月历
		if (!SSQ::ZQ[0] || ob->d0 < SSQ::ZQ[0] || ob->d0 >= SSQ::ZQ[24])	//如果d0已在计算农历范围内则不再计算
			SSQ::calcY(ob->d0);
		int mk = int2((ob->d0 - SSQ::HS[0]) / 30.0);
		if (mk < 13 && SSQ::HS[mk + 1] <= ob->d0)
			mk++;				//农历所在月的序数

		ob->Ldi = ob->d0 - SSQ::HS[mk];	//距农历月首的编移量,0对应初一
		ob->Ldc=str_rmc[ob->Ldi];	//农历日名称
		
		ob->cur_dz = ob->d0 - SSQ::ZQ[0]; 	// 距冬至的天数
		ob->cur_xz = ob->d0 - SSQ::ZQ[12];	// 距夏至的天数
		ob->cur_lq = ob->d0 - SSQ::ZQ[15];	// 距立秋的天数
		ob->cur_mz = ob->d0 - SSQ::ZQ[11];	// 距芒种的天数
		ob->cur_xs = ob->d0 - SSQ::ZQ[13];	// 距小暑的天数

		if (ob->d0 == SSQ::HS[mk] || ob->d0 == Bd0)
		{						//月的信息
			ob->Lmc = SSQ::ym[mk];	//月名称
			ob->Ldn = SSQ::dx[mk];	//月大小
			ob->Lleap = (SSQ::leap && SSQ::leap == mk) ? "闰" : "";	//闰状况
			ob->Lmc2= mk<13?SSQ::ym[mk+1]:"未知";
		}
		else
		{
			ob2 = &lun.day[i - 1];
			ob->Lmc = ob2->Lmc;
			ob->Ldn = ob2->Ldn;
			ob->Lleap = ob2->Lleap;
			ob->Lmc2=ob2->Lmc2;
		}
		int qk = int2((ob->d0 - SSQ::ZQ[0] - 7) / 15.2184);
		if (qk < 23 && ob->d0 >= SSQ::ZQ[qk + 1])
			qk++;	//节气的取值范围是0-23
		if (ob->d0 == SSQ::ZQ[qk])
			ob->Ljq =str_jqmc[qk];
		else
			ob->Ljq = "";

		ob->yxmc = "";	//月相名称,月相时刻(儒略日),月相时间串
		ob->jqmc = "";	//定气名称,节气时刻(儒略日),节气时间串

		//干支纪年处理
		//以立春为界定年首
		D = SSQ::ZQ[3] + (ob->d0 < SSQ::ZQ[3] ? -365 : 0) + 365.25 * 16 - 35;	//以立春为界定纪年
		ob->Lyear = floor(D / 365.2422 + 0.5);	//农历纪年(10进制,1984年起算)
		//以下几行以正月初一定年首
		D = SSQ::HS[2];	//一般第3个月为春节
		for (j = 0; j < 14; j++)
		{						//找春节
			if (SSQ::ym[j] != "正" || SSQ::leap == j && j)
				continue;
			D = SSQ::HS[j];
			if (ob->d0 < D)
			{
				D -= 365;
				break;
			}//无需再找下一个正月
		}
		D = D + 5810;//计算该年春节与1984年平均春节(立春附近)相差天数估计
		ob->Lyear0 = floor(D / 365.2422 + 0.5);
		D = ob->Lyear + 12000;
		ob->Lyear2 = str_gan[D % 10];
		ob->Lyear2 += str_zhi[D % 12];//干支纪年(立春)
		D = ob->Lyear0 + 12000;
		ob->Lyear3 = str_gan[D % 10];
		ob->Lyear3 += str_zhi[D % 12];//干支纪年(正月)
		ob->Lyear4 = ob->Lyear0 + 1984 + 2698;//黄帝纪年

		//纪月处理,1998年12月7(大雪)开始连续进行节气计数,0为甲子
		mk = int2((ob->d0 - SSQ::ZQ[0]) / 30.43685);
		if (mk < 12 && ob->d0 >= SSQ::ZQ[2 * mk + 1])
			mk++;//相对大雪的月数计算,mk的取值范围0-12

		D = mk + int2((SSQ::ZQ[12] + 390) / 365.2422) * 12 + 900000;	//相对于1998年12月7(大雪)的月数,900000为正数基数
		ob->Lmonth = D % 12;
		ob->Lmonth2 = str_gan[D % 10];
		ob->Lmonth2 += str_zhi[D % 12];

		//纪日,2000年1月7日起算
		D = ob->d0 - 6 + 9000000;
		ob->Lday2 = str_gan[D % 10];
		ob->Lday2 += str_zhi[D % 12];

		//星座
		mk = int2((ob->d0 - SSQ::ZQ[0] - 15) / 30.43685);
		if (mk < 11 && ob->d0 >= SSQ::ZQ[2 * mk + 2])
			mk++;				//星座所在月的序数,(如果j=13,ob->d0不会超过第14号中气)
		ob->XiZ = str_xz[(mk + 12) % 12];
		
		
		//回历
		OBA::getHuiLi(ob->d0,*ob);
		//节日
	    OBA::getDayName(*ob); //公历
	    OBB::getDayName2(*ob); //农历
	}

	//以下是月相与节气的处理
	double d, jd2 = Bd0 + dt_T(Bd0) - 8 / 24.0;
	//月相查找
	w = MS_aLon(jd2 / 36525, 10, 3);
	w = int2((w - 0.78) / M_PI * 2) * M_PI / 2;
	do
	{
		d = OBB::so_accurate(w);
		D = int2(d + 0.5);
		xn = int2(w / pi2 * 4 + 4000000.01) % 4;
		w += pi2 / 4;
		if (D >= Bd0 + Bdn)
			break;
		if (D < Bd0)
			continue;
		ob = &lun.day[D - Bd0];
		ob->yxmc = str_yxmc[xn];			//取得月相名称
		ob->yxjd = d;
		ob->yxsj = timeStr(d);
	}
	while (D + 5 < Bd0 + Bdn);

	//节气查找
	w = S_aLon(jd2 / 36525, 3);
	w = int2((w - 0.13) / pi2 * 24) * pi2 / 24;
	do
	{
		d = OBB::qi_accurate(w);
		D = int2(d + 0.5);
		xn = int2(w / pi2 * 24 + 24000006.01) % 24;
		w += pi2 / 24.0;
		if (D >= Bd0 + Bdn)
			break;
		if (D < Bd0)
			continue;
		ob = &lun.day[D - Bd0];
		ob->jqmc = str_jqmc[xn];			//取得节气名称
		ob->jqjd = d;
		ob->jqsj = timeStr(d);
	}
	while (D + 12 < Bd0 + Bdn);
	return lun;
}

mystl::string nianLiSTR(int y)
{ //字符串年历生成
 int i,j;
 mystl::string s="", s1,s2;
 double v,qi;
 SSQ::calcY( int2((y-2000.0)*365.2422+180) );
 for(i=0;i<14;i++)
 {
  if(SSQ::HS[i+1]>SSQ::ZQ[24]) break; //已包含下一年的冬至
  if(SSQ::leap && i==SSQ::leap) s1="闰"; else s1="  ";
  s1 += SSQ::ym[i];
  if(s1.length()<6 || (s1.length()<9&&(SSQ::leap && i==SSQ::leap))) 
  s1 += "月";
  s1 += SSQ::dx[i]>29?"大":"小";
  s1 += " "+JD2str(SSQ::HS[i]+J2000).substr(6,5);

  v = OBB::so_accurate2(SSQ::HS[i]);
  s2 = "("+ JD2str(v+J2000).substr(9,11)+")";
  if(int2(v+0.5)!=SSQ::HS[i]) s2 = "\033[31m"+s2+"\033[0m";
 // s2+="\n";
  //v=(v+0.5+J2000)%1; if(v>0.5) v=1-v; if(v<8/1440) s2 = "<u>"+s2+"</u>"; //对靠近0点的加注
  s1 += s2;

  for(j=-2;j<24;j++)
  {
    if(j>=0)  qi=SSQ::ZQ[j];
    if(j==-1) qi=SSQ::pe[0];
    if(j==-2) qi=SSQ::pe[1];

    if(qi<SSQ::HS[i] || qi>=SSQ::HS[i+1]) continue;
    s1 += "  ";
    s1 += str_jqmc[(j+24)%24]+JD2str(qi+J2000).substr(6,5);

    v = OBB::qi_accurate2(qi);
    s2 = "("+ JD2str(v+J2000).substr(9,11)+")";
    if(int2(v+0.5)!=qi) s2 = "\033[31m"+s2+"\033[0m";
    //v=(v+0.5+J2000)%1; if(v>0.5) v=1-v; if(v<8/1440) s2 = "<u>"+s2+"</u>"; //对靠近0点的加注
    s1 += s2;
  }
  s += s1 + "\n";
 }
 return s;
}

/*
main()
{
	init_ob();
//	OB_LUN lun=yueLiCalc(2008,1);
	std::cout<<nianLiSTR(2009);
}
*/