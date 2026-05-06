<?php

function safe_convert($x) {
            $r = 100-$x;
            $s = $r%9;
            if($s==5){ $s=2; }
        return $s;          }

function safe_convert_a($x) {
            $r = $x-4;
            $s = $r%9;
            if($s==5){ $s=8; }
        return $s;          }


function shengchen($i) {
         switch ($i) {
    case '00':
        $s="庚辰";
        break;
    case '01':
        $s="辛丑";
        break;
    case '02':
        $s="壬寅";
        break;
    case '03':
        $s="癸卯";
        break;
    case '04':
        $s="甲辰";
        break;
    case '05':
        $s="乙已";
        break;
    case '06':
        $s="丙午";
        break;
    case '07':
        $s="丁未";
        break;
    case '08':
        $s="戊申";
        break;
    case '09':
        $s="己酉";
        break;
    case '10':
        $s="庚戌";
        break;
    case '11':
        $s="辛亥";
        break;
    case '12':
        $s="壬子";
        break;
    case '13':
        $s="癸丑";
        break;
    case '14':
        $s="甲寅";
        break;
    case '15':
        $s="乙卯";
        break;
    case '16':
        $s="丙辰";
        break;
    case '17':
        $s="丁巳";
        break;
    case '18':
        $s="戊午";
        break;
    case '19':
        $s="己未";
        break;
    case '20':
        $s="庚申";
        break;
    case '21':
        $s="辛酉";
        break;
    case '22':
        $s="壬戌";
        break;
    case '23':
        $s="癸亥";
        break;
    case '24':
        $s="甲子";
        break;
    case '25':
        $s="乙丑";
        break;
    case '26':
        $s="丙寅";
        break;
    case '27':
        $s="丁卯";
        break;
    case '28':
        $s="戊辰";
        break;
    case '29':
        $s="己巳";
        break;
    case '30':
        $s="庚午";
        break;
    case '31':
        $s="辛未";
        break;
    case '32':
        $s="壬申";
        break;
    case '33':
        $s="癸酉";
        break;
    case '34':
        $s="甲戌";
        break;
    case '35':
        $s="乙亥";
        break;
    case '36':
        $s="丙子";
        break;
    case '37':
        $s="丁丑";
        break;
    case '38':
        $s="戊寅";
        break;
    case '39':
        $s="己卯";
        break;
    case '40':
        $s="庚辰";
        break;
    case '41':
        $s="辛巳";
        break;
    case '42':
        $s="壬午";
        break;
    case '43':
        $s="癸未";
        break;
    case '44':
        $s="甲申";
        break;
    case '45':
        $s="乙酉";
        break;
    case '46':
        $s="丙戌";
        break;
    case '47':
        $s="丁亥";
        break;
    case '48':
        $s="戊子";
        break;
    case '49':
        $s="己丑";
        break;
    case '50':
        $s="庚寅";
        break;
    case '51':
        $s="辛卯";
        break;
    case '52':
        $s="壬辰";
        break;
    case '53':
        $s="癸巳";
        break;
    case '54':
        $s="甲午";
        break;
    case '55':
        $s="乙未";
        break;
    case '56':
        $s="丙申";
        break;
    case '57':
        $s="丁酉";
        break;
    case '58':
        $s="戊戌";
        break;
    case '59':
        $s="己亥";
        break;
    case '60':
        $s="庚子";
        break;
    case '61':
        $s="辛丑";
        break;
    case '62':
        $s="壬寅";
        break;
    case '63':
        $s="癸卯";
        break;
    case '64':
        $s="甲辰";
        break;
    case '65':
        $s="乙巳";
        break;
    case '66':
        $s="丙午";
        break;
    case '67':
        $s="丁未";
        break;
    case '68':
        $s="戊申";
        break;
    case '69':
        $s="己酉";
        break;
    case '70':
        $s="庚戌";
        break;
    case '71':
        $s="辛亥";
        break;
    case '72':
        $s="壬子";
        break;
    case '73':
        $s="癸丑";
        break;
    case '74':
        $s="甲寅";
        break;
    case '75':
        $s="乙卯";
        break;
    case '76':
        $s="丙辰";
        break;
    case '77':
        $s="丁巳";
        break;
    case '78':
        $s="戊午";
        break;
    case '79':
        $s="己未";
        break;
    case '80':
        $s="庚申";
        break;
    case '81':
        $s="辛酉";
        break;
    case '82':
        $s="壬戌";
        break;
    case '83':
        $s="癸亥";
        break;
    case '84':
        $s="甲子";
        break;
    case '85':
        $s="乙丑";
        break;
    case '86':
        $s="丙寅";
        break;
    case '87':
        $s="丁卯";
        break;
    case '88':
        $s="戊辰";
        break;
    case '89':
        $s="己巳";
        break;
    case '90':
        $s="庚午";
        break;
    case '91':
        $s="辛未";
        break;
    case '92':
        $s="壬申";
        break;
    case '93':
        $s="癸酉";
        break;
    case '94':
        $s="甲戌";
        break;
    case '95':
        $s="乙亥";
        break;
    case '96':
        $s="丙子";
        break;
    case '97':
        $s="丁丑";
        break;
    case '98':
        $s="戊寅";
        break;
    case '99':
        $s="己卯";
        break;
    default:
        $s="不存在";
}
        return $s;          }
		
		function mgong($i) {
         switch ($i) {
    case 0:
        $s="离";
        break;
    case 1:
        $s="坎";
        break;
    case 2:
        $s="坤";
        break;
    case 3:
        $s="震";
        break;
    case 4:
        $s="巽";
        break;
    case 5:
        $s="坤";
        break;
    case 6:
        $s="乾";
        break;
    case 7:
        $s="兑";
        break;
    case 8:
        $s="艮";
        break;
    case 9:
        $s="离";
        break;
}
        return $s;          }

