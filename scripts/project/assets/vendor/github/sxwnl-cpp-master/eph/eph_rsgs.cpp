#include "eph0.h"
#include "eph.h"
#include "eph_rsgs.h"
#include "../mylib/tool.h"
#include "../mylib/math_patch.h"

double RS_GS::Zjd  = 0;
mystl::vector<double> RS_GS::Zs;  //日月赤道坐标插值表
double RS_GS::Zdt  = 0.04;   //插值点之间的时间间距
double RS_GS::dT   = 0;      //deltatT
double RS_GS::tanf1= 0.0046; //半影锥角
double RS_GS::tanf2= 0.0045; //本影锥角
double RS_GS::srad = 0.0046; //太阳视半径
double RS_GS::bba  = 1;      //贝圆极赤比
double RS_GS::bhc  = 0;      //黄交线与赤交线的夹角简易作图用
double RS_GS::dyj  = 23500;  //地月距

void RS_GS::init(double jd,int n)
{ //创建插值表(根数表)
  if(suoN(jd)==suoN(RS_GS::Zjd) && RS_GS::Zs.size()==n*9) return;
  RS_GS::Zs.clear();
  RS_GS::Zjd  = jd = MS_aLon_t2( suoN(jd)*_pi*2 )*36525; //低精度的朔(误差10分钟)
  RS_GS::dT   = dt_T(jd); //deltat T

  mystl::array2 zd = nutation2(jd/36525.0); //章动
  double E = hcjj(jd/36525.0)+zd[1]; //黄赤交角
  double T;
  mystl::array3 S,M,B;
  mystl::vector<double> a(n*9);
  int i,k;
  
  for (i=0;i<n;i++)
  { //插值点范围不要超过360度(约1个月)
   T=( RS_GS::Zjd + (i-n/2.0+0.5)*RS_GS::Zdt ) / 36525.0;

   if(n==7) S = e_coord(T,-1,-1,-1), M = m_coord(T,-1,-1,-1);    //地球坐标及月球坐标,全精度
   if(n==3) S = e_coord(T,65,65,65), M = m_coord(T,-1,150,150);  //中精度
   if(n==2) S = e_coord(T,20,20,20), M = m_coord(T,30,30,30);    //低精度


   S[0] = S[0]+zd[0]+gxc_sunLon(T)+_pi;  S[1] = -S[1] + gxc_sunLat(T);  //补上太阳光行差及章动
   M[0] = M[0]+zd[0]+gxc_moonLon(T);         M[1] =  M[1] + gxc_moonLat(T); //补上月球光行差及章动
   S = llrConv( S, E );  M = llrConv( M, E ); S[2]*=cs_AU; //转为赤道坐标
   if(i && S[0]<a[0]) S[0]+=pi2;  //确保插值数据连续
   if(i && M[0]<a[3]) M[0]+=pi2;  //确保插值数据连续

   k = i*9;
   a[k+0]=S[0], a[k+1]=S[1], a[k+2]=S[2]; //存入插值表
   a[k+3]=M[0], a[k+4]=M[1], a[k+5]=M[2];


   //贝塞尔坐标的z轴坐标计算,得到a[k+6,7,8]交点赤经,贝赤交角,真恒星时
   S=llr2xyz(S), M=llr2xyz(M);
   B = xyz2llr({S[0]-M[0],S[1]-M[1],S[2]-M[2]});
   B[0] = _pi/2+B[0];
   B[1] = _pi/2-B[1];
   if(i && B[0]<a[6]) B[0]+=pi2; //确保插值数据连续

   a[k+6]=B[0], a[k+7]=B[1], a[k+8]=pGST(T*36525-RS_GS::dT, RS_GS::dT)+zd[0]*cos(E); //真恒星时
  }
  RS_GS::Zs=a;
  //一些辅助参数的计算
  double p=a.size()-9;
  RS_GS::dyj = (a[2]+a[p+2]-a[5]-a[p+5])/2.0/cs_rEar; //地月平均距离
  RS_GS::tanf1 = (cs_k0+cs_k )/RS_GS::dyj; //tanf1半影锥角
  RS_GS::tanf2 = (cs_k0-cs_k2)/RS_GS::dyj; //tanf2本影锥角
  RS_GS::srad = cs_k0/((a[2]+a[p+2])/2.0/cs_rEar);
  RS_GS::bba = sin( (a[1]+a[p+1])/2.0 );
  RS_GS::bba = cs_ba*(1+(1-cs_ba2)*RS_GS::bba*RS_GS::bba/2.0);
  RS_GS::bhc = -atan(tan(E)*sin( (a[6]+a[p+6])/2.0 )); //黄交线与赤交线的夹角

 }

