#include <cstring>
#include "eph.h"
#include "eph0.h"
#include "../mylib/tool.h"
#include "../mylib/math_patch.h"

//大距计算
double xingJJ(int xt, double t, int jing)
{								//行星的距角,jing为精度控
	mystl::array3 a, z;
	a = p_coord(0, t, 10, 10, 10);	//地球
	z = p_coord(xt, t, 10, 10, 10);	//行星
	z = h2g(z, a);				//转到地心
	//if (jing == 0) ;			//低精度
	if (jing == 1)
	{							//中精度
		a = p_coord(0, t, 60, 60, 60);	//地球
		z = p_coord(xt, t, 60, 60, 60);	//行星
		z = h2g(z, a);			//转到地心
	}
	if (jing >= 2)
	{							//高精度(补光行时)
		a = p_coord(0, t - a[2] * cs_Agx, -1, -1, -1);	//地球
		z = p_coord(xt, t - z[2] * cs_Agx, -1, -1, -1);	//行星
		z = h2g(z, a);			//转到地心
	}
	a[0] += _pi, a[1] = -a[1];		//太阳
	return j1_j2(z[0], z[1], a[0], a[1]);
}

mystl::array2 daJu(int xt, double t, bool dx)
{								//大距计算超底速算法, dx=1东大距,t儒略世纪TD
	double a = 0, b, c[5] = {};
	if (xt == 1)
	{
		a = 115.8774777586 / 36525.0;
		double arr[] = { 2, 0.2, 0.01, 46, 87 };
		memcpy(c, arr, sizeof(arr));
	}							//水星
	if (xt == 2)
	{
		a = 583.9213708245 / 36525.0;
		double arr[] = { 4, 0.2, 0.01, 382, 521 };
		memcpy(c, arr, sizeof(arr));
	}							//金星
	if (dx)
		b = c[3] / 36525.0;
	else
		b = c[4] / 36525.0;
	t = b + a * int2((t - b) / a + 0.5);	//大距平时间
	double dt, r1, r2, r3;
	int i;
	for (i = 0; i < 3; i++)
	{
		dt = c[i] / 36525.0;
		r1 = xingJJ(xt, t - dt, i);
		r2 = xingJJ(xt, t, i);
		r3 = xingJJ(xt, t + dt, i);
		t += (r1 - r3) / (r1 + r3 - 2 * r2) * dt / 2;
	}
	r2 += (r1 - r3) / (r1 + r3 - 2 * r2) * (r3 - r1) / 8;
	return {t, r2};
}

mystl::array3 xingLiu0(int xt, double t, int n, double gxs)
{								//行星的视坐标
	mystl::array3 a, z;
	mystl::array2 zd;
	double E = hcjj(t);
	a = p_coord(0, t - gxs, n, n, n);	//地球
	z = p_coord(xt, t - gxs, n, n, n);	//行星
	z = h2g(z, a);				//转到地心
	if (gxs)
	{							//如果计算了光行时，那么也计算章动
		zd = nutation2(t);		//章动计算
		z[0] += zd[0];
		E += zd[1];
	}
	z = llrConv(z, E);
	return z;
}

double xingLiu(int xt, double t, bool sn)
{								//留,sn=1顺留
	mystl::array3 y1, y2, y3;
	double g;
	int i,n;
	//先求冲(下合)
	double hh = cs_xxHH[xt - 1] / 36525.0;	//会合周期
	double v = pi2 / hh;
	if (xt > 2)
		v = -v;					//行星相对地球的黄经平速度
	for (i = 0; i < 6; i++)
		t -= rad2rrad(XL0_calc(xt, 0, t, 8) - XL0_calc(0, 0, t, 8)) / v;	//水星的平速度与真速度相差较多,所以多算几次

	double tt[] = { 5 / 36525.0, 1 / 36525.0, 0.5 / 36525.0, 2e-6, 2e-6 };
	double dt;
	double tc0[] = { 17.4, 28, 52, 82, 86, 88, 89, 90 };
	double tc = tc0[xt - 1] / 36525.0;

	if (sn)
	{
		if (xt > 2)
			t -= tc;
		else
			t += tc;
	}							//顺留
	else
	{
		if (xt > 2)
			t += tc;
		else
			t -= tc;
	}							//逆留
	for (i = 0; i < 4; i++)
	{
		dt = tt[i], n = 8, g = 0;
		if (i >= 3)
		{
			g = y2[2] * cs_Agx;
			n = -1;
		}
		y1 = xingLiu0(xt, t - dt, n, g);
		y2 = xingLiu0(xt, t, n, g);
		y3 = xingLiu0(xt, t + dt, n, g);
		t += (y1[0] - y3[0]) / (y1[0] + y3[0] - 2 * y2[0]) * dt / 2;
	}
	return t;
}

