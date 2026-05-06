#include <cstring>

#include "lunar_ssq.h"
#include "lunar_ob.h"
#include "../eph/eph0.h"
#include "../mylib/tool.h"
#include "../mylib/math_patch.h"

#define int2(v) ((int)floor(v))
/************************
  实气实朔计算器
  适用范围 -722年2月22日——1959年12月
  平气平朔计算使用古历参数进行计算
  定朔、定气计算使用开普勒椭圆轨道计算，同时考虑了光行差和力学时与UT1的时间差
  古代历算仅在晚期才使用开普勒方法计算，此前多采用一些修正表并插值得到，精度很低，与本程序中
的开普勒方法存在误差，造成朔日计算错误1千多个，这些错误使用一个修正表进行订正。同样，定气部分
也使用了相同的方法时行订正。
  平气朔表的算法(线性拟合)：
  气朔日期计算公式：D = k*n + b  , 式中n=0,1,2,3,...,N-1, N为该式适用的范围
  h表示k不变b允许的误差,如果b不变则k许可误差为h/N
  每行第1个参数为k,第2参数为b
  public中定义的成员可以直接使用
  
*************************/

//实朔实气计算器
double SSQ::suoKB[]={ //朔直线拟合参数
  1457698.231017,29.53067166, // -721-12-17 h=0.00032 古历·春秋
  1546082.512234,29.53085106, // -479-12-11 h=0.00053 古历·战国
  1640640.735300,29.53060000, // -221-10-31 h=0.01010 古历·秦汉
  1642472.151543,29.53085439, // -216-11-04 h=0.00040 古历·秦汉

  1683430.509300,29.53086148, // -104-12-25 h=0.00313 汉书·律历志(太初历)平气平朔
  1752148.041079,29.53085097, //   85-02-13 h=0.00049 后汉书·律历志(四分历)
  1807665.420323,29.53059851, //  237-02-12 h=0.00033 晋书·律历志(景初历)
  1883618.114100,29.53060000, //  445-01-24 h=0.00030 宋书·律历志(何承天元嘉历)
  1907360.704700,29.53060000, //  510-01-26 h=0.00030 宋书·律历志(祖冲之大明历)
  1936596.224900,29.53060000, //  590-02-10 h=0.01010 随书·律历志(开皇历)
  1939135.675300,29.53060000, //  597-01-24 h=0.00890 随书·律历志(大业历)
  1947168.00//  619-01-21
};

