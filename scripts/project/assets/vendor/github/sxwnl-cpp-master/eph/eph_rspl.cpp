#include "eph.h"
#include "eph0.h"
#include "eph_rsgs.h"
#include "eph_rspl.h"
#include "../mylib/tool.h"
#include "../mylib/math_patch.h"

bool RS_PL::nasa_r = 0;//为1表示采用NASA的视径比
mystl::array5 RS_PL::sT;//地方日食时间表
mystl::string RS_PL::LX;
double RS_PL::sf;
double RS_PL::sf2;
double RS_PL::sf3;
mystl::string RS_PL::sflx;
double RS_PL::b1;
double RS_PL::dur;
double RS_PL::sun_s;
double RS_PL::sun_j;
double RS_PL::P1;
double RS_PL::V1;
double RS_PL::P2;
double RS_PL::V2;

mystl::array3 RS_PL::A={};
mystl::array3 RS_PL::B={}; //本半影锥顶点坐标
_ZB RS_PL::P={};//t1时刻的日月坐标,g为恒星时
_ZB RS_PL::Q={};//t2时刻的日月坐标
mystl::array10 RS_PL::V;//食界表
mystl::string RS_PL::Vc = "";
mystl::string RS_PL::Vb = "";  //食中心类型,本影南北距离

void RS_PL::secXY(double jd,double L,double fa,double high,_SECXY &re)
{ //日月xy坐标计算。参数：jd是力学时,站点经纬L,fa,海拔high(千米)
  //基本参数计算
  double deltat = dt_T(jd); //TD-UT
  mystl::array2 zd=nutation2(jd/36525.0);
  double gst= pGST(jd-deltat,deltat) + zd[0]*cos(hcjj(jd/36525.0) + zd[1]); //真恒星时(不考虑非多项式部分)

  mystl::array3 z;
  //=======月亮========
  z=RS_GS::moon(jd); re.mCJ=z[0]; re.mCW=z[1]; re.mR=z[2]; //月亮视赤经,月球赤纬
  double mShiJ = rad2rrad(gst + L - z[0]); //得到此刻月亮时角
  z=parallax(z, mShiJ,fa, high); re.mCJ2=z[0], re.mCW2=z[1], re.mR2=z[2]; //修正了视差的赤道坐标

  //=======太阳========
  z=RS_GS::sun(jd); re.sCJ=z[0]; re.sCW=z[1]; re.sR=z[2]; //太阳视赤经,太阳赤纬
  double sShiJ = rad2rrad(gst + L - z[0]); //得到此刻太阳时角
  z=parallax(z,sShiJ,fa,high); re.sCJ2=z[0], re.sCW2=z[1], re.sR2=z[2]; //修正了视差的赤道坐标

  //=======视半径========
  re.mr = cs_sMoon/re.mR2/rad;
  re.sr = 959.63/re.sR2/rad*cs_AU;
  if(RS_PL::nasa_r) re.mr*=cs_sMoon2/cs_sMoon; //0.99925;
  //=======日月赤经纬差转为日面中心直角坐标(用于日食)==============
  re.x = rad2rrad(re.mCJ2-re.sCJ2) * cos((re.mCW2+re.sCW2)/2.0);
  re.y = re.mCW2-re.sCW2;
  re.t = jd;
}

double RS_PL::lineT(_SECXY G, double v,double u, double r, bool n)
{//已知t1时刻星体位置、速度，求x*x+y*y=r*r时,t的值
  double b=G.y*v-G.x*u;
  double A=u*u+v*v;
  double B=u*b;
  double C=b*b-r*r*v*v;
  double D=B*B-A*C;
  if(D<0) return 0;
  D=sqrt(D); if(!n) D=-D;
  return G.t+((-B+D)/A-G.x)/v;
}

