/*紫微斗數 Chinese Astrology Zi Wei Dou Shu*/
var ziweiUI = {
	//主星列印方向 true:由右向左,false:由左向右
	right2left:false,
	//UI resize
	resize:function (){
		//var wdth=$(window).width();
	  //$("#divZiWei").css("left",wdth>640?(wdth-640)/2:0);
	},
	genNowDateZiwei:function (){
		this.getNowDate();
		this.genZiwei();
	},
	getNowDate:function(){
		var Today=new Date();
		var h=Today.getHours();
		Today.setDate(Today.getDate()+(h>=23?1:0)); 
		document.getElementById("sel_Year").value=Today.getFullYear();
		document.getElementById("sel_Month").value=Today.getMonth()+1;
		document.getElementById("sel_Day").value=Today.getDate();
		document.getElementById("sel_Hour").value=EarthlyBranches[(h+(h%2?1:0))%24/2];
	},
	//initial    	  
	initial:function (){
	  //畫紫微斗數空表格
	  //document.getElementById("container").innerHTML="<div id='queryDiv'><h2>紫微斗數命盤</h2><div>西元<select id='sel_Year'></select> 年<select id='sel_Month'></select> 月<select id='sel_Day'></select> 日<select id='sel_Hour'></select> 時<input type='radio' id='gender' name='gender' value='M' checked>男<input type='radio' name='gender' value='F'>女<input type='button' value='現在時間*' id='btnNowDate'></div></div><div class='ziwei'><div><div id='zw6'></div><div id='zw7'></div><div id='zw8'></div><div id='zw9'></div></div><div><div id='zw5'></div><div id='zw4'></div><div id='zwHome' class='zwDivCenter'></div><div id='zw10'></div><div id='zw11'></div></div><div><div id='zw3'></div><div id='zw2'></div><div id='zw1'></div><div id='zw12'></div></div></div>";
	  document.getElementById("container").innerHTML="<div class='zwDivHeader'><h2>紫微斗數命盤 </h2><div>西元<select id='sel_Year'></select> 年<select id='sel_Month'></select> 月<select id='sel_Day'></select> 日<select id='sel_Hour'></select> 時<input type='radio' id='gender' name='gender' value='M' checked>男<input type='radio' name='gender' value='F'>女<input type='button' value='現在時間*' id='btnNowDate'></div></div><div class='ziwei'><div id='zw6'></div><div id='zw7'></div><div id='zw8'></div><div id='zw9'></div><div id='zw5'></div><div id='zwHome' class='zwDivCenter'></div><div id='zw10'></div><div id='zw4'></div><div id='zw11'></div><div id='zw3'></div><div id='zw2'></div><div id='zw1'></div><div id='zw12'></div></div>";
	  function addOption(id,a,b){
	  	for (i=a;i<=b;i++){ 
				let op = document.createElement('option');
	      op.value = i;
	      op.innerHTML = i;
	      document.getElementById(id).appendChild(op);
			}
	  }
	  addOption("sel_Year",1900,2049);
	  addOption("sel_Month",1,12);
	  addOption("sel_Day",1,31);
	  for (i=0;i<EarthlyBranches.length;i++){ 
	  	let op = document.createElement('option');
	  	op.value = EarthlyBranches[i];
	    op.innerHTML = EarthlyBranches[i]+"【"+((24+(i*2-1))%24).toString()+"~"+ (i*2+1).toString()+"】";
	  	document.getElementById("sel_Hour").appendChild(op);
	  }
	  //初始日期
	  this.genNowDateZiwei();
	  this.resize();
	},
	clearPalce:function (){
		for (i=0;i<12;i++){ 
			document.getElementById("zw"+(i+1).toString()).innerHTML="<div class='MangA'>" +EarthlyBranches[i]+ "</div>";
		}
	},
	cleanZiwei:function (){
		//$("#zwHome").html(""); 
		document.getElementById("zwHome").innerHTML = "";
		this.clearPalce();
	},
	genZiwei:function(){
		
		let gender=	document.querySelectorAll("input[type=radio]");
		let genderValue="M";
		for (i=0;i<gender.length;i++){
				if (gender[i].checked){
					genderValue=gender[i].value;
					break;
				}
		}
		var zw = ziwei.computeZiWei( document.getElementById("sel_Year").value, document.getElementById("sel_Month").value, document.getElementById("sel_Day").value, document.getElementById("sel_Hour").value, genderValue);
		document.getElementById("zwHome").innerHTML = "國曆：" + ziwei.getSolarDay() + "<br>"
					+ "農曆：" + ziwei.getLunarDay()+ "<br>"
					+ "生肖：【" + ziwei.getShengXiao() + "】"+"<br>"
					+ "<div>"+ ziwei.getFiveElement() +"</div>" 
					+ "<div>"+ ziwei.getYinYangGender()+"</div>"
					+ "<div class='zwcopy'>by cubshuang</div>";
	  //render Direction
		var styleLR=[" zwStarLeft"," zwStarRight"];
		if(this.right2left){ styleLR.reverse(); }
		//render Star
	    for (i=0;i<12;i++){
	  		document.getElementById("zw"+(i+1).toString()).innerHTML+=    
	  				"<div class='MangA'>" + zw[i].MangA + "</div>" +
						"<div class='MangB'>" + zw[i].MangB + "</div>" +
						"<div class='MangC'>" + zw[i].MangC + "</div>" +
						"<div class='StarAll'>" + zw[i].StarAll + "</div>" ;
	  		var StarA1,StarA2,StarA3,StarB1,StarB2,StarC1,StarC2;
	  		StarA1="";StarA2="";StarA3="";StarB1="";StarB2="";StarC1="";StarC2="";
			var tmpSatrA=[[],[],[]];
			var k=0;
			for (j=0;j<zw[i].StarA.length;j++){
				tmpSatrA[0][k]=zw[i].StarA[j].substring(0,1);
	  			tmpSatrA[1][k]=zw[i].StarA[j].substring(1,2);
	  			tmpSatrA[2][k]=(zw[i].StarA[j].length>2)?"<span>"+zw[i].StarA[j].substring(3,4)+"</span>":"　";
				k+=1;
			}	
			for (j=0;j<zw[i].Star6.length;j++){
		  		tmpSatrA[0][k]="<span>"+zw[i].Star6[j].substring(0,1)+"</span>"
		  		tmpSatrA[1][k]="<span>"+zw[i].Star6[j].substring(1,2)+"</span>"
		  		tmpSatrA[2][k]=(zw[i].Star6[j].length>2)?"<span>"+zw[i].Star6[j].substring(3,4)+"</span>":"　";
				k+=1;
			}
			//style Left or Right
			if(this.right2left){
				for(j=0;j<3;j++){ tmpSatrA[j].reverse(); }
			}
			//render StarA & B & C
	  		for (j=0;j<tmpSatrA[0].length;j++){
				StarA1+=tmpSatrA[0][j];
	  			StarA2+=tmpSatrA[1][j];
	  			StarA3+=tmpSatrA[2][j];
	  		}
	  		for (j=0;j<zw[i].StarB.length;j++){
	  			StarB1+=zw[i].StarB[j].substring(0,1);
	  			StarB2+=zw[i].StarB[j].substring(1,2);
				}
	  		for (j=0;j<zw[i].StarC.length;j++){
	  			StarC1+=zw[i].StarC[j].substring(0,1);
	  			StarC2+=zw[i].StarC[j].substring(1,2);
		  	}
				document.getElementById("zw"+(i+1).toString()).innerHTML+=
						"<div class='StarA"+ styleLR[0] + "'>" + StarA1+ "<br>"+StarA2 + "<br><div class='Star4'>"+StarA3 + "</div></div>" +
	  				"<div class='StarB"+ styleLR[1] + "'>" + StarB1+ "<br>"+StarB2 + "</div>" +
	  				"<div class='StarC'>" + StarC1+ "<br>"+StarC2 + "</div>";
		}
		//大小限表
		var DS_Shian=ziwei.getDaShian();
		for (i=0;i<12;i++){
			document.getElementById("zw"+(i+1).toString()).innerHTML+=
					"<div class='MangY10'>"+ DS_Shian.DShian[i+1] + "</div>" +
					"<div class='MangY1'>" + DS_Shian.SShian[i+1] + "</div>" ;
		}
	}
};
window.addEventListener('load' ,function(){
//開始使用
	ziweiUI.initial();
	document.getElementById("btnNowDate").addEventListener('click',function () {ziweiUI.genNowDateZiwei();});
	let s = document.querySelectorAll("select");
	for (i=0;i<s.length;i++){
		s[i].addEventListener('change',function () {ziweiUI.genZiwei();});	
	}
	let r=document.querySelectorAll("input[type=radio]");
	for (i=0;i<r.length;i++){
		r[i].addEventListener('change',function () {ziweiUI.genZiwei();});	
	}
	window.addEventListener('resize',function() { ziweiUI.resize();});
	//$(window).resize(function() { ziweiUI.resize();});
})