double SSQ::qiKB[]={ //气直线拟合参数
  1640650.479938,15.21842500, // -221-11-09 h=0.01709 古历·秦汉
  1642476.703182,15.21874996, // -216-11-09 h=0.01557 古历·秦汉

  1683430.515601,15.218750011, // -104-12-25 h=0.01560 汉书·律历志(太初历)平气平朔 回归年=365.25000
  1752157.640664,15.218749978, //   85-02-23 h=0.01559 后汉书·律历志(四分历) 回归年=365.25000
  1807675.003759,15.218620279, //  237-02-22 h=0.00010 晋书·律历志(景初历) 回归年=365.24689
  1883627.765182,15.218612292, //  445-02-03 h=0.00026 宋书·律历志(何承天元嘉历) 回归年=365.24670
  1907369.128100,15.218449176, //  510-02-03 h=0.00027 宋书·律历志(祖冲之大明历) 回归年=365.24278
  1936603.140413,15.218425000, //  590-02-17 h=0.00149 随书·律历志(开皇历) 回归年=365.24220
  1939145.524180,15.218466998, //  597-02-03 h=0.00121 随书·律历志(大业历) 回归年=365.24321
  1947180.798300,15.218524844, //  619-02-03 h=0.00052 新唐书·历志(戊寅元历)平气定朔 回归年=365.24460
  1964362.041824,15.218533526, //  666-02-17 h=0.00059 新唐书·历志(麟德历) 回归年=365.24480
  1987372.340971,15.218513908, //  729-02-16 h=0.00096 新唐书·历志(大衍历,至德历) 回归年=365.24433
  1999653.819126,15.218530782, //  762-10-03 h=0.00093 新唐书·历志(五纪历) 回归年=365.24474
  2007445.469786,15.218535181, //  784-02-01 h=0.00059 新唐书·历志(正元历,观象历) 回归年=365.24484
  2021324.917146,15.218526248, //  822-02-01 h=0.00022 新唐书·历志(宣明历) 回归年=365.24463
  2047257.232342,15.218519654, //  893-01-31 h=0.00015 新唐书·历志(崇玄历) 回归年=365.24447
  2070282.898213,15.218425000, //  956-02-16 h=0.00149 旧五代·历志(钦天历) 回归年=365.24220
  2073204.872850,15.218515221, //  964-02-16 h=0.00166 宋史·律历志(应天历) 回归年=365.24437
  2080144.500926,15.218530782, //  983-02-16 h=0.00093 宋史·律历志(乾元历) 回归年=365.24474
  2086703.688963,15.218523776, // 1001-01-31 h=0.00067 宋史·律历志(仪天历,崇天历) 回归年=365.24457
  2110033.182763,15.218425000, // 1064-12-15 h=0.00669 宋史·律历志(明天历) 回归年=365.24220
  2111190.300888,15.218425000, // 1068-02-15 h=0.00149 宋史·律历志(崇天历) 回归年=365.24220
  2113731.271005,15.218515671, // 1075-01-30 h=0.00038 李锐补修(奉元历) 回归年=365.24438
  2120670.840263,15.218425000, // 1094-01-30 h=0.00149 宋史·律历志 回归年=365.24220
  2123973.309063,15.218425000, // 1103-02-14 h=0.00669 李锐补修(占天历) 回归年=365.24220
  2125068.997336,15.218477932, // 1106-02-14 h=0.00056 宋史·律历志(纪元历) 回归年=365.24347
  2136026.312633,15.218472436, // 1136-02-14 h=0.00088 宋史·律历志(统元历,乾道历,淳熙历) 回归年=365.24334
  2156099.495538,15.218425000, // 1191-01-29 h=0.00149 宋史·律历志(会元历) 回归年=365.24220
  2159021.324663,15.218425000, // 1199-01-29 h=0.00149 宋史·律历志(统天历) 回归年=365.24220
  2162308.575254,15.218461742, // 1208-01-30 h=0.00146 宋史·律历志(开禧历) 回归年=365.24308
  2178485.706538,15.218425000, // 1252-05-15 h=0.04606 淳祐历 回归年=365.24220
  2178759.662849,15.218445786, // 1253-02-13 h=0.00231 会天历 回归年=365.24270
  2185334.020800,15.218425000, // 1271-02-13 h=0.00520 宋史·律历志(成天历) 回归年=365.24220
  2187525.481425,15.218425000, // 1277-02-12 h=0.00520 本天历 回归年=365.24220
  2188621.191481,15.218437494, // 1280-02-13 h=0.00015 元史·历志(郭守敬授时历) 回归年=365.24250
  2322147.76// 1645-09-21
};

char* SSQ::str_qi;
char* SSQ::str_so;