mystl::array3 RS_GS::chazhi(double jd,int xt)
{//日月坐标快速计算(贝赛尔插值法),计算第p个根数开始的m个根数
  int p=xt*3,m=3; //计算第p个根数开始的m个根数
  int i, N=RS_GS::Zs.size()/9;
  mystl::vector<double> B=RS_GS::Zs;
  mystl::array3 z;
  int w = B.size()/N; //每节点个数
  double t = (jd-RS_GS::Zjd)/RS_GS::Zdt+N/2.0-0.5; //相对于第一点的时间距离

  if(N==2) 
  {
  for(i=0; i<m; i++,p++)
   z[i] = B[p] + (B[p+w]-B[p])*t; return z; 
  }
  int c=floor(t+0.5); if(c<=0) c=1; if(c>N-2) c=N-2; //确定c,并对超出范围的处理
  t-=c, p+=c*w; //c插值中心,t为插值因子,t再转为插值中心在数据中的位置
  for(i=0; i<m; i++,p++)
    z[i] = B[p] + ( B[p+w]-B[p-w] + (B[p+w]+B[p-w]-B[p]*2)*t ) * t/2;
  return z;
 }

mystl::array3 RS_GS::cd2bse(mystl::array3 z,mystl::array3 I)
{ //赤道转贝塞尔坐标
  mystl::array3 r={z[0]-I[0],z[1],z[2]};
  r = llrConv(r,-I[1]);
  return llr2xyz(r);
}
mystl::array3 RS_GS::bse2cd(mystl::array3 z,mystl::array3 I )
{ //贝塞尔转赤道坐标
  mystl::array3 r = xyz2llr(z);
  r = llrConv(r,I[1]);
  r[0] = rad2mrad(r[0]+I[0]);
  return r;
 }
mystl::array3 RS_GS::bse2db(mystl::array3 z,mystl::array3 I ,bool f)
{ //贝赛尔转地标(p点到原点连线与地球的交点,z为p点直角坐标),f=1时把地球看成椭球
  mystl::array3 r = xyz2llr(z);
  r = llrConv(r,I[1]);
  r[0] = rad2rrad(r[0]+I[0]-I[2]);
  if(f) r[1] = atan( tan(r[1])/cs_ba2 );
  return r;
 }
mystl::array3 RS_GS::bseXY2db(double x,double y,mystl::array3 I,bool f)
{ //贝赛尔转地标(过p点垂直于基面的线与地球的交点,p坐标为(x,y,任意z)),f=1时把地球看成椭球
  double b=f?cs_ba:1;
  COORDP F = lineEar2(x,y,2,  x,y,0,  b,1,I);//求中心对应的地标
  return {F.J,F.W};
 }

mystl::array3 RS_GS::bseM(double jd)
{  //月亮的贝塞尔坐标
   mystl::array3 a=RS_GS::cd2bse(RS_GS::chazhi(jd,1),RS_GS::chazhi(jd,2));
   a[0]/=cs_rEar, a[1]/=cs_rEar, a[2]/=cs_rEar;
   return a;
}

 //以下计算日食总体情况

_VXY RS_GS::Vxy(double x,double y,double s, double vx,double vy)
 { //地球上一点的速度，用贝塞尔坐标表达，s为贝赤交角
   _VXY r = {};
   double h = 1-x*x-y*y;
   if(h<0) h = 0;  //越界置0，使速度场连续，置零有助于迭代时单向收敛
   else    h = sqrt(h);
   r.vx = pi2*( sin(s)*h-cos(s)*y );
   r.vy = pi2*x*cos(s);
   r.Vx = vx - r.vx;
   r.Vy = vy - r.vy;
   r.V = sqrt(r.Vx*r.Vx+r.Vy*r.Vy);
   return r;
 }
_RSM RS_GS::rSM(double mR)
{ //rm,rs单位千米
  _RSM re = {};
  re.r1 = cs_k +RS_GS::tanf1*mR; //半影半径
  re.r2 = cs_k2-RS_GS::tanf2*mR; //本影半径
  re.ar2 = fabs(re.r2);
  re.sf = cs_k2/mR/cs_k0*(RS_GS::dyj+mR); //食分
  return re;
 }