//合月计算
mystl::array4 xingMP(int xt, double t, int n, double E, mystl::array4 g)
{								//月亮行星视赤经差
	mystl::array3 a, p, m;
	a = p_coord(0, t - g[1], n, n, n);	//地球
	p = p_coord(xt, t - g[1], n, n, n);	//行星
	m = m_coord(t - g[0], n, n, n);	//月亮
	p = h2g(p, a);
	m[0] += g[2];
	p[0] += g[2];
	m = llrConv(m, E + g[3]);
	p = llrConv(p, E + g[3]);
	mystl::array4 re = { rad2rrad(m[0] - p[0]), m[1] - p[1], m[2] / cs_GS / 86400 / 36525.0, p[2] / cs_GS / 86400 / 36525.0 * cs_AU };	//赤经差及光行时
	return re;
}

mystl::array4 xingHY(int xt, double t)
{								//行星合月(视赤经),t儒略世纪TD
	double i, v, E;
	mystl::array4 d,d2,g = { 0, 0, 0, 0 };
	for (i = 0; i < 3; i++)
	{
		d = xingMP(xt, t, 8, 0.4091, g);
		t -= d[0] / 8192;
	}
	E = hcjj(t);
	mystl::array2 zd = nutation2(t);
	g = {d[2], d[3], zd[0], zd[1]};	//光行时,章动

	d = xingMP(xt, t, 8, E, g);
	d2 = xingMP(xt, t + 1e-6, 8, E, g);
	v = (d2[0] - d[0]) / 1e-6;	//速度

	d = xingMP(xt, t, 30, E, g);
	t -= d[0] / v;
	d = xingMP(xt, t, -1, E, g);
	t -= d[0] / v;
	mystl::array4 re = { t, d[1] };
	return re;
}

//合冲日计算(视黄经合冲)
mystl::array4 xingSP(int xt, double t, int n, double w0, double ts, double tp)
{								//行星太阳视黄经差与w0的差
	mystl::array3 a, p, s;
	a = p_coord(0, t - tp, n, n, n);	//地球
	p = p_coord(xt, t - tp, n, n, n);	//行星
	s = p_coord(0, t - ts, n, n, n);
	s[0] += _pi;
	s[1] = -s[1];					//太阳
	p = h2g(p, a);
	mystl::array4 re = { rad2rrad(p[0] - s[0] - w0), p[1] - s[1], s[2] * cs_Agx, p[2] * cs_Agx };	//赤经差及光行时
	return re;
}

mystl::array2 xingHR(int xt, double t, bool f)
{								//xt星体号,t儒略世纪TD,f=1求冲(或下合)否则求合(或下合)
	mystl::array4 a, b;
	double i, v, dt = 2e-5;
	double w0 = _pi, w1 = 0;	//合(或上合)时,日心黄经差为180，地心黄经差为0
	if (f)
	{							//求冲(或下合)
		w0 = 0;					//日心黄经差
		if (xt > 2)
			w1 = _pi;			//地心黄经差(冲)
	}
	v = pi2 / cs_xxHH[xt - 1] * 36525;
	if (xt > 2)
		v = -v;					//行星相对地球的黄经平速度
	for (i = 0; i < 6; i++)
		t -= rad2rrad(XL0_calc(xt, 0, t, 8) - XL0_calc(0, 0, t, 8) - w0) / v;	//水星的平速度与真速度相差较多,所以多算几次
	//严格计算
	a = xingSP(xt, t, 8, w1, 0, 0);
	b = xingSP(xt, t + dt, 8, w1, 0, 0);
	v = (b[0] - a[0]) / dt;
	a = xingSP(xt, t, 40, w1, a[2], a[3]);
	t -= a[0] / v;
	a = xingSP(xt, t, -1, w1, a[2], a[3]);
	t -= a[0] / v;
	mystl::array2 re = { t, a[1] };
	return re;
}