char *SSQ::jieya(int type)
{

	 mystl::string suoS = //  619-01-21开始16598个朔日修正表 d0=1947168
		"EqoFscDcrFpmEsF2DfFideFelFpFfFfFiaipqti1ksttikptikqckstekqttgkqttgkqteksttikptikq2fjstgjqttjkqttgkqt"
		"ekstfkptikq2tijstgjiFkirFsAeACoFsiDaDiADc1AFbBfgdfikijFifegF1FhaikgFag1E2btaieeibggiffdeigFfqDfaiBkF"
		"1kEaikhkigeidhhdiegcFfakF1ggkidbiaedksaFffckekidhhdhdikcikiakicjF1deedFhFccgicdekgiFbiaikcfi1kbFibef"
		"gEgFdcFkFeFkdcfkF1kfkcickEiFkDacFiEfbiaejcFfffkhkdgkaiei1ehigikhdFikfckF1dhhdikcfgjikhfjicjicgiehdik"
		"cikggcifgiejF1jkieFhegikggcikFegiegkfjebhigikggcikdgkaFkijcfkcikfkcifikiggkaeeigefkcdfcfkhkdgkegieid"
		"hijcFfakhfgeidieidiegikhfkfckfcjbdehdikggikgkfkicjicjF1dbidikFiggcifgiejkiegkigcdiegfggcikdbgfgefjF1"
		"kfegikggcikdgFkeeijcfkcikfkekcikdgkabhkFikaffcfkhkdgkegbiaekfkiakicjhfgqdq2fkiakgkfkhfkfcjiekgFebicg"
		"gbedF1jikejbbbiakgbgkacgiejkijjgigfiakggfggcibFifjefjF1kfekdgjcibFeFkijcfkfhkfkeaieigekgbhkfikidfcje"
		"aibgekgdkiffiffkiakF1jhbakgdki1dj1ikfkicjicjieeFkgdkicggkighdF1jfgkgfgbdkicggfggkidFkiekgijkeigfiski"
		"ggfaidheigF1jekijcikickiggkidhhdbgcfkFikikhkigeidieFikggikhkffaffijhidhhakgdkhkijF1kiakF1kfheakgdkif"
		"iggkigicjiejkieedikgdfcggkigieeiejfgkgkigbgikicggkiaideeijkefjeijikhkiggkiaidheigcikaikffikijgkiahi1"
		"hhdikgjfifaakekighie1hiaikggikhkffakicjhiahaikggikhkijF1kfejfeFhidikggiffiggkigicjiekgieeigikggiffig"
		"gkidheigkgfjkeigiegikifiggkidhedeijcfkFikikhkiggkidhh1ehigcikaffkhkiggkidhh1hhigikekfiFkFikcidhh1hit"
		"cikggikhkfkicjicghiediaikggikhkijbjfejfeFhaikggifikiggkigiejkikgkgieeigikggiffiggkigieeigekijcijikgg"
		"ifikiggkideedeijkefkfckikhkiggkidhh1ehijcikaffkhkiggkidhh1hhigikhkikFikfckcidhh1hiaikgjikhfjicjicgie"
		"hdikcikggifikigiejfejkieFhegikggifikiggfghigkfjeijkhigikggifikiggkigieeijcijcikfksikifikiggkidehdeij"
		"cfdckikhkiggkhghh1ehijikifffffkhsFngErD1pAfBoDd1BlEtFqA2AqoEpDqElAEsEeB2BmADlDkqBtC1FnEpDqnEmFsFsAFn"
		"llBbFmDsDiCtDmAB2BmtCgpEplCpAEiBiEoFqFtEqsDcCnFtADnFlEgdkEgmEtEsCtDmADqFtAFrAtEcCqAE1BoFqC1F1DrFtBmF"
		"tAC2ACnFaoCgADcADcCcFfoFtDlAFgmFqBq2bpEoAEmkqnEeCtAE1bAEqgDfFfCrgEcBrACfAAABqAAB1AAClEnFeCtCgAADqDoB"
		"mtAAACbFiAAADsEtBqAB2FsDqpFqEmFsCeDtFlCeDtoEpClEqAAFrAFoCgFmFsFqEnAEcCqFeCtFtEnAEeFtAAEkFnErAABbFkAD"
		"nAAeCtFeAfBoAEpFtAABtFqAApDcCGJ",

	qiS = // 1645-09-23开始7567个节气修正表
		"FrcFs22AFsckF2tsDtFqEtF1posFdFgiFseFtmelpsEfhkF2anmelpFlF1ikrotcnEqEq2FfqmcDsrFor22FgFrcgDscFs22FgEe"
		"FtE2sfFs22sCoEsaF2tsD1FpeE2eFsssEciFsFnmelpFcFhkF2tcnEqEpFgkrotcnEqrEtFermcDsrE222FgBmcmr22DaEfnaF22"
		"2sD1FpeForeF2tssEfiFpEoeFssD1iFstEqFppDgFstcnEqEpFg11FscnEqrAoAF2ClAEsDmDtCtBaDlAFbAEpAAAAAD2FgBiBqo"
		"BbnBaBoAAAAAAAEgDqAdBqAFrBaBoACdAAf1AACgAAAeBbCamDgEifAE2AABa1C1BgFdiAAACoCeE1ADiEifDaAEqAAFe1AcFbcA"
		"AAAAF1iFaAAACpACmFmAAAAAAAACrDaAAADG0",

	o = "0000000000",
	o2 = "00000000000000000000",
	o3 = "000000000000000000000000000000",
	o4 = "0000000000000000000000000000000000000000",
	o5 = "00000000000000000000000000000000000000000000000000",
	o6 = "000000000000000000000000000000000000000000000000000000000000";
	
	mystl::string str;
	if (type) {
		str=suoS;
	} else {
		str=qiS;
	}
	string_replace(str, "J", "00");
	string_replace(str, "I", "000");
	string_replace(str, "H", "0000");
	string_replace(str, "G", "00000");
	string_replace(str, "t", "02");
	string_replace(str, "s", "002");
	string_replace(str, "r", "0002");
	string_replace(str, "q", "00002");
	string_replace(str, "p", "000002");
	string_replace(str, "o", "0000002");
	string_replace(str, "n", "00000002");
	string_replace(str, "m", "000000002");
	string_replace(str, "l", "0000000002");
	string_replace(str, "k", "01");
	string_replace(str, "j", "0101");
	string_replace(str, "i", "001");
	string_replace(str, "h", "001001");
	string_replace(str, "g", "0001");
	string_replace(str, "f", "00001");
	string_replace(str, "e", "000001");
	string_replace(str, "d", "0000001");
	string_replace(str, "c", "00000001");
	string_replace(str, "b", "000000001");
	string_replace(str, "a", "0000000001");
	string_replace(str, "F", o);
	string_replace(str, "E", o2);
	string_replace(str, "D", o3);
	string_replace(str, "C", o4);
	string_replace(str, "B", o5);
	string_replace(str, "A", o6);
	char *result = (char *)malloc(strlen(str.c_str())+1);
	strncpy(result, str.c_str(), str.size() + 1);
	return result;
}