mystl::array3 RS_GS::qrd(double jd,double dx,double dy,bool fs)
{ //求切入点
  double ba2 = RS_GS::bba*RS_GS::bba;
  mystl::array3 M = RS_GS::bseM(jd);
  double x=M[0], y=M[1];
  _RSM B = RS_GS::rSM(M[2]);
  double r = 0; if(fs==1) r = B.r1;
  double d = 1-(1/ba2-1)*y*y/(x*x+y*y)/2 + r;
  double t = (d*d-x*x-y*y)/(dx*x+dy*y)/2;
  x+=t*dx, y+=t*dy, jd+=t;

  double c=(1-ba2)*r*x*y/d/d/d;
  x += c*y;
  y -= c*x;
  mystl::array3 re=RS_GS::bse2db({x/d,y/d,0},RS_GS::bse(jd),1);
  //re[0] +=0.275/radd; //转为deltatT为66秒的历书经度
  re[2]=jd;
  return re;
}

_FEATURE RS_GS::feature(double jd)
 {//日食的基本特征
  jd = RS_GS::Zjd; //低精度的朔(误差10分钟)

  double tg=0.04;
  double jd1=jd-tg/2;
  _FEATURE re={};
  
  double ls;
  mystl::array3 a = RS_GS::bseM(jd-tg);
  mystl::array3 b = RS_GS::bseM(jd);
  mystl::array3 c = RS_GS::bseM(jd+tg);
  double vx = (c[0]-a[0])/tg/2;
  double vy = (c[1]-a[1])/tg/2;
  double vz = (c[2]-a[2])/tg/2;
  double ax = (c[0]+a[0]-2*b[0])/tg/tg;
  double ay = (c[1]+a[1]-2*b[1])/tg/tg;
  double v = sqrt(vx*vx+vy*vy), v2=v*v;

  //影轴在贝塞尔面扫线的特征参数
  re.jdSuo = jd;    //朔
  re.dT = RS_GS::dT;  //deltat T
  re.ds = RS_GS::bhc; //黄交线与赤交线的夹角
  re.vx = vx;       //影速x
  re.vy = vy;       //影速y
  re.ax = ax;
  re.ay = ay;
  re.v  = v;
  re.k  = vy/vx;    //斜率

  double t0 = -(b[0]*vx+b[1]*vy)/v2;
  re.jd = jd+t0;  //中点时间
  re.xc = b[0]+vx*t0;  //中点坐标x
  re.yc = b[1]+vy*t0;  //中点坐标y
  re.zc = b[2]+vz*t0-1.37*t0*t0;  //中点坐标z
  re.D  = (vx*b[1]-vy*b[0])/v;
  re.d  = fabs(re.D);  //直线到圆心的距离
  re.I  = RS_GS::bse(re.jd); //中心点的贝塞尔z轴的赤道坐标及恒星时，(J,W,g)

  //影轴交点判断
  COORDP F = lineEar2(re.xc,re.yc,2,  re.xc,re.yc,0,  cs_ba,1,re.I);//求中心对应的地标
  //四个关键点的影子半径计算
  _RSM Bc,Bp,B2,B3;
  double dt,t2,t3,t4,t5,t6;
  Bc=Bp=B2=B3 = RS_GS::rSM(re.zc); //中点处的影子半径
  if(F.W!=100)  Bp = RS_GS::rSM(re.zc - F.R2);
  if(re.d<1)
  {
    dt=sqrt(1-re.d*re.d)/v;  t2=t0-dt, t3=t0+dt; //中心始终参数
    B2 = RS_GS::rSM(t2*vz+b[2]-1.37*t2*t2);   //中心线始影半径
    B3 = RS_GS::rSM(t3*vz+b[2]-1.37*t3*t3);   //中心线终影半径
  }
  ls = 1;        dt=0; if(re.d<ls) dt=sqrt(ls*ls-re.d*re.d)/v; t2=t0-dt, t3=t0+dt; //偏食始终参数,t2,t3
  ls = 1+Bc.r1;  dt=0; if(re.d<ls) dt=sqrt(ls*ls-re.d*re.d)/v; t4=t0-dt, t5=t0+dt; //偏食始终参数,t4,t5
  t6 = -b[0]/vx; //视午参数l6
  
  if(re.d<1) {
   re.gk1 = RS_GS::qrd(t2+jd,vx,vy,0); //中心始
   re.gk2 = RS_GS::qrd(t3+jd,vx,vy,0); //中心终
  } else {
   re.gk1 = {0,0,0};
   re.gk2 = {0,0,0};
  }
  
  re.gk3 = RS_GS::qrd(t4+jd,vx,vy,1); //偏食始
  re.gk4 = RS_GS::qrd(t5+jd,vx,vy,1); //偏食终
  re.gk5 = RS_GS::bseXY2db(t6*vx+b[0],t6*vy+b[1], RS_GS::bse(t6+jd), 1);
  re.gk5[2]=t6+jd; //地方视午日食

  //日食类型、最大食地标、食分、太阳地平坐标
  mystl::array3 lls;
  if(F.W==100)
  { //无中心线
   //最大食地标及时分
   lls = RS_GS::bse2db({re.xc,re.yc,0},re.I, 0);
   re.zxJ=lls[0], re.zxW=lls[1]; //最大食地标
   re.sf = (Bc.r1-(re.d-0.9972))/(Bc.r1-Bc.r2); //0.9969是南北极区的平半径
   //类型判断
   if     (re.d>0.9972+Bc.r1)  { re.lx = "N"; } //无食,半影没有进入
   else if(re.d>0.9972+Bc.ar2) { re.lx = "P"; } //偏食,本影没有进入
   else                        { if(Bc.sf<1) re.lx = "A0"; else re.lx = "T0"; } //中心线未进入,本影部分进入(无中心，所以只是部分地入)
  }
  else
  { //有中心线
   //最大食地标及时分
   re.zxJ=F.J, re.zxW=F.W;  //最大食地标
   re.sf = Bp.sf; //食分
   //类型判断
   if(re.d>0.9966-Bp.ar2) { if(Bp.sf<1) re.lx = "A1"; else re.lx = "T1"; } //中心进入,但本影没有完全进入
   else
   { //本影全进入有中心日食
    if(Bp.sf>=1)
    {
      re.lx = "H";
      if(B2.sf>1) re.lx = "H2"; //全环食,全始
      if(B3.sf>1) re.lx = "H3"; //全环食,全终
      if(B2.sf>1 && B3.sf>1) re.lx="T"; //全食
    }
    else
    {
     re.lx = "A"; //环食
    }
   }
  }
  re.Sdp = CD2DP(RS_GS::sun(re.jd),re.zxJ,re.zxW,re.I[2]);  //太阳在中心点的地平坐标

  //食带宽度和时延
  if(F.W!=100)
  {
    re.dw = fabs(2*Bp.r2*cs_rEar) / sin(re.Sdp[1]); //食带宽度
    _VXY llls = RS_GS::Vxy(re.xc,re.yc,re.I[1], re.vx,re.vy); //求地表影速
    re.tt = 2*fabs(Bp.r2)/llls.V; //时延
  }
  else re.dw = re.tt =0;
  return re;
}

 //界线图