mystl::string xingX(int xt,double jd,double L,double fa)
{ //行星计算,jd力学时
 //基本参数计算

	double T=jd/36525;
	mystl::array2 zd = nutation2(T);
	double dL = zd[0], dE = zd[1]; //章动
	double E = hcjj(T) + dE; //真黄赤交角

    double gstPing = pGST2(jd); //平恒星时
    double gst= gstPing + dL*cos(E); //真恒星时(不考虑非多项式部分)

	mystl::array3 z,a,z2,a2;
	mystl::string s = "";
	double ra,rb,rc;
	int rfn=8;
	if(xt==10)
	{ //月亮
		rfn = 2;
  	  //求光行时并精确求出地月距
        a = e_coord(T,15,15,15); //地球
        z = m_coord(T,1,1,-1); ra = z[2]; //月亮
        T -= ra*cs_Agx/cs_AU; //光行时计算

        //求视坐标
        a2 = e_coord(T,15,15,15);//地球
        z  = m_coord(T,-1,-1,-1); rc = z[2]; //月亮
        //求光行距
        a2 = h2g(a,a2); a2[2] *= cs_AU;
        z2 = h2g(z,a2); rb = z2[2];

        //地心黄道及地心赤道
		z[0] = rad2mrad(z[0]+dL); //补章动
        s += "视黄经 " +rad2str(z[0],0) +" 视黄纬 " +rad2str(z[1],0) +" 地心距 " +to_str(ra,rfn)+"\n";

        z = llrConv(z,E); //转到赤道坐标
        s += "视赤经 " +rad2str(z[0],1) +" 视赤纬 " +rad2str(z[1],0) +" 光行距 " +to_str(rb,rfn)+"\n";
	}
	else if(xt<10&&xt>=0)
	{	
        a = p_coord(0, T,-1,-1,-1); //地球
        z = p_coord(xt,T,-1,-1,-1); //行星
        z[0] = rad2mrad(z[0]);
        s += "黄经一 " +rad2str(z[0],0) +" 黄纬一 " +rad2str(z[1],0) +" 向径一 " + to_str(z[2],rfn)+"\n";
  
       //地心黄道
        z = h2g(z,a); ra = z[2];  //ra地心距
        T -= ra*cs_Agx; //光行时

       //重算坐标
        a2 = p_coord(0, T,-1,-1,-1); //地球
        z2 = p_coord(xt,T,-1,-1,-1); //行星
      
        z = h2g(z2,a);  rb = z[2]; //rb光行距(在惯性系中看)
        z = h2g(z2,a2); rc = z[2]; //rc视距
        z[0] = rad2mrad(z[0]+dL); //补章动
        s += "视黄经 " +rad2str(z[0],0) +" 视黄纬 " +rad2str(z[1],0) +" 地心距 " +to_str(ra,rfn)+"\n";

        z = llrConv(z,E); //转到赤道坐标
        s += "视赤经 " +rad2str(z[0],1) +" 视赤纬 " +rad2str(z[1],0) +" 光行距 " +to_str(rb,rfn)+"\n";
	}
    double sj = rad2rrad(gst + L - z[0]); //得到天体时角
    z=parallax(z, sj,fa, 0); //视差修正
	s += "站赤经 " +rad2str(z[0],1) +" 站赤纬 " +rad2str(z[1],0) +" 视距离 " +to_str(rc,rfn)+"\n";
  
    z[0] += M_PI/2-gst-L;  //修正了视差的赤道坐标
    z = llrConv( z, M_PI/2-fa ); //转到时角坐标转到地平坐标
    z[0] = rad2mrad(-M_PI/2 - z[0]);

    if(z[1]>0)
        z[1] += MQC(z[1]); //大气折射修正
    s += "方位角 " +rad2str(z[0],0) +" 高度角 " +rad2str(z[1],0)+"\n";
	s += "恒星时 " +rad2str(rad2mrad(gstPing),1) +"(平) " +rad2str(rad2mrad(gst),1)+"(真)\n";

	return s;
}

//========日月食计算使用的一些函数=============
COORDP lineEll(double x1,double y1,double z1, double x2,double y2,double z2, double e,double r)
{ //求空间两点连线与地球的交点(靠近点x1的交点)
  double dx=x2-x1, dy=y2-y1, dz=z2-z1, e2=e*e, A,B,C,D,R,t;
  COORDP p={};
  A = dx*dx + dy*dy + dz*dz/e2;
  B = x1*dx + y1*dy + z1*dz/e2;
  C = x1*x1 + y1*y1 + z1*z1/e2 - r*r;
  p.D = B*B-A*C; if(p.D<0) return p; //判别式小于0无解
  D = sqrt(p.D); if(B<0) D = -D;     //只求靠近x1的交点
  t = (-B+D)/A;
  p.x=x1+dx*t, p.y=y1+dy*t, p.z=z1+dz*t;
  R = sqrt(dx*dx + dy*dy + dz*dz);
  p.R1 = R*fabs(t), p.R2 = R*fabs(t-1); //R1,R2分别为x1,x2到交点的距离
  return p;
}

