<?php
include(__DIR__ . '/lib/class.paipan.php');
$p = new paipan();

if($_POST['act'] == 'fatemaps'){
    $p->zwz = false;
    
    $d = $_POST['param'];
    
    $o = $p->fatemaps($d[0],$d[1],$d[2],$d[3],$d[4],$d[5],$d[6],$d[7],$d[8]);
    
    die(json_encode($o));
}

$fm = $p->fatemaps(0, 1990, 1, 1, 12, 0, 0, 120, 35);

print_r($fm);

$tg = $fm['tg'];
$dz = $fm['dz'];

$ckey = array(
    0 => '年柱',
    1 => '月柱',
    2 => '日柱',
    3 => '时柱',
    4 => '大运',
    5 => '流年',
    6 => '流月',
    7 => '流日',
    8 => '流时'
);
$tgdz = array(
    0 => '天干',
    1 => '地支'
);

//$tg = [0,1,2,3,4,5,6,7,5];
//$dz = [0,1,4,8,11,6,2,5,6];
$gxs = $p->GetGX($tg, $dz);
foreach ($gxs as $type => $list){ //$type指示0天干1地支
    foreach ($list as $gx){
        $a = [];
        foreach ($gx[0] as $k => $v){
            $a[] = $ckey[$k] . $tgdz[$gx[1][0]];
        }
        
        echo implode('+', $a) . ':' . $gx[1][4]."<br />\n";
    }
}
