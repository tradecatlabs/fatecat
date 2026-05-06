<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>合婚系统</title>
<style type="text/css">
<!--
body,td,th {
	font-size: 12px;
}
.xx {
	font-size: 12px;
	line-height: 18px;
	color: #0000FF;
}
.hs {
	font-size: 12px;
	color: #FF0000;
}
.style1 {
	font-size: 18px;
	color: #FF00FF;
	font-weight: bold;
}
-->
</style>
</head>

<body>
<table width="100%"  border="1" cellpadding="0" cellspacing="0" bordercolor="#CCCCCC">
  <tr bgcolor="#FFFFFF">
    <td width="50%" bgcolor="#FFF5EC"><?php
include("algorithm.php");

function pdyl($x,$y) {
         switch ($x) {
		        #子
		        case 31:
                     switch ($y) {
					 case 31:#子
					 $s = 0;
					 break;
					 case 32:#丑
					 $s = 1;
					 break;
					 case 33:#寅
					 $s = 1;
					 break;
					 case 34:#卯
					 $s = 1;
					 break;
					 case 35:#辰
					 $s = 1;
					 break;
					 case 36:#巳
					 $s = 1;
					 break;
					 case 37:#午
					 $s = 1;
					 break;
					 case 38:#未
					 $s = 1;
					 break;
					 case 39:#申
					 $s = 0;
					 break;
					 case 40:#酉
					 $s = 0;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 0;
					 break;
					 }
                break;

				case 32:
                     switch ($y) {
					 case 31:#子
					 $s = 0;
					 break;
					 case 32:#丑
					 $s = 0;
					 break;
					 case 33:#寅
					 $s = 1;
					 break;
					 case 34:#卯
					 $s = 1;
					 break;
					 case 35:#辰
					 $s = 0;
					 break;
					 case 36:#巳
					 $s = 0;
					 break;
					 case 37:#午
					 $s = 0;
					 break;
					 case 38:#未
					 $s = 1;
					 break;
					 case 39:#申
					 $s = 1;
					 break;
					 case 40:#酉
					 $s = 1;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 1;
					 break;
					 }
                break;
	
				case 33:
                     switch ($y) {
					 case 31:#子
					 $s = 0;
					 break;
					 case 32:#丑
					 $s = 1;
					 break;
					 case 33:#寅
					 $s = 0;
					 break;
					 case 34:#卯
					 $s = 0;
					 break;
					 case 35:#辰
					 $s = 1;
					 break;
					 case 36:#巳
					 $s = 1;
					 break;
					 case 37:#午
					 $s = 1;
					 break;
					 case 38:#未
					 $s = 1;
					 break;
					 case 39:#申
					 $s = 1;
					 break;
					 case 40:#酉
					 $s = 1;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 0;
					 break;
					 }
                break;

				case 34:
                     switch ($y) {
					 case 31:#子
					 $s = 0;
					 break;
					 case 32:#丑
					 $s = 1;
					 break;
					 case 33:#寅
					 $s = 0;
					 break;
					 case 34:#卯
					 $s = 0;
					 break;
					 case 35:#辰
					 $s = 1;
					 break;
					 case 36:#巳
					 $s = 1;
					 break;
					 case 37:#午
					 $s = 1;
					 break;
					 case 38:#未
					 $s = 1;
					 break;
					 case 39:#申
					 $s = 1;
					 break;
					 case 40:#酉
					 $s = 1;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 0;
					 break;
					 }
                break;
				#辰
				case 35:
                     switch ($y) {
					 case 31:#子
					 $s = 1;
					 break;
					 case 32:#丑
					 $s = 0;
					 break;
					 case 33:#寅
					 $s = 1;
					 break;
					 case 34:#卯
					 $s = 1;
					 break;
					 case 35:#辰
					 $s = 0;
					 break;
					 case 36:#巳
					 $s = 0;
					 break;
					 case 37:#午
					 $s = 0;
					 break;
					 case 38:#未
					 $s = 0;
					 break;
					 case 39:#申
					 $s = 1;
					 break;
					 case 40:#酉
					 $s = 1;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 1;
					 break;
					 }
                break;
				#巳
				case 36:
                     switch ($y) {
					 case 31:#子
					 $s = 1;
					 break;
					 case 32:#丑
					 $s = 1;
					 break;
					 case 33:#寅
					 $s = 0;
					 break;
					 case 34:#卯
					 $s = 0;
					 break;
					 case 35:#辰
					 $s = 1;
					 break;
					 case 36:#巳
					 $s = 0;
					 break;
					 case 37:#午
					 $s = 0;
					 break;
					 case 38:#未
					 $s = 1;
					 break;
					 case 39:#申
					 $s = 1;
					 break;
					 case 40:#酉
					 $s = 1;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 1;
					 break;
					 }
                break;
				#午
				case 37:
                     switch ($y) {
					 case 31:#子
					 $s = 1;
					 break;
					 case 32:#丑
					 $s = 1;
					 break;
					 case 33:#寅
					 $s = 0;
					 break;
					 case 34:#卯
					 $s = 0;
					 break;
					 case 35:#辰
					 $s = 1;
					 break;
					 case 36:#巳
					 $s = 0;
					 break;
					 case 37:#午
					 $s = 0;
					 break;
					 case 38:#未
					 $s = 1;
					 break;
					 case 39:#申
					 $s = 1;
					 break;
					 case 40:#酉
					 $s = 1;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 1;
					 break;
					 }
                break;
				#未
				case 38:
                     switch ($y) {
					 case 31:#子
					 $s = 1;
					 break;
					 case 32:#丑
					 $s = 1;
					 break;
					 case 33:#寅
					 $s = 1;
					 break;
					 case 34:#卯
					 $s = 1;
					 break;
					 case 35:#辰
					 $s = 0;
					 break;
					 case 36:#巳
					 $s = 0;
					 break;
					 case 37:#午
					 $s = 0;
					 break;
					 case 38:#未
					 $s = 0;
					 break;
					 case 39:#申
					 $s = 1;
					 break;
					 case 40:#酉
					 $s = 1;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 1;
					 break;
					 }
                break;
				#申
				case 39:
                     switch ($y) {
					 case 31:#子
					 $s = 1;
					 break;
					 case 32:#丑
					 $s = 0;
					 break;
					 case 33:#寅
					 $s = 1;
					 break;
					 case 34:#卯
					 $s = 1;
					 break;
					 case 35:#辰
					 $s = 1;
					 break;
					 case 36:#巳
					 $s = 1;
					 break;
					 case 37:#午
					 $s = 1;
					 break;
					 case 38:#未
					 $s = 1;
					 break;
					 case 39:#申
					 $s = 0;
					 break;
					 case 40:#酉
					 $s = 0;
					 break;
					 case 41:#戌
					 $s = 0;
					 break;
					 case 30:#亥
					 $s = 1;
					 break;
					 }
                break;
				#酉
				case 40:
                     switch ($y) {
					 case 31:#子
					 $s = 1;
					 break;
					 case 32:#丑
					 $s = 0;
					 break;
					 case 33:#寅
					 $s = 1;
					 break;
					 case 34:#卯
					 $s = 1;
					 break;
					 case 35:#辰
					 $s = 0;
					 break;
					 case 36:#巳
					 $s = 1;
					 break;
					 case 37:#午
					 $s = 1;
					 break;
					 case 38:#未
					 $s = 0;
					 break;
					 case 39:#申
					 $s = 0;
					 break;
					 case 40:#酉
					 $s = 0;
					 break;
					 case 41:#戌
					 $s = 0;
					 break;
					 case 30:#亥
					 $s = 1;
					 break;
					 }
                break;
				#戌
				case 41:
                     switch ($y) {
					 case 31:#子
					 $s = 1;
					 break;
					 case 32:#丑
					 $s = 1;
					 break;
					 case 33:#寅
					 $s = 1;
					 break;
					 case 34:#卯
					 $s = 1;
					 break;
					 case 35:#辰
					 $s = 1;
					 break;
					 case 36:#巳
					 $s = 0;
					 break;
					 case 37:#午
					 $s = 0;
					 break;
					 case 38:#未
					 $s = 0;
					 break;
					 case 39:#申
					 $s = 1;
					 break;
					 case 40:#酉
					 $s = 1;
					 break;
					 case 41:#戌
					 $s = 0;
					 break;
					 case 30:#亥
					 $s = 1;
					 break;
					 }
                break;
				#亥
				case 30:
                     switch ($y) {
					 case 31:#子
					 $s = 0;
					 break;
					 case 32:#丑
					 $s = 1;
					 break;
					 case 33:#寅
					 $s = 1;
					 break;
					 case 34:#卯
					 $s = 1;
					 break;
					 case 35:#辰
					 $s = 1;
					 break;
					 case 36:#巳
					 $s = 1;
					 break;
					 case 37:#午
					 $s = 1;
					 break;
					 case 38:#未
					 $s = 1;
					 break;
					 case 39:#申
					 $s = 0;
					 break;
					 case 40:#酉
					 $s = 0;
					 break;
					 case 41:#戌
					 $s = 1;
					 break;
					 case 30:#亥
					 $s = 0;
					 break;
					 }
                break;
                      }
        return $s;          }
		