void RS_PL::secMax(double jd,double L,double fa,double high)
{ //日食的食甚计算(jd为近朔的力学时,误差几天不要紧)
  int i;
  for(i=0;i<5;i++) RS_PL::sT[i]=0; //分别是:食甚,初亏,复圆,食既,生光
  RS_PL::LX=""; //类型
  RS_PL::sf=0;  //食分
  RS_PL::b1=1.0;  //月日半径比(食甚时刻)
  RS_PL::dur = 0; //持续时间
  RS_PL::P1 = RS_PL::V1 = 0;  //初亏方位,P北点起算,V顶点起算
  RS_PL::P2 = RS_PL::V2 = 0;  //复圆方位,P北点起算,V顶点起算
  RS_PL::sun_s = RS_PL::sun_j = 0; //日出日没
  RS_PL::sf2=0; //食分(日出食分)
  RS_PL::sf3=0; //食分(日没食分)
  RS_PL::sflx = " "; //食分类型
  RS_GS::init(jd,7);
  jd=RS_GS::Zjd; //食甚初始估值为插值表中心时刻(粗朔)

  _SECXY G={}, g={};
  RS_PL::secXY(jd,L,fa,high,G);
  jd -= G.x/0.2128; //与食甚的误差在20分钟以内

  double u,v,dt=60/86400.0,dt2;
  for (i=0;i<2;i++)
  {
   RS_PL::secXY(jd,L,fa,high,G);
   RS_PL::secXY(jd+dt,L,fa,high,g);
   u = (g.y-G.y)/dt;
   v = (g.x-G.x)/dt;
   dt2 = -(G.y*u+G.x*v)/(u*u+v*v);
   jd += dt2; //极值时间
  }

  // 求直线到太阳中心的最小值
  // double x=G.x+dt2*v, y=G.y+dt2*u, rmin=sqrt(x*x+y*y); 
  // js v5.10更新计算公式
  double maxsf = 0, maxjd = jd, rmin, ls, tt;
  for (i = -30; i < 30; i += 6) {
   tt = jd + i / 86400.0;
   RS_PL::secXY(tt, L, fa, high, g);
   ls = (g.mr + g.sr - sqrt(g.x * g.x + g.y * g.y)) / g.sr / 2;
   if (ls > maxsf) maxsf = ls, maxjd = tt;
  }
  jd = maxjd;
  for (i = -5; i < 5; i += 1) {
   tt = jd + i / 86400.0;
   RS_PL::secXY(tt, L, fa, high, g);
   ls = (g.mr + g.sr - sqrt(g.x * g.x + g.y * g.y)) / g.sr / 2;
   if (ls > maxsf) maxsf = ls, maxjd = tt;
  }
  jd = maxjd;
  RS_PL::secXY(jd, L, fa, high, G);
  rmin = sqrt(G.x * G.x + G.y * G.y);

  RS_PL::sun_s = sunShengJ(jd-dt_T(jd)+L/pi2,L,fa,-1) + dt_T(jd);; //日出 统一用力学时
  RS_PL::sun_j = sunShengJ(jd-dt_T(jd)+L/pi2,L,fa, 1) + dt_T(jd);; //日没 统一用力学时

  if(rmin<=G.mr+G.sr)
  { //偏食计算
   RS_PL::sT[1] = jd; //食甚
   RS_PL::LX="偏";
   RS_PL::sf=(G.mr+G.sr-rmin)/G.sr/2.0; //食分
   RS_PL::b1=G.mr/G.sr;
   
   RS_PL::secXY(RS_PL::sun_s,L,fa,high,g); //日出食分
   RS_PL::sf2=(g.mr+g.sr-sqrt(g.x*g.x+g.y*g.y))/g.sr/2; //日出食分
   if(RS_PL::sf2<0) RS_PL::sf2=0;

   RS_PL::secXY(RS_PL::sun_j,L,fa,high,g); //日没食分
   RS_PL::sf3=(g.mr+g.sr-sqrt(g.x*g.x+g.y*g.y))/g.sr/2; //日没食分
   if(RS_PL::sf3<0) RS_PL::sf3=0;

   RS_PL::sT[0] = RS_PL::lineT(G,v,u, G.mr+G.sr, 0); //初亏
   for(i=0;i<3;i++)
   { //初亏再算3次
    RS_PL::secXY(RS_PL::sT[0],L,fa,high,g);
    RS_PL::sT[0] = RS_PL::lineT(g,v,u, g.mr+g.sr, 0);
   }

   RS_PL::P1 = rad2mrad(atan2(g.x,g.y)); //初亏位置角
   RS_PL::V1 = rad2mrad(RS_PL::P1-shiChaJ(pGST2(RS_PL::sT[0]),L,fa,g.sCJ,g.sCW)); //这里g.sCJ与g.sCW对应的时间与sT[0]还差了一点，所以有一小点误差，不采用真恒星时也误差一点

   RS_PL::sT[2] = RS_PL::lineT(G,v,u, G.mr+G.sr, 1); //复圆
   for(i=0;i<3;i++)
   { //复圆再算3次
    RS_PL::secXY(RS_PL::sT[2],L,fa,high,g);
    RS_PL::sT[2] = RS_PL::lineT(g,v,u, g.mr+g.sr, 1);
   }
   RS_PL::P2 = rad2mrad(atan2(g.x,g.y));
   RS_PL::V2 = rad2mrad(RS_PL::P2-shiChaJ(pGST2(RS_PL::sT[2]),L,fa,g.sCJ,g.sCW)); //这里g.sCJ与g.sCW对应的时间与sT[2]还差了一点，所以有一小点误差，不采用真恒星时也误差一点
  }
  if(rmin<=G.mr-G.sr){ //全食计算
   RS_PL::LX="全";
   RS_PL::sT[3] = RS_PL::lineT(G,v,u, G.mr-G.sr, 0); //食既
   RS_PL::secXY(RS_PL::sT[3],L,fa,high,g);
   RS_PL::sT[3] = RS_PL::lineT(g,v,u, g.mr-g.sr, 0); //食既再算1次

   RS_PL::sT[4] = RS_PL::lineT(G,v,u, G.mr-G.sr, 1); //生光
   RS_PL::secXY(RS_PL::sT[4],L,fa,high,g);
   RS_PL::sT[4] = RS_PL::lineT(g,v,u, g.mr-g.sr, 1); //生光再算1次
   RS_PL::dur = RS_PL::sT[4]-RS_PL::sT[3];
  }
  if(rmin<=G.sr-G.mr){ //环食计算
   RS_PL::LX="环";
   RS_PL::sT[3] = RS_PL::lineT(G,v,u, G.sr-G.mr, 0); //食既
   RS_PL::secXY(RS_PL::sT[3],L,fa,high,g);
   RS_PL::sT[3] = RS_PL::lineT(g,v,u, g.sr-g.mr, 0); //食既再算1次

   RS_PL::sT[4] = RS_PL::lineT(G,v,u, G.sr-G.mr, 1); //生光
   RS_PL::secXY(RS_PL::sT[4],L,fa,high,g);
   RS_PL::sT[4] = RS_PL::lineT(g,v,u, g.sr-g.mr, 1); //生光再算1次
   RS_PL::dur = RS_PL::sT[4]-RS_PL::sT[3];
  }
  
  
  if(RS_PL::sT[1]<RS_PL::sun_s && RS_PL::sf2>0 ) RS_PL::sf=RS_PL::sf2,RS_PL::sflx="#"; //食甚在日出前，取日出食分
  if(RS_PL::sT[1]>RS_PL::sun_j && RS_PL::sf3>0 ) RS_PL::sf=RS_PL::sf3,RS_PL::sflx="*"; //食甚在日没后，取日没食分

  for(i=0;i<5;i++){
    if(RS_PL::sT[i]<RS_PL::sun_s || RS_PL::sT[i]>RS_PL::sun_j) RS_PL::sT[i]=0; //升降时间之外的日食算值无效，因为地球不是透明的
  }

  RS_PL::sun_s -= dt_T(jd);
  RS_PL::sun_j -= dt_T(jd);
}

 //以下涉及南北界计算
 mystl::array3 A={}, B={}; //本半影锥顶点坐标
 _ZB P={};//t1时刻的日月坐标,g为恒星时
 _ZB Q={};//t2时刻的日月坐标
 mystl::array10 V;//食界表
 mystl::string Vc = "", Vb = "";  //食中心类型,本影南北距离

