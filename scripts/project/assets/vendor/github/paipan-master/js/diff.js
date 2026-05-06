"use strict";
//用于跟寿星万年历进行比对
//使用方法: 在寿星万年历的 sxwnl/source/index.htm 页脚加入 <script language="javascript" src="../../js/diff.js"></script> 浏览器中打开开发者工具,浏览 https://....sxwnl/source/index.htm

window.src = document.currentScript.src + "/../";
function loadJS(js, callback) {
    var script = document.createElement('script');
    script.type = 'text/javascript';
	script.charset = 'UTF-8';
    if (script.readyState) { //IE
        script.onreadystatechange = function() {
            if (script.readyState == 'loaded' || script.readyState == 'complete') {
                script.onreadystatechange = null;
                callback();
            }
        };
    } else {
        script.onload = function() { //其他浏览器
            callback();
        };
    }

    script.src = window.src + js;
    document.getElementsByTagName('head')[0].appendChild(script);
}
function log(o){
	for(var i in arguments){
		console.log(arguments[i]);
	}
}
function go(){ //廿四节气与寿星万年历比对
	var h = [];
	var c = 0; //1为秋分
	var start = 1457698.231017 - 14; //-721-12-17 - 14
	var year = 0;
	var fs = [];
	
	for0:for(var st=0; ; st++){
		if(start + st >= 2561118){ //2300-01-01
			log("End.");
			break;
		}
		
		var jd = start + st - 2451545;
		var W = Math.floor((jd - 355 + 183) / 365.2422) * 365.2422 + 355; //355是2000.12冬至,得到较靠近jd的冬至估计值
		if (SSQ.calc(W, '气') > jd) {
			W -= 365.2422;
		}

		var A = [];
		var B = [];
		for (var i = 0; i < 24; i++) {
			A[i] = SSQ.calc(W + 15.2184 * i, '气') + 2451545; //24个节气时刻(北京时间),从冬至开始到下一个冬至以后
		}
		
		var [year] = p.Jtime(A[0]);
		var dj = p.GetAdjustedJQ(year, true);
		B[0] = dj[18];
		B[1] = dj[19];
		B[2] = dj[20];
		B[3] = dj[21];
		B[4] = dj[22];
		B[5] = dj[23];
		var dj = p.GetAdjustedJQ(year+1, true);
		for(var j=6; j<=23; j++){
			B[j] = dj[j-6];
		}
		for(var j=0; j<24; j++){

			var i = (18 + j)%24;
			
			var [yy, mm, dd, hh, mt, ss] = p.Jtime(A[j]);
			
			var [yy2, mm2, dd2, hh2, mt2, ss2] = p.Jtime(B[j]);
			
			if((yy != yy2) || (mm != mm2) || (dd != dd2)){
				if(j <= 5){
					var fy = year;
					var fi = j + 18;
				}
				if(j >= 6){
					var fy = year + 1;
					var fi = j - 6;
				}
				var fd = A[j] - p.Jdays(yy2, mm2, dd2, 12, 0, 0);
				
				if(fs[fy] == undefined){
					fs[fy] = new Array();
				}
				fs[fy][fi] = fd;
				
				//log(p.jq[i])
				
				log([yy, mm, dd, hh, mt, ss]);
				log([yy2, mm2, dd2, hh2, mt2, ss2]);
				break for0;
			}
		}
	}
	
	var sp = '';
	var sj = "var jqXFu = {\n";
	for(var year in fs){
		sp += (year + "=>[");
		sj += ((year<0?"'":"")+year+(year<0?"'":"") + ":{");
		for(var i in fs[year]){
			sp += (i+"=>"+fs[year][i]+",");
			sj += (i+":"+fs[year][i]+",");
		}
		sp = sp.substr(0, sp.length-1);
		sj = sj.substr(0, sj.length-1);
		sp += "],\n";
		sj += "},\n";
	}
	sj += "}\n";
	log(sp);
	log(sj)
}
function go2(){ //朔望日与寿星万年历比对(很耗时)
	var h = [];
	var c = 0; //1为秋分
	var start = 1457698.231017 - 14; //-721-12-17 - 14
	var year = 0;
	var fs = [];
	
	for0:for(var st=0; ; st++){
		if(start + st >=  2561118){ //2300-01-01
			log("End.");
			break;
		}
		var jd = start + st - 2451545;
		var W = Math.floor((jd - 355 + 183) / 365.2422) * 365.2422 + 355; //355是2000.12冬至,得到较靠近jd的冬至估计值
		if (SSQ.calc(W, '气') > jd) {
			W -= 365.2422;
		}

		var A = [];
		var B = [];
		for (var i = 0; i < 24; i++) {
			A[i] = SSQ.calc(W + 15.2184 * i, '气') + 2451545; //24个节气时刻(北京时间),从冬至开始到下一个冬至以后
		}
		var w = SSQ.calc(A[0] - 2451545, '朔') + 2451545; //求较靠近冬至的朔日
        if (w > A[0]) {
			w -= 29.53;
        }

		var A = [];
        //该年所有朔,包含14个月的始末
        for (i = 0; i <= 15; i++) {
            A[i] = SSQ.calc(w - 2451545 + 29.5306 * i, '朔') + 2451545;
        }

		var [year] = p.Jtime(A[0]);
		var [MC, B] = p.GetZQandSMandLunarMonthCode(year+1);
		for(var j=0; j<16; j++){
			var [yy, mm, dd, hh, mt, ss] = p.Jtime(A[j]);
			var [yy2, mm2, dd2, hh2, mt2, ss2] = p.Jtime(B[j]);
			
			if((yy != yy2) || (mm != mm2) || (dd != dd2)){
				var fy = year + 1;
				var fi = j;

				var fd = A[j] - p.Jdays(yy2, mm2, dd2, 12, 0, 0);
				
				if(fs[fy] == undefined){
					fs[fy] = new Array();
				}
				fs[fy][fi] = fd;

				//log("寿星:",[yy, mm, dd, hh, mt, ss]);
				//log([yy2, mm2, dd2, hh2, mt2, ss2]);
				log(A);
				log(B);
		
				break for0;
			}
		}
	}

	var sp = '';
	var sj = "var smXFu = {\n";
	for(var year in fs){
		sp += (year + "=>[");
		sj += (year + ":{");
		for(var i in fs[year]){
			sp += (i+"=>"+fs[year][i]+",");
			sj += (i+":"+fs[year][i]+",");
		}
		sp = sp.substr(0, sp.length-1);
		sj = sj.substr(0, sj.length-1);
		sp += "],\n";
		sj += "},\n";
	}
	sj += "}\n";
	log(sp);
	log(sj)
}
function go3(){ //619-01-21至2300-01-01所有朔月
	var tjd = new Array();
	var tjd2 = new Array();

	for(var jd = 1947148; jd <= 2561118; jd += 1){
		var [yy, mm, dd] = p.Jtime(jd);
		var [MC, jdnm] = p.GetZQandSMandLunarMonthCode(yy+1);
		
		for(var i in jdnm){
			jdnm[i] = Math.floor(jdnm[i] + 0.5);
			if(tjd.indexOf(jdnm[i]) == -1){
				tjd.push(jdnm[i]);
			}
		}
	}
	
	var start = 1947148;
	var fs = [];
	for0:for(var st=0; ; st++){
		if(start + st >= 2561118){
			break;
		}
		var jd = start + st - 2451545;
		var W = Math.floor((jd - 355 + 183) / 365.2422) * 365.2422 + 355; //355是2000.12冬至,得到较靠近jd的冬至估计值
		if (SSQ.calc(W, '气') > jd) {
			W -= 365.2422;
		}

		var A = [];
		for (var i = 0; i < 24; i++) {
			A[i] = SSQ.calc(W + 15.2184 * i, '气') + 2451545; //24个节气时刻(北京时间),从冬至开始到下一个冬至以后
		}
		var w = SSQ.calc(A[0] - 2451545, '朔') + 2451545; //求较靠近冬至的朔日
        if (w > A[0]) {
			w -= 29.53;
        }
        //该年所有朔,包含14个月的始末
        for (i = 0; i <= 15; i++) {
            var moon = SSQ.calc(w - 2451545 + 29.5306 * i, '朔') + 2451545;
			if(tjd2.indexOf(moon) == -1){
				tjd2.push(moon);
			}
		}
	}
	log(tjd);
	log(tjd2);
}
loadJS('jquery-3.6.0.min.js', function(){
	loadJS('paipan.js', function(){ //逐日与寿星万年历比较农历日期
		var ym = SSQ.ym.slice(2);

		for(var Y=2000,M=1; Y <= 2000; M++){//break; //公历转农历支持-721年至2300年,公农历互转支持-104年至2300年
			for(var i = 0; i < 31; i++) {
				lun.lun[i] = new Object();
			}
			lun.yueLiCalc(Y, M);
			for(var i = 0; ; i++){
				var a = lun.lun[i];
				if(a == undefined){
					break;
				}
				if(Object.keys(a).length == 0){
					continue;
				}
				var [y, m, d, r, ob] = p.Solar2Lunar(a.y, a.m, a.d);
				ob.ym = ob.ym.replace("月",''); //从ob中拿出的才能进行比对

				var y2 = a.Lyear0 + 1984;
				var m2 = a.Lmc;
				var d2 = a.Ldi+1;
				var r2 = a.Lleap == '' ? false : true;
				
				if(m2 == '十三' || m2 == '后九'){
					r2 = true;
				}
				var flag = true;
				if(ob.yi != y2){ //农历年份
					flag = false;
				}
				if(ob.ym != m2){ //农历月份
					flag = false;
				}
				if(d != d2){ //农历日期
					flag = false;
				}
				if(r != r2){ //是否闰月
					flag = false;
				}
				if(ob.gz != a.Lyear3){ //农历干支纪年
					flag = false;
				}
				if(ob.days != a.Ldn){ //农历,该月多少天
					flag = false;
				}
				if(a.y > -104){ //这之后的才能逆转
					var [y3, m3, d3] = p.Lunar2Solar(y, m, d, r);
					if((y3 != a.y) || (m3 != a.m) || (d3 != a.d)){
						log("出错: 农历不能逆转.");
						flag = false;
					}
				}

				if(flag == false){

					log("公历:"+a.y+"-"+a.m+"-"+a.d+":::::::::寿星:"+y2+"-"+m2+"-"+d2+r2+a.Lyear3+":::::::::本尊:"+ob.yi+"-"+ob.ym+"-"+d+"-"+r+ob.gz+"::::"+flag);

					break;
				}
				
				continue;
				
				for(var h = 0; h <= 24; h += 1){ //逐时对比四柱
					var ob = new Object();

					var jd = JD.JD(a.y, a.m, a.d + h / 24);

					var j = parseInt(Math.random() * (134 - 75 + 1) + 75, 10); //真太阳时存在20秒左右的差别

					obb.mingLiBaZi(jd+curTZ/24-J2000, j/radd, ob); //八字计算
					
					p.zwz = false; //寿星不考虑早晚子
					var fm = p.fatemaps(0, a.y, a.m, a.d, h, 0, 0, j, 35); //寿星不考虑纬度
					if(false){ //与PHP比对
						var fm;
						$.ajax({
							type: "POST",
							url: "../../demo.php",
							data: {
								act: 'fatemaps',
								param: [0, a.y, a.m, a.d, h, 0, 0, j, 35]
							},
							async: false,
							cache: false,
							dataType: 'json',
							success: function(o) {
								fm = o;
							}
						});
					}
					if(a.XiZ != fm.xz+"座"){ //寿星精确到日定星座,本项目精确到秒定星座,所以在节气交接日会出现差别
						//log("星座不一致:\t"+a.y+"年"+a.m+"月"+a.d+"日"+h+"时\t"+a.XiZ+fm.xz+"\t真太阳相差:"+zty+"秒\t经度:"+j);
					}
					
					var zty = (timeStr2hour(ob.bz_zty) - timeStr2hour(fm['zty'][3]+":"+fm['zty'][4]+":"+fm['zty'][5])) * 60 * 60;
					
					if(ob.bz_jn != fm['sz'][0]){ //年月柱的差别是由于以下原因导致: 1,节气计算存在20秒左右的差别;2,寿星的年月柱计算不采用真太阳时
						log("年柱不一致:\t"+a.y+"年"+a.m+"月"+a.d+"日"+h+"时\t"+ob.bz_jn+fm['sz'][0]+"\t真太阳相差:["+ob.bz_zty+"]["+fm['zty'][3]+":"+fm['zty'][4]+":"+fm['zty'][5]+"]"+zty+"秒\t经度:"+j);
					}
					if(ob.bz_jy != fm['sz'][1]){
						log("月柱不一致:\t"+a.y+"年"+a.m+"月"+a.d+"日"+h+"时\t"+ob.bz_jy+fm['sz'][1]+"\t真太阳相差:["+ob.bz_zty+"]["+fm['zty'][3]+":"+fm['zty'][4]+":"+fm['zty'][5]+"]"+zty+"秒\t经度:"+j);
					}
					if(ob.bz_jr != fm['sz'][2]){ //日时柱的差别: 1,真太阳时存在20秒左右的差别;
						log("日柱不一致:\t"+a.y+"年"+a.m+"月"+a.d+"日"+h+"时\t"+ob.bz_jr+fm['sz'][2]+"\t真太阳相差:["+ob.bz_zty+"]["+fm['zty'][3]+":"+fm['zty'][4]+":"+fm['zty'][5]+"]"+zty+"秒\t经度:"+j);
					}
					if(ob.bz_js != fm['sz'][3]){
						log("时柱不一致:\t"+a.y+"年"+a.m+"月"+a.d+"日"+h+"时\t"+ob.bz_js+fm['sz'][3]+"\t真太阳相差:["+ob.bz_zty+"]["+fm['zty'][3]+":"+fm['zty'][4]+":"+fm['zty'][5]+"]"+zty+"秒\t经度:"+j);
					}
				}
			}
			if(flag === false){
				break;
			}
			if(M >= 12){
				M = 0; 
				Y += 1;
				
				log(Y)
			}
		}
	});
});