/*
dim $md
'确定节气 yz 月支  起运基数 $qyjs
*/
$b[31] = "鼠 ";
$b[32] = "牛 ";
$b[33] = "虎 ";
$b[34] = "兔 ";
$b[35] = "龙 ";
$b[36] = "蛇 ";
$b[37] = "马 ";
$b[38] = "羊 ";
$b[39] = "猴 ";
$b[40] = "鸡 ";
$b[41] = "狗 ";
$b[30] = "猪 ";

$c[31] = "水 ";
$c[32] = "水 ";
$c[33] = "木 ";
$c[34] = "木 ";
$c[35] = "木 ";
$c[36] = "火 ";
$c[37] = "火 ";
$c[38] = "火 ";
$c[39] = "金 ";
$c[40] = "金 ";
$c[41] = "金 ";
$c[30] = "水 ";

#天干
$d[21] = "a";
$d[22] = "a";
$d[23] = "b";
$d[24] = "b";
$d[25] = "c";
$d[26] = "c";
$d[27] = "d";
$d[28] = "d";
$d[29] = "e";
$d[20] = "e";

$da[21] = "1";
$da[22] = "0";
$da[23] = "1";
$da[24] = "0";
$da[25] = "1";
$da[26] = "0";
$da[27] = "1";
$da[28] = "0";
$da[29] = "1";
$da[20] = "0";

#天干合化
$e[21] = "土";
$e[22] = "金";
$e[23] = "水";
$e[24] = "木";
$e[25] = "火";
$e[26] = "土";
$e[27] = "金";
$e[28] = "水";
$e[29] = "木";
$e[20] = "火";

$a[21] = "甲";
$a[22] = "乙";
$a[23] = "丙";
$a[24] = "丁";
$a[25] = "戊";
$a[26] = "己";
$a[27] = "庚";
$a[28] = "辛";
$a[29] = "壬";
$a[20] = "癸";

$a[31] = "子 ";
$a[32] = "丑 ";
$a[33] = "寅 ";
$a[34] = "卯 ";
$a[35] = "辰 ";
$a[36] = "巳 ";
$a[37] = "午 ";
$a[38] = "未 ";
$a[39] = "申 ";
$a[40] = "酉 ";
$a[41] = "戌 ";
$a[30] = "亥 ";

#十神名称

$a[1] = "比肩";
$a[2] = "劫财";
$a[3] = "食神";
$a[4] = "伤官";
$a[5] = "偏财";
$a[6] = "正财";
$a[7] = "七杀";
$a[8] = "正官";
$a[9] = "偏印";
$a[0] = "正印";

####男命
$name=$_POST["name"];; #姓名
$year=$_POST["year"];; #年干
$month =$_POST["month"];; #月份
$day =$_POST["day"];; #日
$t_ime=$_POST["t_ime"];; #时
####女命
$name_a=$_POST["name_a"];; #姓名
$year_a=$_POST["year_a"];; #年干
$month_a =$_POST["month_a"];; #月份
$day_a =$_POST["day_a"];; #日
$t_ime_a=$_POST["t_ime_a"];; #时
###########################################
#1先算男命
$yearday='';
#确定节气 yz 月支  起运基数 qyjs
$md=$month * 100 + $day;
if($md>=204 and $md<= 305) {
$mz = 3;
$qyjs = (($month - 2) * 30 + $day - 4)/3;
    }
if($md>=306 and $md<=404) {
$mz = 4;
$qyjs = (($month - 3) * 30 + $day - 6)/3;
}

if($md>=405 and $md<= 504) {
$mz = 5;
$qyjs = (($month - 4) * 30 + $day - 5)/3;
}

if($md>=505 and $md<=  605) {
$mz = 6;
$qyjs = (($month - 5) * 30 + $day - 5)/3;
}