void RS_GS::push(mystl::array3 z,mystl::vector<double> &p)
{
   p.push_back(z[0]); //保存第一食甚线A或B根
   p.push_back(z[1]);
}

/*
*/

mystl::array4 RS_GS::nanbei(mystl::array3 M,double vx0,double vy0, double h,double r,mystl::array3 I)
 { //vx0,vy0为影足速度(也是整个影子速度),h=1计算北界,h=-1计算南界
   double x=M[0]-vy0/vx0*r*h, y=M[1]+h*r, z;
   double vx,vy,v,sinA,cosA;
   
   for(int i=0,js=0;i<3;i++)
   {
    z = 1 - x*x - y*y;
    if(z<0)
    {
     if(js) break;
     z=0;
     js++;
    } //z小于0则置0，如果两次小于0，可能不收敛造成的，故不再迭代了
    z = sqrt(z);
    x -= (x-M[0])*z/M[2];
    y -= (y-M[1])*z/M[2];
    vx = vx0 - pi2*( sin(I[1])*z-cos(I[1])*y );
    vy = vy0 - pi2*  cos(I[1])*x;
    v  = sqrt(vx*vx+vy*vy);
    sinA = h*vy/v, cosA = h*vx/v;
    x = M[0] - r*sinA, y = M[1] + r*cosA;
   }
   double X = M[0] - cs_k*sinA, Y = M[1] + cs_k*cosA;
   COORDP p = lineEar2(X,Y,M[2],  x,y,0,  cs_ba,1,I);
   return {p.J, p.W, x, y};
 }