void SSQ::init()
{
	str_qi=jieya(0);
	str_so=jieya(1);	
}

double SSQ::so_low(double W)
{ //低精度定朔计算,在2000年至600，误差在2小时以内(仍比古代日历精准很多)
    double v = 7771.37714500204;
    double 
    t  = ( W + 1.08472 )/v, L;
    t -= ( -0.0000331*t*t
    + 0.10976 *cos( 0.785 + 8328.6914*t)
    + 0.02224 *cos( 0.187 + 7214.0629*t)
    - 0.03342 *cos( 4.669 +  628.3076*t ) )/v
    + (32*(t+1.8)*(t+1.8)-20)/86400/36525;
    return t*36525 + 8.0/24;
 }
 
 
double SSQ::qi_low(double W)
{ //最大误差小于30分钟，平均5分
    double t,L,v= 628.3319653318;
    t =  ( W - 4.895062166 )/v; //第一次估算,误差2天以内
    t -= ( 53*t*t + 334116*cos( 4.67+628.307585*t) + 2061*cos( 2.678+628.3076*t)*t )/v/10000000; //第二次估算,误差2小时以内

    L = 48950621.66 + 6283319653.318*t + 53*t*t //平黄经
      +334166 * cos( 4.669257+  628.307585*t) //地球椭圆轨道级数展开
      +3489 * cos( 4.6261  + 1256.61517*t ) //地球椭圆轨道级数展开
      +2060.6 * cos( 2.67823 +  628.307585*t ) * t  //一次泊松项
      - 994 - 834*sin(2.1824-33.75705*t); //光行差与章动修正
    t -= (L/10000000 -W )/628.332 + (32*(t+1.8)*(t+1.8)-20)/86400/36525;
    return t*36525 + 8.0/24;
 }
 
double SSQ::qi_high(double W)
{ //较高精度气
    double t = S_aLon_t2(W)*36525;
    t = t - dt_T(t)+8.0/24;
    double v = fmod(t+0.5,1 ) * 86400;
    if (v<1200 || v >86400-1200) t = S_aLon_t(W)*36525 - dt_T(t)+8.0/24;
    return  t;
 }
 