if($md>=606 and $md<= 706) {
$mz = 7;
$qyjs = (($month - 6) * 30 + $day - 6)/3;
}

if($md>=707 and $md<= 807) {
$mz = 8;
$qyjs = (($month - 7) * 30 + $day - 7)/3;
}

if($md>=808 and $md<=907) {
$mz = 9;
$qyjs = (($month - 8) * 30 + $day - 8)/3;
}

if($md>=908 and $md<=1007) {
$mz = 10;
$qyjs = (($month - 9) * 30 + $day - 8)/3;
}

if($md>=1008 and $md<= 1106) {
$mz = 11;
$qyjs = (($month - 10) * 30 + $day - 8)/3;
}

if($md>=1107 and $md<=  1207) {
$mz = 0;
$qyjs = (($month - 11) * 30 + $day - 7)/3;
}

if($md>=1208 and $md<=  1231) {
$mz = 1;
$qyjs = ($day - 8)/3;
}

if($md>=101 and $md<= 105) {
$mz = 1;
$qyjs = (30 + $day - 4)/3;
}

if($md>=106 and $md<=  203) {
$mz = 2;
$qyjs = (($month - 1) * 30 + $day - 6)/3;
}


###############
#确定年干和年支 yg 年干 yz 年支
if($md>=204 and $md<=1231){
$yg = ($year-3)%10;
$yz = ($year-3)%12;
}
if($md>=101 and $md<=203 ){
$yg = ($year-4)%10;
$yz = ($year-4)%12;
}

If ($mz > 2 And $mz <= 11) {

$mg = ($yg * 2 + $mz + 8)%10;
} else {
$mg = ($yg * 2 + $mz)%10;
}


$yearlast = ($year  - 1) * 5 + ($year  - 1) / 4 - ($year  - 1)/ 100 + ($year  - 1)/ 400;

for($i=1;$i<$month;$i++){
switch ($i) {
case 1:
$yearday = $yearday + 31;
break;
case 3:
$yearday = $yearday + 31;
break;
case 5:
$yearday = $yearday + 31;
break;
case 7:
$yearday = $yearday + 31;
break;
case 8:
$yearday = $yearday + 31;
break;
case 10:
$yearday = $yearday + 31;
break;
case 12:
$yearday = $yearday + 31;
break;
case 4:
$yearday = $yearday + 30;
break;
case 6:
$yearday = $yearday + 30;
break;
case 9:
$yearday = $yearday + 30;
break;
case 11:
$yearday = $yearday + 30;
break;
case 2:
If ($year%4==0 And $year%100<>0 Or $year%400==0) {
$yearday = $yearday + 29;} 
Else {
$yearday = $yearday + 28;
}
break;
		}
	}
	$yearday = $yearday + $day;
#计算日的六十甲子数 day60
$day60 = ($yearlast + $yearday + 6015)%60;
#确定 日干 dg  日支  dz
$dg = $day60%10;
$dz = $day60%12;
#确定 时干 tg 时支 tz
$tz = ($t_ime + 3)/2%12;
#tg = (dg * 2 + tz + 8) Mod 10
If($tz == 0){
$tg = ($dg * 2 + $tz)%10; }

Else {
$tg = ($dg * 2 + $tz + 8)%10; }
/*#到此，已经完成把 年月日时 转换成为 生辰八字的任务	
'确定各地支所纳天干
'年支纳干 yzg 月支纳干 mzg  日支纳干 dzg 时支纳干 tzg
'年支纳干 yzg*/

switch ($yz) {
   case 1:
        $yzg =0;
        break;
   case 2:
        $yzg =6;
        break;
   case 8:
        $yzg =6;
        break;
   case 3:
        $yzg =1;
        break;
   case 4:
        $yzg =2;
        break;
   case 5:
        $yzg =5;
        break;
   case 11:
        $yzg =5;
        break;
   case 6:
        $yzg =3;
        break;
   case 7:
        $yzg =4;
        break;
   case 9:
        $yzg =7;
        break;
   case 10:
        $yzg =8;
        break;
   case 0:
        $yzg =9;
        break;
}
#月支纳干 mzg
switch ($mz) {
   case 1:
        $mzg =0;
        break;
   case 2:
        $mzg =6;
        break;
   case 8:
        $mzg =6;
        break;
   case 3:
        $mzg =1;
        break;
   case 4:
        $mzg =2;
        break;
   case 5:
        $mzg =5;
        break;
   case 11:
        $mzg =5;
        break;
   case 6:
        $mzg =3;
        break;
   case 7:
        $mzg =4;
        break;
   case 9:
        $mzg =7;
        break;
   case 10:
        $mzg =8;
        break;
   case 0:
        $mzg =9;
        break;
}
#'日支纳干 dzg
switch ($dz) {
   case 1:
        $dzg =0;
        break;
   case 2:
        $dzg =6;
        break;
   case 8:
        $dzg =6;
        break;
   case 3:
        $dzg =1;
        break;
   case 4:
        $dzg =2;
        break;
   case 5:
        $dzg =5;
        break;
   case 11:
        $dzg =5;
        break;
   case 6:
        $dzg =3;
        break;
   case 7:
        $dzg =4;
        break;
   case 9:
        $dzg =7;
        break;
   case 10:
        $dzg =8;
        break;
   case 0:
        $dzg =9;
        break;
}
#'时支纳干 tzg
switch ($tz) {
   case 1:
        $tzg =0;
        break;
   case 2:
        $tzg =6;
        break;
   case 8:
        $tzg =6;
        break;
   case 3:
        $tzg =1;
        break;
   case 4:
        $tzg =2;
        break;
   case 5:
        $tzg =5;
        break;
   case 11:
        $tzg =5;
        break;
   case 6:
        $tzg =3;
        break;
   case 7:
        $tzg =4;
        break;
   case 9:
        $tzg =7;
        break;
   case 10:
        $tzg =8;
        break;
   case 0:
        $tzg =9;
        break;
}
#到此，完成各地支所纳天干的确定任务

#确定各支对应的十神

#年干十神 ygs
$ygs = (($yg + 11 - $dg) + (($dg + 1) % 2) * (($yg + 10 - $dg) % 2) * 2) % 10;

#月干十神 $mgs
$mgs = (($mg + 11 - $dg) + (($dg + 1) % 2) * (($mg + 10 - $dg) % 2) * 2) % 10;

#时干十神 $dgs
$tgs = (($tg + 11 - $dg) + (($dg + 1) % 2) * (($tg + 10 - $dg) % 2) * 2) % 10;