function mgong_a($i) {
         switch ($i) {
    case 0:
        $s="离";
        break;
    case 1:
        $s="坎";
        break;
    case 2:
        $s="坤";
        break;
    case 3:
        $s="震";
        break;
    case 4:
        $s="巽";
        break;
    case 5:
        $s="艮";
        break;
    case 6:
        $s="乾";
        break;
    case 7:
        $s="兑";
        break;
    case 8:
        $s="艮";
        break;
    case 9:
        $s="离";
        break;
}
        return $s;          }
		

function safew($s) {
        $s=str_replace("|","│",$s);
        $s=str_replace("<","&lt;",$s);
        $s=str_replace(">","&gt;",$s);
        $s=str_replace("\r","",$s);
        $s=str_replace("\t","",$s);
        @$s=str_replace("\n","<br><br>&nbsp;&nbsp;&nbsp;&nbsp;",$s);
        $s=str_replace(" ","&nbsp;",$s);
        return $s;          }


function dxsz($i) {
         switch ($i) {
    case 0:
        $s="东";
        break;
    case 1:
        $s="东";
        break;
    case 2:
        $s="西";
        break;
    case 3:
        $s="东";
        break;
    case 4:
        $s="东";
        break;
    case 5:
        $s="西";
        break;
    case 6:
        $s="西";
        break;
    case 7:
        $s="西";
        break;
    case 8:
        $s="西";
        break;
    case 9:
        $s="东";
        break;

}
        return $s;          }
function dxsz_a($i) {
         switch ($i) {
    case 0:
        $s="东";
        break;
    case 1:
        $s="东";
        break;
    case 2:
        $s="西";
        break;
    case 3:
        $s="东";
        break;
    case 4:
        $s="东";
        break;
    case 5:
        $s="西";
        break;
    case 6:
        $s="西";
        break;
    case 7:
        $s="西";
        break;
    case 8:
        $s="西";
        break;
    case 9:
        $s="东";
        break;
}
        return $s;          }
		
function fangwei($i) {
         switch ($i) {
    case 0:
        $s="坐南向北";
        break;
    case 1:
        $s="坐北向南";
        break;
    case 2:
        $s="坐西南向东北";
        break;
    case 3:
        $s="坐东向西";
        break;
    case 4:
        $s="坐东南向西北";
        break;
    case 5:
        $s="坐西南向东北";
        break;
    case 6:
        $s="坐西北向东南";
        break;
    case 7:
        $s="坐西向东";
        break;
    case 8:
        $s="坐东北向西南";
        break;
    case 9:
        $s="坐南向北";
        break;
}
        return $s;          }

function fangwei_a($i) {
         switch ($i) {
    case 0:
        $s="坐南向北";
        break;
    case 1:
        $s="坐北向南";
        break;
    case 2:
        $s="坐西南向东北";
        break;
    case 3:
        $s="坐东向西";
        break;
    case 4:
        $s="坐东南向西北";
        break;
    case 5:
        $s="坐东北向西南";
        break;
    case 6:
        $s="坐西北向东南";
        break;
    case 7:
        $s="坐西向东";
        break;
    case 8:
        $s="坐东北向西南";
        break;
    case 9:
        $s="坐南向北";
        break;
}
        return $s;          }
?>