COORDP lineEar2(double x1,double y1,double z1, double x2,double y2,double z2, double e,double r, mystl::array3 I)
{ //I是贝塞尔坐标参数
  double P=cos(I[1]), Q=sin(I[1]);
  double X1=x1, Y1=P*y1-Q*z1, Z1=Q*y1+P*z1;
  double X2=x2, Y2=P*y2-Q*z2, Z2=Q*y2+P*z2;
  COORDP p=lineEll(X1,Y1,Z1, X2,Y2,Z2, e,r);
  p.J=p.W=100;
  if(p.D<0) return p;
  p.J = rad2rrad(atan2(p.y,p.x)+I[0]-I[2]);
  p.W = atan( p.z/e/e/sqrt(p.x*p.x+p.y*p.y) );
  return p;
}

COORDP lineEar(mystl::array3 P,mystl::array3 Q,double gst)
{ //在分点坐标中求空间两点连线与地球的交点(靠近点P的交点),返回地标
  mystl::array3 p=llr2xyz(P), q=llr2xyz(Q);
  COORDP r=lineEll(p[0],p[1],p[2], q[0],q[1],q[2], cs_ba,cs_rEar);
  if(r.D<0) 
  {
   r.J=r.W=100;
   return r;
  } //反回100表示无解
  r.W = atan( r.z/cs_ba2/sqrt(r.x*r.x+r.y*r.y) );
  r.J = rad2rrad( atan2(r.y,r.x)-gst );
  return r;
}

NODE cirOvl(double R,double ba,double R2,double x0,double y0)
{ //椭圆与圆的交点,R椭圆长半径,R2圆半径,x0,y0圆的圆心
  NODE re = {};
  double d = sqrt(x0*x0+y0*y0);
  double sinB = y0/d, cosB = x0/d;
  double cosA = (R*R+d*d-R2*R2)/(2*d*R);
  if(fabs(cosA)>1){ re.n=0; return re; } //无解
  double sinA = sqrt(1-cosA*cosA);
 
  double g,ba2=ba*ba, C,S;
  int k;
  for(k=-1;k<2;k+=2){
   S = cosA*sinB + sinA*cosB*k;
   g= R - S*S*(1/ba2-1)/2;
   cosA = (g*g+d*d-R2*R2)/(2*d*g);
   if(fabs(cosA)>1){ re.n=0; return re; } //无解
   sinA = sqrt(1-cosA*cosA);
   C = cosA*cosB - sinA*sinB*k;
   S = cosA*sinB + sinA*cosB*k;
   if(k==1) re.A={g*C,g*S}; else re.B={g*C,g*S};
  }
  re.n=2;
  return re;
}

NODE lineOvl(double x1,double y1,double dx,double dy,double r,double ba)
{
  double A,B,C,D,L,t1,t2;
  NODE p={};
  double f=ba*ba;
  A = dx*dx + dy*dy/f;
  B = x1*dx + y1*dy/f;
  C = x1*x1 + y1*y1/f - r*r;
  D = B*B-A*C; if(D<0) { p.n=0; return p; }//判别式小于0无解
  if(!D) p.n=1; else p.n=2;
  D = sqrt(D);
  t1 = (-B+D)/A, t2 = (-B-D)/A;
  p.A = {x1+dx*t1,y1+dy*t1};
  p.B = {x1+dx*t2,y1+dy*t2};
  L = sqrt(dx*dx + dy*dy);
  p.R1 = L*fabs(t1); //x1到交点1的距离
  p.R2 = L*fabs(t2); //x1到交点2的距离
  return p;
}