#年支十神 yzs
$yzs = (($yzg + 11 - $dg) + (($dg + 1) % 2) * (($yzg + 10 - $dg) % 2) * 2) % 10;

#月支十神 mzs;
$mzs = (($mzg + 11 - $dg) + (($dg + 1) % 2) * (($mzg + 10 - $dg) % 2) * 2) % 10;

#日支十神 dzs
$dzs = (($dzg + 11 - $dg) + (($dg + 1) % 2) * (($dzg + 10 - $dg) % 2) * 2) % 10;

#时支十神 tzs
$tzs = (($tzg + 11 - $dg) + (($dg + 1) % 2) * (($tzg + 10 - $dg) % 2) * 2) % 10;

#到此，完成年月日时，各干支十神的确定
#确定起运数
##################################################################
#女命
$yearday_a='';
#确定节气 yz 月支  起运基数 qyjs
$md_a=$month_a * 100 + $day_a;
if($md_a>=204 and $md_a<= 305) {
$mz_a = 3;
$qyjs_a = (($month_a - 2) * 30 + $day_a - 4)/3;
    }
if($md_a>=306 and $md_a<=404) {
$mz_a = 4;
$qyjs_a = (($month_a - 3) * 30 + $day_a - 6)/3;
}

if($md_a>=405 and $md_a<= 504) {
$mz_a = 5;
$qyjs_a = (($month_a - 4) * 30 + $day_a - 5)/3;
}

if($md_a>=505 and $md_a<=  605) {
$mz_a = 6;
$qyjs_a = (($month_a - 5) * 30 + $day_a - 5)/3;
}

if($md_a>=606 and $md_a<= 706) {
$mz_a = 7;
$qyjs_a = (($month_a - 6) * 30 + $day_a - 6)/3;
}

if($md_a>=707 and $md_a<= 807) {
$mz_a = 8;
$qyjs_a = (($month_a - 7) * 30 + $day_a - 7)/3;
}

if($md_a>=808 and $md_a<=907) {
$mz_a = 9;
$qyjs_a = (($month_a - 8) * 30 + $day_a - 8)/3;
}

if($md_a>=908 and $md_a<=1007) {
$mz_a = 10;
$qyjs_a = (($month_a - 9) * 30 + $day_a - 8)/3;
}

if($md_a>=1008 and $md_a<= 1106) {
$mz_a = 11;
$qyjs_a = (($month_a - 10) * 30 + $day_a - 8)/3;
}

if($md_a>=1107 and $md_a<=  1207) {
$mz_a = 0;
$qyjs_a = (($month_a - 11) * 30 + $day_a - 7)/3;
}

if($md_a>=1208 and $md_a<=  1231) {
$mz_a = 1;
$qyjs_a = ($day_a - 8)/3;
}

if($md_a>=101 and $md_a<= 105) {
$mz_a = 1;
$qyjs_a = (30 + $day_a - 4)/3;
}

if($md_a>=106 and $md_a<=  203) {
$mz_a = 2;
$qyjs_a = (($month_a - 1) * 30 + $day_a - 6)/3;
}


###############
#确定年干和年支 yg 年干 yz 年支
if($md_a>=204 and $md_a<=1231){
$yg_a = ($year_a-3)%10;
$yz_a = ($year_a-3)%12;
}
if($md_a>=101 and $md_a<=203 ){
$yg_a = ($year_a-4)%10;
$yz_a = ($year_a-4)%12;
}
###############
#确定月干 mg 月干
If ($mz_a > 2 And $mz_a <= 11) {

$mg_a = ($yg_a * 2 + $mz_a + 8)%10;
} else {
$mg_a = ($yg_a * 2 + $mz_a)%10;
}
###############
#从公元0年到目前年份的天数 yearlast
$yearlast_a = ($year_a  - 1) * 5 + ($year_a  - 1) / 4 - ($year_a  - 1)/ 100 + ($year_a  - 1)/ 400;

for($i_a=1;$i_a<$month_a;$i_a++){
switch ($i_a) {
case 1:
$yearday_a = $yearday_a + 31;
break;
case 3:
$yearday_a = $yearday_a + 31;
break;
case 5:
$yearday_a = $yearday_a + 31;
break;
case 7:
$yearday_a = $yearday_a + 31;
break;
case 8:
$yearday_a = $yearday_a + 31;
break;
case 10:
$yearday_a = $yearday_a + 31;
break;
case 12:
$yearday_a = $yearday_a + 31;
break;
case 4:
$yearday_a = $yearday_a + 30;
break;
case 6:
$yearday_a = $yearday_a + 30;
break;
case 9:
$yearday_a = $yearday_a + 30;
break;
case 11:
$yearday_a = $yearday_a + 30;
break;
case 2:
If ($year_a%4==0 And $year_a%100<>0 Or $year_a%400==0) {
$yearday_a = $yearday_a + 29;} 
Else {
$yearday_a = $yearday_a + 28;
}
break;
		}
	}
	$yearday_a = $yearday_a + $day_a;
#计算日的六十甲子数 day60
$day60_a = ($yearlast_a + $yearday_a + 6015)%60;
#确定 日干 dg  日支  dz
$dg_a = $day60_a%10;
$dz_a = $day60_a%12;
#确定 时干 tg 时支 tz
$tz_a = ($t_ime_a + 3)/2%12;
#tg = (dg * 2 + tz + 8) Mod 10
If($tz_a == 0){
$tg_a = ($dg_a * 2 + $tz_a)%10; }

Else {
$tg_a = ($dg_a * 2 + $tz_a + 8)%10; }
/*#到此，已经完成把 年月日时 转换成为 生辰八字的任务	
'确定各地支所纳天干
'年支纳干 yzg 月支纳干 mzg  日支纳干 dzg 时支纳干 tzg
'年支纳干 yzg*/