double SSQ::so_high(double W)
{ //较高精度朔
    double t = MS_aLon_t2(W)*36525;
    t = t - dt_T(t)+8.0/24;
    double v = fmod(t+0.5,1) * 86400;
    if (v<1800 || v >86400-1800) t = MS_aLon_t(W)*36525 - dt_T(t)+8.0/24;
    return  t;
}

int SSQ::calc(double jd, int qs)
{// jd应靠近所要取得的气朔日,qs=1定气
	jd += 2451545;
	int i,L=sizeof (suoKB)/sizeof (double);
	double D;
	char n;
	char *str_qs=str_so;
	double *B = suoKB, pc = 14;
	if (qs)
		B = qiKB, pc = 7,L=sizeof (qiKB)/sizeof (double),str_qs=str_qi;
	double f1 = B[0] - pc, f2 = B[L - 1] - pc, f3 = 2436935;

	if (jd < f1 || jd >= f3)
	{// 平气朔表中首个之前，使用现代天文算法。1960.1.1以后，使用现代天文算法 
	 // (这一部分调用了qi_high和so_high,所以需星历表支持)
	 
		if (qs == 1)
			return floor(qi_high(floor((jd + pc - 2451259) / 365.2422 * 24) * M_PI / 12) + 0.5);	// 2451259是1999.3.21,太阳视黄经为0,春分.定气计算
		else
			return floor(so_high(floor((jd + pc - 2451551) / 29.5306) * M_PI * 2) + 0.5);	// 2451551是2000.1.7的那个朔日,黄经差为0.定朔计算
	}

	if (jd >= f1 && jd < f2)
	{// 平气或平朔
		for (i = 0; i < L; i += 2)
			if (jd + pc < B[i + 2])
				break;
		D = B[i] + B[i + 1] * floor((jd + pc - B[i]) / B[i + 1]);
		D = floor(D + 0.5);
		if (D == 1683460)
			D++;// 如果使用太初历计算-103年1月24日的朔日,结果得到的是23日,这里修正为24日(实历)。修正后仍不影响-103的无中置闰。如果使用秦汉历，得到的是24日，本行D不会被执行。
		return D - 2451545;
	}

	if (jd >= f2 && jd < f3)
	{// 定气或定朔
		if (qs)
		{
			D = floor(qi_low(floor((jd + pc - 2451259) / 365.2422 * 24) * M_PI / 12) + 0.5);	// 2451259是1999.3.21,太阳视黄经为0,春分.定气计算
			n = str_qs[int2((jd - f2) / 365.2422 * 24)];	// 找定气修正值
		}
		else
		{
			D = floor(so_low(floor((jd + pc - 2451551) / 29.5306) * M_PI * 2) + 0.5);	// 2451551是2000.1.7的那个朔日,黄经差为0.定朔计算
			n = str_qs[int2((jd - f2) / 29.5306)];	// 找定朔修正值
		}
		if (n == '1')
			return D + 1;
		if (n == '2')
			return D - 1;
		return D;
	}
	return 0;
}

int SSQ::leap;  //闰月位置
mystl::static_array<mystl::string,14> SSQ::ym;//各月名称索引
int SSQ::ZQ[25];//中气表
int SSQ::HS[15];//合朔表
int SSQ::dx[14];//各月大小
int SSQ::pe[2]; //补算二气

