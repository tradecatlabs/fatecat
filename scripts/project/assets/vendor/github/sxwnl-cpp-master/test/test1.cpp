/*
寿星天文历v5.05js版 C++翻译工程
API测试
2018-8-28
*/
#include <ctime>
#include <iostream>
#include <array>

#include "../mylib/tool.h"
#include "../lunar/lunar.h"
#include "../eph/eph_show.h"
#include "../eph/eph0.h"
#include "../eph/eph.h"
#include "../mylib/lat_lon_data.h"
#include "../mylib/tool.h"
#include "../mylib/math_patch.h"
#include "../mylib/mystl/static_array.h"
#include "../mylib/mystl/map.h"

#define MAP_H 18
#define MAP_W  7
std::array<std::array<mystl::string,MAP_W>,MAP_H> strmap;

#include <iostream>
#include <chrono>

mystl::string txFormatT(double t)
{ //天象时间格式化输出
    double t1 = t * 36525 + J2000;
    double t2 = t1 - dt_T(t1 - J2000) + 8.0 / 24;
    return JD2str(t1) + " TD " + JD2str(t2).substr(9, 11) + " UT ";
}

void tianXiang(int xm, int xm2, Date dat,int n=10)
{
    mystl::static_array<mystl::string,9> xxName = {"地球","水星","金星","火星","木星","土星","天王星","海王星","冥王星"};
    double jd = toJD({dat.Y, dat.M, dat.D}) - J2000;//取屏幕时间
    mystl::string s = "";
    int i;
    double re0;
    mystl::array2 re;
    mystl::array4 re2;
    jd /= 36525.0;
    if (xm == 1 || xm == 2)
    { //求月亮近远点
        for (i = 0; i < n; i++, jd = re[0] + 27.555 / 36525.0)
        {
            if (xm == 1)
                re = moonMinR(jd, 1);//求近点
            if (xm == 2)
                re = moonMinR(jd, 0);//求远点
            s += txFormatT(re[0]) + to_str(re[1],2) + "千米\n";
        }

    }
    if (xm == 3 || xm == 4)
    { //求月亮升降交点
        for (i = 0; i < n; i++, jd = re[0] + 27.555 / 36525.0)
        {
            if (xm == 3)
                re = moonNode(jd, 1);//求升
            if (xm == 4)
                re = moonNode(jd, 0);//求降
            s += txFormatT(re[0]) + rad2str(rad2mrad(re[1]), 0) + "\n";
        }

    }
    if (xm == 5 || xm == 6)
    { //求地球近远点
        for (i = 0; i < n; i++, jd = re[0] + 365.259636 / 36525.0)
        {
            if (xm == 5)
                re = earthMinR(jd, 1);//求近点
            if (xm == 6)
                re = earthMinR(jd, 0);//求远点
            s += txFormatT(re[0]) + to_str(re[1],8) + " AU\n";
        }
    }
    if (xm == 7 || xm == 8)
    { //大距计算
        for (i = 0; i < n; i++, jd = re[0] + 115.8774777586 / 36525.0)
        {
            if (xm == 7)
                re = daJu(1, jd, 1);//求水星东大距
            if (xm == 8)
                re = daJu(1, jd, 0);//求水星东西距
            s += txFormatT(re[0]) + to_str((re[1] / M_PI * 180),5) + "度\n";
        }
    }
    if (xm == 9 || xm == 10)
    { //大距计算
        for (i = 0; i < n; i++, jd = re[0] + 583.9213708245 / 36525.0)
        {
            if (xm == 9)
                re = daJu(2, jd, 1);//求金星东大距
            if (xm == 10)
                re = daJu(2, jd, 0);//求金星东西距
            s += txFormatT(re[0]) + to_str((re[1] / M_PI * 180),5) + "度\n";
        }
    }
    if (xm == 11)
    { //合月计算
        s += xxName[xm2] + "赤经合月\n";
        s += "合月时间(TD UT) 星月赤纬差(小于1度可能月掩星,由视差决定)\n";
        for (i = 0; i < n; i++, jd = re2[0] + 28.0 / 36525.0)
        {
            re2 = xingHY(xm2, jd);
            s += txFormatT(re2[0]) + to_str((-re2[1] / M_PI * 180),5) + "度\n";
        }
    }
    if (xm == 12 || xm == 13)
    {
        if (xm == 12)
            s = xxName[xm2] + "合日(地内行星上合)\n";
        if (xm == 13)
            s = xxName[xm2] + "冲日(地内行星下合)\n";
        s += "黄经合/冲日时间(TD UT) 星日赤纬差\n";
        for (i = 0; i < n; i++, jd = re[0] + cs_xxHH[xm2 - 1] / 36525.0)
        {
            if (xm == 12)
                re = xingHR(xm2, jd, 0);
            if (xm == 13)
                re = xingHR(xm2, jd, 1);
            s += txFormatT(re[0]) + to_str((-re[1] / M_PI * 180),5) + "度\n";
        }
    }

    if (xm == 14 || xm == 15)
    { //顺留
        if (xm == 14)
            s = xxName[xm2] + "顺留\n";
        if (xm == 15)
            s = xxName[xm2] + "逆留\n";
        s += "留时间(TD UT)\n";
        for (i = 0; i < n; i++, jd = re0 + cs_xxHH[xm2 - 1] / 36525.0)
        {
            if (xm == 14)
                re0 = xingLiu(xm2, jd, 1);
            if (xm == 15)
                re0 = xingLiu(xm2, jd, 0);
            s += txFormatT(re0) + "\n";
        }
    }
    std::cout<< s<<std::endl;
}