switch ($yz_a) {
   case 1:
        $yzg_a =0;
        break;
   case 2:
        $yzg_a =6;
        break;
   case 8:
        $yzg_a =6;
        break;
   case 3:
        $yzg_a =1;
        break;
   case 4:
        $yzg_a =2;
        break;
   case 5:
        $yzg_a =5;
        break;
   case 11:
        $yzg_a =5;
        break;
   case 6:
        $yzg_a =3;
        break;
   case 7:
        $yzg_a =4;
        break;
   case 9:
        $yzg_a =7;
        break;
   case 10:
        $yzg_a =8;
        break;
   case 0:
        $yzg_a =9;
        break;
}
#月支纳干 mzg
switch ($mz_a) {
   case 1:
        $mzg_a =0;
        break;
   case 2:
        $mzg_a =6;
        break;
   case 8:
        $mzg_a =6;
        break;
   case 3:
        $mzg_a =1;
        break;
   case 4:
        $mzg_a =2;
        break;
   case 5:
        $mzg_a =5;
        break;
   case 11:
        $mzg_a =5;
        break;
   case 6:
        $mzg_a =3;
        break;
   case 7:
        $mzg_a =4;
        break;
   case 9:
        $mzg_a =7;
        break;
   case 10:
        $mzg_a =8;
        break;
   case 0:
        $mzg_a =9;
        break;
}
#'日支纳干 dzg
switch ($dz_a) {
   case 1:
        $dzg_a =0;
        break;
   case 2:
        $dzg_a =6;
        break;
   case 8:
        $dzg_a =6;
        break;
   case 3:
        $dzg_a =1;
        break;
   case 4:
        $dzg_a =2;
        break;
   case 5:
        $dzg_a =5;
        break;
   case 11:
        $dzg_a =5;
        break;
   case 6:
        $dzg_a =3;
        break;
   case 7:
        $dzg_a =4;
        break;
   case 9:
        $dzg_a =7;
        break;
   case 10:
        $dzg_a =8;
        break;
   case 0:
        $dzg_a =9;
        break;
}
#'时支纳干 tzg
switch ($tz_a) {
   case 1:
        $tzg_a =0;
        break;
   case 2:
        $tzg_a =6;
        break;
   case 8:
        $tzg_a =6;
        break;
   case 3:
        $tzg_a =1;
        break;
   case 4:
        $tzg_a =2;
        break;
   case 5:
        $tzg_a =5;
        break;
   case 11:
        $tzg_a =5;
        break;
   case 6:
        $tzg_a =3;
        break;
   case 7:
        $tzg_a =4;
        break;
   case 9:
        $tzg_a =7;
        break;
   case 10:
        $tzg_a =8;
        break;
   case 0:
        $tzg_a =9;
        break;
}
#到此，完成各地支所纳天干的确定任务

#确定各支对应的十神

#年干十神 ygs
$ygs_a = (($yg_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($yg_a + 10 - $dg_a) % 2) * 2) % 10;

#月干十神 $mgs
$mgs_a = (($mg_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($mg_a + 10 - $dg_a) % 2) * 2) % 10;

#时干十神 $dgs
$tgs_a = (($tg_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($tg_a + 10 - $dg_a) % 2) * 2) % 10;

#年支十神 yzs
$yzs_a = (($yzg_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($yzg_a + 10 - $dg_a) % 2) * 2) % 10;

#月支十神 mzs;
$mzs_a = (($mzg_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($mzg_a + 10 - $dg_a) % 2) * 2) % 10;

#日支十神 dzs
$dzs_a = (($dzg_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($dzg_a + 10 - $dg_a) % 2) * 2) % 10;

#时支十神 tzs
$tzs_a = (($tzg_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($tzg_a + 10 - $dg_a) % 2) * 2) % 10;
#女命已算完
#到此，完成年月日时，各干支十神的确定

##############################################
#合婚开始
###求出年份后两位数
$f_n=substr("$year", 2); 
$f_v=substr("$year_a", 2); 
###求出所属宫位(数值表示）
$z_n=safe_convert("$f_n");
$z_v=safe_convert_a("$f_v");
if($z_n==5) {$z_nn="2";} else {$z_nn=$z_n;}
if($z_v==5) {$z_vv="8";} else {$z_vv=$z_v;}

if($z_n==0) {$z_nn="9";} else {$z_nn=$z_n;}
if($z_v==0) {$z_vv="9";} else {$z_vv=$z_v;}

###推出年干年支
$qq_n=shengchen($f_n);
$qq_v=shengchen($f_v);
###求出所属宫位(汉字表示）
$m_n=mgong("$z_n");
$m_v=mgong_a("$z_v");

if($z_nn==1 and $z_vv==4){ $bb="30";   }
if($z_nn==4 and $z_vv==1){ $bb="30";   }

if($z_nn==2 and $z_vv==8){ $bb="30";   }
if($z_nn==8 and $z_vv==2){ $bb="30";   }

if($z_nn==3 and $z_vv==9){ $bb="30";   }
if($z_nn==9 and $z_vv==3){ $bb="30";   }

if($z_nn==6 and $z_vv==7){ $bb="30";   }
if($z_nn==7 and $z_vv==6){ $bb="30";   }
#########
if($z_nn==1 and $z_vv==8){ $bb="0";   }
if($z_nn==8 and $z_vv==1){ $bb="0";   }

if($z_nn==2 and $z_vv==4){ $bb="0";   }
if($z_nn==4 and $z_vv==2){ $bb="0";   }

if($z_nn==3 and $z_vv==6){ $bb="0";   }
if($z_nn==6 and $z_vv==3){ $bb="0";   }

if($z_nn==9 and $z_vv==7){ $bb="0";   }
if($z_nn==7 and $z_vv==9){ $bb="0";   }
#######3
if($z_nn==1 and $z_vv==9){ $bb="30";   }
if($z_nn==9 and $z_vv==1){ $bb="30";   }

if($z_nn==2 and $z_vv==6){ $bb="30";   }
if($z_nn==6 and $z_vv==2){ $bb="30";   }

if($z_nn==3 and $z_vv==4){ $bb="30";   }
if($z_nn==4 and $z_vv==3){ $bb="30";   }

if($z_nn==8 and $z_vv==7){ $bb="30";   }
if($z_nn==7 and $z_vv==8){ $bb="30";   }
#########
if($z_nn==1 and $z_vv==6){ $bb="0";   }
if($z_nn==6 and $z_vv==1){ $bb="0";   }

if($z_nn==2 and $z_vv==9){ $bb="0";   }
if($z_nn==9 and $z_vv==2){ $bb="0";   }

if($z_nn==3 and $z_vv==8){ $bb="0";   }
if($z_nn==8 and $z_vv==3){ $bb="0";   }

if($z_nn==4 and $z_vv==7){ $bb="0";   }
if($z_nn==7 and $z_vv==4){ $bb="0";   }
######
if($z_nn==1 and $z_vv==7){ $bb="0";   }
if($z_nn==7 and $z_vv==1){ $bb="0";   }

if($z_nn==2 and $z_vv==3){ $bb="0";   }
if($z_nn==3 and $z_vv==2){ $bb="0";   }

if($z_nn==4 and $z_vv==6){ $bb="0";   }
if($z_nn==6 and $z_vv==4){ $bb="0";   }