void SSQ::calcY(double jd)
{//农历排月序计算,可定出农历,有效范围：两个冬至之间(冬至一 <= d < 冬至二)

    int *A=ZQ, *B=HS;  //中气表,日月合朔表(整日)
    int i;
    double W, w;

    //该年的气
    W = int2((jd-355+183)/365.2422)*365.2422+355;  //355是2000.12冬至,得到较靠近jd的冬至估计值
    if (calc(W,1)>jd)  W-=365.2422;
    for (i=0;i<25;i++)
    {
        A[i]=calc(W+15.2184*i,1); //25个节气时刻(北京时间),从冬至开始到下一个冬至以后
    }
    pe[0]=calc(W-15.2,1),pe[1]=calc(W-30.4,1); //补算二气,确保一年中所有月份的“气”全部被计算在内

    //今年"首朔"的日月黄经差w
    w = calc(A[0],0); //求较靠近冬至的朔日
    if (w>A[0]) w -= 29.53;

    //该年所有朔,包含14个月的始末
    for (i=0;i<15;i++)
    {
        B[i]=calc(w+29.5306*i,0);
    }

    //月大小
    leap = 0;
    int ym[14];
    for (i=0;i<14;i++)
    {
        dx[i] = HS[i+1]-HS[i]; //月大小
        ym[i]=i;  //月序初始化
    }

    //-721年至-104年的后九月及月建问题,与朔有关，与气无关
    int YY = int2( (ZQ[0]+10 +180)/365.2422) + 2000; //确定年份
    if ( YY>=-721 && YY <=-104 )
    {
        int ns[9] = {};
        int yy;
        const char *str[]={"十三","后九"};
        for (i=0;i<3;i++)
        {
            yy = YY+i-1;
            //颁行历年首, 闰月名称, 月建
            if (yy>=-721) ns[i]=calc(1457698-J2000+int2(0.342+(yy+721)*12.368422)*29.5306,0), ns[i+3]=0, ns[i+6]=2;  //春秋历,ly为-722.12.17
            if (yy>=-479) ns[i]=calc(1546083-J2000+int2(0.500+(yy+479)*12.368422)*29.5306,0), ns[i+3]=0, ns[i+6]=2;  //战国历,ly为-480.12.11
            if (yy>=-220) ns[i]=calc(1640641-J2000+int2(0.866+(yy+220)*12.369000)*29.5306,0), ns[i+3]=1, ns[i+6]=11; //秦汉历,ly为-221.10.31
        }
        int nn,f1;
        for (i=0;i<14;i++)
        {
            for (nn=2;nn>=0;nn--) if (HS[i]>=ns[nn]) break;
            f1 = int2( (HS[i]-ns[nn]+15)/29.5306 ); //该月积数
            if (f1 < 12) SSQ::ym[i] = str_ymc[(f1+ns[nn+6])%12]; else SSQ::ym[i] = str[ns[nn+3]];
        }
        return;
    }

    //无中气置闰法确定闰月,(气朔结合法,数据源需有冬至开始的的气和朔)
    if ( B[13] <= A[24] )
    { //第13月的月末没有超过冬至(不含冬至),说明今年含有13个月
        for (i=1; B[i+1]>A[2*i] && i<13; i++); //在13个月中找第1个没有中气的月份
        leap = i;
        for (;i<14;i++) ym[i]--;
    }

    //名称转换(月建别名)
    for (i=0;i<14;i++)
    {
        double Dm = HS[i]+J2000;
        int v2=ym[i]; //Dm初一的儒略日,v2为月建序号
        mystl::string mc = str_ymc[v2%12]; //月建对应的默认月名称：建子十一,建丑十二,建寅为正……
        if      ( Dm>=1724360 && Dm<=1729794 ) mc = str_ymc[(v2+1)%12]; //  8.01.15至 23.12.02 建子为十二,其它顺推
        else if ( Dm>=1807724 && Dm<=1808699 ) mc = str_ymc[(v2+1)%12]; //237.04.12至239.12.13 建子为十二,其它顺推
        else if ( Dm>=1999349 && Dm<=1999467 ) mc = str_ymc[(v2+2)%12]; //761.12.02至762.03.30 建子为正月,其它顺推
        else if ( Dm>=1973067 && Dm<=1977052 )
        {
        	if (v2%12==0) mc="正";
        	if (v2==2)    mc="一";
        } //689.12.18至700.11.15 建子为正月,建寅为一月,其它不变
        if (Dm==1729794||Dm==1808699) mc="拾贰"; //239.12.13及23.12.02均为十二月,为避免两个连续十二月，此处改名
        SSQ::ym[i]=mc;
    }

}