_ECFAST ecFast(double jd)
{ //快速日食搜索,jd为朔时间(J2000起算的儒略日数,不必很精确)
 _ECFAST re={};
 double t,t2,t3,t4;
 double L,mB,mR,sR, vL,vB,vR;
 double W = floor((jd+8)/29.5306)*_pi*2; //合朔时的日月黄经差

 //合朔时间计算,2000前+-4000年误差1小时以内，+-2000年小于10分钟
 t  = ( W + 1.08472 )/7771.37714500204; //平朔时间
 re.jd = re.jdSuo = t*36525;

 t2=t*t,t3=t2*t,t4=t3*t;
 L = ( 93.2720993+483202.0175273*t-0.0034029*t2-t3/3526000+t4/863310000 )/180*_pi;
 re.ac=1, re.lx="N";
 if(fabs(sin(L))>0.4) return re; //一般大于21度已不可能

 t -= ( -0.0000331*t*t + 0.10976 *cos( 0.785 + 8328.6914*t) )/7771;
 t2=t*t;
 L = -1.084719 +7771.377145013*t -0.0000331*t2 +
 (22640 * cos(0.785+  8328.6914*t +0.000152*t2)
  +4586 * cos(0.19 +  7214.063*t  -0.000218*t2)
  +2370 * cos(2.54 + 15542.754*t  -0.000070*t2)
  + 769 * cos(3.1  + 16657.383*t)
  + 666 * cos(1.5  +   628.302*t)
  + 412 * cos(4.8  + 16866.93*t)
  + 212 * cos(4.1    -1114.63*t)
  + 205 * cos(0.2  +  6585.76*t)
  + 192 * cos(4.9  + 23871.45*t)
  + 165 * cos(2.6  + 14914.45*t)
  + 147 * cos(5.5    -7700.39*t)
  + 125 * cos(0.5  +  7771.38*t)
  + 109 * cos(3.9  +  8956.99*t)
  +  55 * cos(5.6    -1324.18*t)
  +  45 * cos(0.9  + 25195.62*t)
  +  40 * cos(3.8    -8538.24*t)
  +  38 * cos(4.3  + 22756.82*t)
  +  36 * cos(5.5  + 24986.07*t)
  -6893 * cos(4.669257+628.3076*t)
  -  72 * cos(4.6261 +1256.62*t)
  -  43 * cos(2.67823 +628.31*t)*t
  +  21) / rad;
 t += ( W - L ) / ( 7771.38
  - 914 * sin( 0.7848 + 8328.691425*t + 0.0001523*t2 )
  - 179 * sin( 2.543  +15542.7543*t )
  - 160 * sin( 0.1874 + 7214.0629*t ) );
 re.jd = re.jdSuo = jd = t*36525; //朔时刻

 //纬 52,15 (角秒)
 t2=t*t/10000,t3=t2*t/10000;
 mB=
  18461*cos(0.0571+  8433.46616*t   -0.640*t2    -1*t3)
 + 1010*cos(2.413 + 16762.1576 *t +  0.88 *t2 +  25*t3)
 + 1000*cos(5.440    -104.7747 *t +  2.16 *t2 +  26*t3)
 +  624*cos(0.915 +  7109.2881 *t +  0    *t2 +   7*t3)
 +  199*cos(1.82  + 15647.529  *t   -2.8  *t2   -19*t3)
 +  167*cos(4.84    -1219.403  *t   -1.5  *t2   -18*t3)
 +  117*cos(4.17  + 23976.220  *t   -1.3  *t2 +   6*t3)
 +   62*cos(4.8   + 25090.849  *t +  2    *t2 +  50*t3)
 +   33*cos(3.3   + 15437.980  *t +  2    *t2 +  32*t3)
 +   32*cos(1.5   +  8223.917  *t +  4    *t2 +  51*t3)
 +   30*cos(1.0   +  6480.986  *t +  0    *t2 +   7*t3)
 +   16*cos(2.5     -9548.095  *t   -3    *t2   -43*t3)
 +   15*cos(0.2   + 32304.912  *t +  0    *t2 +  31*t3)
 +   12*cos(4.0   +  7737.590  *t)
 +    9*cos(1.9   + 15019.227  *t)
 +    8*cos(5.4   +  8399.709  *t)
 +    8*cos(4.2   + 23347.918  *t)
 +    7*cos(4.9     -1847.705  *t)
 +    7*cos(3.8    -16133.856  *t)
 +    7*cos(2.7   + 14323.351  *t);
 mB/=rad;

 //距 106, 23 (千米)
 mR = 385001
 +20905*cos(5.4971+  8328.691425*t+  1.52 *t2 +  25*t3)
 + 3699*cos(4.900 +  7214.06287*t   -2.18 *t2   -19*t3)
 + 2956*cos(0.972 + 15542.75429*t   -0.66 *t2 +   6*t3)
 +  570*cos(1.57  + 16657.3828 *t +  3.0  *t2 +  50*t3)
 +  246*cos(5.69    -1114.6286 *t   -3.7  *t2   -44*t3)
 +  205*cos(1.02  + 14914.4523 *t   -1    *t2 +   6*t3)
 +  171*cos(3.33  + 23871.4457 *t +  1    *t2 +  31*t3)
 +  152*cos(4.94  +  6585.761  *t   -2    *t2   -19*t3)
 +  130*cos(0.74    -7700.389  *t   -2    *t2   -25*t3)
 +  109*cos(5.20  +  7771.377  *t)
 +  105*cos(2.31  +  8956.993  *t +  1    *t2 +  25*t3)
 +   80*cos(5.38    -8538.241  *t +  2.8  *t2 +  26*t3)
 +   49*cos(6.24  +   628.302  *t)
 +   35*cos(2.7   + 22756.817  *t   -3    *t2   -13*t3)
 +   31*cos(4.1   + 16171.056  *t   -1    *t2 +   6*t3)
 +   24*cos(1.7   +  7842.365  *t   -2    *t2   -19*t3)
 +   23*cos(3.9   + 24986.074  *t +  5    *t2 +  75*t3)
 +   22*cos(0.4   + 14428.126  *t   -4    *t2   -38*t3)
 +   17*cos(2.0   +  8399.679  *t);
 mR/=6378.1366;

 t=jd/365250, t2=t*t, t3=t2*t;
 //误0.0002AU
 sR = 10001399 //日地距离
 +167070*cos(3.098464 +  6283.07585*t)
 +  1396*cos(3.0552   + 12566.1517 *t)
 + 10302*cos(1.10749  +  6283.07585*t)*t
 +   172*cos(1.064    + 12566.152  *t)*t
 +   436*cos(5.785    +  6283.076  *t)*t2
 +    14*cos(4.27     +  6283.08   *t)*t3;
 sR*=1.49597870691/6378.1366*10;

 //经纬速度
 t=jd/36525;
 vL = 7771 //月日黄经差速度
     -914*sin(0.785 + 8328.6914*t)
     -179*sin(2.543 +15542.7543*t)
     -160*sin(0.187 + 7214.0629*t);
 vB =-755*sin(0.057 + 8433.4662*t) //月亮黄纬速度
     - 82*sin(2.413 +16762.1576*t);
 vR =-27299*sin(5.497 + 8328.691425*t)
     - 4184*sin(4.900 + 7214.06287*t)
     - 7204*sin(0.972 +15542.75429*t);
 vL/=36525, vB/=36525, vR/=36525; //每日速度


 double gm = mR*sin(mB)*vL/sqrt(vB*vB+vL*vL), smR=sR-mR; //gm伽马值,smR日月距
 double mk = 0.2725076, sk = 109.1222;
 double f1 = (sk+mk)/smR, r1 = mk+f1*mR; //tanf1半影锥角, r1半影半径
 double f2 = (sk-mk)/smR, r2 = mk-f2*mR; //tanf2本影锥角, r2本影半径
 double b = 0.9972, Agm = fabs(gm), Ar2 = fabs(r2);
 double fh2 = mR-mk/f2, h = Agm<1 ? sqrt(1-gm*gm) : 0; //fh2本影顶点的z坐标
 double ls1,ls2,ls3,ls4;

 if(fh2<h) re.lx = "T";
 else      re.lx = "A";

 ls1 = Agm-(b+r1 ); if(fabs(ls1)<0.016) re.ac=0; //无食分界
 ls2 = Agm-(b+Ar2); if(fabs(ls2)<0.016) re.ac=0; //偏食分界
 ls3 = Agm-(b    ); if(fabs(ls3)<0.016) re.ac=0; //无中心食分界
 ls4 = Agm-(b-Ar2); if(fabs(ls4)<0.016) re.ac=0; //有中心食分界(但本影未全部进入)

 if     (ls1>0) re.lx  = "N"; //无日食
 else if(ls2>0) re.lx  = "P"; //偏食
 else if(ls3>0) re.lx += "0"; //无中心
 else if(ls4>0) re.lx += "1"; //有中心(本影未全部进入)
 else{ //本影全进入
  if(fabs(fh2-h)<0.019) re.ac=0;
  if( fabs(fh2)<h ){
    double dr = vR*h/vL/mR;
    double H1 = mR-dr-mk/f2;  //入点影锥z坐标
    double H2 = mR+dr-mk/f2;  //出点影锥z坐标
    if(H1>0) re.lx="H3";      //环全全
    if(H2>0) re.lx="H2";      //全全环
    if(H1>0&&H2>0) re.lx="H"; //环全环
    if(fabs(H1)<0.019) re.ac=0;
    if(fabs(H2)<0.019) re.ac=0;
  }
 }
 return re;
}