if($z_nn==8 and $z_vv==9){ $bb="0";   }
if($z_nn==9 and $z_vv==8){ $bb="0";   }
######
if($z_nn==1 and $z_vv==3){ $bb="30";   }
if($z_nn==3 and $z_vv==1){ $bb="30";   }

if($z_nn==2 and $z_vv==7){ $bb="30";   }
if($z_nn==7 and $z_vv==2){ $bb="30";   }

if($z_nn==4 and $z_vv==9){ $bb="30";   }
if($z_nn==9 and $z_vv==4){ $bb="30";   }

if($z_nn==8 and $z_vv==6){ $bb="30";   }
if($z_nn==6 and $z_vv==8){ $bb="30";   }
######
if($z_nn==1 and $z_vv==2){ $bb="0";   }
if($z_nn==2 and $z_vv==1){ $bb="0";   }

if($z_nn==7 and $z_vv==3){ $bb="0";   }
if($z_nn==3 and $z_vv==7){ $bb="0";   }

if($z_nn==4 and $z_vv==8){ $bb="0";   }
if($z_nn==8 and $z_vv==4){ $bb="0";   }

if($z_nn==9 and $z_vv==6){ $bb="0";   }
if($z_nn==6 and $z_vv==9){ $bb="0";   }
#####
if($z_nn==1 and $z_vv==1){ $bb="15";   }
if($z_nn==2 and $z_vv==2){ $bb="15";   }

if($z_nn==3 and $z_vv==3){ $bb="15";   }
if($z_nn==4 and $z_vv==4){ $bb="15";   }

if($z_nn==6 and $z_vv==6){ $bb="15";   }
if($z_nn==7 and $z_vv==7){ $bb="15";   }

if($z_nn==8 and $z_vv==8){ $bb="15";   }
if($z_nn==9 and $z_vv==9){ $bb="15";   }
######命宫合婚完
###年支合
if($c[30+$yz_a]==$c[30+$yz]) { $c = "20"; } else  { $c = "0"; } 
###月令合
if($a[30+$mz_a]==$a[30+$mz]){ $yh = "5"; } else  { $yh = "0"; } 
###日合
if($a[20+$dg_a]<>$a[20+$dg]) {
if($e[20+$dg_a]==$e[20+$dg]){ $rh = "5"; } else  { $rh = "0"; } } else { $rh = "0"; }
if($d[20+$dg_a]==$d[20+$dg]){ $rrh = "25"; } else  { $rrh = "0"; } 
###子女同步
if($tgs==7 or $tgs==8) { $erzi ="男"; }
if($tgs==5 or $tgs==6) { $erzi ="女"; }
if($tgs==1 or $tgs==2) { $erzi ="女"; }
if($tgs==3 or $tgs==4) { $erzi ="女"; }
if($tgs==9 or $tgs==0) { $erzi ="女"; }

if($tgs_a==5 or $tgs_a==6) { $erzi_a ="男"; }
if($tgs_a==7 or $tgs_a==8) { $erzi_a ="女"; }
if($tgs_a==1 or $tgs_a==2) { $erzi_a ="女"; }
if($tgs_a==3 or $tgs_a==4) { $erzi_a ="女"; }
if($tgs_a==9 or $tgs_a==0) { $erzi_a ="女"; }
if($erzi_a==$erzi){ $ez = "15"; } else  { $ez = "0"; } 


$sea =0;
$yza =$yz_a%2;
If($sea Xor $yza){
$qyjs_a = $qyjs_a-1; }
Else {
$qyjs_a = 10 - $qyjs_a;
}
######东西四命
$m_na=dxsz("$z_n");
$m_va=dxsz_a("$z_v");

$m_nfw=fangwei("$z_n");
$m_vfw=fangwei_a("$z_v");

?>
      <strong><br>
      姓名：</strong>
      <?php echo $name ?>      <br>
      <br>
      <strong>出生地时间</strong><strong>公历：</strong> <?php echo $year.'年'.$month.'月'.$day.'日'.$t_ime.'时'?><br>

<br>
<strong>胎元： </strong> <strong>命宫： </strong> <br>
<br>
<table width="90%" height="131"  border="0" align="center" cellpadding="0" cellspacing="0">
  <tr>
    <td width="54"><strong>旬空：</strong></td>
    <td width="51">&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="59">&nbsp;</td>
    <td width="53">&nbsp;</td>
  </tr>
  <tr class="xx">
    <td><strong>十神：</strong></td>
    <td width="51"><div align="center">
        <?php echo $a[$ygs] ?>
    </div></td>
    <td width="51"><div align="center">
        <?php echo $a[$mgs] ?>
    </div></td>
    <td width="59"><div align="center">日主</div></td>
    <td width="53"><div align="center">
        <?php echo $a[$tgs] ?>
    </div></td>
  </tr>
  <tr class="hs">
    <td>乾造 </td>
    <td width="51"><div align="center"><?php echo $a[20+$yg].$a[30+$yz];	?></div></td>
    <td width="51"><div align="center"><?php echo $a[20+$mg].$a[30+$mz];	?></div></td>
    <td width="59"><div align="center"><?php echo $a[20+$dg].$a[30+$dz];	?></div></td>
    <td width="53"><div align="center"><?php echo $a[20+$tg].$a[30+$tz];	?></div></td>
  </tr>
  <tr>
    <td><strong>支十神：</strong></td>
    <td width="51"><div align="center">
        <?php echo $a[$yzs] ?>
    </div></td>
    <td width="51"><div align="center">
        <?php echo $a[$mzs] ?>
    </div></td>
    <td width="59"><div align="center">
        <?php echo $a[$dzs] ?>
    </div></td>
    <td width="53"><div align="center">
        <?php echo $a[$tzs] ?>
    </div></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="59">&nbsp;</td>
    <td width="53">&nbsp;</td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="59">&nbsp;</td>
    <td width="53">&nbsp;</td>
  </tr>