void RS_PL::zb0(double jd)
{
  //基本参数计算
  double deltat = dt_T(jd); //TD-UT
  double E=hcjj(jd/36525.0);
  mystl::array2 zd=nutation2(jd/36525.0);
  
  RS_PL::P.g = pGST(jd-deltat, deltat) + zd[0]*cos(E+zd[1]); //真恒星时(不考虑非多项式部分)
  RS_PL::P.S=RS_GS::sun(jd);
  RS_PL::P.M=RS_GS::moon(jd);

  double t2=jd+60/86400.0;
  RS_PL::Q.g = pGST(t2-deltat,deltat) + zd[0]*cos(E+zd[1]);
  RS_PL::Q.S=RS_GS::sun(t2);
  RS_PL::Q.M=RS_GS::moon(t2);

  //转为直角坐标
  mystl::array3 z1={}, z2={};
  z1 = llr2xyz(RS_PL::P.S);
  z2 = llr2xyz(RS_PL::P.M);

  double k=959.63/cs_sMoon*cs_AU; //k为日月半径比
  //本影锥顶点坐标计算
  mystl::array3 F = {
   (z1[0]-z2[0])/(1-k)+z2[0],
   (z1[1]-z2[1])/(1-k)+z2[1],
   (z1[2]-z2[2])/(1-k)+z2[2]};
  RS_PL::A = xyz2llr(F);
  //半影锥顶点坐标计算
  mystl::array3 FF = {
   (z1[0]-z2[0])/(1+k)+z2[0],
   (z1[1]-z2[1])/(1+k)+z2[1],
   (z1[2]-z2[2])/(1+k)+z2[2]};
  RS_PL::B = xyz2llr(FF);
 }