void pCalc(int xt,Date dat, int n=10, int dt=1, bool Cd_ut=1)
{ //行星星历计算
    double jd = toJD({dat.Y,dat.M,dat.D,dat.h,dat.m,dat.s}) - J2000;//取屏幕时间
    if (Cd_ut)
        jd += -8.0 / 24 + dt_T(jd);//转为力学时
    double L = jw.J / 180 * M_PI;//地标
    double fa = jw.W / 180 * M_PI;
    if (n > 1000)
    {
        std::cout<<"个数太多了"<<std::endl;
        return;
    }
    mystl::string s = "";
    int i;
    //求星历
    for (i = 0; i < n; i++, jd += dt)
    {
        double jd2 = jd + 2451545;
        s += JD2str(jd2) + "TD, JED = " + to_str(jd2,7) + " " + "\n";
        s += xingX(xt, jd, L, fa) + "\n";
    }
    std::cout<< s<<std::endl;
}

void suoCalc(int y,int n=24,int jiao=0)
{//定朔测试函数
    y-=2000;
    if (jiao == -1)
    {
        std::cout<<"请输入角度(0朔,90上弦,180望,270下弦,或其它):"<<std::endl;
        std::cin>>jiao;
    }
    int i;
    double r, T;
    mystl::string s = "月-日黄经差" + to_str(jiao) + "\n", s2 = "";
    int n0 = int2(y * (365.2422 / 29.53058886));//截止当年首经历朔望的个数
    for (i = 0; i < n; i++)
    {
        T = MS_aLon_t((n0 + i + jiao / 360.0) * 2 * M_PI);//精确时间计算,入口参数是当年各朔望黄经
        r = XL1_calc(2, T, -1);//计算月亮
        s2 += JD2str(T * 36525 + J2000 + 8.0 / 24 - dt_T(T * 36525)) + " " + to_str(r,2) + "千米\n";//日期转为字串
        if (i % 50 == 0)
            s += s2, s2 = "";
    }

    std::cout<< s + s2<<std::endl;
}

void qiCalc(int y,int n=24)
{//定气测试函数
    y-=2000;
    int i;
    double T;
    mystl::string s = "", s2 = "";
    
    for (i = 0; i < n; i++)
    {
        T = S_aLon_t((y + i * 15 / 360.0 + 1) * 2 * M_PI);//精确节气时间计算
        s2 += JD2str(T * 36525 + J2000 + 8 / 24.0 - dt_T(T * 36525)) + str_jqmc[(i + 6) % 24];//日期转为字串
        if (i % 2 == 1)
            s2 += " 视黄经" + to_str(i * 15) + "\n";
        else
        s2 += " " ;
        if (i % 50 == 0)
            s += s2, s2 = "";
    }
    std::cout<< s + s2<<std::endl;
}

void houCalc(int y,int n=24)
{//定候测试函数
    y-=2000;
    int i;
    double T;
    mystl::string s = "初候　　　　　　　　　　　　二候　　　　　　　　　三候", s2 = "";    
    for (i = 0; i < n * 3; i++)
    {
        T = S_aLon_t((y + i * 5 / 360.0 + 1) * 2 * M_PI);//精确节气时间计算
        if (i % 3 == 0)
            s2 = s2+"\n" + str_jqmc[(i / 3 + 6) % 24];
        else
            s2 += " ";
        s2 += JD2str(T * 36525 + J2000 + 8.0 / 24.0 - dt_T(T * 36525));//日期转为字串
        if (i % 50 == 0)
            s += s2, s2 = "";
    }
    std::cout<< s + s2<<std::endl;
}