</table>
<p> <br>
  <table width="80%"  border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td width="40" height="20">十神：</td>
  <?php
  for($i=1;$i<9;$i++) {
    $sx = (($mg+10)-$i)%10;
	 $xy = (($sx + 11 - $dg) + (($dg + 1) % 2) * (($sx + 10 - $dg) % 2) * 2) % 10;; 
   echo '<td>'.$a[$xy].'</td>';
}
  ?>
  </tr>
  <tr  class="hs">
    <td height="20">大运：</td>
  <?php
  for($i=1;$i<9;$i++) {
   echo  '<td>'.$a[20+((($mg+10)-$i)%10)].$a[30+((($mz+12)-$i)%12)].'</td>';   
}
  ?>
  </tr>
  <tr>
    <td height="20"></td>
  <?php
 $qyjsxy= floor($qyjs)+1;
    for($i=1;$i<9;$i++) {
	
    echo '<td>'.$qyjsxy.'岁</td>'; 
   $qyjsxy=($qyjsxy+10);
}
?>
  </tr>
  <tr>
    <td height="20">&nbsp;</td>
    <td><?php echo $year+floor($qyjs)+1 ?></td>
    <td><?php echo $year+floor($qyjs)+11 ?></td>
    <td><?php echo $year+floor($qyjs)+21 ?></td>
    <td><?php echo $year+floor($qyjs)+31 ?></td>
    <td><?php echo $year+floor($qyjs)+41 ?></td>
	<td><?php echo $year+floor($qyjs)+51 ?></td>
	<td><?php echo $year+floor($qyjs)+61 ?></td>
    <td><?php echo $year+floor($qyjs)+71 ?></td>
  </tr>
</table>
</p><p>生肖属：<?php echo $b[30+$yz] ?><br>
  命宫为：<?php echo $m_n ?>
  <br>
  头胎为：<?php echo $erzi ?>
</p>
<p>&#24744;&#23646;&#20110;&#65306;
  <?php echo $m_na ?>&#22235;&#21629;&#65292;&#23452;&#20303;<?php echo $m_na ?>&#22235;&#23429;&#30340;&#25151;&#23376;&#20026;&#26368;&#20339;&#65292;&#26368;&#20339;&#22352;&#21521;&#65306;<?php echo $m_nfw ?>
</p>
<p>&nbsp;</p>
<p>&nbsp;</p></td>
    <td width="50%" bgcolor="#FFF0FF">姓名：
      <?php echo $name_a ?>      <br>
      <br>
      <strong>出生地时间</strong><strong>公历：</strong> <?php echo $year_a.'年'.$month_a.'月'.$day_a.'日'.$t_ime_a.'时'?>
<br>
<strong>胎元： </strong> <strong>命宫： </strong> <br>
<br>
<table width="90%" height="131"  border="0" align="center" cellpadding="0" cellspacing="0">
  <tr>
    <td width="54"><strong>旬空：</strong></td>
    <td width="51">&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="59">&nbsp;</td>
    <td width="53">&nbsp;</td>
  </tr>
  <tr class="xx">
    <td><strong>十神：</strong></td>
    <td width="51"><div align="center">
        <?php echo $a[$ygs_a] ?>
    </div></td>
    <td width="51"><div align="center">
        <?php echo $a[$mgs_a] ?>
    </div></td>
    <td width="59"><div align="center">日主</div></td>
    <td width="53"><div align="center">
        <?php echo  $a[$tgs_a] ?>
    </div></td>
  </tr>
  <tr class="hs">
    <td>坤造</td>
    <td width="51"><div align="center"><?php echo $a[20+$yg_a].$a[30+$yz_a];	?></div></td>
    <td width="51"><div align="center"><?php echo $a[20+$mg_a].$a[30+$mz_a];	?></div></td>
    <td width="59"><div align="center"><?php echo $a[20+$dg_a].$a[30+$dz_a];	?></div></td>
    <td width="53"><div align="center"><?php echo $a[20+$tg_a].$a[30+$tz_a];	?></div></td>
  </tr>
  <tr>
    <td><strong>支十神：</strong></td>
    <td width="51"><div align="center">
        <?php echo $a[$yzs_a]?>
    </div></td>
    <td width="51"><div align="center">
        <?php echo $a[$mzs_a]?>
    </div></td>
    <td width="59"><div align="center">
        <?php echo $a[$dzs_a]?>
    </div></td>
    <td width="53"><div align="center">
        <?php echo $a[$tzs_a]?>
    </div></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="59">&nbsp;</td>
    <td width="53">&nbsp;</td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="51">&nbsp;</td>
    <td width="59">&nbsp;</td>
    <td width="53">&nbsp;</td>
  </tr>
</table>
<p>&nbsp;  </p>
<?php

If($sex==1 Xor $yz_a%2){ ?>
<table width="80%"  border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td width="40" height="20">十神：</td>
    <?php
  for($i=0;$i<8;$i++) {
    $sx_a = (($mg_a+10)-$i)%10;
	 $xy_a = (($sx_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($sx_a + 10 - $dg_a) % 2) * 2) % 10; 
   echo '<td>'.$a[$xy_a].'</td>';
}
  ?>
  </tr>
  <tr  class="hs">
    <td height="20">大运：</td>
    <?php
  for($i=1;$i<9;$i++) {
   echo  '<td>'.$a[20+((($mg_a+10)-$i)%10)].$a[30+((($mz_a+12)-$i)%12)].'</td>';   
}
  ?>
  </tr>
  <tr>
    <td height="20"></td>
    <?php
 $qyjsxy_a= floor($qyjs_a);
    for($i=1;$i<9;$i++) {
	
    echo '<td>'.$qyjsxy_a.'岁</td>'; 
   $qyjsxy_a=($qyjsxy_a+10);
}
?>
  </tr>
  <tr>
    <td height="20">&nbsp;</td>
    <td><?php $year_a+floor($qyjs_a) ?></td>
    <td><?php $year_a+floor($qyjs_a)+10 ?></td>
    <td><?php $year_a+floor($qyjs_a)+20 ?></td>
    <td><?php $year_a+floor($qyjs_a)+30 ?></td>
    <td><?php $year_a+floor($qyjs_a)+40 ?></td>
    <td><?php $year_a+floor($qyjs_a)+50 ?></td>
    <td><?php $year_a+floor($qyjs_a)+60 ?></td>
    <td><?php $year_a+floor($qyjs_a)+70 ?></td>
  </tr>
</table>

<?php
 }