bool RS_GS::mDian(mystl::array3 M,double vx0,double vy0,bool AB, double r,mystl::array3 I,mystl::vector<double> &A)
{ //日出日没食甚
   double R;
   NODE p;
   mystl::array3 a = M;
   _VXY c={};
   for (int i=0;i<2;i++)
   { //迭代求交点
     c = RS_GS::Vxy(a[0],a[1],I[1], vx0,vy0);
     p = lineOvl(M[0],M[1],c.Vy,-c.Vx,1,RS_GS::bba);
     if(!p.n) break;
     if(AB) a={p.A[0],p.A[1]}, R=p.R1;
     else   a={p.B[0],p.B[1]}, R=p.R2;
   }
   if(p.n && R<=r)
   { //有交点
     a=RS_GS::bse2db({a[0],a[1],0}, I,1); //转为地标
     A.push_back(a[0]); //保存第一食甚线A或B根
     A.push_back(a[1]);
     return 1;
   }
   return 0;
}


mystl::string RS_GS::jieX3(double jd)
 { //界线表
  double k, ls;
  mystl::array4 p;
  int i;
  _FEATURE re=RS_GS::feature(jd);  //求特征参数

  double t = floor(re.jd*1440)/1440.0 - 3/24.0;
  double N=360, dt=1/1440.0;
  mystl::string s="",s2;

  for(i=0;i<N;i++,t+=dt)
  {
   double vx = re.vx+re.ax*(t-re.jdSuo);
   double vy = re.vy+re.ay*(t-re.jdSuo);
   mystl::array3 M = RS_GS::bseM(t);    //此刻月亮贝塞尔坐标(其x和y正是影足)
   _RSM B = RS_GS::rSM(M[2]);  //本半影等
   double r = B.r1;            //半影半径
   mystl::array3 I = RS_GS::bse(t);     //贝塞尔坐标参数
   s2 = JD2str(t+J2000)+" ", k=0;
   //南北界
   p = RS_GS::nanbei(M,vx,vy, +1, r,     I); if(p[1]!=100) s2+=rad2str2(p[0])+"  "+rad2str2(p[1])+" |", k++; else s2+="-------------------|"; //半影北界
   p = RS_GS::nanbei(M,vx,vy, +1, B.r2,  I); if(p[1]!=100) s2+=rad2str2(p[0])+"  "+rad2str2(p[1])+" |", k++; else s2+="-------------------|"; //本影北界
   mystl::array3 pp = RS_GS::bseXY2db(M[0],M[1],I,1);
   p={pp[0],pp[1],pp[2]};
          if(p[1]!=100) s2+=rad2str2(p[0])+"  "+rad2str2(p[1])+" |", k++; else s2+="-------------------|"; //中心线
   p = RS_GS::nanbei(M,vx,vy, -1, B.r2,  I); if(p[1]!=100) s2+=rad2str2(p[0])+"  "+rad2str2(p[1])+" |", k++; else s2+="-------------------|"; //本影南界
   p = RS_GS::nanbei(M,vx,vy, -1, r,     I); if(p[1]!=100) s2+=rad2str2(p[0])+" "+rad2str2(p[1])+" ", k++; else s2+="------------------- "; //半影南界
   if(k) s+=s2+"\n";
  }
  return "\033[41;37;1m 时间(力学时) 半影北界限 本影北界线 中心线 本影南界线 半影南界线\033[0m(伪本影南北界应互换)\n\n\n\n"+s;
}