void dingQi_cmp(int y = 2000, int N = 10)
{//定气误差测试
    y -= 2000;
    int i;
    double W, T, maxT = 0;
    for (i = 0; i < N; i++)
    {
        W = (y + i / 24) * 2 * M_PI;
        T = S_aLon_t2(W) - S_aLon_t(W);//节气粗算与精算的差异
        T = int2(abs(T * 36525 * 86400));
        if (T > maxT)
            maxT = T;
    }
    std::cout << "\033[31;1m" << to_str(2000 + y) << "年之后" << to_str(N) << "个朔日粗算与精算的最大差异:" << to_str(maxT) << "秒。\033[0m" << std::endl;
}

void dingSuo_cmp(int y=2000,int N=10)
{ //定朔测试函数
    y-=2000;
    int i; 
    double T, maxT = 0,W;
    int n = int2(y * (365.2422 / 29.53058886));//截止当年首经历朔望的个数
    for (i = 0; i < N; i++)
    {
        W = (n + i / 24.0) * 2 * M_PI;
        T = MS_aLon_t2(W) - MS_aLon_t(W);//合塑粗算与精算的差异
        T = int2(abs(T * 36525 * 86400));
        if (T > maxT)
            maxT = T;
    }
    std::cout<<"\033[31;1m"<< to_str(2000 + y) << "年之后" << to_str(N) << "个朔日粗算与精算的最大差异:" << to_str(maxT) << "秒。\033[0m"<<std::endl;
}

void dingQi_v()
{ //定气计算速度测试
    int i;
    auto d1 = std::chrono::system_clock::now();
    for (i = 0; i < 10000; i++)
        S_aLon_t(0);
    auto d2 = std::chrono::system_clock::now();
    for (i = 0; i < 10000; i++)
        S_aLon_t2(0);
        
    auto d3 = std::chrono::system_clock::now();
    std::cout<< "定气测试\n\033[31;1m高精度:" << std::chrono::duration<double> (d2 - d1).count()*1000 << "毫秒/10千个\n" << "低精度:" << std::chrono::duration<double> (d3 - d2).count()*1000 << "毫秒/10千个\n\033[0m";
}

void dingSuo_v() 
{ //定朔计算速度测试
    int i;
    auto d1 = std::chrono::system_clock::now();
    for (i = 0; i < 10000; i++)
        MS_aLon_t(0);

    auto d2 = std::chrono::system_clock::now();
    for (i = 0; i < 10000; i++)
        MS_aLon_t2(0);

    auto d3 = std::chrono::system_clock::now(); 
    std::cout<< "\033[31;1m高精度:" << std::chrono::duration<double> (d2 - d1).count()*1000 << "毫秒/10千个\n" << "低精度:" << std::chrono::duration<double> (d3 - d2).count()*1000 << "毫秒/10千个\n\033[0m";
}

void ML_calc(Date dat)
{
    MLBZ ob={};
    double jd = toJD({dat.Y,dat.M,dat.D,dat.h,dat.m,dat.s});
    OBB::mingLiBaZi( jd+(-8.0)/24-J2000, jw.J/radd, ob ); //八字计算

    std::cout<<
     "\033[31;1m[日标]：\033[0m"<<"公历 "<<dat.Y<<"-"<<dat.M<<"-"<<dat.D << " 儒略日数 " << int2(jd+0.5) << " 距2000年首" << int2(jd+0.5-J2000) << "日\n"
   << "\033[31;1m[八字]：\033[0m"    << ob.bz_jn<<"年 "<<ob.bz_jy<<"月 "<<ob.bz_jr<<"日 "<<ob.bz_js<<"时 真太阳 \033[31m" << ob.bz_zty<< "\033[0m"
   << "\n\033[1;32m[纪时]：\033[0m" << ob.bz_JS << "\n"
   << "\033[1;32m[时标]：\033[0;1;35m" << "23　 01　 03　 05　 07　 09　 11　 13　 15　 17　 19　 21　 23\033[0m"<<std::endl;
}

Date get_time(void)
{
    struct tm *bjs;
    time_t time0;
    time0 = time(NULL);
    bjs = localtime(&time0);
    Date dat=
    {
        bjs->tm_year + 1900,
        bjs->tm_mon+1,
        bjs->tm_mday,
        bjs->tm_hour,
        bjs->tm_min,
        (double)bjs->tm_sec
    };
    return dat;
}