Else
{ 
	?>
<table width="80%"  border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td width="40" height="20">十神：</td>
    <?php
  for($i=1;$i<9;$i++) {
    $sx_a = (($mg_a+10)+$i)%10;
	 $xy_a = (($sx_a + 11 - $dg_a) + (($dg_a + 1) % 2) * (($sx_a + 10 - $dg_a) % 2) * 2) % 10; 
   echo '<td>'.$a[$xy_a].'</td>';
}
  ?>
  </tr>
  <tr  class="hs">
    <td height="20">大运：</td>
    <?php
  for($i=1;$i<9;$i++) {
   echo  '<td>'.$a[20+((($mg_a+10)+$i)%10)].$a[30+((($mz_a+12)+$i)%12)].'</td>';   
}
  ?>
  </tr>
  <tr>
    <td height="20"></td>
    <?php
 $qyjsxy_a= floor($qyjs_a)+1;
    for($i=1;$i<9;$i++) {
	
    echo '<td>'.$qyjsxy_a.'岁</td>'; 
   $qyjsxy_a=($qyjsxy_a+10);
}
?>
  </tr>
  <tr>
    <td height="20">&nbsp;</td>
    <td><?php echo $year_a+floor($qyjs_a)+2?></td>
    <td><?php  echo $year_a+floor($qyjs_a)+12?></td>
    <td><?php  echo $year_a+floor($qyjs_a)+22?></td>
    <td><?php  echo $year_a+floor($qyjs_a)+32?></td>
    <td><?php  echo $year_a+floor($qyjs_a)+42?></td>
    <td><?php  echo $year_a+floor($qyjs_a)+52?></td>
    <td><?php  echo $year_a+floor($qyjs_a)+62?></td>
    <td><?php  echo $year_a+floor($qyjs_a)+72?></td>
  </tr>
</table>

<?php }
?><p><br>
    <span class="hs">  </span></p><p>生肖属：<?php  echo $b[30+$yz_a]?>
  <br>
命宫为：<?php echo $m_v ?>
<br>
头胎为：<?php echo $erzi_a ?>
</p>
<p>&#24744;&#23646;&#20110;&#65306;<?php echo $m_va ?>&#22235;&#21629;&#65292;&#23452;&#20303;<?php echo $m_va?>&#22235;&#23429;&#30340;&#25151;&#23376;&#20026;&#26368;&#20339;&#65292;&#26368;&#20339;&#22352;&#21521;&#65306;<?php echo  $m_vfw?>
</p>
<p>&nbsp;</p></td>
  </tr>
  <tr valign="top">
    <td height="221" colspan="2"><table width="100%"  border="0" cellpadding="0" cellspacing="0">
      <tr>
        <td height="36" colspan="3"> <div align="left"> <span class="xx">传统风水学将家宅分为东四宅和西四宅，请读者根据自己住所的坐向找出所属的宅卦 。 <br>
</span><span class="hs">东四宅，分别是： 坎宅（坐北向南）、离宅（坐南向北）、震宅（坐东向西）、巽宅（坐东南向西北）。 <br>
西四宅，分别是： 乾宅（坐西北向东南）、兑宅（坐西向东）、艮宅（坐东北向西南）、坤宅（坐西南向东北）。</span><span class="xx"> <br>
阳宅十书.论福元第二》云：“盖厥初太极生两仪，两仪生四象，四象生八卦。故生人分东位西位乃两仪之说，分东四位西四位乃四象之说，分乾、坤、艮、兑、坎、离、震、巽乃八卦之说，是皆天地大道造化自然之理。若福元（即生年八卦属性）一错，则东四修西，西四修东，吉星反变凶星，虽外形内形俱吉，皆无用矣，关系最大。”<br>
故此 ，东四命的朋友，适合居住东四宅，西四命的朋友适合居住西四宅，两者不可混淆，否则，皆为不吉。 </span><br>
        </div></td>
        </tr>
      <tr bgcolor="#FFFFDD">
        <td height="40" colspan="3"><div align="center" class="style1">合婚结果如下</div></td>
      </tr>
      <tr>
      
      </tr>
      <tr valign="middle" bgcolor="#FFE6E6" class="hs">
        <td width="15%" height="50" class="xx"><div align="right">命宫：</div></td>
        <td width="13%" height="22"><?php echo $bb ?>分 &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
        <td width="72%">此项为30分 <span class="xx">说明：以东四命与西四命之说来合，如果相合，那么在购房时，应买与自己命宫相合的房子。</span></td>
      </tr>
      <tr valign="middle" bgcolor="#FFE6E6" class="hs">
        <td height="50" class="xx"><div align="right">年支同气：</div></td>
        <td height="22" class="hs"><?php echo $c ?>分 &nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp; </td>
        <td height="22" class="hs">此项为20分 <span class="xx">说明：如寅卯辰会东方木气，虎兔龙结合的机缘就大于其它属相；巳午未会南方火气，蛇马羊结合的机缘就大于其它属相；申酉戌会西方金气，猴鸡狗结合的机缘就大于其它属相；亥子丑会北方水气，猪鼠牛结合的机缘就大于其它属相。 </span></td>
      </tr>
      <tr valign="middle" bgcolor="#FFE6E6" class="hs">
        <td height="50" class="xx"><div align="right">月令合：</div></td>
        <td height="22"><?php echo  $yh ?>分 &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;</td>
        <td height="22">此项为5分 <span class="xx">说明：男女生月相同者互相间也是很有缘份的 </span></td>
      </tr>
      <tr valign="middle" bgcolor="#FFE6E6" class="hs">
        <td height="50" class="xx"><div align="right">日干相合：</div></td>
        <td height="22"><?php echo $rrh ?>分 &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;</td>
        <td height="22">此项为25分 <span class="xx">说明：谓日干舒配得所？日干五行相同，一阴一阳的组合男女结合的机缘最大，如甲日干逢乙日干，庚日干逢辛日干之类。 </span></td>
      </tr>
      <tr valign="middle" bgcolor="#FFE6E6" class="hs">
        <td height="50" class="xx"><div align="right">天干五合：</div></td>
        <td height="22"><?php echo $rh ?>分 &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;</td>
        <td height="22">此项为5分 <span class="xx">说明：其次是天干五合，如甲日干逢己日干，庚日干逢乙日干之类。再次则是比和或相生。 </span></td>
      </tr>
      <tr valign="middle" bgcolor="#FFE6E6" class="hs">
        <td height="50" class="xx"><div align="right">子女同步：</div></td>
        <td height="22"><?php echo $ez ?>分 </td>
        <td height="22">此项为15分 <span class="xx">说明：何谓子女同步？西方的科学家在探索男女结合的奥秘时提出了 &quot; 性染色体论 &quot; ，我们东方人在四柱预测中看头胎子女的性别，男女双方的八字中头胎子女的性别必须一致。 </span></td>
      </tr>
      <tr valign="middle" bgcolor="#FFE6E6" class="hs">
        <td height="50" class="xx"><div align="right">总分：</div></td>
        <td height="22" colspan="2"><?php echo $rh+$bb+$c+$yh+$rrh+$ez ?> 分 </td>
      </tr>
    </table></td>
  </tr>
</table>
<hr size="1">
<span class="unnamed1"><br>
</span>


</body>
</html>