/*
1.暂时还没有作图工具
2.可能存在bug
void RS_GS::elmCpy(mystl::vector<double> &a,int n,mystl::vector<double> b,int m)
{ //数据元素复制
   if(!b.size()) return;
   if(n==-2) n=a.size();
 //  if(m==-2) m=b.size();
   if(n==-1) n=a.size()-2;
   if(m==-1) m=b.size()-2;
   
   if(n>=a.size()) a.push_back(0),a.push_back(0);
   a[n]=b[m], a[n+1]=b[m+1];
}

void RS_GS::mQie(mystl::array3 M,double vx0,double vy0,double h, double r,mystl::array3 I, mystl::vector<double> &A,_FLAG &FLAG)
{ //vx0,vy0为影足速度(也是整个影子速度),h=1计算北界,h=-1计算南界
   mystl::array4 p=RS_GS::nanbei(M,vx0,vy0,h,r,I);
   if(!FLAG.f2) FLAG.f2=0;   FLAG.f = p[1]==100?0:1; //记录有无解
   if(FLAG.f2!=FLAG.f)
   { //补线头线尾
     NODE g=lineOvl(p[2],p[3],vx0,vy0,1,RS_GS::bba);
     double dj;
     mystl::array3 F;
     if(g.n){
      if(FLAG.f) dj=g.R2, F={g.B[0],g.B[1]};
      else    dj=g.R1, F={g.A[0],g.A[1]};
      F[2]=0;
      mystl::array3 I2 = { I[0], I[1], I[2] - dj/sqrt(vx0*vx0+vy0*vy0)*6.28 };  //也可以不重算计算恒星时，直接用I[2]代替，但线头不会严格落在日出日没食甚线上
      RS_GS::push( RS_GS::bse2db(F,I2,1), A);//有解补线头
     }
   }
   FLAG.f2 = FLAG.f; //记录上次有无解

   if(p[1]!=100) RS_GS::push({p[0],p[1]},A);
}

_FEATURE RS_GS::jieX(double jd)
{ //日出日没的初亏食甚复圆线，南北界线等
  NODE p, ls;
  int i;
  _FEATURE re=RS_GS::feature(jd);  //求特征参数

  double T = 1.7*1.7-re.d*re.d; if(T<0) T=0; T=sqrt(T)/re.v+0.01;
  double t=re.jd-T, N=400, dt=2*T/N;
  int n1=0, n4=0; //n1切入时序

  _FLAG F1={},F2={},F3={},F4={},F5={},F6;
  //对日出日没食甚线预置一个点
  mystl::vector<double> &Ua=re.q1,&Ub=re.q2;
  
  RS_GS::push({0,0},re.q2); RS_GS::push({0,0},re.q3); RS_GS::push({0,0},re.q4);

  for(i=0;i<=N;i++,t+=dt)
  {
   double vx = re.vx+re.ax*(t-re.jdSuo);
   double vy = re.vy+re.ay*(t-re.jdSuo);
   mystl::array3 M = RS_GS::bseM(t);    //此刻月亮贝塞尔坐标(其x和y正是影足)
   _RSM B = RS_GS::rSM(M[2]);  //本半影等
   double r = B.r1;            //半影半径
   mystl::array3 I = RS_GS::bse(t);     //贝塞尔坐标参数

   p=cirOvl(1,RS_GS::bba, r,M[0],M[1]); //求椭圆与圆交点
   if(n1%2) {if(!p.n) n1++;} else {if(p.n) n1++;}
   if(p.n) { //有交点
    p.A[2]=p.B[2]=0;  p.A=RS_GS::bse2db(p.A,I,1);  p.B=RS_GS::bse2db(p.B,I,1); //转为地标
    if(n1==1){ RS_GS::push(p.A,re.p1); RS_GS::push(p.B,re.p2); }//保存第一亏圆界线
    if(n1==3){ RS_GS::push(p.A,re.p3); RS_GS::push(p.B,re.p4); }//保存第二亏圆界线
   }

   //日出日没食甚线
   if( !RS_GS::mDian(M,vx,vy,0,r,I, Ua) ) { if(Ua.size()>0) Ua=re.q3; };
   if( !RS_GS::mDian(M,vx,vy,1,r,I, Ub) ) { if(Ub.size()>2) Ub=re.q4; };
   if(t>re.jd){
     if(Ua.size()==0) Ua=re.q3;
     if(Ub.size()==2) Ub=re.q4;
   }

   //求中心线
   mystl::array3 lls;
   mystl::array3 pp = RS_GS::bseXY2db(M[0],M[1],I,1);
   if( pp[1]!=100&&n4==0 || pp[1]==100&&n4==1 )
   { //从无交点跳到有交点或反之
     ls=lineOvl(M[0],M[1],vx,vy,1,RS_GS::bba);
     double dj;
     if(n4==0) dj=ls.R2,lls=ls.B; //首坐标
     else      dj=ls.R1,lls=ls.A; //末坐标
     lls[2]=0;
     mystl::array3 I2 = {I[0], I[1], I[2] - dj/sqrt(vx*vx+vy*vy)*6.28 };  //也可以不重算计算恒星时，直接用I[2]代替，但线头不会严格落在日出日没食甚线上
     RS_GS::push( RS_GS::bse2db(lls,I2,1), re.L0 );
     n4++;
   }
   if(pp[1]!=100) RS_GS::push(pp,re.L0); //保存中心线

   //南北界
   RS_GS::mQie(M,vx,vy, +1, r,          I, re.L1,F1); //半影北界
   RS_GS::mQie(M,vx,vy, -1, r,          I, re.L2,F2); //半影南界
   RS_GS::mQie(M,vx,vy, +1, B.r2,       I, re.L3,F3); //本影北界
   RS_GS::mQie(M,vx,vy, -1, B.r2,       I, re.L4,F4); //本影南界
   RS_GS::mQie(M,vx,vy, +1, (r+B.r2)/2, I, re.L5,F5); //0.5半影北界
   RS_GS::mQie(M,vx,vy, -1, (r+B.r2)/2, I, re.L6,F6); //0.5半影南界
  }


  //日出日没食甚线的线头连接
  RS_GS::elmCpy(re.q3, 0, re.q1,-1); //连接q1和a3,单边界必须
  RS_GS::elmCpy(re.q4, 0, re.q2,-1); //连接q2和a4,单边界必须

  RS_GS::elmCpy(re.q1,-2, re.L1, 0); //半影北界线西端
  RS_GS::elmCpy(re.q2,-2, re.L2, 0); //半影南界线西端
  RS_GS::elmCpy(re.q3, 0, re.L1,-1); //半影北界线东端
  RS_GS::elmCpy(re.q4, 0, re.L2,-1); //半影南界线东端

  RS_GS::elmCpy(re.q2, 0, re.q1, 0);
  RS_GS::elmCpy(re.q3,-2, re.q4,-1);

  return re;
}
_JIEX2 RS_GS::jieX2(double jd)
{ //jd力学时
  _JIEX2 re={};
  mystl::vector<double> p1, p2, p3;

  if(fabs(jd-RS_GS::Zjd)>0.5) return re;
  
  int i;
  COORDP p;
  double s,x,y,X,Y;
  mystl::array3 S = RS_GS::sun(jd);   //此刻太阳赤道坐标
  mystl::array3 M = RS_GS::bseM(jd);  //此刻月亮
  _RSM B = RS_GS::rSM(M[2]); //本半影等
  mystl::array3 I = RS_GS::bse(jd);   //贝塞尔坐标参数
  double Z = M[2];           //月亮的坐标的z量

  double a0=M[0]*M[0]+M[1]*M[1];
  double a1=a0-B.r2*B.r2;
  double a2=a0-B.r1*B.r1;
  double N = 200;
  for(i=0;i<N;i++)
  {//第0和第N点是同一点，可形成一个环，但不必计算，因为第0点可能在界外而无效
    s=i/N*pi2;
    double cosS=cos(s), sinS=sin(s);
    X = M[0] + cs_k*cosS, Y = M[1] + cs_k*sinS;
    //本影
    x = M[0] + B.r2*cosS, y = M[1] + B.r2*sinS;
    p = lineEar2(X,Y,Z,  x,y,0,  cs_ba,1,I);
    if(p.W!=100) RS_GS::push( {p.J,p.W}, p1 );
    else { if(sqrt(x*x+y*y)>a1) RS_GS::push( RS_GS::bse2db({x,y,0},I,1), p1 ); }
    //半影
    x = M[0] + B.r1*cosS, y = M[1] + B.r1*sinS;
    p = lineEar2(X,Y,Z,  x,y,0,  cs_ba,1,I);
    if(p.W!=100) RS_GS::push( {p.J,p.W}, p2 );
    else { if(sqrt(x*x+y*y)>a2) RS_GS::push( RS_GS::bse2db({x,y,0},I,1), p2 ); }
    //晨昏圈
    mystl::array3 pp = llrConv({s,0,0},pi_2-S[1]);
    pp[0] = rad2rrad( pp[0]+S[0]+pi_2-I[2] );
    RS_GS::push(pp, p3);
  }
  p1[p1.size()]=p1[0], p1[p1.size()]=p1[1];
  p2[p2.size()]=p2[0], p2[p2.size()]=p2[1];
  p3[p3.size()]=p3[0], p3[p3.size()]=p3[1];

  re.p1=p1, re.p2=p2, re.p3=p3;
  return re;
}
*/