void initmap(OB_LUN lun)
{
    mystl::map<mystl::string,mystl::string> str_yx={{"望","\033[33m●"},{"上弦","\033[33m∪"},{"朔","\033[38;5;245m●"},{"下弦","\033[33m∩"}};
    for (int i=0;i<18;i++)
    {
        for (int j=0;j<7;j++)
        {
            if (i%3==2)
            strmap[i][j]="\033[32m--------";
            else 
            strmap[i][j]="        ";
        }
    }
    for (int i = 0;i < lun.dn;i++)
    {
        int y=lun.day[i].weeki;
        int x=lun.day[i].week;
        int j=i<9?6:4;
        strmap[y*3][x] = x==0||x==6?"\033[31m":"\033[37m";
        strmap[y*3][x] += str_rmc0[i];
        if (lun.day[i].jqmc.length())
            strmap[y*3][x]+="\033[32m◆",j--;
        if (lun.day[i].yxmc.length())
            strmap[y*3][x]+=str_yx[lun.day[i].yxmc],j--;
        for (int k = 0;k < j;k++)
            strmap[y*3][x]+=" \033[0m\033[1m";
        if (!j) 
            strmap[y*3][x]+="\033[0m\033[1m";
        if (lun.day[i].Ldi==0)
            strmap[y*3+1][x]="\033[38;5;123m",strmap[y*3+1][x]
            =strmap[y*3+1][x]+lun.day[i].Lleap+strmap[y*3+1][x]
            +lun.day[i].Lmc+strmap[y*3+1][x]
            +(lun.day[i].Lmc.length()==6?"":"月")
            +strmap[y*3+1][x]+str_dx[lun.day[i].Ldn-29]+strmap[y*3+1][x]
            +(lun.day[i].Lleap.length()?"\033[0m\033[1m":"  \033[0m\033[1m");
        else
            strmap[y*3+1][x]="",strmap[y*3+1][x]=strmap[y*3+1][x]
            +lun.day[i].Ldc+strmap[y*3+1][x]+"    \033[0m\033[1m";
        if (lun.day[i].Ljq.length())
            strmap[y*3+1][x]="\033[34m",strmap[y*3+1][x]=strmap[y*3+1][x]
            +lun.day[i].Ljq+strmap[y*3+1][x]+="    \033[0m\033[1m";
            
    }
//    printf("公元 %04d年%02d月%02d日 周%s %s座\n",lun.day[1].XiZ);
}
void drawmap()
{
    for (int k=0;k<MAP_W;k++)
        std::cout<<"\033[3"<<((k&&k<6)?3:1)<<";1m周"<<str_xqmc[k]<<"    ";
    std::cout<<std::endl;
    for (int k=0;k<MAP_W*4;k++)
        std::cout<<"\033[33m--";
    std::cout<<std::endl;
    for (std::array<mystl::string,MAP_W> i:strmap)
    {
        for (mystl::string j:i)
            std::cout<<j;
        std::cout<<std::endl;
    }
    std::cout<<"\033[0m";
}
int main()
{
#if defined(_WIN32) || defined(_MSC_VER)
    system("@chcp 65001");
#endif


    Date dat=get_time();
    
    // 农历基础
    init_ob();
    
    OB_LUN lun=yueLiCalc(dat.Y,dat.M);
    std::cout<<DD2str(get_time())<<std::endl;
    std::cout<<lun.nianhao<<std::endl; //年号
    
    initmap(lun);
    drawmap();
    
    // 节日
    for (int i = 0;i < 30;i++)
    {
        std::cout<<lun.day[i].y<<"年"<<lun.day[i].m<<"月"<<lun.day[i].d<<"日: "<<lun.day[i].Lday2;
        if (lun.day[i].A.length())
        std::cout<<"A"<<lun.day[i].A;
        if (lun.day[i].B.length())
        std::cout<<"B"<<lun.day[i].B;
        if (lun.day[i].C.length())
        std::cout<<"C"<<lun.day[i].C;
        
        std::cout<<std::endl;
    }
    
    // 星历计算
    pCalc(1, {2008,1,1}, 3);
    // 天象
    tianXiang(15,2,{2022,1,1});
    
    // 气朔测试
    dingQi_v ();
    dingSuo_v();
    
    /*
    int y=dat.Y;
    suoCalc(y);
    qiCalc (y);
    houCalc(y); // 定候
    */
    // 粗算气朔误差
    // dingQi_cmp();
    // dingSuo_cmp(2000,10);
    
    // 命理八字
    ML_calc(dat);
    
    // 升降
    std::cout<<"\n========--升降计算--========\n";
    std::cout<<shengjiang(dat.Y, dat.M, dat.D)<<"\n";
    
    // 日月食
    Date d = {2008, 8, 1, 18, 17, 15.0};
    std::cout<<rysCalc(d, true, false)<<"\n";
    
    std::cout<<rs_search(2008,8,200,1)<<std::endl; // 日食粗搜索
    std::cout<<rs2_calc(5,0,29.5306)<<"\n";
    
  //  rs2_jxb();     // 日食界线表

#if defined(_WIN32) || defined(_MSC_VER)
    system("pause");
#endif
    return 0;
}