void RS_PL::zbXY(_ZB &p,double L,double fa)
{
  mystl::array3 s = {p.S[0],p.S[1],p.S[2]};
  mystl::array3 m = {p.M[0],p.M[1],p.M[2]};
  s=parallax(s, p.g+L-p.S[0],fa, 0); //修正了视差的赤道坐标
  m=parallax(m, p.g+L-p.M[0],fa, 0); //修正了视差的赤道坐标
  //=======视半径========
  p.mr = cs_sMoon/m[2]/rad;
  p.sr = 959.63/s[2]/rad*cs_AU;
  //=======日月赤经纬差转为日面中心直角坐标(用于日食)==============
  p.x = rad2rrad(m[0]-s[0]) * cos((m[1]+s[1])/2.0);
  p.y = m[1]-s[1];
}
 
void RS_PL::p2p(double L,double fa,_GJW &re,bool fAB,int f)
{ //f取+-1
  _ZB &p=RS_PL::P, &q=RS_PL::Q;
  RS_PL::zbXY(RS_PL::P,L,fa);
  RS_PL::zbXY(RS_PL::Q,L,fa);

  double u=q.y-p.y, v=q.x-p.x, a=sqrt(u*u+v*v),r=959.63/p.S[2]/rad*cs_AU;
  double W=p.S[1]+f*r*v/a, J=p.S[0]-f*r*u/a/cos((W+p.S[1])/2.0), R=p.S[2];
  mystl::array3 AA = fAB ? RS_PL::A : RS_PL::B;
  
  COORDP pp = lineEar({J,W,R}, AA, p.g );
  re.J = pp.J;
  re.W = pp.W;
 }
void RS_PL::pp0(_GJW &re)
 { //食中心点计算
  _ZB p=RS_PL::P;
  COORDP pp = lineEar( p.M, p.S, p.g );
  re.J = pp.J;
  re.W = pp.W; //无解返回值是100
  
  if(re.W==100) { re.c = ""; return; }
  re.c="全";
  RS_PL::zbXY(p,re.J,re.W);
  if(p.sr>p.mr) re.c="环";
 }
void RS_PL::nbj(double jd)
 { //南北界计算
  RS_GS::init(jd,7);
  _GJW G={};
  mystl::array10 &V=RS_PL::V;
  int i;
  for(i=0;i<10;i++) V[i]=100; RS_PL::Vc="",RS_PL::Vb=""; //返回初始化,纬度值为100表示无解,经度100也是无解,但在以下程序中经度会被转为-PI到+PI

  RS_PL::zb0(jd);
  RS_PL::pp0(G); V[0]=G.J, V[1]=G.W, RS_PL::Vc=G.c; //食中心

  G.J=G.W=0; for(i=0;i<2;i++) RS_PL::p2p(G.J,G.W,G,1, 1); V[2]=G.J, V[3]=G.W; //本影北界,环食为南界(本影区之内,变差u,v基本不变,所以计算两次足够)
  G.J=G.W=0; for(i=0;i<2;i++) RS_PL::p2p(G.J,G.W,G,1,-1); V[4]=G.J, V[5]=G.W; //本影南界,环食为北界
  G.J=G.W=0; for(i=0;i<3;i++) RS_PL::p2p(G.J,G.W,G,0,-1); V[6]=G.J, V[7]=G.W; //半影北界
  G.J=G.W=0; for(i=0;i<3;i++) RS_PL::p2p(G.J,G.W,G,0, 1); V[8]=G.J, V[9]=G.W; //半影南界

  if(V[3]!=100&&V[5]!=100)
  { //粗算本影南北距离
    double x=(V[2]-V[4])*cos((V[3]+V[5])/2. ), y=V[3]-V[5];
    RS_PL::Vb = to_str(cs_rEarA*sqrt(x*x+y*y),0)+"千米";
  }
}